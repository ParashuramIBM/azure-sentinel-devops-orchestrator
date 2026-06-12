# agents/integrations/fabric_iq_client.py
from typing import Any, Dict, Iterable

class FabricIQClient:
    """Simple Fabric IQ client stub for event ingestion."""

    def __init__(self, workspace: str, eventhouse: str):
        self.workspace = workspace
        self.eventhouse = eventhouse

    async def ingest_events(self, events: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
        event_list = list(events)
        return {
            "status": "success",
            "workspace": self.workspace,
            "eventhouse": self.eventhouse,
            "events_ingested": len(event_list)
        }
