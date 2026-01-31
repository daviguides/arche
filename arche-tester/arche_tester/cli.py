"""CLI for Arché functional testing.

Commands for running tests, analyzing results, and comparing versions.
"""

import asyncio
from pathlib import Path

import typer

from arche_tester.analyzer import ResponseAnalyzer
from arche_tester.comparator import VersionComparator
from arche_tester.display import (
    console,
    print_error,
    print_header,
    print_step,
    print_success,
)
from arche_tester.runner import TestRunner

app = typer.Typer(
    name="arche-test",
    help="Functional testing for Arché principles",
)

# Default paths
DEFAULT_DATA_PATH = Path(__file__).parent.parent / "data"


@app.command()
def run(
    version: str = typer.Argument(
        help="Arché version to test (e.g., 0.1.0)",
    ),
    data_path: Path = typer.Option(
        DEFAULT_DATA_PATH,
        "--data-path",
        "-d",
        help="Path to data directory",
    ),
    concurrency: int = typer.Option(
        8,
        "--concurrency",
        "-c",
        help="Number of parallel tests (default: 8)",
    ),
    verbose: bool = typer.Option(
        True,
        "--verbose/--quiet",
        "-v/-q",
        help="Enable verbose output",
    ),
    skip_cli_check: bool = typer.Option(
        True,
        "--skip-cli-check/--check-cli",
        "-s/-S",
        help="Skip Claude CLI check (default: skip)",
    ),
    transcripts: bool = typer.Option(
        True,
        "--transcripts/--no-transcripts",
        "-t/-T",
        help="Capture full transcripts of agent steps (default: enabled)",
    ),
) -> None:
    """Run functional tests for a version."""
    runner = TestRunner(
        data_path=data_path,
        verbose=verbose,
        skip_cli_check=skip_cli_check,
        concurrency=concurrency,
        capture_transcripts=transcripts,
    )

    asyncio.run(runner.run_suite(version=version))


@app.command()
def analyze(
    version: str = typer.Argument(
        help="Version to analyze (e.g., 0.1.0)",
    ),
    data_path: Path = typer.Option(
        DEFAULT_DATA_PATH,
        "--data-path",
        "-d",
        help="Path to data directory",
    ),
    use_llm: bool = typer.Option(
        True,
        "--use-llm/--no-llm",
        "-l/-L",
        help="Use LLM-based semantic analysis (default) or keyword matching",
    ),
    skip_cli_check: bool = typer.Option(
        True,
        "--skip-cli-check/--check-cli",
        "-s/-S",
        help="Skip Claude CLI check (default: skip)",
    ),
) -> None:
    """Analyze test responses for a version."""
    # Validate version directory exists
    version_dir = data_path / "versions" / version
    if not version_dir.exists():
        print_error(f"Version directory not found: {version_dir}")
        print_step("Run tests first with: arche-test run {version}")
        raise typer.Exit(1)

    # Validate responses.yaml exists
    responses_file = version_dir / "responses.yaml"
    if not responses_file.exists():
        print_error(f"Responses file not found: {responses_file}")
        print_step("Run tests first with: arche-test run {version}")
        raise typer.Exit(1)

    analyzer = ResponseAnalyzer(
        data_path=data_path,
        use_llm=use_llm,
        skip_cli_check=skip_cli_check,
    )

    if use_llm:
        asyncio.run(analyzer.analyze_version_async(version=version))
    else:
        analyzer.analyze_version(version=version)


@app.command()
def compare(
    baseline: str = typer.Argument(
        help="Baseline version (e.g., 0.1.0)",
    ),
    current: str = typer.Argument(
        help="Current version (e.g., 0.2.0)",
    ),
    data_path: Path = typer.Option(
        DEFAULT_DATA_PATH,
        "--data-path",
        "-d",
        help="Path to data directory",
    ),
) -> None:
    """Compare versions for degradation."""
    print_header("Version Comparison", f"{baseline} → {current}")

    comparator = VersionComparator(data_path=data_path)
    comparator.compare(
        baseline_version=baseline,
        current_version=current,
    )


@app.command()
def report(
    phase: int = typer.Argument(
        help="Phase number (1, 2, or 3)",
    ),
    baseline: str = typer.Option(
        "0.1.0",
        "--baseline",
        "-b",
        help="Baseline version",
    ),
    data_path: Path = typer.Option(
        DEFAULT_DATA_PATH,
        "--data-path",
        "-d",
        help="Path to data directory",
    ),
) -> None:
    """Generate report for a phase."""
    version_map = {1: "0.2.0", 2: "0.3.0", 3: "0.4.0"}
    current = version_map.get(phase)

    if not current:
        print_error(f"Invalid phase: {phase}. Use 1, 2, or 3.")
        raise typer.Exit(1)

    print_header("Phase Report", f"Phase {phase}")
    print_step(f"Comparing {baseline} → {current}")

    comparator = VersionComparator(data_path=data_path)
    report_path = comparator.generate_report(
        baseline_version=baseline,
        current_version=current,
        phase=phase,
    )

    print_success(f"Report ready: {report_path}")


@app.command()
def baseline(
    data_path: Path = typer.Option(
        DEFAULT_DATA_PATH,
        "--data-path",
        "-d",
        help="Path to data directory",
    ),
    concurrency: int = typer.Option(
        8,
        "--concurrency",
        "-c",
        help="Number of parallel tests (default: 8)",
    ),
    skip_cli_check: bool = typer.Option(
        True,
        "--skip-cli-check/--check-cli",
        "-s/-S",
        help="Skip Claude CLI check (default: skip)",
    ),
    use_llm: bool = typer.Option(
        True,
        "--use-llm/--no-llm",
        "-l/-L",
        help="Use LLM-based semantic analysis (default) or keyword matching",
    ),
    transcripts: bool = typer.Option(
        True,
        "--transcripts/--no-transcripts",
        "-t/-T",
        help="Capture full transcripts of agent steps (default: enabled)",
    ),
) -> None:
    """Run baseline tests (v0.1.0) and analyze."""
    print_header("Baseline Execution", "0.1.0")

    # Run tests
    print_step("Phase 1: Running functional tests...")
    console.print()

    runner = TestRunner(
        data_path=data_path,
        verbose=True,
        skip_cli_check=skip_cli_check,
        concurrency=concurrency,
        capture_transcripts=transcripts,
    )
    asyncio.run(runner.run_suite(version="0.1.0"))

    # Analyze
    console.print()
    print_step("Phase 2: Analyzing responses...")
    console.print()

    analyzer = ResponseAnalyzer(
        data_path=data_path,
        use_llm=use_llm,
        skip_cli_check=skip_cli_check,
    )

    if use_llm:
        asyncio.run(analyzer.analyze_version_async(version="0.1.0"))
    else:
        analyzer.analyze_version(version="0.1.0")

    print_success("Baseline complete!")


if __name__ == "__main__":
    app()
