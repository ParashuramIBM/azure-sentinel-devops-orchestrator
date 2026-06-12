# Azure Portal Checklist for Azure Sentinel DevOps Orchestrator

This guide helps you understand the runtime flow, where to inspect changes in Azure Portal, and how to query telemetry for this repository.

## 1. Understand the repo flow

The project flow is:

1. `run_orchestrator.py` starts the workflow.
2. `DevOpsOrchestrator.execute_pipeline()` orchestrates the pipeline.
3. The pipeline runs:
   - `SecurityComplianceAgent.scan_pipeline(...)`
   - `IntelligentDeploymentAgent.evaluate_deployment_readiness(...)`
   - `MonitoringIntelligenceAgent.configure_observability(...)`
   - optional `IncidentResponseAgent.create_incident(...)`
   - telemetry ingestion through `FabricIQClient`

### Important repo files

- `agents/orchestrator/main_orchestrator.py`
- `agents/reasoning_agents/deployment_agent.py`
- `agents/reasoning_agents/security_agent.py`
- `agents/reasoning_agents/monitoring_agent.py`
- `agents/reasoning_agents/incident_agent.py`
- `agents/integrations/fabric_iq_client.py`
- `foundry_iq/` and `fabric_iq/` stub packages
- `run_orchestrator.py`
- `foundry_integration/eventhouse/devops_telemetry.kql`
- `foundry_integration/eventhouse/devops_telemetry_extended.kql`

## 2. Azure Portal checklist

### Step 1: Open the right resource group

- In Azure Portal, search for `Resource groups`.
- Open the resource group used by this project.
- This is the main place where deployed resources and telemetry backends appear.

### Step 2: Review deployment history

- Inside the resource group, click `Deployments`.
- Inspect the deployment records.
- Look for:
  - status (Succeeded/Failed)
  - resources created or updated
  - deployment time and details

### Step 3: Check the activity log

- Search for `Monitor` in Azure Portal.
- Open `Activity log`.
- Filter by:
  - subscription
  - resource group
  - relevant time range
- This shows Azure-side configuration changes and operations.

### Step 4: Inspect logs with Log Analytics

- Search for `Log Analytics workspaces`.
- Open the workspace connected to this solution.
- Click `Logs`.
- Run queries against telemetry tables such as `DevOpsTelemetry`.

### Step 5: If Microsoft Sentinel is enabled

- Search for `Microsoft Sentinel`.
- Open the workspace.
- Check:
  - `Incidents`
  - `Analytics rules`
  - `Hunting queries`

## 3. Sample Log Analytics queries

Use these in `Monitor > Logs`.

### Query all telemetry events in the last 24 hours

```kql
DevOpsTelemetry
| where Timestamp > ago(24h)
| project Timestamp, AgentName, Action, ResourceId, Success, ResponseTimeMs, ErrorCode, ReasoningTrace
| order by Timestamp desc
```

### Query failed runs only

```kql
DevOpsTelemetry
| where Timestamp > ago(24h)
| where Success == false
| project Timestamp, AgentName, Action, ResourceId, ErrorCode, ReasoningTrace
| order by Timestamp desc
```

## 4. Beginner guidance

- Start with `Resource groups` and `Deployments` to find what Azure changed.
- Use `Activity log` to see operations and audit events.
- Use `Logs` in Log Analytics to see actual runtime telemetry.
- Map Azure resource changes back to the repo files above.

## 5. How this maps to your repo code

- The orchestrator triggers the flow in `run_orchestrator.py`.
- All decision and telemetry logic is in `agents/orchestrator/main_orchestrator.py`.
- Reasoning steps live in `agents/reasoning_agents/*.py`.
- Telemetry schema lives in `foundry_integration/eventhouse/devops_telemetry.kql`.
- If you want to inspect actual changes from the use case, look at those files first.
