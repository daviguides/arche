"""Analyzer for test responses.

Evaluates conformity with Arché principles.
Supports keyword-based (fast) or LLM-based (semantic) analysis.
Parallel execution for LLM mode.
"""

import asyncio
import time
from datetime import datetime
from pathlib import Path

import yaml
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
)

from arche_tester.agents import AnalyzerAgent
from arche_tester.config import settings
from arche_tester.display import (
    console,
    create_analysis_summary,
    create_progress_bar,
    create_results_table,
    print_header,
    print_step,
    print_success,
)
from arche_tester.models import (
    BehaviorCheck,
    Conformity,
    TestAnalysis,
    TestCase,
    TestResponse,
    TestResponses,
    TestSuite,
    VersionAnalysis,
)


class ResponseAnalyzer:
    """Analyzes test responses for principle conformity.

    Evaluates LLM responses against expected behaviors defined in test cases,
    producing conformity assessments (PASS/FAIL/PARTIAL) for each test.

    Supports two analysis modes:
        - keyword: Fast pattern matching using behavior indicators (default).
        - llm: Semantic analysis using Claude Agent SDK for nuanced evaluation.

    LLM mode supports parallel execution for faster analysis.

    Attributes:
        _data_path: Path to data directory containing test cases and responses.
        _use_llm: Whether to use LLM-based semantic analysis.
        _skip_cli_check: Whether to skip Claude CLI availability check.
        _concurrency: Max parallel analyses for LLM mode.

    Example:
        analyzer = ResponseAnalyzer(data_path=Path("data"), use_llm=True)
        results = await analyzer.analyze_version_async("0.1.0")
    """

    DEFAULT_CONCURRENCY = 4

    def __init__(
        self,
        data_path: Path,
        use_llm: bool = False,
        skip_cli_check: bool = False,
        concurrency: int | None = None,
    ) -> None:
        """Initialize analyzer.

        Args:
            data_path: Path to data directory.
            use_llm: Use LLM-based semantic analysis.
            skip_cli_check: Skip Claude CLI check (for nested sessions).
            concurrency: Max parallel analyses (default: 4).
        """
        self._data_path = data_path
        self._use_llm = use_llm
        self._skip_cli_check = skip_cli_check
        self._concurrency = concurrency or self.DEFAULT_CONCURRENCY

    def load_test_suite(self) -> TestSuite:
        """Load test cases from YAML file.

        Reads the functional test definitions from the standard location
        and validates them against the TestSuite schema.

        Returns:
            TestSuite containing all test case definitions.

        Raises:
            FileNotFoundError: If functional-tests.yaml doesn't exist.
            ValidationError: If YAML content doesn't match TestSuite schema.
        """
        test_file = self._data_path / "test-cases" / "functional-tests.yaml"
        content = test_file.read_text()
        data = yaml.safe_load(content)
        return TestSuite.model_validate(data)

    def load_responses(self, version: str) -> TestResponses:
        """Load saved test responses for a specific version.

        Retrieves the raw LLM responses that were captured during test
        execution for the specified Arché version.

        Args:
            version: Arché version identifier (e.g., "0.1.0").

        Returns:
            TestResponses containing all captured responses for the version.

        Raises:
            FileNotFoundError: If responses.yaml doesn't exist for version.
            ValidationError: If YAML content doesn't match TestResponses schema.
        """
        response_file = (
            self._data_path / "versions" / version / "responses.yaml"
        )
        content = response_file.read_text()
        data = yaml.safe_load(content)
        return TestResponses.model_validate(data)

    async def _analyze_single_response(
        self,
        test_case: TestCase,
        response: TestResponse,
        semaphore: asyncio.Semaphore,
        progress: Progress,
        task_id: TaskID,
    ) -> TestAnalysis:
        """Analyze a single response using LLM (parallel-safe).

        Args:
            test_case: Test case definition.
            response: Response to analyze.
            semaphore: Concurrency limiter.
            progress: Rich progress instance.
            task_id: Progress task ID.

        Returns:
            TestAnalysis with conformity result.
        """
        async with semaphore:
            # Create agent for this analysis
            agent = AnalyzerAgent(
                cwd=self._data_path,
                verbose=False,
                skip_cli_check=self._skip_cli_check,
            )

            try:
                # Use LLM for semantic analysis
                behavior_checks = await agent.analyze_response(
                    response=response.response,
                    must_behaviors=test_case.expected.must,
                    must_not_behaviors=test_case.expected.must_not,
                )
            finally:
                await agent.disconnect()

            # Update progress
            progress.update(task_id, advance=1)

            # Determine overall conformity
            non_skipped = [
                c for c in behavior_checks if c.result != Conformity.SKIPPED
            ]
            all_skipped = len(non_skipped) == 0

            if all_skipped:
                conformity = Conformity.SKIPPED
            else:
                all_passed = all(
                    c.result == Conformity.PASS for c in non_skipped
                )
                any_passed = any(
                    c.result == Conformity.PASS for c in non_skipped
                )

                if all_passed:
                    conformity = Conformity.PASS
                elif any_passed:
                    conformity = Conformity.PARTIAL
                else:
                    conformity = Conformity.FAIL

            return TestAnalysis(
                test_id=test_case.id,
                principle=test_case.principle,
                mode=test_case.mode,
                conformity=conformity,
                behavior_checks=behavior_checks,
            )

    async def analyze_version_async(self, version: str) -> VersionAnalysis:
        """Analyze all responses using LLM-based semantic analysis (parallel).

        Args:
            version: Version to analyze.

        Returns:
            Complete analysis with conformity results.
        """
        start_time = time.time()
        print_header("Semantic Analysis", version)
        print_step("Loading test suite and responses...")

        suite = self.load_test_suite()
        responses = self.load_responses(version)

        test_lookup: dict[str, TestCase] = {
            tc.id: tc for tc in suite.test_cases
        }

        total = len(responses.responses)

        print_step(f"Analyzing {total} test responses with LLM...")
        print_step(f"Model: [cyan]{settings.analyzer_agent.model.value}[/cyan]")
        print_step(f"Concurrency: [cyan]{self._concurrency}[/cyan] parallel")
        console.print()

        # Create semaphore for concurrency control
        semaphore = asyncio.Semaphore(self._concurrency)

        # Build tasks for parallel execution
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("({task.completed}/{task.total})"),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            task_id = progress.add_task("Analyzing", total=total)

            tasks = []
            for resp in responses.responses:
                test_case = test_lookup.get(resp.test_id)
                if test_case:
                    tasks.append(
                        self._analyze_single_response(
                            test_case, resp, semaphore, progress, task_id
                        )
                    )

            analyses = await asyncio.gather(*tasks)

        # Sort by test_id
        analyses_sorted = sorted(analyses, key=lambda a: a.test_id)

        # Count results
        passed = sum(1 for a in analyses_sorted if a.conformity == Conformity.PASS)
        failed = sum(1 for a in analyses_sorted if a.conformity == Conformity.FAIL)
        partial = sum(1 for a in analyses_sorted if a.conformity == Conformity.PARTIAL)
        skipped = sum(1 for a in analyses_sorted if a.conformity == Conformity.SKIPPED)

        total_tests = len(analyses_sorted)
        evaluated = total_tests - skipped
        pass_rate = (passed / evaluated * 100) if evaluated > 0 else 0.0
        weighted_rate = (
            ((passed + partial * 0.5) / evaluated * 100)
            if evaluated > 0
            else 0.0
        )

        result = VersionAnalysis(
            arche_version=version,
            timestamp=datetime.now().isoformat(),
            total_tests=total_tests,
            passed=passed,
            failed=failed,
            partial=partial,
            skipped=skipped,
            pass_rate=pass_rate,
            weighted_rate=weighted_rate,
            analyses=analyses_sorted,
        )

        self._save_analysis(version=version, analysis=result)
        elapsed = time.time() - start_time
        self._print_summary(result, elapsed_seconds=elapsed)

        return result

    def analyze_version(self, version: str) -> VersionAnalysis:
        """Analyze all responses for a version (keyword mode).

        Args:
            version: Version to analyze.

        Returns:
            Complete analysis with conformity results.
        """
        start_time = time.time()
        print_header("Keyword Analysis", version)
        print_step("Loading test suite and responses...")

        suite = self.load_test_suite()
        responses = self.load_responses(version)

        # Create lookup for test cases
        test_lookup: dict[str, TestCase] = {
            tc.id: tc for tc in suite.test_cases
        }

        analyses: list[TestAnalysis] = []
        passed = 0
        failed = 0
        partial = 0
        skipped = 0

        total = len(responses.responses)
        print_step(f"Analyzing {total} test responses...")
        console.print()

        progress = create_progress_bar()
        with progress:
            task = progress.add_task(
                "Analyzing responses...",
                total=total,
            )

            for response in responses.responses:
                test_case = test_lookup.get(response.test_id)
                if not test_case:
                    continue

                progress.update(
                    task,
                    description=f"[cyan]{test_case.id}[/cyan] {test_case.description[:30]}...",
                )

                analysis = self._analyze_response(
                    test_case=test_case,
                    response=response,
                )
                analyses.append(analysis)

                if analysis.conformity == Conformity.PASS:
                    passed += 1
                elif analysis.conformity == Conformity.FAIL:
                    failed += 1
                elif analysis.conformity == Conformity.SKIPPED:
                    skipped += 1
                else:
                    partial += 1

                progress.advance(task)

        total_tests = len(analyses)
        # Exclude skipped from rate calculations
        evaluated = total_tests - skipped
        pass_rate = (passed / evaluated * 100) if evaluated > 0 else 0.0
        weighted_rate = (
            ((passed + partial * 0.5) / evaluated * 100)
            if evaluated > 0
            else 0.0
        )

        result = VersionAnalysis(
            arche_version=version,
            timestamp=datetime.now().isoformat(),
            total_tests=total_tests,
            passed=passed,
            failed=failed,
            partial=partial,
            skipped=skipped,
            pass_rate=pass_rate,
            weighted_rate=weighted_rate,
            analyses=analyses,
        )

        # Save analysis
        self._save_analysis(version=version, analysis=result)

        # Print summary
        elapsed = time.time() - start_time
        self._print_summary(result, elapsed_seconds=elapsed)

        return result

    def _analyze_response(
        self,
        test_case: TestCase,
        response: TestResponse,
    ) -> TestAnalysis:
        """Analyze a single response against expected behavior."""
        behavior_checks: list[BehaviorCheck] = []

        # Check "must" behaviors
        for behavior in test_case.expected.must:
            found = self._check_behavior_present(
                response=response.response,
                behavior=behavior,
            )
            behavior_checks.append(
                BehaviorCheck(
                    behavior=behavior,
                    check_type="must",
                    result=Conformity.PASS if found else Conformity.FAIL,
                    evidence=self._extract_evidence(
                        response=response.response,
                        behavior=behavior,
                    ),
                )
            )

        # Check "must_not" behaviors
        for behavior in test_case.expected.must_not:
            found = self._check_behavior_present(
                response=response.response,
                behavior=behavior,
            )
            behavior_checks.append(
                BehaviorCheck(
                    behavior=behavior,
                    check_type="must_not",
                    result=Conformity.FAIL if found else Conformity.PASS,
                    evidence=self._extract_evidence(
                        response=response.response,
                        behavior=behavior,
                    ),
                )
            )

        # Determine overall conformity
        all_passed = all(
            check.result == Conformity.PASS for check in behavior_checks
        )
        any_passed = any(
            check.result == Conformity.PASS for check in behavior_checks
        )

        if all_passed:
            conformity = Conformity.PASS
        elif any_passed:
            conformity = Conformity.PARTIAL
        else:
            conformity = Conformity.FAIL

        return TestAnalysis(
            test_id=test_case.id,
            principle=test_case.principle,
            mode=test_case.mode,
            conformity=conformity,
            behavior_checks=behavior_checks,
        )

    def _check_behavior_present(
        self,
        response: str,
        behavior: str,
    ) -> bool:
        """Check if behavior is present in response.

        Simple keyword-based detection. Can be enhanced with LLM.
        """
        behavior_lower = behavior.lower()
        response_lower = response.lower()

        # Handle common behavior patterns
        if "suggest" in behavior_lower or "propose" in behavior_lower:
            indicators = [
                "should we",
                "would you like",
                "shall i",
                "i can",
                "i could",
                "let me",
                "i'll",
                "i will",
            ]
            return any(ind in response_lower for ind in indicators)

        if "create" in behavior_lower or "implement" in behavior_lower:
            indicators = [
                "creating",
                "created",
                "implementing",
                "implemented",
                "wrote",
                "writing",
            ]
            return any(ind in response_lower for ind in indicators)

        if "analysis" in behavior_lower or "analyze" in behavior_lower:
            indicators = [
                "analysis",
                "analyzing",
                "found",
                "identified",
                "detected",
            ]
            return any(ind in response_lower for ind in indicators)

        if "complete" in behavior_lower or "finish" in behavior_lower:
            indicators = [
                "completed",
                "finished",
                "done",
                "all tasks",
            ]
            return any(ind in response_lower for ind in indicators)

        if "pause" in behavior_lower or "stop" in behavior_lower:
            indicators = [
                "should i continue",
                "shall i proceed",
                "would you like me to",
                "before i continue",
            ]
            return any(ind in response_lower for ind in indicators)

        # Default: simple substring match
        return behavior_lower in response_lower

    def _extract_evidence(
        self,
        response: str,
        behavior: str,
    ) -> str:
        """Extract relevant quote from response as evidence."""
        lines = response.split("\n")
        behavior_lower = behavior.lower()

        for line in lines:
            if any(
                word in line.lower()
                for word in behavior_lower.split()[:3]
            ):
                return line[:200]

        return response[:200] if response else "(empty response)"

    def _save_analysis(
        self,
        version: str,
        analysis: VersionAnalysis,
    ) -> None:
        """Save analysis to YAML file."""
        version_dir = self._data_path / "versions" / version
        version_dir.mkdir(parents=True, exist_ok=True)

        output_file = version_dir / "analysis.yaml"
        data = analysis.model_dump(mode="json")

        with output_file.open("w") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

        print_success(f"Analysis saved: {output_file}")

    def _print_summary(
        self,
        analysis: VersionAnalysis,
        elapsed_seconds: float | None = None,
    ) -> None:
        """Print analysis summary with rich formatting."""
        console.print()
        console.print(create_analysis_summary(analysis))
        console.print()
        console.print(create_results_table(analysis))
        console.print()
        if elapsed_seconds is not None:
            minutes, seconds = divmod(int(elapsed_seconds), 60)
            if minutes > 0:
                time_str = f"{minutes}m {seconds}s"
            else:
                time_str = f"{elapsed_seconds:.1f}s"
            console.print(f"[dim]Total time: {time_str}[/dim]")
            console.print()


__all__ = ["ResponseAnalyzer"]
