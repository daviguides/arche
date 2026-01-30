"""Agent for testing Arche principles.

Sends test prompts to Claude with Arche principles loaded
and collects responses for analysis.
"""

import time
from pathlib import Path
from typing import Final

from arche_tester.agents.base_agent import BaseAgent
from arche_tester.config import ClaudeModel, settings

LOAD_PROMPT_PATH: Final[str] = "prompts/load-essential.md"


class ArcheTestAgent(BaseAgent):
    """Agent for testing Arche principles.

    Inherits connection management and SDK communication from BaseAgent.
    Adds Arche-specific functionality for principle loading and testing.
    """

    def __init__(
        self,
        arche_path: Path,
        cwd: Path | None = None,
        verbose: bool = True,
        skip_cli_check: bool = False,
        model: ClaudeModel | None = None,
        resume: str | None = None,
        fork_session: bool = False,
    ) -> None:
        """Initialize test agent.

        Args:
            arche_path: Path to arche bundle directory.
            cwd: Working directory for agent (defaults to arche_path.parent).
            verbose: Enable detailed logging.
            skip_cli_check: Skip Claude CLI check (for nested sessions).
            model: Claude model (defaults to settings.test_agent.model).
            resume: Session ID to resume from.
            fork_session: Fork from resumed session.
        """
        self._arche_path = arche_path
        # Use custom cwd if provided, otherwise default to arche parent
        working_dir = cwd if cwd is not None else arche_path.parent
        super().__init__(
            cwd=working_dir,
            verbose=verbose,
            skip_cli_check=skip_cli_check,
            model=model or settings.test_agent.model,
            permission_mode=settings.test_agent.permission_mode,
            resume=resume,
            fork_session=fork_session,
        )

    @property
    def agent_name(self) -> str:
        """Return agent identifier."""
        return "arche-test-agent"

    async def load_arche_principles(self) -> str:
        """Load Arche principles into agent context.

        Returns:
            Response confirming principles loaded.
        """
        load_prompt = self._arche_path / LOAD_PROMPT_PATH
        prompt = f"Load Arche principles from: {load_prompt}"
        return await self._call_agent(prompt)

    async def run_test(
        self,
        prompt: str,
        context: str | None = None,
    ) -> tuple[str, int]:
        """Run a test prompt and return response.

        Args:
            prompt: Test prompt to send.
            context: Optional additional context.

        Returns:
            Tuple of (response_text, duration_ms).
        """
        full_prompt = prompt
        if context:
            full_prompt = f"{prompt}\n\nContext:\n{context}"

        start_time = time.time()
        response = await self._call_agent(full_prompt)
        duration_ms = int((time.time() - start_time) * 1000)

        return response, duration_ms


__all__ = ["ArcheTestAgent"]
