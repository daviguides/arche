"""Agent for testing Arche principles.

Sends test prompts to Claude with Arche principles loaded
and collects responses for analysis.
"""

import time
from pathlib import Path
from typing import Any

from arche_tester.agents.base_agent import BaseAgent
from arche_tester.config import ClaudeModel, settings


class ArcheTestAgent(BaseAgent):
    """Agent for testing Arche principles.

    Inherits connection management and SDK communication from BaseAgent.
    Adds Arche-specific functionality for principle loading and testing.
    """

    def __init__(
        self,
        cwd: Path,
        verbose: bool = True,
        skip_cli_check: bool = True,
        model: ClaudeModel | None = None,
        resume: str | None = None,
        fork_session: bool = False,
    ) -> None:
        """Initialize test agent.

        Args:
            cwd: Working directory for agent.
            verbose: Enable detailed logging.
            skip_cli_check: Skip Claude CLI check (for nested sessions).
            model: Claude model (defaults to settings.test_agent.model).
            resume: Session ID to resume from.
            fork_session: Fork from resumed session (keeps context, isolated).
        """
        super().__init__(
            cwd=cwd,
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
        """Load Arche principles using the installed plugin.

        Returns:
            Response confirming principles loaded.
        """
        return await self._call_agent("/arche:load-essential")

    async def run_test(
        self,
        prompt: str,
        context: str | None = None,
        work_dir: str | None = None,
        capture_transcript: bool = False,
    ) -> tuple[str, int] | tuple[str, int, list[dict[str, Any]]]:
        """Run a test prompt and return response.

        Args:
            prompt: Test prompt to send.
            context: Optional additional context.
            work_dir: Subdirectory to work in (for fork_session isolation).
            capture_transcript: If True, return transcript of all steps.

        Returns:
            Tuple of (response_text, duration_ms) or
            (response_text, duration_ms, transcript) if capture_transcript=True.
        """
        full_prompt = prompt

        # Direct agent to work in specific subdirectory
        if work_dir:
            full_prompt = f"Work in the `{work_dir}/` directory.\n\n{prompt}"

        if context:
            full_prompt = f"{full_prompt}\n\nContext:\n{context}"

        start_time = time.time()
        result = await self._call_agent(full_prompt, capture_transcript=capture_transcript)
        duration_ms = int((time.time() - start_time) * 1000)

        if capture_transcript:
            response, transcript = result
            return response, duration_ms, transcript
        return result, duration_ms


__all__ = ["ArcheTestAgent"]
