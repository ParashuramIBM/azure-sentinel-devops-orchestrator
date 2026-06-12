# 📁 Enterprise Folder Structure

## Complete Project Organization

This document describes the complete folder structure of the Azure Sentinel DevOps Orchestrator enterprise implementation.

---

## 🏗️ Directory Tree

```
azure-sentinel-devops-orchestrator/
├── 📁 agents/                              # Core agent implementations
│   ├── __init__.py
│   ├── 📁 orchestrator/                    # Main orchestration logic
│   │   ├── __init__.py
│   │   └── main_orchestrator.py           # DevOpsOrchestrator class
│   ├── 📁 reasoning_agents/                # Specialized AI agents
│   │   ├── __init__.py
│   │   ├── deployment_agent.py            # IntelligentDeploymentAgent
│   │   ├── security_agent.py              # SecurityComplianceAgent
│   │   ├── monitoring_agent.py            # MonitoringIntelligenceAgent
│   │   └── incident_agent.py              # IncidentResponseAgent
│   └── 📁 integrations/                    # External integrations
│       ├── __init__.py
│       └── fabric_iq_client.py            # FabricIQClient
│
├── 📁 azure_sentinel/                      # ⭐ NEW: Azure Sentinel integration
│   ├── __init__.py
│   └── sentinel_client.py                 # AzureSentinelClient
│
├── 📁 foundry_iq/                          # Foundry IQ reasoning framework
│   ├── __init__.py
│   ├── reasoning.py                       # ReasoningAgent, ChainOfThought
│   └── models.py                          # DecisionResult, ReasoningContext
│
├── 📁 fabric_iq/                           # Fabric IQ telemetry library
│   ├── __init__.py
│   ├── telemetry.py                       # TelemetryClient
│   └── events.py                          # EventSchema, EventIngestion
│
├── 📁 foundry_integration/                 # Integration configurations
│   ├── 📁 eventhouse/                      # KQL schemas and queries
│   │   ├── devops_telemetry.kql           # Core telemetry schema
│   │   └── devops_telemetry_extended.kql  # Extended analytics
│   └── 📁 reasoning_models/                # Reasoning model configs
│       └── deployment_reasoning.json      # Deployment reasoning config
│
├── 📁 scripts/                             # Utility scripts
│   ├── validate_fabric_integration.py     # Fabric IQ validation
│   └── validate_foundry_integration.py    # Foundry IQ validation
│
├── 📁 tests/                               # Test suite
│   └── 📁 reasoning/
│       └── test_agents.py                 # Agent unit tests
│
├── 📁 logs/                                # ⭐ NEW: Log files (created at runtime)
│   └── orchestrator.log                   # Application logs
│
├── 📁 .github/                             # GitHub workflows
│   └── workflows/
│       └── ci-cd.yml                      # CI/CD pipeline
│
├── 📁 .venv/                               # Virtual environment (not in git)
│
├── 📄 config.py                            # Configuration management
├── 📄 logger.py                            # Logging setup
├── 📄 run_orchestrator.py                  # Main entry point
├── 📄 test_orchestrator.py                 # Comprehensive test suite
├── 📄 setup.py                             # Package setup
├── 📄 requirements.txt                     # Python dependencies
├── 📄 .env                                 # Environment variables (not in git)
├── 📄 .env.example                         # Environment template
├── 📄 .gitignore                           # Git ignore rules
│
├── 📄 README.md                            # Project overview
├── 📄 RUN_GUIDE.md                         # ⭐ NEW: Complete run guide
├── 📄 FOLDER_STRUCTURE.md                  # ⭐ NEW: This file
├── 📄 INSTALLATION.md                      # Installation guide
├── 📄 API_REFERENCE.md                     # API documentation
├── 📄 AZURE_PORTAL_CHECKLIST.md            # Azure Portal guide
├── 📄 QUICKSTART.md                        # Quick start guide
├── 📄 IMPLEMENTATION_COMPLETE.md           # Implementation summary
├── 📄 IMPLEMENTATION_STATUS.md             # Status tracking
├── 📄 DELIVERY_SUMMARY.md                  # Delivery summary
├── 📄 PROJECT_INDEX.md                     # Project index
├── 📄 START_HERE.txt                       # Getting started
│
├── 📄 quick_start.sh                       # ⭐ NEW: Quick start (Linux/Mac)
└── 📄 quick_start.bat                      # ⭐ NEW: Quick start (Windows)
```

---

## 📂 Directory Descriptions

### `/agents/` - Core Agent Implementations

**Purpose:** Contains all AI agent implementations for the orchestration pipeline.

**Key Files:**
- `orchestrator/main_orchestrator.py` - Main pipeline coordinator
- `reasoning_agents/deployment_agent.py` - Deployment decision making
- `reasoning_agents/security_agent.py` - Security scanning
- `reasoning_agents/monitoring_agent.py` - Monitoring configuration
- `reasoning_agents/incident_agent.py` - Incident management
- `integrations/fabric_iq_client.py` - Telemetry ingestion

**Usage:**
```python
from agents.orchestrator.main_orchestrator import DevOpsOrchestrator
from agents.reasoning_agents.security_agent import SecurityComplianceAgent
```

---

### `/azure_sentinel/` - ⭐ NEW: Azure Sentinel Integration

**Purpose:** Enterprise Azure Sentinel integration for incident management and SOAR automation.

**Key Files:**
- `sentinel_client.py` - AzureSentinelClient for incident creation and management

**Features:**
- ✅ Incident creation in Azure Sentinel
- ✅ Incident status updates
- ✅ Incident listing and querying
- ✅ SOAR automation triggers
- ✅ Managed Identity support

**Usage:**
```python
from azure_sentinel import AzureSentinelClient

client = AzureSentinelClient(
    subscription_id="your-sub-id",
    resource_group="sentinel-devops-rg",
    workspace_name="sentinel-devops-workspace"
)

incident = await client.create_incident(
    title="Deployment Failure",
    description="Critical deployment failed",
    severity="High"
)
```

---

### `/foundry_iq/` - Foundry IQ Reasoning Framework

**Purpose:** AI reasoning framework with chain-of-thought capabilities.

**Key Files:**
- `reasoning.py` - ReasoningAgent base class, ChainOfThought
- `models.py` - Data models (DecisionResult, ReasoningContext, RemediationPlan)

**Usage:**
```python
from foundry_iq import ReasoningAgent, ChainOfThought

agent = ReasoningAgent(name="CustomAgent", model="gpt-4o-reasoning")
chain = ChainOfThought(["Step 1", "Step 2", "Step 3"])
result = await agent.reason(context, chain)
```

---

### `/fabric_iq/` - Fabric IQ Telemetry Library

**Purpose:** Telemetry collection and ingestion to Fabric IQ.

**Key Files:**
- `telemetry.py` - TelemetryClient with buffering
- `events.py` - Event schema validation

**Usage:**
```python
from fabric_iq import TelemetryClient

client = TelemetryClient(workspace="devops_fabric")
await client.log_event("DevOpsTelemetry", {"AgentName": "Test", "Success": True})
await client.flush()
```

---

### `/foundry_integration/` - Integration Configurations

**Purpose:** KQL schemas, queries, and reasoning model configurations.

**Key Files:**
- `eventhouse/devops_telemetry.kql` - Core telemetry schema
- `eventhouse/devops_telemetry_extended.kql` - Advanced analytics
- `reasoning_models/deployment_reasoning.json` - Deployment reasoning config

**Usage:**
Apply KQL schemas in Azure Log Analytics workspace for telemetry tables.

---

### `/scripts/` - Utility Scripts

**Purpose:** Validation and utility scripts.

**Key Files:**
- `validate_fabric_integration.py` - Validate Fabric IQ connection
- `validate_foundry_integration.py` - Validate Foundry IQ connection

**Usage:**
```bash
python scripts/validate_fabric_integration.py
python scripts/validate_foundry_integration.py
```

---

### `/tests/` - Test Suite

**Purpose:** Unit and integration tests.

**Key Files:**
- `reasoning/test_agents.py` - Agent unit tests

**Usage:**
```bash
pytest tests/reasoning/test_agents.py -v
```

---

### `/logs/` - ⭐ NEW: Log Files

**Purpose:** Application logs (created at runtime).

**Key Files:**
- `orchestrator.log` - Main application log file

**Note:** This directory is created automatically when the application runs.

---

## 📄 Root Files

### Configuration Files

| File | Purpose |
|------|---------|
| `config.py` | Centralized configuration management |
| `logger.py` | Logging setup with JSON formatting |
| `.env` | Environment variables (not in git) |
| `.env.example` | Environment variable template |
| `requirements.txt` | Python dependencies |
| `setup.py` | Package setup configuration |

### Entry Points

| File | Purpose |
|------|---------|
| `run_orchestrator.py` | Main application entry point |
| `test_orchestrator.py` | Comprehensive test suite |
| `quick_start.sh` | ⭐ Quick start script (Linux/Mac) |
| `quick_start.bat` | ⭐ Quick start script (Windows) |

### Documentation

| File | Purpose |
|------|---------|
| `README.md` | Project overview and features |
| `RUN_GUIDE.md` | ⭐ Complete step-by-step run guide |
| `FOLDER_STRUCTURE.md` | ⭐ This file - folder organization |
| `INSTALLATION.md` | Detailed installation instructions |
| `API_REFERENCE.md` | Complete API documentation |
| `AZURE_PORTAL_CHECKLIST.md` | Azure Portal navigation guide |
| `QUICKSTART.md` | 5-minute quick start |
| `IMPLEMENTATION_COMPLETE.md` | Implementation summary |
| `START_HERE.txt` | Getting started pointer |

---

## 🚀 Quick Navigation

### For New Users
1. Start with `START_HERE.txt`
2. Read `README.md` for overview
3. Follow `RUN_GUIDE.md` for setup
4. Run `quick_start.sh` or `quick_start.bat`

### For Developers
1. Review `API_REFERENCE.md`
2. Check `FOLDER_STRUCTURE.md` (this file)
3. Explore `/agents/` directory
4. Run tests with `pytest test_orchestrator.py -v`

### For Operations
1. Follow `INSTALLATION.md`
2. Configure using `.env.example`
3. Review `AZURE_PORTAL_CHECKLIST.md`
4. Monitor using KQL queries in `/foundry_integration/eventhouse/`

---

## 🔧 Key Integration Points

### 1. Azure Sentinel Integration
```
run_orchestrator.py
    ↓
agents/orchestrator/main_orchestrator.py
    ↓
azure_sentinel/sentinel_client.py
    ↓
Azure Sentinel (Incidents)
```

### 2. Telemetry Flow
```
agents/reasoning_agents/*.py
    ↓
agents/integrations/fabric_iq_client.py
    ↓
fabric_iq/telemetry.py
    ↓
Azure Log Analytics
```

### 3. Reasoning Pipeline
```
agents/orchestrator/main_orchestrator.py
    ↓
foundry_iq/reasoning.py
    ↓
agents/reasoning_agents/*.py
    ↓
Decision Results
```

---

## 📊 File Statistics

| Category | Count | Purpose |
|----------|-------|---------|
| Python Modules | 25+ | Core application code |
| Test Files | 2 | Unit and integration tests |
| Documentation | 10+ | Guides and references |
| Configuration | 5 | Setup and environment |
| Scripts | 4 | Automation and utilities |
| KQL Files | 2 | Telemetry schemas |

---

## 🔐 Security Notes

### Files NOT in Git
- `.env` - Contains sensitive credentials
- `.venv/` - Virtual environment
- `logs/` - Log files may contain sensitive data
- `__pycache__/` - Python cache
- `*.pyc` - Compiled Python files
- `.pytest_cache/` - Test cache
- `htmlcov/` - Coverage reports

### Files in Git
- `.env.example` - Template (no secrets)
- All source code
- Documentation
- Configuration templates

---

## 🎯 Development Workflow

### 1. Setup
```bash
git clone <repo>
cd azure-sentinel-devops-orchestrator
./quick_start.sh  # or quick_start.bat on Windows
```

### 2. Development
```bash
# Edit code in /agents/ or /azure_sentinel/
# Run tests
pytest test_orchestrator.py -v

# Run orchestrator
python run_orchestrator.py
```

### 3. Testing
```bash
# Unit tests
pytest tests/reasoning/test_agents.py -v

# Integration tests
pytest test_orchestrator.py -v

# Coverage
pytest --cov=agents --cov=azure_sentinel --cov-report=html
```

### 4. Deployment
```bash
# See RUN_GUIDE.md Phase 6: Production Deployment
```

---

## 📚 Additional Resources

- **Azure Sentinel Docs**: https://docs.microsoft.com/azure/sentinel/
- **KQL Reference**: https://docs.microsoft.com/azure/data-explorer/kusto/query/
- **Python Async**: https://docs.python.org/3/library/asyncio.html
- **Azure SDK**: https://docs.microsoft.com/python/api/overview/azure/

---

**Last Updated:** 2026-06-12  
**Version:** 1.0.0  
**Status:** Production Ready ✅