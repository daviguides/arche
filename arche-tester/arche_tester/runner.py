"""Test runner for Arché functional tests.

Executes test suite and saves responses.
"""

from datetime import datetime
from pathlib import Path

import yaml
from rich.live import Live

from arche_tester.agents import ArcheTestAgent
from arche_tester.display import (
    console,
    create_test_panel,
    print_header,
    print_step,
    print_success,
)
from arche_tester.models import (
    TestResponse,
    TestResponses,
    TestSuite,
)


class TestRunner:
    """Runs functional tests against Arché principles."""

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
        self._agent = ArcheTestAgent(
            arche_path=arche_path,
            verbose=False,  # We handle our own display
            skip_cli_check=skip_cli_check,
        )

    def load_test_suite(self) -> TestSuite:
        """Load test cases from YAML."""
        test_file = self._data_path / "test-cases" / "functional-tests.yaml"
        content = test_file.read_text()
        data = yaml.safe_load(content)
        return TestSuite.model_validate(data)

    async def run_suite(
        self,
        version: str,
    ) -> TestResponses:
        """Run all tests and save responses.

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
        print_step(f"Arche path: {self._arche_path}")
        console.print()

        # Load principles first
        print_step("Loading Arché principles...")
        await self._agent.load_arche_principles()
        print_step("Principles loaded", "green")
        console.print()

        for idx, test_case in enumerate(suite.test_cases, 1):
            # Show current test panel
            panel = create_test_panel(
                test_case=test_case,
                current=idx,
                total=total,
                status="sending",
            )

            with Live(panel, console=console, refresh_per_second=4) as live:
                # Update to running
                live.update(
                    create_test_panel(
                        test_case=test_case,
                        current=idx,
                        total=total,
                        status="receiving",
                    )
                )

                response_text, duration_ms = await self._agent.run_test(
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
                    )
                )

            responses.append(
                TestResponse(
                    test_id=test_case.id,
                    prompt=test_case.prompt,
                    response=response_text,
                    duration_ms=duration_ms,
                )
            )

        await self._agent.disconnect()

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
