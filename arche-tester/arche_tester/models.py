"""Pydantic models for test cases and results.

Defines schema for functional tests, responses, and analysis.
"""

from enum import Enum
from pydantic import BaseModel, Field


class Principle(str, Enum):
    """Arché principles under test."""

    PRINCIPLE_ENFORCEMENT = "principle-enforcement"
    ANTI_DUPLICATION = "anti-duplication"
    ANTI_PRECOCITY = "anti-precocity"
    ANTI_BABYSITTING = "anti-babysitting"
    LLM_CONCISENESS = "llm-conciseness"


class CognitiveMode(str, Enum):
    """Essential cognitive modes."""

    EXPLORING = "EXPLORING"
    RESEARCHING = "RESEARCHING"
    PLANNING = "PLANNING"
    IMPLEMENTING = "IMPLEMENTING"


class ExpectedBehavior(BaseModel):
    """Expected behavior for a test case."""

    must: list[str] = Field(default_factory=list)
    must_not: list[str] = Field(default_factory=list)


class TestCase(BaseModel):
    """Single functional test case."""

    id: str = Field(description="Unique test case ID (e.g., AP-001)")
    principle: Principle
    mode: CognitiveMode
    description: str = Field(description="What this test validates")
    prompt: str = Field(description="Prompt to send to agent")
    context: str | None = Field(
        default=None,
        description="Additional context (file content, etc.)",
    )
    expected: ExpectedBehavior


class TestSuite(BaseModel):
    """Collection of test cases."""

    version: str = Field(description="Test suite version")
    test_cases: list[TestCase]


class TestResponse(BaseModel):
    """Response from agent for a test case."""

    test_id: str
    prompt: str
    response: str
    duration_ms: int | None = None
    tokens_used: int | None = None


class TestResponses(BaseModel):
    """All responses for a version."""

    arche_version: str
    timestamp: str
    responses: list[TestResponse]


class Conformity(str, Enum):
    """Conformity assessment result.

    SKIPPED is used when a test cannot be evaluated due to:
    - Missing dependencies or prerequisites
    - Test case not applicable to current context
    - External service unavailable during analysis
    - Response empty or malformed beyond recovery

    SKIPPED tests are excluded from pass_rate calculations.
    """

    PASS = "pass"
    FAIL = "fail"
    PARTIAL = "partial"
    SKIPPED = "skipped"


class BehaviorCheck(BaseModel):
    """Result of checking a single behavior.

    When result is SKIPPED, evidence should contain the skip reason.
    """

    behavior: str
    check_type: str = Field(description="must or must_not")
    result: Conformity
    evidence: str = Field(
        description="Quote from response supporting result, or skip reason if SKIPPED"
    )


class TestAnalysis(BaseModel):
    """Analysis of a single test response."""

    test_id: str
    principle: Principle
    mode: CognitiveMode
    conformity: Conformity
    behavior_checks: list[BehaviorCheck]
    notes: str | None = None


class VersionAnalysis(BaseModel):
    """Complete analysis for a version."""

    arche_version: str
    timestamp: str
    total_tests: int
    passed: int
    failed: int
    partial: int
    skipped: int = Field(default=0, description="Tests that could not be evaluated")
    pass_rate: float = Field(
        description="Percentage 0-100 (passed only, excludes skipped)"
    )
    weighted_rate: float = Field(
        default=0.0,
        description="Percentage 0-100 (passed + partial*0.5, excludes skipped)",
    )
    analyses: list[TestAnalysis]


class Degradation(BaseModel):
    """Degradation comparison between versions."""

    test_id: str
    baseline_conformity: Conformity
    current_conformity: Conformity
    degraded: bool
    notes: str | None = None


class VersionComparison(BaseModel):
    """Comparison between baseline and current version."""

    baseline_version: str
    current_version: str
    timestamp: str
    baseline_pass_rate: float
    current_pass_rate: float
    degradation_pct: float = Field(description="Negative = improvement")
    degradations: list[Degradation]
    summary: str
