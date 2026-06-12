"""Data models for Foundry IQ reasoning framework."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime


@dataclass
class ReasoningContext:
    """Context for a reasoning operation."""
    domain: str
    scenario: str
    variables: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class DecisionResult:
    """Result from a reasoning decision."""
    decision: str
    is_safe: bool
    reasoning_chain: str
    processing_time: int
    confidence: float = 0.95
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RemediationPlan:
    """Plan for automated remediation."""
    actions: List[str]
    priority: str
    estimated_duration_seconds: int
    rollback_available: bool = True
    approval_required: bool = False
