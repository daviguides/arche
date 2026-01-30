"""Backward compatibility - import from agents subpackage.

DEPRECATED: Use `from arche_tester.agents import ...` instead.
"""

from arche_tester.agents import (  # noqa: F401
    ArcheTestAgent,
    BaseAgent,
    DependencyError,
    MAX_RETRIES,
)

__all__ = ["ArcheTestAgent", "BaseAgent", "DependencyError", "MAX_RETRIES"]
