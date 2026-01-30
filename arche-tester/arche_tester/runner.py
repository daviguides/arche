"""Test runner for Arché functional tests.

Executes test suite against isolated mock project environments.
Supports parallel execution with configurable concurrency.
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
    print_header,
    print_step,
    print_success,
)
from arche_tester.models import (
    TestCase,
    TestResponse,
    TestResponses,
    TestSuite,
)


class TestRunner:
    """Runs functional tests against Arché principles.

    Supports parallel execution with isolated workspaces per test.
    Each test gets its own workspace and agent instance.
    """

    DEFAULT_CONCURRENCY = 4

    def __init__(
        self,
        arche_path: Path,
        data_path: Path,
        verbose: bool = True,
        skip_cli_check: bool = False,
        concurrency: int | None = None,
    ) -> None:
        """Initialize runner.

        Args:
            arche_path: Path to arche bundle.
            data_path: Path to data directory.
            verbose: Enable detailed logging.
            skip_cli_check: Skip Claude CLI check (for nested sessions).
            concurrency: Max parallel tests (default: 4).
        """
        self._arche_path = arche_path
        self._data_path = data_path
        self._verbose = verbose
        self._skip_cli_check = skip_cli_check
        self._concurrency = concurrency or self.DEFAULT_CONCURRENCY
        self._mock_project_path = data_path / "mock-project"
        self._temp_base = Path("/tmp/arche-test")

    def load_test_suite(self) -> TestSuite:
        """Load test cases from YAML."""
        test_file = self._data_path / "test-cases" / "functional-tests.yaml"
        content = test_file.read_text()
        data = yaml.safe_load(content)
        return TestSuite.model_validate(data)

    def _create_workspace(self, test_id: str) -> Path:
        """Create isolated workspace for a test.

        Args:
            test_id: Test case ID for workspace naming.

        Returns:
            Path to the workspace directory.
        """
        workspace = self._temp_base / f"workspace-{test_id}"
        if workspace.exists():
            shutil.rmtree(workspace)
        shutil.copytree(self._mock_project_path, workspace)
        return workspace

    def _cleanup_workspace(self, workspace: Path) -> None:
        """Remove a test workspace."""
        if workspace.exists():
            shutil.rmtree(workspace)

    def _cleanup_all_workspaces(self) -> None:
        """Remove all test workspaces."""
        if self._temp_base.exists():
            shutil.rmtree(self._temp_base)

    async def _run_single_test(
        self,
        test_case: TestCase,
        semaphore: asyncio.Semaphore,
        progress: Progress,
        task_id: TaskID,
    ) -> TestResponse:
        """Run a single test with its own isolated workspace.

        Args:
            test_case: Test case to run.
            semaphore: Concurrency limiter.
            progress: Rich progress instance.
            task_id: Progress task ID.

        Returns:
            TestResponse with result.
        """
        async with semaphore:
            workspace = self._create_workspace(test_case.id)
            try:
                # Create agent with principles for this test
                agent = ArcheTestAgent(
                    arche_path=self._arche_path,
                    cwd=workspace,
                    verbose=False,
                    skip_cli_check=self._skip_cli_check,
                )

                # Load principles and run test
                await agent.load_arche_principles()
                response_text, duration_ms = await agent.run_test(
                    prompt=test_case.prompt,
                    context=test_case.context,
                )
                await agent.disconnect()

                # Update progress
                progress.update(task_id, advance=1)

                return TestResponse(
                    test_id=test_case.id,
                    prompt=test_case.prompt,
                    response=response_text,
                    duration_ms=duration_ms,
                )
            finally:
                self._cleanup_workspace(workspace)

    async def run_suite(
        self,
        version: str,
    ) -> TestResponses:
        """Run all tests in parallel and save responses.

        Parallel execution with isolated workspaces:
        1. Create semaphore to limit concurrency
        2. Each test gets its own workspace and agent
        3. Run all tests concurrently (up to concurrency limit)
        4. Collect and save responses

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
        print_step(f"Mock project: {self._mock_project_path}")
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

                # Launch all tests concurrently
                tasks = [
                    self._run_single_test(test_case, semaphore, progress, task_id)
                    for test_case in suite.test_cases
                ]
                responses = await asyncio.gather(*tasks)

        finally:
            # Cleanup any remaining workspaces
            self._cleanup_all_workspaces()

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
        """Save responses to YAML file."""
        version_dir = self._data_path / "versions" / version
        version_dir.mkdir(parents=True, exist_ok=True)

        output_file = version_dir / "responses.yaml"
        data = responses.model_dump(mode="json")

        with output_file.open("w") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

        print_success(f"Responses saved: {output_file}")


__all__ = ["TestRunner"]
