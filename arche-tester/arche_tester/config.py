"""Configuration management for Arche Tester.

Uses pydantic-settings for type-safe environment variable loading.
"""

from enum import StrEnum
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ClaudeModel(StrEnum):
    """Supported Claude models.

    Claude Agent SDK expects: "haiku", "sonnet", "opus", or "inherit"
    """

    HAIKU = "haiku"
    SONNET = "sonnet"
    OPUS = "opus"


class TestAgentSettings(BaseSettings):
    """Settings for ArcheTestAgent (runs test prompts)."""

    model: ClaudeModel = ClaudeModel.SONNET  # Good balance of speed/quality
    allowed_tools: list[str] = Field(default_factory=lambda: ["Read", "Glob", "Grep"])
    permission_mode: str = "acceptEdits"
    include_partial_messages: bool = True


class AnalyzerAgentSettings(BaseSettings):
    """Settings for AnalyzerAgent (evaluates responses)."""

    model: ClaudeModel = ClaudeModel.HAIKU  # Fast, sufficient for classification
    allowed_tools: list[str] = Field(default_factory=list)  # No tools needed
    permission_mode: str = "acceptEdits"
    include_partial_messages: bool = True


class TesterSettings(BaseSettings):
    """Root settings for Arche Tester."""

    model_config = SettingsConfigDict(
        env_prefix="ARCHE_TESTER_",
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    # Agent configurations
    test_agent: TestAgentSettings = Field(default_factory=TestAgentSettings)
    analyzer_agent: AnalyzerAgentSettings = Field(default_factory=AnalyzerAgentSettings)

    # Paths
    arche_path: Path = Field(
        default=Path("../arche"),
        description="Path to arche bundle directory",
    )
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
    "TestAgentSettings",
    "AnalyzerAgentSettings",
    "TesterSettings",
    "settings",
]
