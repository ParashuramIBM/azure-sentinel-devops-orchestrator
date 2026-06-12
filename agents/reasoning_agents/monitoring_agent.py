# agents/reasoning_agents/monitoring_agent.py
from dataclasses import dataclass
from typing import Any, Dict, List

@dataclass
class MonitoringConfig:
    target_resources: List[str]
    metrics: List[str]
    alert_rules: Dict[str, Any]

class MonitoringIntelligenceAgent:
    """Agent responsible for observability and monitoring configuration."""

    def __init__(self):
        self.name = "MonitoringIntelligenceAgent"

    async def configure_observability(self, target_resources: Any) -> MonitoringConfig:
        resources = []
        if isinstance(target_resources, list):
            resources = [str(r) for r in target_resources]
        elif target_resources is not None:
            resources = [str(target_resources)]

        config = MonitoringConfig(
            target_resources=resources,
            metrics=["cpu_usage", "memory_usage", "request_latency"],
            alert_rules={
                "error_rate": ">= 0.05",
                "latency_ms": ">= 500"
            }
        )
        return config
