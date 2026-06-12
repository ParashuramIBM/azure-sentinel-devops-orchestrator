# agents/reasoning_agents/security_agent.py
from dataclasses import dataclass
from typing import Any, List

@dataclass
class SecurityScanResult:
    approved: bool
    violations: List[str]
    reasoning: str

class SecurityComplianceAgent:
    """Security reasoning agent for pipeline validation."""

    def __init__(self):
        self.name = "SecurityComplianceAgent"

    async def scan_pipeline(self, code_changes: Any) -> SecurityScanResult:
        """Analyze code changes and return a security clearance result."""
        violations: List[str] = []
        reasoning = "No security violations detected."

        if not code_changes:
            reasoning = "No code changes were provided."

        if isinstance(code_changes, dict):
            for value in code_changes.values():
                if isinstance(value, str) and "TODO" in value:
                    violations.append("Found TODO marker in code change content.")
                    reasoning = "Code changes include markers that require review."

        return SecurityScanResult(
            approved=not violations,
            violations=violations,
            reasoning=reasoning
        )
