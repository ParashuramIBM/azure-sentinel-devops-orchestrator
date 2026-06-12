"""Event schemas and ingestion for Fabric IQ."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime
import json


@dataclass
class EventSchema:
    """Schema definition for telemetry events."""
    name: str
    fields: Dict[str, str]  # field_name: field_type
    description: Optional[str] = None
    retention_days: int = 90
    
    def validate_event(self, event: Dict[str, Any]) -> bool:
        """Validate an event against this schema."""
        for field_name, field_type in self.fields.items():
            if field_name not in event:
                return False
            # Basic type checking
            if field_type == "string" and not isinstance(event[field_name], str):
                return False
            if field_type == "int" and not isinstance(event[field_name], int):
                return False
            if field_type == "bool" and not isinstance(event[field_name], bool):
                return False
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert schema to dictionary format."""
        return {
            "name": self.name,
            "fields": self.fields,
            "description": self.description,
            "retention_days": self.retention_days
        }


class EventIngestion:
    """Event ingestion manager for Fabric IQ."""
    
    def __init__(self):
        self.schemas: Dict[str, EventSchema] = {}
        self.ingestion_stats = {
            "total_events": 0,
            "failed_events": 0,
            "successful_batches": 0
        }
    
    def register_schema(self, schema: EventSchema) -> None:
        """Register an event schema."""
        self.schemas[schema.name] = schema
    
    def get_schema(self, name: str) -> Optional[EventSchema]:
        """Get a registered schema by name."""
        return self.schemas.get(name)
    
    async def ingest_batch(
        self,
        schema_name: str,
        events: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Ingest a batch of events."""
        schema = self.get_schema(schema_name)
        
        if not schema:
            return {
                "status": "error",
                "message": f"Schema '{schema_name}' not found"
            }
        
        valid_events = []
        failed_events = []
        
        for event in events:
            if schema.validate_event(event):
                valid_events.append(event)
            else:
                failed_events.append(event)
        
        # Update stats
        self.ingestion_stats["total_events"] += len(events)
        self.ingestion_stats["failed_events"] += len(failed_events)
        
        if valid_events:
            self.ingestion_stats["successful_batches"] += 1
        
        return {
            "status": "success",
            "schema": schema_name,
            "ingested": len(valid_events),
            "failed": len(failed_events),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get ingestion statistics."""
        return self.ingestion_stats.copy()


# Default schemas for DevOps telemetry
DEVOPS_TELEMETRY_SCHEMA = EventSchema(
    name="DevOpsTelemetry",
    fields={
        "Timestamp": "string",
        "AgentName": "string",
        "Action": "string",
        "ResourceId": "string",
        "Success": "bool",
        "ResponseTimeMs": "int",
        "ErrorCode": "string",
        "ReasoningTrace": "string"
    },
    description="Core telemetry for DevOps orchestration events"
)

DEPLOYMENT_METRICS_SCHEMA = EventSchema(
    name="DeploymentMetrics",
    fields={
        "Timestamp": "string",
        "DeploymentId": "string",
        "Status": "string",
        "Duration": "int",
        "SuccessRate": "string",
        "ResourceCount": "int",
        "ErrorCount": "int"
    },
    description="Metrics for deployment operations"
)
