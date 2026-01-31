"""Base agent abstract class for Claude Agent SDK integration.

Provides common functionality for all agents:
- CLI dependency check
- Connection management (lazy)
- Verbose logging
- Agent SDK calls with streaming
"""

import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Final

from claude_agent_sdk import (  # type: ignore[import-untyped]
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
)
from rich.console import Console

from arche_tester.config import ARCHE_PLUGIN_PATH, ClaudeModel, settings

MAX_RETRIES: Final[int] = 3


class DependencyError(Exception):
    """Raised when Claude CLI is not available."""


class BaseAgent(ABC):
    """Abstract base class for Claude Agent SDK agents.

    Subclasses must implement:
    - agent_name property

    Subclasses may override:
    - allowed_tools property
    - model property
    """

    def __init__(
        self,
        cwd: Path | str,
        verbose: bool = True,
        skip_cli_check: bool = True,
        console: Console | None = None,
        model: ClaudeModel | None = None,
        permission_mode: str = "bypassPermissions",
        resume: str | None = None,
        fork_session: bool = False,
    ) -> None:
        """Initialize base agent.

        Args:
            cwd: Working directory for agent.
            verbose: Enable detailed logging.
            skip_cli_check: Skip Claude CLI check (for nested sessions).
            console: Optional Rich console for output.
            model: Claude model to use (haiku, sonnet, opus).
            permission_mode: Claude permission mode.
            resume: Session ID to resume from.
            fork_session: Fork from resumed session (keeps context, isolated).
        """
        self._verbose = verbose
        self._console = console or Console()
        self._model = model
        self._cwd = str(cwd)

        if not skip_cli_check:
            self._check_claude_cli()

        options = ClaudeAgentOptions(
            model=self._model.value if self._model else None,
            allowed_tools=self.allowed_tools,
            permission_mode=permission_mode,
            include_partial_messages=True,
            cwd=self._cwd,
            resume=resume,
            fork_session=fork_session,
            setting_sources=settings.claude_options.setting_sources,
            plugins=[{"type": "local", "path": str(ARCHE_PLUGIN_PATH)}],
        )

        self._client = ClaudeSDKClient(options=options)
        self._connected = False
        self._session_id: str | None = None

    @property
    @abstractmethod
    def agent_name(self) -> str:
        """Unique agent identifier (e.g., 'arche-test-agent')."""
        ...

    @property
    def allowed_tools(self) -> list[str]:
        """Tools allowed for this agent. Override for custom tools."""
        return ["Read", "Glob", "Grep"]

    @staticmethod
    def _check_claude_cli() -> None:
        """Check if Claude CLI is installed."""
        try:
            subprocess.run(
                ["claude", "--version"],
                capture_output=True,
                text=True,
                check=True,
                timeout=5,
            )
        except FileNotFoundError as e:
            raise DependencyError(
                "Claude CLI not found. "
                "Install: npm install -g @anthropic-ai/claude-code"
            ) from e
        except subprocess.CalledProcessError as e:
            raise DependencyError(
                f"Claude CLI check failed: {e.stderr.strip()}"
            ) from e
        except subprocess.TimeoutExpired as e:
            raise DependencyError(
                "Claude CLI check timed out after 5 seconds"
            ) from e

    async def connect(self) -> None:
        """Connect to Claude Agent SDK (lazy connection)."""
        if not self._connected:
            self._log("Connecting to Claude Agent SDK...")
            await self._client.connect()
            self._connected = True
            self._log("Connected", "green")

    async def disconnect(self) -> None:
        """Disconnect from agent."""
        if self._connected:
            await self._client.disconnect()
            self._connected = False

    @property
    def session_id(self) -> str | None:
        """Return current session ID (available after first call)."""
        return self._session_id

    def _log(
        self,
        message: str,
        style: str = "dim",
    ) -> None:
        """Log message if verbose mode enabled."""
        if self._verbose:
            self._console.print(f"  [{style}]{message}[/{style}]")

    async def _call_agent(self, prompt: str) -> str:
        """Call Agent SDK and collect response.

        Args:
            prompt: Prompt to send.

        Returns:
            Response text (last text block).

        Raises:
            ValueError: If no text in response.
        """
        await self.connect()

        self._log(f"[{self.agent_name}] Sending ({len(prompt)} chars)...")
        await self._client.query(prompt)

        text_blocks: list[str] = []
        tool_count = 0

        async for message in self._client.receive_messages():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        text_blocks.append(block.text)
                        preview = block.text[:80].replace("\n", " ")
                        self._log(f"TextBlock: {preview}...")
                    elif isinstance(block, ToolUseBlock):
                        tool_count += 1
                        self._log(f"Tool: {block.name}", "cyan")

            elif isinstance(message, ResultMessage):
                self._session_id = message.session_id
                self._log(f"Agent completed (session: {self._session_id[:8]}...)", "green")
                break

        self._log(f"Received {len(text_blocks)} blocks, {tool_count} tools")

        if not text_blocks:
            raise ValueError(
                f"[{self.agent_name}] No text in agent response"
            )

        return text_blocks[-1]


__all__ = ["BaseAgent", "DependencyError", "MAX_RETRIES"]
