# Azure Sentinel DevOps Orchestrator

## Overview

This repository contains a consolidated, runnable starter implementation of an AI-driven DevOps orchestration engine.

The system is intended to demonstrate an end-to-end orchestration flow that includes:
- security validation
- deployment readiness reasoning
- monitoring/observability setup
- incident creation
- telemetry ingestion and analysis

## What’s included

- `agents/orchestrator/main_orchestrator.py` — central orchestration pipeline
- `agents/reasoning_agents/` — reasoning agent implementations
  - `deployment_agent.py`
  - `security_agent.py`
  - `monitoring_agent.py`
  - `incident_agent.py`
- `agents/integrations/fabric_iq_client.py` — Fabric IQ event ingestion stub
- `foundry_iq/` — local stub package for reasoning abstractions
- `fabric_iq/` — local stub package for telemetry client behavior
- `run_orchestrator.py` — runnable startup script
- `foundry_integration/eventhouse/` — KQL telemetry schema files
- project support docs and helper files:
  - `.env.example`
  - `config.py`
  - `logger.py`
  - `setup.py`
  - `test_orchestrator.py`
  - `API_REFERENCE.md`
  - `INSTALLATION.md`
  - `QUICKSTART.md`
  - `PROJECT_INDEX.md`
  - `DELIVERY_SUMMARY.md`
  - `IMPLEMENTATION_STATUS.md`
  - `IMPLEMENTATION_COMPLETE.md`
  - `START_HERE.txt`

## Architecture

The orchestrator uses a multi-agent pipeline:
1. Security validation via `SecurityComplianceAgent`
2. Deployment readiness evaluation via `IntelligentDeploymentAgent`
3. Observability/monitoring setup via `MonitoringIntelligenceAgent`
4. Deployment execution with safety checks
5. Post-deployment validation and telemetry ingestion

### Key components

- `DevOpsOrchestrator` in `agents/orchestrator/main_orchestrator.py`
  - `execute_pipeline()` is the main orchestration entrypoint.
  - It runs security scans, deployment planning, monitoring configuration, and post-deployment logging.

- `IntelligentDeploymentAgent` in `agents/reasoning_agents/deployment_agent.py`
  - Uses local `foundry_iq` reasoning abstractions.
  - Logs telemetry through Fabric IQ stubs.

- `SecurityComplianceAgent`, `MonitoringIntelligenceAgent`, `IncidentResponseAgent`
  - Provided as local async stubs for starter orchestration flows.

- `foundry_integration/eventhouse/devops_telemetry.kql`
  - Defines the telemetry table schema.
  - Includes a helper function to query failed deployments.

- `foundry_integration/eventhouse/devops_telemetry_extended.kql`
  - Provides extended telemetry query definitions for richer event ingestion.

## Current Implementation Status

Implemented:
- Fully merged single-folder repository structure
- Runnable orchestration starter via `run_orchestrator.py`
- Local stub implementations for core agents and integration clients
- Local `foundry_iq` and `fabric_iq` packages for reasoning and telemetry simulation
- KQL telemetry schema and extended telemetry definitions
- Documentation and package helper files
- Test runner scaffolding via `test_orchestrator.py`

Pending / future work:
- Production-grade Fabric IQ and Foundry IQ client integration
- Real telemetry backend connection and credentials support
- Expanded agent logic beyond starter stub behavior
- Formal unit and integration tests for real workflows

## Installation

### Prerequisites

- Python 3.11+ installed
- Local clone of the repository
- An async-capable runtime for Python scripts

### Setup

```bash
cd c:\Workspaces\ibm\microsoft_hackthon\azure-sentinel-devops-orchestrator
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

> `requirements.txt` currently contains repository notes. The starter version uses local stub packages and does not require external `foundry_iq` / `fabric_iq` dependencies.

## Run the orchestrator

Execute the main orchestrator runner:

```bash
python run_orchestrator.py
```

The starter flow will produce a deployment result payload and simulate telemetry ingestion.

### Example runner usage

The repository already includes `run_orchestrator.py`; it invokes `DevOpsOrchestrator` with sample payloads.

## Validate telemetry

Use the KQL files in `foundry_integration/eventhouse/` to inspect telemetry schema and queries.

Example:

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

## Project structure

- `agents/orchestrator/main_orchestrator.py`
- `agents/reasoning_agents/deployment_agent.py`
- `agents/reasoning_agents/security_agent.py`
- `agents/reasoning_agents/monitoring_agent.py`
- `agents/reasoning_agents/incident_agent.py`
- `agents/integrations/fabric_iq_client.py`
- `foundry_iq/`
- `fabric_iq/`
- `foundry_integration/eventhouse/`
- documentation files: `INSTALLATION.md`, `QUICKSTART.md`, `API_REFERENCE.md`, etc.
- `run_orchestrator.py`
- `test_orchestrator.py`

## Next steps

1. Replace local stubs with real Fabric IQ / Foundry IQ client implementations.
2. Add configuration and credentials support in `config.py` and `.env.example`.
3. Expand reasoning logic in each agent.
4. Add formal tests around orchestrator flow and telemetry events.
5. Connect the pipeline to a real telemetry backend and verify the KQL queries.

## Notes

- This repository now uses a single consolidated folder structure.
- It is runnable as a starter project without external dependencies.
- Production integration and real backends remain future enhancements.
