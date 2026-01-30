"""Test runner for Arché functional tests.

Executes test suite against isolated mock project environments.
"""

import shutil
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

    Each test runs in an isolated copy of the mock project to ensure:
    - Clean state for each test
    - Real file operations can be performed
    - No interference between tests
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

    def load_test_suite(self) -> TestSuite:
        """Load test cases from YAML."""
        test_file = self._data_path / "test-cases" / "functional-tests.yaml"
        content = test_file.read_text()
        data = yaml.safe_load(content)
        return TestSuite.model_validate(data)

    def _create_test_environment(self) -> Path:
        """Create isolated test environment by copying mock project.

        Returns:
            Path to the temporary test directory.
        """
        # Ensure temp base exists
        self._temp_base.mkdir(parents=True, exist_ok=True)

        # Create unique directory for this test
        test_id = str(uuid.uuid4())[:8]
        test_dir = self._temp_base / f"test-{test_id}"

        # Copy mock project to temp
        shutil.copytree(self._mock_project_path, test_dir)

        return test_dir

    def _cleanup_test_environment(self, test_dir: Path) -> None:
        """Remove test environment after test completion.

        Args:
            test_dir: Path to the temporary test directory.
        """
        if test_dir.exists() and test_dir.is_relative_to(self._temp_base):
            shutil.rmtree(test_dir)

    async def run_suite(
        self,
        version: str,
    ) -> TestResponses:
        """Run all tests and save responses.

        Each test runs in an isolated environment:
        1. Copy mock-project to /tmp/arche-test/test-{uuid}/
        2. Run agent with cwd pointing to temp directory
        3. Capture response
        4. Clean up temp directory

        Args:
            version: Arché version being tested.

        Returns:
            TestResponses with all results.
        """
        print_header("Functional Tests", version)

        suite = self.load_test_suite()
        responses: list[TestResponse] = []
        total = len(suite.test_cases)

        print_step(f"Running {total} tests against Arché principles")
        print_step(f"Model: [cyan]{settings.test_agent.model.value}[/cyan]")
        print_step(f"Mock project: {self._mock_project_path}")
        print_step(f"Temp directory: {self._temp_base}")
        console.print()

        for idx, test_case in enumerate(suite.test_cases, 1):
            # Create isolated environment for this test
            test_dir = self._create_test_environment()

            try:
                # Create agent with cwd pointing to test directory
                agent = ArcheTestAgent(
                    arche_path=self._arche_path,
                    cwd=test_dir,
                    verbose=False,
                    skip_cli_check=self._skip_cli_check,
                )

                # Show current test panel
                panel = create_test_panel(
                    test_case=test_case,
                    current=idx,
                    total=total,
                    status="loading",
                )

                with Live(panel, console=console, refresh_per_second=4) as live:
                    # Load principles
                    live.update(
                        create_test_panel(
                            test_case=test_case,
                            current=idx,
                            total=total,
                            status="loading principles",
                        )
                    )
                    await agent.load_arche_principles()

                    # Update to running
                    live.update(
                        create_test_panel(
                            test_case=test_case,
                            current=idx,
                            total=total,
                            status="executing",
                        )
                    )

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
                # Always cleanup the test environment
                self._cleanup_test_environment(test_dir)

        result = TestResponses(
            arche_version=version,
            timestamp=datetime.now().isoformat(),
            responses=responses,
        )

        # Save responses
        self._save_responses(version=version, responses=result)

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
