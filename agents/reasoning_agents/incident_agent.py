# agents/reasoning_agents/incident_agent.py
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

@dataclass
class IncidentRecord:
    incident_id: str
    severity: str
    finding: Any
    status: str

class IncidentResponseAgent:
    """Agent responsible for incident creation and tracking."""

    def __init__(self):
        self.name = "IncidentResponseAgent"

    async def create_incident(self, severity: str, finding: Any) -> IncidentRecord:
        incident_id = f"INC-{uuid4().hex[:8]}"
        status = "created"

        return IncidentRecord(
            incident_id=incident_id,
            severity=severity,
            finding=finding,
            status=status
        )
