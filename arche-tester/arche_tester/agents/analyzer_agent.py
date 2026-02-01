"""Agent for semantic analysis of test responses.

Uses Claude Agent SDK to evaluate conformity with expected behaviors
through semantic understanding rather than keyword matching.
"""

import json
from pathlib import Path

from pydantic import BaseModel

from arche_tester.agents.base_agent import BaseAgent
from arche_tester.config import ClaudeModel, settings
from arche_tester.models import BehaviorCheck, Conformity


class BehaviorEvaluation(BaseModel):
    """LLM evaluation result for a single behavior."""

    behavior: str
    present: bool
    confidence: float
    evidence: str
    reasoning: str


class AnalysisResult(BaseModel):
    """Complete analysis result from LLM."""

    evaluations: list[BehaviorEvaluation]


class AnalyzerAgent(BaseAgent):
    """Agent for semantic behavior analysis.

    Uses LLM to evaluate whether responses conform to expected behaviors.
    Provides semantic understanding instead of keyword matching.
    Can load Arché principles for context-aware analysis.
    """

    def __init__(
        self,
        cwd: Path | str,
        verbose: bool = True,
        skip_cli_check: bool = True,
        model: ClaudeModel | None = None,
    ) -> None:
        """Initialize analyzer agent.

        Args:
            cwd: Working directory for agent.
            verbose: Enable detailed logging.
            skip_cli_check: Skip Claude CLI check.
            model: Claude model (defaults to settings.analyzer_agent.model).
        """
        super().__init__(
            cwd=cwd,
            verbose=verbose,
            skip_cli_check=skip_cli_check,
            model=model or settings.analyzer_agent.model,
            permission_mode=settings.analyzer_agent.permission_mode,
        )

    async def load_arche_principles(self) -> str:
        """Load Arché principles using the installed plugin.

        Returns:
            Response confirming principles loaded.
        """
        return await self._call_agent("/arche:load")

    @property
    def agent_name(self) -> str:
        """Return agent identifier."""
        return "analyzer-agent"

    @property
    def allowed_tools(self) -> list[str]:
        """No tools needed - pure text analysis."""
        return []

    async def analyze_response(
        self,
        response: str,
        must_behaviors: list[str],
        must_not_behaviors: list[str],
        transcript: list[dict] | None = None,
    ) -> list[BehaviorCheck]:
        """Analyze response for behavior conformity.

        Args:
            response: Agent response text to analyze.
            must_behaviors: Behaviors that must be present.
            must_not_behaviors: Behaviors that must not be present.
            transcript: Optional transcript for fallback analysis on failure.

        Returns:
            List of BehaviorCheck with LLM-based evaluation.
        """
        # First pass: analyze response only
        prompt = self._build_analysis_prompt(
            response=response,
            must_behaviors=must_behaviors,
            must_not_behaviors=must_not_behaviors,
        )

        result_text = await self._call_agent(prompt)
        result = self._parse_result(result_text)

        checks = self._convert_to_behavior_checks(
            result=result,
            must_behaviors=must_behaviors,
            must_not_behaviors=must_not_behaviors,
        )

        # Second pass: if any FAIL and transcript available, re-analyze with transcript
        has_failures = any(c.result == Conformity.FAIL for c in checks)
        if has_failures and transcript:
            checks = await self._reanalyze_with_transcript(
                response=response,
                transcript=transcript,
                must_behaviors=must_behaviors,
                must_not_behaviors=must_not_behaviors,
                initial_checks=checks,
            )

        return checks

    async def _reanalyze_with_transcript(
        self,
        response: str,
        transcript: list[dict],
        must_behaviors: list[str],
        must_not_behaviors: list[str],
        initial_checks: list[BehaviorCheck],
    ) -> list[BehaviorCheck]:
        """Re-analyze failed behaviors using transcript as evidence.

        Only re-evaluates behaviors that failed in initial analysis.
        """
        # Get failed behaviors
        failed_must = [
            c.behavior for c in initial_checks
            if c.check_type == "must" and c.result == Conformity.FAIL
        ]
        failed_must_not = [
            c.behavior for c in initial_checks
            if c.check_type == "must_not" and c.result == Conformity.FAIL
        ]

        if not failed_must and not failed_must_not:
            return initial_checks

        # Build transcript summary (tool calls only)
        tool_calls = [
            step for step in transcript
            if step.get("type") == "tool" and step.get("name")
        ]
        transcript_summary = self._summarize_transcript(tool_calls)

        prompt = self._build_transcript_analysis_prompt(
            response=response,
            transcript_summary=transcript_summary,
            failed_must=failed_must,
            failed_must_not=failed_must_not,
        )

        result_text = await self._call_agent(prompt)
        result = self._parse_result(result_text)

        # Merge results: update only re-evaluated behaviors
        eval_lookup = {e.behavior: e for e in result.evaluations}
        updated_checks: list[BehaviorCheck] = []

        for check in initial_checks:
            evaluation = eval_lookup.get(check.behavior)
            if evaluation:
                # Re-evaluated - use new result
                if check.check_type == "must":
                    conformity = Conformity.PASS if evaluation.present else Conformity.FAIL
                else:  # must_not
                    conformity = Conformity.FAIL if evaluation.present else Conformity.PASS

                updated_checks.append(
                    BehaviorCheck(
                        behavior=check.behavior,
                        check_type=check.check_type,
                        result=conformity,
                        evidence=f"[transcript] {evaluation.evidence}",
                    )
                )
            else:
                # Keep original
                updated_checks.append(check)

        return updated_checks

    def _summarize_transcript(self, tool_calls: list[dict]) -> str:
        """Create concise summary of tool calls from transcript."""
        lines = []
        for call in tool_calls[:20]:  # Limit to first 20 calls
            name = call.get("name", "unknown")
            inp = call.get("input", {})

            if name == "Glob":
                lines.append(f"- Glob: {inp.get('pattern', '?')}")
            elif name == "Grep":
                lines.append(f"- Grep: {inp.get('pattern', '?')} in {inp.get('path', '.')}")
            elif name == "Read":
                path = inp.get("file_path", "?")
                # Shorten path
                if "/" in path:
                    path = "..." + path.split("/")[-2] + "/" + path.split("/")[-1]
                lines.append(f"- Read: {path}")
            elif name == "Bash":
                cmd = inp.get("command", "?")[:50]
                lines.append(f"- Bash: {cmd}")
            elif name == "Write":
                path = inp.get("file_path", "?")
                if "/" in path:
                    path = "..." + path.split("/")[-1]
                lines.append(f"- Write: {path}")
            elif name == "Edit":
                path = inp.get("file_path", "?")
                if "/" in path:
                    path = "..." + path.split("/")[-1]
                lines.append(f"- Edit: {path}")
            else:
                lines.append(f"- {name}")

        return "\n".join(lines) if lines else "(no tool calls)"

    def _build_transcript_analysis_prompt(
        self,
        response: str,
        transcript_summary: str,
        failed_must: list[str],
        failed_must_not: list[str],
    ) -> str:
        """Build prompt for transcript-based re-analysis."""
        behaviors_json = json.dumps(
            {
                "must": failed_must,
                "must_not": failed_must_not,
            },
            indent=2,
        )

        return f"""Re-analyze these FAILED behaviors using the TRANSCRIPT as additional evidence.

The initial analysis only saw the final response. Now you have the transcript showing
what tools the agent actually used BEFORE producing the response.

## Final Response

```
{response}
```

## Transcript (Tool Calls)

```
{transcript_summary}
```

## Behaviors to Re-evaluate

```json
{behaviors_json}
```

## Instructions

For each behavior, determine if it was actually satisfied based on the TRANSCRIPT:
- "search for existing" → Did the agent use Glob/Grep/Read BEFORE Write/Edit?
- "skip research phase" → Did the agent skip search tools and go straight to Write?
- "reference source file" → Did the agent Read the file before explaining?

Return ONLY valid JSON:

{{
  "evaluations": [
    {{
      "behavior": "exact behavior text",
      "present": true/false,
      "confidence": 0.0-1.0,
      "evidence": "brief description of what transcript shows",
      "reasoning": "explanation"
    }}
  ]
}}

Evaluate ALL behaviors from both lists."""

    def _build_analysis_prompt(
        self,
        response: str,
        must_behaviors: list[str],
        must_not_behaviors: list[str],
    ) -> str:
        """Build prompt for behavior analysis."""
        behaviors_json = json.dumps(
            {
                "must": must_behaviors,
                "must_not": must_not_behaviors,
            },
            indent=2,
        )

        return f"""Analyze the following response for behavioral conformity.

## Response to Analyze

```
{response}
```

## Expected Behaviors

```json
{behaviors_json}
```

## Instructions

For each behavior in both "must" and "must_not" lists:
1. Determine if the behavior is PRESENT in the response
2. Rate your confidence (0.0 to 1.0)
3. Extract evidence quote from response (max 200 chars)
4. Explain your reasoning briefly

## Output Format

Return ONLY valid JSON (no markdown):

{{
  "evaluations": [
    {{
      "behavior": "exact behavior text",
      "present": true/false,
      "confidence": 0.0-1.0,
      "evidence": "quote from response",
      "reasoning": "brief explanation"
    }}
  ]
}}

Evaluate ALL behaviors from both lists."""

    def _parse_result(self, result_text: str) -> AnalysisResult:
        """Parse LLM response to AnalysisResult."""
        # Clean markdown if present
        cleaned = result_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        data = json.loads(cleaned)
        return AnalysisResult.model_validate(data)

    def _convert_to_behavior_checks(
        self,
        result: AnalysisResult,
        must_behaviors: list[str],
        must_not_behaviors: list[str],
    ) -> list[BehaviorCheck]:
        """Convert LLM evaluations to BehaviorCheck models."""
        checks: list[BehaviorCheck] = []

        # Create lookup for evaluations
        eval_lookup = {e.behavior: e for e in result.evaluations}

        # Process "must" behaviors
        for behavior in must_behaviors:
            evaluation = eval_lookup.get(behavior)
            if evaluation:
                # For "must": present=True means PASS
                conformity = (
                    Conformity.PASS if evaluation.present else Conformity.FAIL
                )
                evidence = evaluation.evidence
            else:
                # Not evaluated - assume fail
                conformity = Conformity.FAIL
                evidence = "(not evaluated by LLM)"

            checks.append(
                BehaviorCheck(
                    behavior=behavior,
                    check_type="must",
                    result=conformity,
                    evidence=evidence,
                )
            )

        # Process "must_not" behaviors
        for behavior in must_not_behaviors:
            evaluation = eval_lookup.get(behavior)
            if evaluation:
                # For "must_not": present=True means FAIL
                conformity = (
                    Conformity.FAIL if evaluation.present else Conformity.PASS
                )
                evidence = evaluation.evidence
            else:
                # Not evaluated - assume pass (benefit of doubt)
                conformity = Conformity.PASS
                evidence = "(not evaluated by LLM)"

            checks.append(
                BehaviorCheck(
                    behavior=behavior,
                    check_type="must_not",
                    result=conformity,
                    evidence=evidence,
                )
            )

        return checks


__all__ = ["AnalyzerAgent", "AnalysisResult", "BehaviorEvaluation"]
