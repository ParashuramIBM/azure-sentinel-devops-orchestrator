import asyncio
from agents.orchestrator.main_orchestrator import DevOpsOrchestrator
from agents.reasoning_agents.security_agent import SecurityComplianceAgent
from agents.reasoning_agents.deployment_agent import IntelligentDeploymentAgent
from agents.reasoning_agents.monitoring_agent import MonitoringIntelligenceAgent
from agents.reasoning_agents.incident_agent import IncidentResponseAgent
from agents.integrations.fabric_iq_client import FabricIQClient


def test_security_scan_no_violations():
    agent = SecurityComplianceAgent()
    result = asyncio.run(agent.scan_pipeline({"files": ["app.py"], "content": "print('hello')"}))

    assert result.approved is True
    assert len(result.violations) == 0


def test_security_scan_with_violations():
    agent = SecurityComplianceAgent()
    result = asyncio.run(agent.scan_pipeline({"files": ["app.py"], "content": "# TODO: fix security"}))

    assert result.approved is False
    assert len(result.violations) > 0


def test_deployment_readiness():
    agent = IntelligentDeploymentAgent()
    deployment_context = {
        "changes": ["config update"],
        "target_resources": ["resource-group-1"]
    }
    result = asyncio.run(agent.evaluate_deployment_readiness(deployment_context))

    assert hasattr(result, "is_safe")
    assert result.is_safe is True


def test_monitoring_configuration():
    agent = MonitoringIntelligenceAgent()
    config = asyncio.run(agent.configure_observability(["resource-1", "resource-2"]))

    assert config.target_resources == ["resource-1", "resource-2"]
    assert len(config.metrics) > 0
    assert len(config.alert_rules) > 0


def test_incident_creation():
    agent = IncidentResponseAgent()
    incident = asyncio.run(agent.create_incident(severity="HIGH", finding="Security violation detected"))

    assert incident.incident_id.startswith("INC-")
    assert incident.severity == "HIGH"
    assert incident.status == "created"


def test_orchestrator_pipeline_execution():
    orchestrator = DevOpsOrchestrator()

    class PipelineTrigger:
        def __init__(self):
            self.code_changes = {"files": ["app.py"], "content": "print('hello')"}
            self.deployment_context = {
                "changes": ["config update"],
                "target_resources": ["resource-group"]
            }

    trigger = PipelineTrigger()
    result = asyncio.run(orchestrator.execute_pipeline(trigger))

    assert result is not None
    assert "status" in result


def test_fabric_client_event_ingestion():
    client = FabricIQClient(workspace="test_workspace", eventhouse="test_eventhouse")
    events = [
        {
            "Timestamp": "2026-06-07T00:00:00Z",
            "AgentName": "TestAgent",
            "Action": "test_action",
            "ResourceId": "resource-1",
            "Success": True,
            "ResponseTimeMs": 100
        }
    ]
    result = asyncio.run(client.ingest_events(events))

    assert result["status"] == "success"
    assert result["events_ingested"] == 1
