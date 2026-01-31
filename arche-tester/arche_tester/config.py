"""Configuration management for Arche Tester.

Uses pydantic-settings for type-safe environment variable loading.
"""

from enum import StrEnum
from pathlib import Path
from typing import Final

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Constants
DEFAULT_SETTING_SOURCES: Final[list[str]] = ["user", "project", "local"]
DEFAULT_TEST_WORKSPACE: Final[Path] = Path("/tmp/arche-test")
ARCHE_PLUGIN_PATH: Final[Path] = Path.home() / ".claude" / "arche"


class ClaudeModel(StrEnum):
    """Supported Claude models.

    Claude Agent SDK expects: "haiku", "sonnet", "opus", or "inherit"
    """

    HAIKU = "haiku"
    SONNET = "sonnet"
    OPUS = "opus"


class ClaudeOptions(BaseSettings):
    """Claude SDK options."""

    setting_sources: list[str] = Field(
        default_factory=lambda: list(DEFAULT_SETTING_SOURCES)
    )


class TestAgentSettings(BaseSettings):
    """Settings for ArcheTestAgent (runs test prompts)."""

    model: ClaudeModel = ClaudeModel.SONNET
    allowed_tools: list[str] = Field(default_factory=lambda: ["Skill", "Read", "Glob", "Grep"])
    permission_mode: str = "bypassPermissions"
    include_partial_messages: bool = True


class AnalyzerAgentSettings(BaseSettings):
    """Settings for AnalyzerAgent (evaluates responses)."""

    model: ClaudeModel = ClaudeModel.HAIKU
    allowed_tools: list[str] = Field(default_factory=list)
    permission_mode: str = "bypassPermissions"
    include_partial_messages: bool = True


class TesterSettings(BaseSettings):
    """Root settings for Arche Tester."""

    model_config = SettingsConfigDict(
        env_prefix="ARCHE_TESTER_",
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    # Claude SDK options
    claude_options: ClaudeOptions = Field(default_factory=ClaudeOptions)

    # Agent configurations
    test_agent: TestAgentSettings = Field(default_factory=TestAgentSettings)
    analyzer_agent: AnalyzerAgentSettings = Field(default_factory=AnalyzerAgentSettings)

    # Paths
    test_workspace: Path = DEFAULT_TEST_WORKSPACE
    data_path: Path = Field(
        default=Path("data"),
        description="Path to test data directory",
    )

    # Logging
    verbose: bool = True


# Global settings instance
settings = TesterSettings()


__all__ = [
    "ClaudeModel",
    "ClaudeOptions",
    "TestAgentSettings",
    "AnalyzerAgentSettings",
    "TesterSettings",
    "settings",
    "DEFAULT_SETTING_SOURCES",
    "DEFAULT_TEST_WORKSPACE",
    "ARCHE_PLUGIN_PATH",
]
