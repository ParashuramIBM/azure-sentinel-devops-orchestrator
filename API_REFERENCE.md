# API Reference Guide

## Azure Sentinel DevOps Orchestrator API

Complete reference for all public APIs in the orchestrator.

---

## Table of Contents

1. [DevOpsOrchestrator](#devops-orchestrator)
2. [Security Agent](#security-agent)
3. [Deployment Agent](#deployment-agent)
4. [Monitoring Agent](#monitoring-agent)
5. [Incident Agent](#incident-agent)
6. [Fabric IQ Client](#fabric-iq-client)
7. [Telemetry Client](#telemetry-client)
8. [Reasoning Agent](#reasoning-agent)

---

## DevOpsOrchestrator

Main orchestration engine that coordinates all agents.

### Class: `DevOpsOrchestrator`

```python
from agents.orchestrator.main_orchestrator import DevOpsOrchestrator

orchestrator = DevOpsOrchestrator()
```

#### Methods

##### `execute_pipeline(pipeline_trigger) → Dict`

Execute the full DevOps pipeline with security, deployment, monitoring, and post-deployment validation.

**Parameters:**
- `pipeline_trigger` (PipelineTrigger): Object containing:
  - `code_changes` (Dict): Code changes to be deployed
  - `deployment_context` (Dict): Deployment context with target resources

**Returns:**
- `Dict` with keys:
  - `status` (str): "success", "blocked", or "failed"
  - `reason` (str, optional): Reason if blocked/failed
  - `deployment_plan` (Dict, optional): Generated deployment plan
  - `monitoring_config` (Dict, optional): Monitoring configuration

**Example:**
```python
import asyncio

class PipelineTrigger:
    def __init__(self):
        self.code_changes = {"files": ["app.py"], "summary": "Update"}
        self.deployment_context = {"changes": ["config"], "target_resources": ["rg"]}

async def main():
    orchestrator = DevOpsOrchestrator()
    trigger = PipelineTrigger()
    result = await orchestrator.execute_pipeline(trigger)
    print(result)

asyncio.run(main())
```

---

## Security Agent

Performs security scanning and compliance validation.

### Class: `SecurityComplianceAgent`

```python
from agents.reasoning_agents.security_agent import SecurityComplianceAgent

agent = SecurityComplianceAgent()
```

#### Methods

##### `scan_pipeline(code_changes) → SecurityScanResult`

Scan code changes for security violations.

**Parameters:**
- `code_changes` (Dict or Any): Code changes to scan

**Returns:**
- `SecurityScanResult` with:
  - `approved` (bool): Whether changes are approved
  - `violations` (List[str]): List of found violations
  - `reasoning` (str): Reasoning summary

**Example:**
```python
result = await agent.scan_pipeline({"files": ["app.py"]})
if result.approved:
    print("✓ Security check passed")
else:
    print(f"✗ Violations found: {result.violations}")
```

---

## Deployment Agent

Evaluates deployment readiness and generates deployment plans.

### Class: `IntelligentDeploymentAgent`

```python
from agents.reasoning_agents.deployment_agent import IntelligentDeploymentAgent

agent = IntelligentDeploymentAgent()
```

#### Methods

##### `evaluate_deployment_readiness(deployment_context) → DecisionResult`

Evaluate if the deployment is ready to proceed.

**Parameters:**
- `deployment_context` (Dict): Deployment context containing:
  - `changes` (List[str]): List of changes
  - `target_resources` (List[str], optional): Target resources

**Returns:**
- `DecisionResult` with:
  - `decision` (str): Decision details
  - `is_safe` (bool): Whether deployment is safe
  - `reasoning_chain` (str): Reasoning process
  - `processing_time` (int): Processing time in milliseconds

**Example:**
```python
context = {
    "changes": ["service config update"],
    "target_resources": ["resource-group-1"]
}
result = await agent.evaluate_deployment_readiness(context)
print(f"Safe: {result.is_safe}, Time: {result.processing_time}ms")
```

##### `auto_remediate_failure(failure_context) → Dict`

Attempt automatic remediation for deployment failures.

**Parameters:**
- `failure_context` (Dict): Information about the failure

**Returns:**
- `Dict` with remediation results

---

## Monitoring Agent

Configures observability and monitoring.

### Class: `MonitoringIntelligenceAgent`

```python
from agents.reasoning_agents.monitoring_agent import MonitoringIntelligenceAgent

agent = MonitoringIntelligenceAgent()
```

#### Methods

##### `configure_observability(target_resources) → MonitoringConfig`

Configure monitoring for target resources.

**Parameters:**
- `target_resources` (List[str] or str): Resources to monitor

**Returns:**
- `MonitoringConfig` with:
  - `target_resources` (List[str]): Configured resources
  - `metrics` (List[str]): Enabled metrics
  - `alert_rules` (Dict): Alert rule configurations

**Example:**
```python
config = await agent.configure_observability(["resource-1", "resource-2"])
print(f"Resources: {config.target_resources}")
print(f"Metrics: {config.metrics}")
print(f"Alerts: {config.alert_rules}")
```

---

## Incident Agent

Manages incident creation and tracking.

### Class: `IncidentResponseAgent`

```python
from agents.reasoning_agents.incident_agent import IncidentResponseAgent

agent = IncidentResponseAgent()
```

#### Methods

##### `create_incident(severity, finding) → IncidentRecord`

Create an incident record.

**Parameters:**
- `severity` (str): Severity level ("LOW", "MEDIUM", "HIGH", "CRITICAL")
- `finding` (Any): The finding/issue to report

**Returns:**
- `IncidentRecord` with:
  - `incident_id` (str): Unique incident ID (INC-xxxxxxxx)
  - `severity` (str): Severity level
  - `finding` (Any): The reported finding
  - `status` (str): Incident status

**Example:**
```python
incident = await agent.create_incident(
    severity="HIGH",
    finding="Security vulnerability detected"
)
print(f"Created incident {incident.incident_id} with status: {incident.status}")
```

---

## Fabric IQ Client

Ingests events and telemetry into Fabric IQ.

### Class: `FabricIQClient`

```python
from agents.integrations.fabric_iq_client import FabricIQClient

client = FabricIQClient(
    workspace="devops_orchestration",
    eventhouse="devops_telemetry"
)
```

#### Methods

##### `ingest_events(events) → Dict`

Ingest events into Fabric IQ.

**Parameters:**
- `events` (Iterable[Dict]): Events to ingest with fields:
  - `Timestamp` (str): Event timestamp
  - `AgentName` (str): Agent name
  - `Action` (str): Action performed
  - `ResourceId` (str): Resource identifier
  - `Success` (bool): Whether action succeeded
  - `ResponseTimeMs` (int): Response time

**Returns:**
- `Dict` with:
  - `status` (str): "success" or error
  - `workspace` (str): Workspace name
  - `eventhouse` (str): Eventhouse name
  - `events_ingested` (int): Number of events ingested

**Example:**
```python
events = [{
    "Timestamp": "2026-06-07T12:00:00Z",
    "AgentName": "DeploymentAgent",
    "Action": "deployment_complete",
    "ResourceId": "resource-1",
    "Success": True,
    "ResponseTimeMs": 150
}]

result = await client.ingest_events(events)
print(f"Ingested {result['events_ingested']} events")
```

---

## Telemetry Client

Logs and manages telemetry events.

### Class: `TelemetryClient`

```python
from fabric_iq import TelemetryClient

client = TelemetryClient(workspace="devops_fabric")
```

#### Methods

##### `log_event(table, data, flush=False) → Dict`

Log a single telemetry event.

**Parameters:**
- `table` (str): Target table name
- `data` (Dict): Event data
- `flush` (bool): Whether to flush after logging

**Returns:**
- `Dict` with status information

##### `log_events(events) → Dict`

Log multiple telemetry events.

**Parameters:**
- `events` (List[Dict]): Events to log

**Returns:**
- `Dict` with ingestion status

##### `flush() → Dict`

Flush buffered events to Fabric IQ.

**Returns:**
- `Dict` with:
  - `status` (str): "success" or "empty"
  - `events_sent` (int): Number of events sent

**Example:**
```python
client = TelemetryClient(workspace="devops_fabric")

await client.log_event(
    table="DevOpsTelemetry",
    data={"AgentName": "TestAgent", "Success": True}
)

result = await client.flush()
print(f"Sent {result['events_sent']} events")
```

##### `query_events(table, where_clause=None, limit=1000) → List[Dict]`

Query telemetry events.

**Parameters:**
- `table` (str): Table to query
- `where_clause` (str, optional): Query condition
- `limit` (int): Maximum results

**Returns:**
- `List[Dict]`: Query results

---

## Reasoning Agent

Base class for reasoning agents.

### Class: `ReasoningAgent`

```python
from foundry_iq import ReasoningAgent, ChainOfThought

class CustomAgent(ReasoningAgent):
    def __init__(self):
        super().__init__(
            name="CustomAgent",
            model="gpt-4o-reasoning"
        )
```

#### Methods

##### `reason(context, reasoning_chain, constraints=None) → DecisionResult`

Execute reasoning with a chain of thought.

**Parameters:**
- `context` (Any): Context for reasoning
- `reasoning_chain` (ChainOfThought): Steps to reason through
- `constraints` (Dict, optional): Constraints to apply

**Returns:**
- `DecisionResult` with reasoning result

##### `get_infrastructure_state() → Dict`

Get current infrastructure state.

**Returns:**
- `Dict` with infrastructure information

##### `analyze_change_impact(changes) → Dict`

Analyze impact of proposed changes.

**Parameters:**
- `changes` (List[str]): Changes to analyze

**Returns:**
- `Dict` with impact analysis

---

## Chain of Thought

Represents a chain of reasoning steps.

### Class: `ChainOfThought`

```python
from foundry_iq import ChainOfThought

chain = ChainOfThought([
    "Assess infrastructure health",
    "Identify conflicting changes",
    "Calculate risk score",
    "Make deployment decision"
])
```

#### Methods

##### `add_step(step) → None`

Add a reasoning step.

##### `get_summary() → str`

Get formatted summary of all steps.

---

## Configuration

### Class: `Config`

```python
from config import Config

workspace = Config.FABRIC_WORKSPACE
model = Config.FOUNDRY_MODEL
debug = Config.DEBUG
```

#### Attributes

- `FABRIC_WORKSPACE` (str): Fabric workspace name
- `FABRIC_EVENTHOUSE` (str): Fabric eventhouse name
- `FOUNDRY_MODEL` (str): Foundry reasoning model
- `FOUNDRY_KNOWLEDGE_BASE` (str): Path to knowledge base
- `AZURE_SUBSCRIPTION_ID` (str): Azure subscription ID
- `AZURE_RESOURCE_GROUP` (str): Azure resource group
- `AZURE_TENANT_ID` (str): Azure tenant ID
- `LOG_LEVEL` (str): Logging level
- `LOG_FORMAT` (str): Log format (json or text)
- `DEBUG` (bool): Debug mode

#### Methods

##### `get_all() → Dict`

Get all configuration as dictionary.

---

## Logging

### Function: `setup_logging`

```python
from logger import setup_logging, get_logger

setup_logging(
    log_level="INFO",
    log_format="json",
    log_file="app.log"
)

logger = get_logger(__name__)
logger.info("Application started")
```

---

## Complete Example

```python
import asyncio
from agents.orchestrator.main_orchestrator import DevOpsOrchestrator
from logger import setup_logging, get_logger
from config import Config

setup_logging(
    log_level=Config.LOG_LEVEL,
    log_format=Config.LOG_FORMAT
)

logger = get_logger(__name__)

class PipelineTrigger:
    def __init__(self):
        self.code_changes = {
            "files": ["service.py"],
            "summary": "Critical service update"
        }
        self.deployment_context = {
            "changes": ["service configuration update"],
            "target_resources": ["prod-resource-group"]
        }

async def main():
    logger.info("Starting orchestrator")
    
    orchestrator = DevOpsOrchestrator()
    trigger = PipelineTrigger()
    
    result = await orchestrator.execute_pipeline(trigger)
    
    logger.info(f"Pipeline completed with status: {result.get('status')}")
    print(f"\n✓ Orchestration Result:\n{result}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Error Handling

All async methods may raise exceptions. Always use try-except blocks:

```python
try:
    result = await orchestrator.execute_pipeline(trigger)
except Exception as e:
    logger.error(f"Pipeline failed: {str(e)}")
    # Handle error
```

---

## Performance Tips

1. **Batch events**: Use `log_events()` instead of multiple `log_event()` calls
2. **Use async/await**: Always use async context for I/O operations
3. **Cache results**: Reuse orchestrator and agent instances
4. **Monitor telemetry**: Track agent performance via Fabric IQ

---

## See Also

- [INSTALLATION.md](INSTALLATION.md) - Setup instructions
- [README.md](README.md) - Project overview
- [KQL Queries](foundry_integration/eventhouse/devops_telemetry_extended.kql) - Telemetry analysis
