"""Agent for testing Arche principles.

Sends test prompts to Claude with Arche principles loaded
and collects responses for analysis.
"""

import time
from pathlib import Path
from typing import Final

from arche_tester.agents.base_agent import BaseAgent

LOAD_PROMPT_PATH: Final[str] = "prompts/load-essential.md"


class ArcheTestAgent(BaseAgent):
    """Agent for testing Arche principles.

    Inherits connection management and SDK communication from BaseAgent.
    Adds Arche-specific functionality for principle loading and testing.
    """

    def __init__(
        self,
        arche_path: Path,
        verbose: bool = True,
        skip_cli_check: bool = False,
    ) -> None:
        """Initialize test agent.

        Args:
            arche_path: Path to arche bundle directory.
            verbose: Enable detailed logging.
            skip_cli_check: Skip Claude CLI check (for nested sessions).
        """
        self._arche_path = arche_path
        super().__init__(
            cwd=arche_path.parent,
            verbose=verbose,
            skip_cli_check=skip_cli_check,
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
