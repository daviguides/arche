"""Pydantic models for test cases and results.

This module defines the schema for functional tests, responses, and analysis
results used throughout the Arché Tester framework.

Example:
    Loading and validating a test suite::

        import yaml
        from arche_tester.models import TestSuite

        with open("functional-tests.yaml") as f:
            data = yaml.safe_load(f)
        suite = TestSuite.model_validate(data)
"""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class Principle(str, Enum):
    """Arché principles under test.

    Each principle represents a core behavioral guideline that LLM agents
    should follow when operating under the Arché framework.

    Attributes:
        PRINCIPLE_ENFORCEMENT: Ensures principles are actively enforced.
        ANTI_DUPLICATION: Prevents redundant explanations or code.
        ANTI_PRECOCITY: Prevents premature action before understanding.
        ANTI_BABYSITTING: Prevents excessive hand-holding or over-explaining.
        LLM_CONCISENESS: Ensures responses are appropriately concise.
    """

    PRINCIPLE_ENFORCEMENT = "principle-enforcement"
    ANTI_DUPLICATION = "anti-duplication"
    ANTI_PRECOCITY = "anti-precocity"
    ANTI_BABYSITTING = "anti-babysitting"
    LLM_CONCISENESS = "llm-conciseness"


class CognitiveMode(str, Enum):
    """Essential cognitive modes for agent operation.

    Defines the operational context that affects expected agent behavior.
    Different modes have different behavioral expectations.

    Attributes:
        EXPLORING: Initial discovery and orientation phase.
        RESEARCHING: Deep investigation and analysis phase.
        PLANNING: Strategy and approach definition phase.
        IMPLEMENTING: Active code writing and modification phase.
    """

    EXPLORING = "EXPLORING"
    RESEARCHING = "RESEARCHING"
    PLANNING = "PLANNING"
    IMPLEMENTING = "IMPLEMENTING"


class ExpectedBehavior(BaseModel):
    """Expected behavior specification for a test case.

    Defines what behaviors must be present and what behaviors must be
    absent in an agent's response for a test to pass.

    Attributes:
        must: List of behaviors that must be present in the response.
        must_not: List of behaviors that must not be present in the response.

    Example:
        >>> behavior = ExpectedBehavior(
        ...     must=["provide analysis", "cite sources"],
        ...     must_not=["suggest changes", "create TODO list"]
        ... )
    """

    must: list[str] = Field(default_factory=list)
    must_not: list[str] = Field(default_factory=list)


class TestCase(BaseModel):
    """Single functional test case definition.

    Represents a complete test specification including the prompt to send,
    expected behaviors, and metadata for categorization.

    Attributes:
        id: Unique test case identifier (e.g., "AP-001").
        principle: The Arché principle being tested.
        mode: The cognitive mode context for the test.
        description: Human-readable description of what the test validates.
        prompt: The prompt text to send to the agent.
        context: Optional additional context (file content, etc.).
        expected: Expected behavior specification.

    Raises:
        ValueError: If id is empty or whitespace-only.

    Example:
        >>> test = TestCase(
        ...     id="AP-001",
        ...     principle=Principle.ANTI_PRECOCITY,
        ...     mode=CognitiveMode.EXPLORING,
        ...     description="Test exploration behavior",
        ...     prompt="Explain the auth module",
        ...     expected=ExpectedBehavior(must=["analyze structure"])
        ... )
    """

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

    @field_validator("id")
    @classmethod
    def id_must_not_be_empty(cls, v: str) -> str:
        """Validate that id is not empty or whitespace-only.

        Args:
            v: The id value to validate.

        Returns:
            The validated id value.

        Raises:
            ValueError: If id is empty or contains only whitespace.
        """
        if not v or not v.strip():
            raise ValueError("id must not be empty")
        return v


class TestSuite(BaseModel):
    """Collection of test cases.

    Represents a versioned collection of functional test definitions
    that can be executed against an agent.

    Attributes:
        version: Test suite version identifier.
        test_cases: List of test case definitions.

    Example:
        >>> suite = TestSuite(
        ...     version="1.0.0",
        ...     test_cases=[test1, test2]
        ... )
    """

    version: str = Field(description="Test suite version")
    test_cases: list[TestCase]


class TranscriptEntry(BaseModel):
    """Single entry in a test transcript.

    Captures either a text response or a tool call from the agent.

    Attributes:
        type: Either "text" or "tool".
        content: Text content (for type="text").
        name: Tool name (for type="tool").
        input: Tool input parameters (for type="tool").
    """

    type: str = Field(description="'text' or 'tool'")
    content: str | None = Field(default=None, description="Text content")
    name: str | None = Field(default=None, description="Tool name")
    input: dict[str, Any] | None = Field(default=None, description="Tool input")


class TestResponse(BaseModel):
    """Response captured from an agent for a test case.

    Stores the raw response along with metadata about the execution.

    Attributes:
        test_id: ID of the test case this response is for.
        prompt: The prompt that was sent to the agent.
        response: The raw response text from the agent.
        duration_ms: Response time in milliseconds, if measured.
        tokens_used: Number of tokens consumed, if available.
        transcript: Full transcript of agent steps (optional).
    """

    test_id: str
    prompt: str
    response: str
    duration_ms: int | None = None
    tokens_used: int | None = None
    transcript: list[TranscriptEntry] | None = Field(
        default=None,
        description="Full transcript of agent steps",
    )


class TestResponses(BaseModel):
    """All responses captured for a specific version.

    Groups all test responses together with version and timing metadata.

    Attributes:
        arche_version: The Arché version that was tested.
        timestamp: ISO format timestamp when responses were captured.
        responses: List of individual test responses.
        total_duration_ms: Total execution time in milliseconds.
    """

    arche_version: str
    timestamp: str
    responses: list[TestResponse]
    total_duration_ms: int | None = None


class Conformity(str, Enum):
    """Conformity assessment result for a test or behavior check.

    Represents the outcome of evaluating an agent's response against
    expected behaviors.

    Attributes:
        PASS: All expected behaviors were satisfied.
        FAIL: Required behaviors were missing or prohibited behaviors present.
        PARTIAL: Some but not all expected behaviors were satisfied.
        SKIPPED: Test could not be evaluated (excluded from pass rates).

    Note:
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
    """Result of checking a single expected behavior.

    Records whether a specific behavior was detected in the response
    along with supporting evidence.

    Attributes:
        behavior: The behavior description being checked.
        check_type: Either "must" or "must_not".
        result: The conformity result for this behavior.
        evidence: Quote from response supporting the result,
            or skip reason if result is SKIPPED.

    Note:
        When result is SKIPPED, the evidence field should contain
        the reason why the check could not be performed.
    """

    behavior: str
    check_type: str = Field(description="must or must_not")
    result: Conformity
    evidence: str = Field(
        description="Quote from response supporting result, or skip reason if SKIPPED"
    )


class TestAnalysis(BaseModel):
    """Analysis result for a single test response.

    Contains the overall conformity assessment and detailed behavior
    checks for one test case.

    Attributes:
        test_id: ID of the analyzed test case.
        principle: The principle that was tested.
        mode: The cognitive mode context.
        conformity: Overall conformity assessment.
        behavior_checks: List of individual behavior check results.
        notes: Optional notes about the analysis.
    """

    test_id: str
    principle: Principle
    mode: CognitiveMode
    conformity: Conformity
    behavior_checks: list[BehaviorCheck]
    notes: str | None = None


class VersionAnalysis(BaseModel):
    """Complete analysis results for a version.

    Aggregates all test analyses with summary statistics.

    Attributes:
        arche_version: The Arché version that was analyzed.
        timestamp: ISO format timestamp of the analysis.
        total_tests: Total number of tests analyzed.
        passed: Number of tests that passed.
        failed: Number of tests that failed.
        partial: Number of tests with partial conformity.
        skipped: Number of tests that could not be evaluated.
        pass_rate: Percentage of passed tests (0-100), excludes skipped.
        weighted_rate: Weighted percentage where partial counts as 0.5,
            excludes skipped tests.
        analyses: List of individual test analyses.

    Example:
        >>> analysis = VersionAnalysis(
        ...     arche_version="0.1.0",
        ...     timestamp="2024-01-15T10:30:00",
        ...     total_tests=20,
        ...     passed=15,
        ...     failed=3,
        ...     partial=2,
        ...     skipped=0,
        ...     pass_rate=75.0,
        ...     weighted_rate=80.0,
        ...     analyses=[...]
        ... )
    """

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
    """Degradation record for a single test between versions.

    Tracks conformity changes for a test case when comparing two versions.

    Attributes:
        test_id: ID of the test case being compared.
        baseline_conformity: Conformity result in the baseline version.
        current_conformity: Conformity result in the current version.
        degraded: True if conformity worsened from baseline to current.
        notes: Optional notes explaining the degradation.
    """

    test_id: str
    baseline_conformity: Conformity
    current_conformity: Conformity
    degraded: bool
    notes: str | None = None


class VersionComparison(BaseModel):
    """Comparison results between baseline and current versions.

    Provides summary statistics and detailed degradation information
    for comparing two versions.

    Attributes:
        baseline_version: The baseline version identifier.
        current_version: The current version identifier.
        timestamp: ISO format timestamp of the comparison.
        baseline_pass_rate: Pass rate of the baseline version.
        current_pass_rate: Pass rate of the current version.
        degradation_pct: Percentage change in pass rate.
            Negative values indicate improvement.
        degradations: List of tests that degraded between versions.
        summary: Human-readable summary of the comparison.

    Example:
        >>> comparison = VersionComparison(
        ...     baseline_version="0.1.0",
        ...     current_version="0.2.0",
        ...     timestamp="2024-01-15T10:30:00",
        ...     baseline_pass_rate=75.0,
        ...     current_pass_rate=80.0,
        ...     degradation_pct=-5.0,  # Improvement
        ...     degradations=[],
        ...     summary="Version 0.2.0 shows 5% improvement"
        ... )
    """

    baseline_version: str
    current_version: str
    timestamp: str
    baseline_pass_rate: float
    current_pass_rate: float
    degradation_pct: float = Field(description="Negative = improvement")
    degradations: list[Degradation]
    summary: str
