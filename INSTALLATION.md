# Complete Installation & Setup Guide

## Azure Sentinel DevOps Orchestrator

This guide provides step-by-step instructions to set up and run the Azure Sentinel DevOps Orchestrator.

---

## Prerequisites

- Python 3.11 or higher
- Git
- Virtual environment tool (venv or conda)
- Azure Subscription (for production deployment)
- Access to Fabric IQ and Foundry IQ services (optional, for advanced features)

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/azure-sentinel-devops-orchestrator.git
cd azure-sentinel-devops-orchestrator
```

---

## Step 2: Create and Activate Virtual Environment

### On macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### On Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### On Windows (Command Prompt):
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

---

## Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

For development (including testing and linting):
```bash
pip install -e ".[dev]"
```

---

## Step 4: Configure Environment

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your configuration:
```
FABRIC_WORKSPACE=devops_orchestration
FABRIC_EVENTHOUSE=devops_telemetry
FOUNDRY_MODEL=gpt-4o-reasoning
FOUNDRY_KNOWLEDGE_BASE=foundry_integration/knowledge_bases/devops_runbooks.json

# For Azure integration
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP=<your-resource-group>
AZURE_TENANT_ID=<your-tenant-id>

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

---

## Step 5: Verify Installation

Run the basic smoke test:
```bash
python -c "from agents.orchestrator.main_orchestrator import DevOpsOrchestrator; print('✓ Installation successful!')"
```

---

## Step 6: Run the Orchestrator

### Option A: Run the default example
```bash
python run_orchestrator.py
```

### Option B: Create and run a custom script
Create `my_orchestrator.py`:
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
    def __init__(self, code_changes, deployment_context):
        self.code_changes = code_changes
        self.deployment_context = deployment_context

async def main():
    logger.info("Starting DevOps Orchestrator pipeline")
    
    orchestrator = DevOpsOrchestrator()
    
    trigger = PipelineTrigger(
        code_changes={
            "files": ["main.py", "config.py"],
            "summary": "Production deployment"
        },
        deployment_context={
            "changes": ["service configuration update"],
            "target_resources": ["resource-group-prod", "app-service-prod"]
        }
    )
    
    try:
        result = await orchestrator.execute_pipeline(trigger)
        logger.info(f"Pipeline result: {result}")
        print(f"\n✓ Orchestration completed successfully!")
        print(f"Status: {result.get('status')}")
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        print(f"\n✗ Orchestration failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
python my_orchestrator.py
```

---

## Step 7: Run Tests

Run all tests:
```bash
pytest test_orchestrator.py -v
```

Run specific test class:
```bash
pytest test_orchestrator.py::TestOrchestrator -v
```

Run with coverage:
```bash
pytest test_orchestrator.py --cov=agents --cov-report=html
```

---

## Step 8: Configure Fabric IQ Telemetry (Optional)

1. Set up Fabric IQ workspace and eventhouse
2. Create the telemetry tables using KQL:

```bash
# Apply the schema
kusto < foundry_integration/eventhouse/devops_telemetry.kql

# For extended queries
kusto < foundry_integration/eventhouse/devops_telemetry_extended.kql
```

3. Verify table creation:
```kql
.show tables
| project TableName
| where TableName startswith "DevOps"
```

---

## Step 9: Verify Telemetry Ingestion

Test telemetry ingestion:
```python
import asyncio
from agents.integrations.fabric_iq_client import FabricIQClient

async def test_telemetry():
    client = FabricIQClient(
        workspace="devops_orchestration",
        eventhouse="devops_telemetry"
    )
    
    events = [{
        "Timestamp": "2026-06-07T12:00:00Z",
        "AgentName": "TestAgent",
        "Action": "test_action",
        "ResourceId": "resource-1",
        "Success": True,
        "ResponseTimeMs": 100
    }]
    
    result = await client.ingest_events(events)
    print(result)

asyncio.run(test_telemetry())
```

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'foundry_iq'`
**Solution:** Install the package in development mode:
```bash
pip install -e .
```

### Issue: `ImportError: cannot import name 'ReasoningAgent'`
**Solution:** Verify the foundry_iq package is properly installed:
```bash
python -c "from foundry_iq import ReasoningAgent; print('OK')"
```

### Issue: Async errors in tests
**Solution:** Install pytest-asyncio:
```bash
pip install pytest-asyncio
```

### Issue: Environment variables not loaded
**Solution:** Ensure `.env` file exists and is in the project root:
```bash
ls -la .env
```

---

## Project Structure

```
azure-sentinel-devops-orchestrator/
├── agents/
│   ├── orchestrator/
│   │   ├── __init__.py
│   │   └── main_orchestrator.py          # Main orchestration logic
│   ├── reasoning_agents/
│   │   ├── __init__.py
│   │   ├── deployment_agent.py           # Deployment reasoning
│   │   ├── security_agent.py             # Security scanning
│   │   ├── monitoring_agent.py           # Monitoring configuration
│   │   └── incident_agent.py             # Incident tracking
│   └── integrations/
│       ├── __init__.py
│       └── fabric_iq_client.py           # Fabric IQ integration
├── foundry_iq/
│   ├── __init__.py
│   ├── reasoning.py                      # Reasoning framework
│   └── models.py                         # Data models
├── fabric_iq/
│   ├── __init__.py
│   ├── telemetry.py                      # Telemetry client
│   └── events.py                         # Event schemas
├── foundry_integration/
│   ├── eventhouse/
│   │   ├── devops_telemetry.kql          # KQL schema
│   │   └── devops_telemetry_extended.kql # Extended KQL queries
│   └── reasoning_models/
│       └── deployment_reasoning.json     # Reasoning model config
├── config.py                             # Configuration management
├── logger.py                             # Logging setup
├── run_orchestrator.py                   # Main entry point
├── test_orchestrator.py                  # Test suite
├── requirements.txt                      # Dependencies
├── setup.py                              # Package setup
├── .env.example                          # Environment template
└── README.md                             # Documentation
```

---

## Quick Reference: Common Commands

```bash
# Setup
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run
python run_orchestrator.py

# Test
pytest test_orchestrator.py -v

# Development
pip install -e ".[dev]"
black agents/
flake8 agents/
mypy agents/

# Clean
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

---

## Next Steps

1. **Customize agents:** Modify `agents/reasoning_agents/` to add your business logic
2. **Add telemetry:** Configure Fabric IQ workspace and eventhouse
3. **Extend orchestration:** Add new agents for custom workflows
4. **Deploy to Azure:** Use Azure DevOps or GitHub Actions for CI/CD
5. **Monitor:** Set up dashboards in Fabric IQ or Power BI

---

## Support & Contribution

For issues, questions, or contributions, please submit a GitHub issue or pull request.

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.
