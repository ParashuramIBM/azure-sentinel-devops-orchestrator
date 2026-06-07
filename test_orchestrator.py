"""Tests for the Azure Sentinel DevOps Orchestrator."""
import asyncio
import pytest
from agents.orchestrator.main_orchestrator import DevOpsOrchestrator
from agents.reasoning_agents.security_agent import SecurityComplianceAgent
from agents.reasoning_agents.deployment_agent import IntelligentDeploymentAgent
from agents.reasoning_agents.monitoring_agent import MonitoringIntelligenceAgent
from agents.reasoning_agents.incident_agent import IncidentResponseAgent
from agents.integrations.fabric_iq_client import FabricIQClient


class TestSecurityAgent:
    """Test cases for SecurityComplianceAgent."""
    
    @pytest.mark.asyncio
    async def test_security_scan_no_violations(self):
        """Test security scan with clean code."""
        agent = SecurityComplianceAgent()
        result = await agent.scan_pipeline({"files": ["app.py"], "content": "print('hello')"})
        
        assert result.approved is True
        assert len(result.violations) == 0
    
    @pytest.mark.asyncio
    async def test_security_scan_with_violations(self):
        """Test security scan detects TODOs."""
        agent = SecurityComplianceAgent()
        result = await agent.scan_pipeline({"files": ["app.py"], "content": "# TODO: fix security"})
        
        assert result.approved is False
        assert len(result.violations) > 0


class TestDeploymentAgent:
    """Test cases for IntelligentDeploymentAgent."""
    
    @pytest.mark.asyncio
    async def test_deployment_readiness(self):
        """Test deployment readiness evaluation."""
        agent = IntelligentDeploymentAgent()
        
        deployment_context = {
            "changes": ["config update"],
            "target_resources": ["resource-group-1"]
        }
        
        result = await agent.evaluate_deployment_readiness(deployment_context)
        
        assert hasattr(result, 'is_safe')
        assert result.is_safe is True


class TestMonitoringAgent:
    """Test cases for MonitoringIntelligenceAgent."""
    
    @pytest.mark.asyncio
    async def test_monitoring_configuration(self):
        """Test observability configuration."""
        agent = MonitoringIntelligenceAgent()
        
        config = await agent.configure_observability(["resource-1", "resource-2"])
        
        assert config.target_resources == ["resource-1", "resource-2"]
        assert len(config.metrics) > 0
        assert len(config.alert_rules) > 0


class TestIncidentAgent:
    """Test cases for IncidentResponseAgent."""
    
    @pytest.mark.asyncio
    async def test_incident_creation(self):
        """Test incident creation."""
        agent = IncidentResponseAgent()
        
        incident = await agent.create_incident(
            severity="HIGH",
            finding="Security violation detected"
        )
        
        assert incident.incident_id.startswith("INC-")
        assert incident.severity == "HIGH"
        assert incident.status == "created"


class TestOrchestrator:
    """Test cases for DevOpsOrchestrator."""
    
    @pytest.mark.asyncio
    async def test_orchestrator_initialization(self):
        """Test orchestrator initialization."""
        orchestrator = DevOpsOrchestrator()
        
        assert orchestrator.deployment_agent is not None
        assert orchestrator.security_agent is not None
        assert orchestrator.monitoring_agent is not None
        assert orchestrator.incident_agent is not None
        assert orchestrator.fabric_client is not None
    
    @pytest.mark.asyncio
    async def test_orchestrator_pipeline_execution(self):
        """Test full pipeline execution."""
        orchestrator = DevOpsOrchestrator()
        
        class PipelineTrigger:
            def __init__(self):
                self.code_changes = {"files": ["app.py"], "content": "print('hello')"}
                self.deployment_context = {
                    "changes": ["config update"],
                    "target_resources": ["resource-group"]
                }
        
        trigger = PipelineTrigger()
        result = await orchestrator.execute_pipeline(trigger)
        
        assert result is not None
        assert "status" in result


class TestFabricIQClient:
    """Test cases for FabricIQClient."""
    
    @pytest.mark.asyncio
    async def test_fabric_client_initialization(self):
        """Test Fabric IQ client initialization."""
        client = FabricIQClient(
            workspace="test_workspace",
            eventhouse="test_eventhouse"
        )
        
        assert client.workspace == "test_workspace"
        assert client.eventhouse == "test_eventhouse"
    
    @pytest.mark.asyncio
    async def test_fabric_client_event_ingestion(self):
        """Test event ingestion."""
        client = FabricIQClient(
            workspace="test_workspace",
            eventhouse="test_eventhouse"
        )
        
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
        
        result = await client.ingest_events(events)
        
        assert result["status"] == "success"
        assert result["events_ingested"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
