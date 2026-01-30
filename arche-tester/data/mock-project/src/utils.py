"""Utility functions for the mock project.

Contains helpers for formatting, validation, and data processing.
"""

from datetime import datetime
from typing import Any


def format_date(dt: datetime) -> str:
    """Format datetime as ISO string."""
    return dt.isoformat()


def parse_date(date_str: str) -> datetime:
    """Parse ISO format date string."""
    return datetime.fromisoformat(date_str)


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format amount as currency string."""
    symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:.2f}"


def format_duration(seconds: int) -> str:
    """Format seconds as human-readable duration."""
    if seconds < 60:
        return f"{seconds}s"
    minutes = seconds // 60
    remaining = seconds % 60
    if minutes < 60:
        return f"{minutes}m {remaining}s"
    hours = minutes // 60
    remaining_mins = minutes % 60
    return f"{hours}h {remaining_mins}m"


# Duplicate validation (also exists in models.py - for anti-duplication tests)
def validate_email(email: str) -> bool:
    """Validate email format."""
    return "@" in email and "." in email.split("@")[1]


def validate_url(url: str) -> bool:
    """Validate URL format."""
    return url.startswith("http://") or url.startswith("https://")


def sanitize_string(value: str) -> str:
    """Remove dangerous characters from string."""
    dangerous = ["<", ">", "&", '"', "'"]
    result = value
    for char in dangerous:
        result = result.replace(char, "")
    return result


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Deep merge two dictionaries."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def chunk_list(items: list[Any], size: int) -> list[list[Any]]:
    """Split list into chunks of given size."""
    return [items[i:i + size] for i in range(0, len(items), size)]
