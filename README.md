# Azure Sentinel DevOps Orchestrator

## Overview

This repository contains the core implementation for an AI-driven DevOps orchestration engine that integrates deployment reasoning, security validation, monitoring configuration, incident response, and telemetry capture.

The current implementation includes:
- `agents/orchestrator/main_orchestrator.py`: orchestrates the end-to-end pipeline.
- `agents/reasoning_agents/deployment_agent.py`: an intelligent deployment reasoning agent.
- `foundry_integration/eventhouse/devops_telemetry.kql`: telemetry schema and failed deployment query.

## Architecture

The orchestrator is designed around a multi-agent pipeline:
1. Security validation via `SecurityComplianceAgent`
2. Deployment readiness evaluation via `IntelligentDeploymentAgent`
3. Observability/monitoring setup via `MonitoringIntelligenceAgent`
4. Execution with safety nets and post-deployment validation
5. Telemetry ingestion into Fabric IQ

### Key components

- `DevOpsOrchestrator` in `agents/orchestrator/main_orchestrator.py`
  - `execute_pipeline()` is the main orchestration entrypoint.
  - It runs security scans, deployment planning, monitoring configuration, and post-deploy validation.

- `IntelligentDeploymentAgent` in `agents/reasoning_agents/deployment_agent.py`
  - Uses Foundry IQ reasoning to assess deployment readiness.
  - Logs telemetry to Fabric IQ.

- `devops_telemetry.kql` in `foundry_integration/eventhouse`
  - Defines the telemetry table schema.
  - Includes a helper function to find failed deployments in the last 24 hours.

## Current Implementation Status

Implemented:
- Deployment agent reasoning and telemetry logging logic
- Orchestrator pipeline skeleton with phase flow
- KQL schema for telemetry ingestion
- Runtime runner `run_orchestrator.py`
- Local stub implementations for `SecurityComplianceAgent`, `MonitoringIntelligenceAgent`, and `IncidentResponseAgent`
- Local stub implementations for `FabricIQClient`, `foundry_iq`, and `fabric_iq`
- `requirements.txt` manifest

Pending / required implementation:
- Production-grade `foundry_iq` and `fabric_iq` client libraries or adapters
- Real Fabric IQ / Foundry IQ credentials and integrations

## Implementation Plan

### Phase 1: Complete missing agent modules

Create the missing reasoning agent classes under `agents/reasoning_agents/`:
- `security_agent.py` → `SecurityComplianceAgent`
- `monitoring_agent.py` → `MonitoringIntelligenceAgent`
- `incident_agent.py` → `IncidentResponseAgent`

Each agent should expose async methods that match the orchestrator expectations:
- `SecurityComplianceAgent.scan_pipeline(code_changes)`
- `MonitoringIntelligenceAgent.configure_observability(target_resources)`
- `IncidentResponseAgent.create_incident(severity, finding)`

### Phase 2: Implement shared integration clients

Implement or wire the following integration layers:
- `FabricIQClient` for event ingestion and telemetry
- `TelemetryClient` for agent-level logging
- `ReasoningAgent` and `ChainOfThought` abstractions from `foundry_iq`

### Phase 3: Define runtime and dependency management

Add package metadata and installation instructions:
- `requirements.txt` or `pyproject.toml`
- A top-level entrypoint script such as `run_orchestrator.py`
- environment configuration for Azure/Fabric/Foundry credentials

### Phase 4: Add tests and validation

Create tests for:
- pipeline control flow in `DevOpsOrchestrator`
- deployment readiness logic in `IntelligentDeploymentAgent`
- telemetry event formatting and ingestion behavior
- failure/rollback handling in the orchestrator

### Phase 5: Deploy and verify

- Provision Fabric IQ / Foundry IQ integration resources
- Deploy or run the orchestrator from a controlled environment
- Use the KQL query in `foundry_integration/eventhouse/devops_telemetry.kql` to validate telemetry

## Execution Steps

### Prerequisites

- Python 3.11+ installed
- An async-capable runtime for the orchestrator
- Local stub packages are included for `foundry_iq` and `fabric_iq`

### Install dependencies

Create a virtual environment and install required packages.

```bash
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
```

> The starter version uses local stub packages for `foundry_iq` and `fabric_iq` that are included in the repository.

### Run the orchestrator

Create a simple runner to invoke the pipeline. Example:

```python
import asyncio
from agents.orchestrator.main_orchestrator import DevOpsOrchestrator

class PipelineTrigger:
    def __init__(self, code_changes, deployment_context):
        self.code_changes = code_changes
        self.deployment_context = deployment_context

async def main():
    orchestrator = DevOpsOrchestrator()

    pipeline_trigger = PipelineTrigger(
        code_changes={"files": ["app.py"], "summary": "Deploy update"},
        deployment_context={"changes": ["service config"], "target_resources": ["resource-group"]}
    )

    result = await orchestrator.execute_pipeline(pipeline_trigger)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

Run the file:

```bash
python run_orchestrator.py
```

### Validate telemetry

Use the KQL definitions in `foundry_integration/eventhouse/devops_telemetry.kql` to create the telemetry table and query failures:

```kql
.create table DevOpsTelemetry (
    Timestamp: datetime,
    AgentName: string,
    Action: string,
    ResourceId: string,
    Success: bool,
    ResponseTimeMs: int,
    ErrorCode: string,
    ReasoningTrace: string
)

.create function GetFailedDeployments() {
    DevOpsTelemetry
    | where Success == false
    | where Timestamp > ago(24h)
    | project Timestamp, AgentName, ResourceId, ErrorCode, ReasoningTrace
}
```

## Project Structure

- `agents/orchestrator/main_orchestrator.py` - main orchestration pipeline
- `agents/reasoning_agents/deployment_agent.py` - deployment reasoning agent
- `foundry_integration/eventhouse/devops_telemetry.kql` - telemetry schema and query

## Next Steps

1. Add the missing reasoning agent modules.
2. Implement the Fabric IQ and Foundry IQ client adapters.
3. Add dependency manifests and environment setup documentation.
4. Write unit/integration tests for orchestration and telemetry flows.
5. Connect to a real Fabric IQ telemetry backend and validate queries.

## Notes

This README reflects the current repository state as of the existing source tree. The implementation is intentionally modular so that security, monitoring, and incident response agents can be added without changing core orchestration flow.
