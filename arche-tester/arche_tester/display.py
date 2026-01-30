"""Rich display components for Arché Tester.

Provides consistent, rich CLI output across all commands.
Display components (panels, tables, progress bars) are defined here.
Basic console output functions are in utils.py but re-exported for compatibility.
"""

from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table
from rich.text import Text

from arche_tester.models import Conformity, TestCase, VersionAnalysis

# Import from utils and re-export for backward compatibility
from arche_tester.utils import (
    console,
    format_duration,
    print_error,
    print_header,
    print_step,
    print_success,
)


def create_progress_bar() -> Progress:
    """Create standard progress bar for test operations."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=30),
        TaskProgressColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        console=console,
        expand=False,
    )


def create_test_panel(
    test_case: TestCase,
    current: int,
    total: int,
    status: str = "analyzing",
    response: str | None = None,
) -> Panel:
    """Create panel showing current test details."""
    # Header with progress
    pct = (current / total) * 100
    header = Text()
    header.append(f"[{current}/{total}] ", style="bold cyan")
    header.append(f"{pct:.0f}% ", style="bold yellow")
    header.append(test_case.id, style="bold white")

    # Build content
    content = Table.grid(padding=(0, 2))
    content.add_column(style="dim", width=12)
    content.add_column(width=70)

    content.add_row("Principle:", f"[magenta]{test_case.principle.value}[/magenta]")
    content.add_row("Mode:", f"[cyan]{test_case.mode.value}[/cyan]")
    content.add_row("Description:", test_case.description)
    content.add_row("", "")
    content.add_row("Prompt:", f"[italic]{test_case.prompt[:100]}{'...' if len(test_case.prompt) > 100 else ''}[/italic]")

    # Status indicator
    if status == "analyzing":
        status_text = "[yellow]⏳ Analyzing...[/yellow]"
    elif status == "sending":
        status_text = "[blue]📤 Sending to LLM...[/blue]"
    elif status == "receiving":
        status_text = "[blue]📥 Receiving response...[/blue]"
    elif status == "pass":
        status_text = "[green]✓ PASS[/green]"
    elif status == "fail":
        status_text = "[red]✗ FAIL[/red]"
    elif status == "partial":
        status_text = "[yellow]◐ PARTIAL[/yellow]"
    elif status == "skipped":
        status_text = "[dim]⊘ SKIPPED[/dim]"
    else:
        status_text = f"[dim]{status}[/dim]"

    content.add_row("", "")
    content.add_row("Status:", status_text)

    # Show response preview if available
    if response:
        content.add_row("", "")
        # Truncate and clean response for display
        preview = response.replace("\n", " ")[:200]
        if len(response) > 200:
            preview += "..."
        content.add_row("Response:", f"[dim]{preview}[/dim]")

    return Panel(
        content,
        title=str(header),
        border_style="blue",
        padding=(1, 2),
    )


def create_analysis_summary(analysis: VersionAnalysis) -> Panel:
    """Create rich summary panel for analysis results."""
    # Results table
    results = Table(show_header=False, box=None, padding=(0, 2))
    results.add_column(style="dim", width=15)
    results.add_column(justify="right", width=10)

    results.add_row("Total Tests", f"[bold]{analysis.total_tests}[/bold]")
    results.add_row("Passed", f"[green]{analysis.passed}[/green]")
    results.add_row("Failed", f"[red]{analysis.failed}[/red]")
    results.add_row("Partial", f"[yellow]{analysis.partial}[/yellow]")
    results.add_row("Skipped", f"[dim]{analysis.skipped}[/dim]")
    results.add_row("", "")
    results.add_row("Pass Rate (strict)", f"{analysis.pass_rate:.1f}%")
    results.add_row(
        "Weighted Rate",
        f"[bold cyan]{analysis.weighted_rate:.1f}%[/bold cyan]",
    )

    # Color based on weighted rate
    if analysis.weighted_rate >= 80:
        border_style = "green"
        title_style = "bold green"
    elif analysis.weighted_rate >= 60:
        border_style = "yellow"
        title_style = "bold yellow"
    else:
        border_style = "red"
        title_style = "bold red"

    return Panel(
        results,
        title=f"[{title_style}]Analysis Summary - v{analysis.arche_version}[/{title_style}]",
        border_style=border_style,
        padding=(1, 2),
    )


def create_test_result_row(
    test_id: str,
    conformity: Conformity,
    principle: str,
    mode: str,
) -> tuple[str, str, str, str]:
    """Create formatted row for test results table."""
    if conformity == Conformity.PASS:
        status = "[green]✓ PASS[/green]"
    elif conformity == Conformity.FAIL:
        status = "[red]✗ FAIL[/red]"
    elif conformity == Conformity.SKIPPED:
        status = "[dim]⊘ SKIPPED[/dim]"
    else:
        status = "[yellow]◐ PARTIAL[/yellow]"

    return (
        f"[bold]{test_id}[/bold]",
        status,
        f"[magenta]{principle}[/magenta]",
        f"[cyan]{mode}[/cyan]",
    )


def create_results_table(analysis: VersionAnalysis) -> Table:
    """Create detailed results table."""
    table = Table(
        title=f"Test Results - v{analysis.arche_version}",
        show_lines=True,
    )

    table.add_column("Test ID", style="bold", width=10)
    table.add_column("Result", justify="center", width=12)
    table.add_column("Principle", width=20)
    table.add_column("Mode", width=15)

    for test in analysis.analyses:
        row = create_test_result_row(
            test_id=test.test_id,
            conformity=test.conformity,
            principle=test.principle.value,
            mode=test.mode.value,
        )
        table.add_row(*row)

    return table


__all__ = [
    "console",
    "create_analysis_summary",
    "create_progress_bar",
    "create_results_table",
    "create_test_panel",
    "create_test_result_row",
    "format_duration",
    "print_error",
    "print_header",
    "print_step",
    "print_success",
]
