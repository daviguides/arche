"""Test runner for Arché functional tests.

Executes test suite against isolated mock project environments.
"""

import shutil
import time
import uuid
from datetime import datetime
from pathlib import Path

import yaml
from rich.live import Live

from arche_tester.agents import ArcheTestAgent
from arche_tester.config import settings
from arche_tester.display import (
    console,
    create_test_panel,
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

    Uses fork_session optimization:
    - Load principles once in base session
    - Fork for each test (keeps context, isolated state)
    - Reset workspace between tests (same cwd for fork compatibility)
    """

    def __init__(
        self,
        arche_path: Path,
        data_path: Path,
        verbose: bool = True,
        skip_cli_check: bool = False,
    ) -> None:
        """Initialize runner.

        Args:
            arche_path: Path to arche bundle.
            data_path: Path to data directory.
            verbose: Enable detailed logging.
            skip_cli_check: Skip Claude CLI check (for nested sessions).
        """
        self._arche_path = arche_path
        self._data_path = data_path
        self._verbose = verbose
        self._skip_cli_check = skip_cli_check
        self._mock_project_path = data_path / "mock-project"
        self._temp_base = Path("/tmp/arche-test")
        # Fixed workspace for fork_session compatibility (same cwd always)
        self._workspace = self._temp_base / "workspace"

    def load_test_suite(self) -> TestSuite:
        """Load test cases from YAML."""
        test_file = self._data_path / "test-cases" / "functional-tests.yaml"
        content = test_file.read_text()
        data = yaml.safe_load(content)
        return TestSuite.model_validate(data)

    def _setup_workspace(self) -> Path:
        """Setup fixed workspace directory with fresh mock project copy.

        Returns:
            Path to the workspace directory.
        """
        # Remove existing workspace if present
        if self._workspace.exists():
            shutil.rmtree(self._workspace)

        # Copy mock project to workspace
        shutil.copytree(self._mock_project_path, self._workspace)

        return self._workspace

    def _reset_workspace(self) -> None:
        """Reset workspace to clean state (fresh mock project copy)."""
        if self._workspace.exists():
            shutil.rmtree(self._workspace)
        shutil.copytree(self._mock_project_path, self._workspace)

    def _cleanup_workspace(self) -> None:
        """Remove workspace after all tests complete."""
        if self._workspace.exists():
            shutil.rmtree(self._workspace)

    async def run_suite(
        self,
        version: str,
    ) -> TestResponses:
        """Run all tests and save responses.

        Optimized flow:
        1. Create base agent and load principles once
        2. For each test, fork session (keeps context, isolated state)
        3. Capture response and cleanup

        Args:
            version: Arché version being tested.

        Returns:
            TestResponses with all results.
        """
        start_time = time.time()
        print_header("Functional Tests", version)

        suite = self.load_test_suite()
        responses: list[TestResponse] = []
        total = len(suite.test_cases)

        print_step(f"Running {total} tests against Arché principles")
        print_step(f"Model: [cyan]{settings.test_agent.model.value}[/cyan]")
        print_step(f"Mock project: {self._mock_project_path}")
        print_step(f"Workspace: {self._workspace}")
        console.print()

        # Setup workspace and load principles once
        workspace = self._setup_workspace()
        print_step("Loading Arché principles (base session)...")

        base_agent = ArcheTestAgent(
            arche_path=self._arche_path,
            cwd=workspace,
            verbose=False,
            skip_cli_check=self._skip_cli_check,
        )
        await base_agent.load_arche_principles()
        base_session_id = base_agent.session_id
        await base_agent.disconnect()

        print_step(f"Base session: [dim]{base_session_id[:12]}...[/dim]")
        console.print()

        # Run tests using forked sessions (same cwd = workspace)
        try:
            for idx, test_case in enumerate(suite.test_cases, 1):
                # Reset workspace to clean state before each test
                self._reset_workspace()

                # Create forked agent (same cwd as base)
                agent = ArcheTestAgent(
                    arche_path=self._arche_path,
                    cwd=workspace,
                    verbose=False,
                    skip_cli_check=self._skip_cli_check,
                    resume=base_session_id,
                    fork_session=True,
                )

                # Show current test panel
                panel = create_test_panel(
                    test_case=test_case,
                    current=idx,
                    total=total,
                    status="executing",
                )

                with Live(panel, console=console, refresh_per_second=4) as live:
                    response_text, duration_ms = await agent.run_test(
                        prompt=test_case.prompt,
                        context=test_case.context,
                    )

                    # Update to complete
                    live.update(
                        create_test_panel(
                            test_case=test_case,
                            current=idx,
                            total=total,
                            status=f"done ({duration_ms}ms)",
                            response=response_text,
                        )
                    )

                # Disconnect agent
                await agent.disconnect()

                responses.append(
                    TestResponse(
                        test_id=test_case.id,
                        prompt=test_case.prompt,
                        response=response_text,
                        duration_ms=duration_ms,
                    )
                )

        finally:
            # Cleanup workspace after all tests
            self._cleanup_workspace()

        # Calculate total duration
        total_duration_ms = int((time.time() - start_time) * 1000)

        result = TestResponses(
            arche_version=version,
            timestamp=datetime.now().isoformat(),
            responses=responses,
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
