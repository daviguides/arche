"""Test runner for Arché functional tests.

Executes test suite against isolated mock project environments.
Supports parallel execution with fork_session optimization.
"""

import asyncio
import shutil
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

from arche_tester.agents import ArcheTestAgent
from arche_tester.config import settings
from arche_tester.display import (
    console,
    create_principles_panel,
    print_header,
    print_step,
    print_success,
)
from arche_tester.models import (
    TestCase,
    TestResponse,
    TestResponses,
    TestSuite,
    TranscriptEntry,
)


class TestRunner:
    """Runs functional tests against Arché principles.

    Uses fork_session + parallel execution:
    - Load principles once in base session
    - Fork for each test (parallel, same cwd)
    - Each test works in its own subdirectory (isolation)
    """

    DEFAULT_CONCURRENCY = 8

    def __init__(
        self,
        data_path: Path,
        verbose: bool = True,
        skip_cli_check: bool = True,
        concurrency: int | None = None,
        capture_transcripts: bool = False,
    ) -> None:
        """Initialize runner.

        Args:
            data_path: Path to data directory.
            verbose: Enable detailed logging.
            skip_cli_check: Skip Claude CLI check (for nested sessions).
            concurrency: Max parallel tests (default: 8).
            capture_transcripts: Capture full transcript of agent steps.
        """
        self._data_path = data_path
        self._verbose = verbose
        self._skip_cli_check = skip_cli_check
        self._concurrency = concurrency or self.DEFAULT_CONCURRENCY
        self._capture_transcripts = capture_transcripts
        self._mock_project_path = data_path / "mock-project"
        self._temp_base = settings.test_workspace

    def load_test_suite(self) -> TestSuite:
        """Load test cases from YAML."""
        test_file = self._data_path / "test-cases" / "functional-tests.yaml"
        content = test_file.read_text()
        data = yaml.safe_load(content)
        return TestSuite.model_validate(data)

    def _setup_base_workspace(self, test_ids: list[str] | None = None) -> Path:
        """Setup base workspace directory with all test subdirectories.

        Pre-creates all test directories so they exist when the base session
        is created. This ensures forked sessions can see all directories.

        Args:
            test_ids: List of test IDs to pre-create directories for.

        Returns:
            Path to the base workspace (cwd for all sessions).
        """
        if self._temp_base.exists():
            shutil.rmtree(self._temp_base)
        self._temp_base.mkdir(parents=True)

        # Pre-create all test directories
        if test_ids:
            for test_id in test_ids:
                test_dir = self._temp_base / f"test-{test_id}"
                shutil.copytree(self._mock_project_path, test_dir)

        return self._temp_base

    def _create_test_subdir(self, test_id: str) -> Path:
        """Get or create isolated subdirectory for a test.

        If directory was pre-created by _setup_base_workspace, returns it.
        Otherwise creates it (fallback for non-parallel execution).

        Args:
            test_id: Test case ID for subdirectory naming.

        Returns:
            Path to the test subdirectory.
        """
        test_dir = self._temp_base / f"test-{test_id}"
        if not test_dir.exists():
            shutil.copytree(self._mock_project_path, test_dir)
        return test_dir

    def _cleanup_test_subdir(self, test_dir: Path) -> None:
        """Remove a test subdirectory."""
        if test_dir.exists():
            shutil.rmtree(test_dir)

    def _cleanup_all(self) -> None:
        """Remove base workspace and all subdirectories."""
        if self._temp_base.exists():
            shutil.rmtree(self._temp_base)

    async def _run_single_test(
        self,
        test_case: TestCase,
        base_session_id: str,
        semaphore: asyncio.Semaphore,
        progress: Progress,
        task_id: TaskID,
    ) -> TestResponse:
        """Run a single test using fork_session with isolated subdirectory.

        Args:
            test_case: Test case to run.
            base_session_id: Session ID to fork from.
            semaphore: Concurrency limiter.
            progress: Rich progress instance.
            task_id: Progress task ID.

        Returns:
            TestResponse with result (and transcript if enabled).
        """
        async with semaphore:
            # Create isolated subdirectory for this test
            test_dir = self._create_test_subdir(test_case.id)
            subdir_name = test_dir.name  # e.g., "test-AP-001"

            try:
                # Fork from base session (same cwd, principles already loaded)
                # skip_cli_check=True: base agent already verified CLI
                agent = ArcheTestAgent(
                    cwd=self._temp_base,
                    verbose=False,
                    skip_cli_check=True,
                    resume=base_session_id,
                    fork_session=True,
                )

                # Run test, directing agent to work in subdirectory
                result = await agent.run_test(
                    prompt=test_case.prompt,
                    context=test_case.context,
                    work_dir=subdir_name,
                    capture_transcript=self._capture_transcripts,
                )
                await agent.disconnect()

                # Update progress
                progress.update(task_id, advance=1)

                # Unpack result based on whether transcripts are captured
                if self._capture_transcripts:
                    response_text, duration_ms, raw_transcript = result
                    transcript = [
                        TranscriptEntry(**entry) for entry in raw_transcript
                    ]
                else:
                    response_text, duration_ms = result
                    transcript = None

                return TestResponse(
                    test_id=test_case.id,
                    prompt=test_case.prompt,
                    response=response_text,
                    duration_ms=duration_ms,
                    transcript=transcript,
                )
            finally:
                self._cleanup_test_subdir(test_dir)

    async def run_suite(
        self,
        version: str,
    ) -> TestResponses:
        """Run all tests in parallel using fork_session.

        Optimized flow:
        1. Create base session and load principles once
        2. Fork for each test (parallel, same cwd)
        3. Each test works in its own subdirectory

        Args:
            version: Arché version being tested.

        Returns:
            TestResponses with all results.
        """
        start_time = time.time()
        print_header("Functional Tests", version)

        suite = self.load_test_suite()
        total = len(suite.test_cases)

        print_step(f"Running {total} tests against Arché principles")
        print_step(f"Model: [cyan]{settings.test_agent.model.value}[/cyan]")
        print_step(f"Concurrency: [cyan]{self._concurrency}[/cyan] parallel tests")
        print_step(f"Mode: [cyan]fork_session + parallel[/cyan]")
        if self._capture_transcripts:
            print_step("Transcripts: [cyan]enabled[/cyan]")
        console.print()

        # Setup base workspace with ALL test directories pre-created
        # This ensures forked sessions can see all directories
        test_ids = [tc.id for tc in suite.test_cases]
        self._setup_base_workspace(test_ids=test_ids)

        # Create base session and load principles once
        print_step("Loading Arché principles (base session)...")
        base_agent = ArcheTestAgent(
            cwd=self._temp_base,
            verbose=False,
            skip_cli_check=self._skip_cli_check,
        )
        principles_response = await base_agent.load_arche_principles()
        base_session_id = base_agent.session_id
        await base_agent.disconnect()

        # Show principles loaded confirmation
        print_step(f"Base session: [dim]{base_session_id[:12]}...[/dim]")
        console.print()
        console.print(create_principles_panel(principles_response))
        console.print()

        # Create semaphore to limit concurrent tests
        semaphore = asyncio.Semaphore(self._concurrency)

        # Run all tests in parallel with progress bar
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TextColumn("({task.completed}/{task.total})"),
                TimeElapsedColumn(),
                console=console,
            ) as progress:
                task_id = progress.add_task("Running tests", total=total)

                # Launch all tests concurrently (forking from base session)
                tasks = [
                    self._run_single_test(
                        test_case, base_session_id, semaphore, progress, task_id
                    )
                    for test_case in suite.test_cases
                ]
                responses = await asyncio.gather(*tasks)

        finally:
            # Cleanup all workspaces
            self._cleanup_all()

        # Calculate total duration
        total_duration_ms = int((time.time() - start_time) * 1000)

        # Sort responses by test_id to maintain order
        responses_sorted = sorted(responses, key=lambda r: r.test_id)

        result = TestResponses(
            arche_version=version,
            timestamp=datetime.now().isoformat(),
            responses=responses_sorted,
            total_duration_ms=total_duration_ms,
        )

        # Save responses
        self._save_responses(version=version, responses=result)

        # Print summary
        console.print()
        minutes, seconds = divmod(total_duration_ms // 1000, 60)
        if minutes > 0:
            time_str = f"{minutes}m {seconds}s"
        else:
            time_str = f"{total_duration_ms / 1000:.1f}s"
        print_success(f"Completed {total} tests")
        console.print(f"[dim]Total time: {time_str}[/dim]")
        console.print()

        return result

    def _save_responses(
        self,
        version: str,
        responses: TestResponses,
    ) -> None:
        """Save responses to YAML file, with optional transcripts."""
        version_dir = self._data_path / "versions" / version
        version_dir.mkdir(parents=True, exist_ok=True)

        # Save transcripts separately if enabled
        if self._capture_transcripts:
            transcripts_dir = version_dir / "transcripts"
            transcripts_dir.mkdir(exist_ok=True)

            for response in responses.responses:
                if response.transcript:
                    transcript_file = transcripts_dir / f"{response.test_id}.yaml"
                    transcript_data = {
                        "test_id": response.test_id,
                        "prompt": response.prompt,
                        "steps": [entry.model_dump(mode="json", exclude_none=True)
                                  for entry in response.transcript],
                    }
                    with transcript_file.open("w") as f:
                        yaml.dump(
                            transcript_data,
                            f,
                            default_flow_style=False,
                            allow_unicode=True,
                        )

            print_success(f"Transcripts saved: {transcripts_dir}/")

        # Save responses without transcripts (keep file clean)
        output_file = version_dir / "responses.yaml"
        # Create a copy without transcripts for cleaner YAML
        responses_clean = responses.model_copy(deep=True)
        for resp in responses_clean.responses:
            resp.transcript = None
        data = responses_clean.model_dump(mode="json", exclude_none=True)

        with output_file.open("w") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

        print_success(f"Responses saved: {output_file}")


__all__ = ["TestRunner"]
