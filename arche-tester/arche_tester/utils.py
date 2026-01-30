"""Utility functions for Arché Tester.

Shared helpers for console output, formatting, and common operations.
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Shared console instance
console = Console()


def format_duration(ms: int | None) -> str:
    """Format milliseconds into human-readable duration.

    Args:
        ms: Duration in milliseconds (None returns "—").

    Returns:
        Formatted string: "500ms", "1.2s", "1m 30s", "1h 5m".

    Examples:
        >>> format_duration(500)
        '500ms'
        >>> format_duration(1500)
        '1.5s'
        >>> format_duration(90000)
        '1m 30s'
        >>> format_duration(None)
        '—'
    """
    if ms is None:
        return "—"

    if ms < 1000:
        return f"{ms}ms"

    seconds = ms / 1000
    if seconds < 60:
        return f"{seconds:.1f}s"

    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)

    if minutes < 60:
        return f"{minutes}m {remaining_seconds}s"

    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours}h {remaining_minutes}m"


def format_percentage(value: float, decimal_places: int = 1) -> str:
    """Format a float as a percentage string.

    Args:
        value: The percentage value (0-100).
        decimal_places: Number of decimal places to show.

    Returns:
        Formatted percentage string.

    Examples:
        >>> format_percentage(85.5)
        '85.5%'
        >>> format_percentage(100.0, 0)
        '100%'
    """
    return f"{value:.{decimal_places}f}%"


def print_header(title: str, version: str | None = None) -> None:
    """Print styled command header.

    Args:
        title: The main header title.
        version: Optional version string to display.
    """
    header = Text()
    header.append("🏛️  ", style="bold")
    header.append(title, style="bold white")
    if version:
        header.append(f" v{version}", style="bold cyan")

    console.print()
    console.print(Panel(header, border_style="blue", padding=(0, 2)))
    console.print()


def print_step(message: str, style: str = "dim") -> None:
    """Print indented step message.

    Args:
        message: The message to print.
        style: Rich style to apply (default: "dim").
    """
    console.print(f"  [{style}]{message}[/{style}]")


def print_success(message: str) -> None:
    """Print success message with checkmark.

    Args:
        message: The success message to print.
    """
    console.print(f"\n[bold green]✓ {message}[/bold green]\n")


def print_error(message: str) -> None:
    """Print error message with X mark.

    Args:
        message: The error message to print.
    """
    console.print(f"\n[bold red]✗ {message}[/bold red]\n")


def print_warning(message: str) -> None:
    """Print warning message with exclamation mark.

    Args:
        message: The warning message to print.
    """
    console.print(f"\n[bold yellow]⚠ {message}[/bold yellow]\n")


def print_info(message: str) -> None:
    """Print info message with info icon.

    Args:
        message: The info message to print.
    """
    console.print(f"\n[bold blue]ℹ {message}[/bold blue]\n")


__all__ = [
    "console",
    "format_duration",
    "format_percentage",
    "print_error",
    "print_header",
    "print_info",
    "print_step",
    "print_success",
    "print_warning",
]
