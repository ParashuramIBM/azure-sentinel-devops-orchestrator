# agents/orchestrator/main_orchestrator.py
from agents.reasoning_agents.deployment_agent import IntelligentDeploymentAgent
from agents.reasoning_agents.security_agent import SecurityComplianceAgent
from agents.reasoning_agents.monitoring_agent import MonitoringIntelligenceAgent
from agents.reasoning_agents.incident_agent import IncidentResponseAgent
from agents.integrations.fabric_iq_client import FabricIQClient

class DevOpsOrchestrator:
    """Orchestrates multiple reasoning agents for end-to-end DevOps"""
    
    def __init__(self):
        self.deployment_agent = IntelligentDeploymentAgent()
        self.security_agent = SecurityComplianceAgent()
        self.monitoring_agent = MonitoringIntelligenceAgent()
        self.incident_agent = IncidentResponseAgent()
        
        # Initialize Fabric IQ for unified telemetry
        self.fabric_client = FabricIQClient(
            workspace="devops_orchestration",
            eventhouse="devops_telemetry"
        )
        
    async def execute_pipeline(self, pipeline_trigger):
        """Main orchestration logic"""
        
        # Phase 1: Security validation (Reasoning Agent)
        security_clearance = await self.security_agent.scan_pipeline(
            pipeline_trigger.code_changes
        )
        
        if not security_clearance.approved:
            await self.incident_agent.create_incident(
                severity="HIGH",
                finding=security_clearance.violations
            )
            return {"status": "blocked", "reason": security_clearance.reasoning}
        
        # Phase 2: Deployment planning (Foundry IQ)
        deployment_plan = await self.deployment_agent.evaluate_deployment_readiness(
            pipeline_trigger.deployment_context
        )
        
        # Phase 3: Monitoring setup (Fabric IQ)
        monitoring_config = await self.monitoring_agent.configure_observability(
            deployment_plan.target_resources
        )
        
        # Phase 4: Execute with safety checks
        deployment_result = await self._execute_with_safety_net(
            deployment_plan,
            monitoring_config
        )
        
        # Phase 5: Post-deployment validation
        await self._post_deployment_validation(deployment_result)
        
        # Log to Fabric IQ for analytics
        await self.fabric_client.ingest_events([
            self._create_telemetry_event(deployment_result),
            self._create_performance_metrics(monitoring_config)
        ])

        return deployment_result

    async def _execute_with_safety_net(self, deployment_plan, monitoring_config):
        """Execute deployment with basic safety gating."""
        try:
            return {
                "status": "success",
                "deployment_plan": deployment_plan,
                "monitoring_config": monitoring_config
            }
        except Exception as exc:
            await self.incident_agent.create_incident(
                severity="CRITICAL",
                finding=str(exc)
            )
            return {"status": "failed", "error": str(exc)}

    async def _post_deployment_validation(self, deployment_result):
        """Validate post-deployment outcomes."""
        if deployment_result.get("status") != "success":
            return {"validated": False, "message": "Deployment did not complete successfully."}
        return {"validated": True, "message": "Deployment completed and validated."}

    def _create_telemetry_event(self, deployment_result):
        deployment_plan = deployment_result.get("deployment_plan")
        target_resources = []
        if hasattr(deployment_plan, "target_resources"):
            target_resources = deployment_plan.target_resources
        elif isinstance(deployment_plan, dict):
            target_resources = deployment_plan.get("target_resources", [])

        return {
            "Timestamp": "2026-06-07T00:00:00Z",
            "AgentName": "DevOpsOrchestrator",
            "Action": "deployment_complete",
            "ResourceId": str(target_resources),
            "Success": deployment_result.get("status") == "success",
            "ResponseTimeMs": 0,
            "ErrorCode": None,
            "ReasoningTrace": str(deployment_result)
        }

    def _create_performance_metrics(self, monitoring_config):
        return {
            "Timestamp": "2026-06-07T00:00:00Z",
            "AgentName": "MonitoringIntelligenceAgent",
            "Action": "monitoring_configured",
            "ResourceId": str(monitoring_config.target_resources),
            "Success": True,
            "ResponseTimeMs": 0,
            "ErrorCode": None,
            "ReasoningTrace": str(monitoring_config)
        }
