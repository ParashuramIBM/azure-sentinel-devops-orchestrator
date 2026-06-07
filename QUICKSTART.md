# Quick Start Guide

## 5-Minute Setup

Get started with Azure Sentinel DevOps Orchestrator in 5 minutes.

### 1. Prerequisites
```bash
python --version  # Ensure Python 3.11+
git --version     # Ensure git is installed
```

### 2. Clone & Setup
```bash
git clone <repository-url>
cd azure-sentinel-devops-orchestrator
python -m venv .venv
# On Windows: .venv\Scripts\activate
# On macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure
```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Run
```bash
python run_orchestrator.py
```

### 5. View Results
Output will show the orchestration pipeline execution results.

---

## Run Your First Test

```python
# test_first_run.py
import asyncio
from agents.orchestrator.main_orchestrator import DevOpsOrchestrator

class PipelineTrigger:
    def __init__(self):
        self.code_changes = {"files": ["app.py"]}
        self.deployment_context = {
            "changes": ["config update"],
            "target_resources": ["resource-group"]
        }

async def main():
    orchestrator = DevOpsOrchestrator()
    trigger = PipelineTrigger()
    result = await orchestrator.execute_pipeline(trigger)
    print("✓ Success!" if result.get("status") == "success" else "✗ Failed")
    print(result)

asyncio.run(main())
```

Run it:
```bash
python test_first_run.py
```

---

## Project Files Overview

### Core Orchestration
- `run_orchestrator.py` - Main entry point
- `agents/orchestrator/main_orchestrator.py` - Orchestration engine
- `config.py` - Configuration management
- `logger.py` - Logging setup

### Reasoning Agents
- `agents/reasoning_agents/security_agent.py` - Security scanning
- `agents/reasoning_agents/deployment_agent.py` - Deployment planning
- `agents/reasoning_agents/monitoring_agent.py` - Monitoring setup
- `agents/reasoning_agents/incident_agent.py` - Incident tracking

### Integration & Libraries
- `agents/integrations/fabric_iq_client.py` - Fabric IQ event ingestion
- `fabric_iq/` - Fabric IQ telemetry library
- `foundry_iq/` - Foundry IQ reasoning framework

### Documentation & Configuration
- `README.md` - Project overview
- `INSTALLATION.md` - Detailed setup guide
- `API_REFERENCE.md` - Complete API reference
- `foundry_integration/eventhouse/devops_telemetry.kql` - KQL schema
- `foundry_integration/eventhouse/devops_telemetry_extended.kql` - Extended KQL queries

### Tests
- `test_orchestrator.py` - Full test suite

---

## Common Tasks

### Run the orchestrator
```bash
python run_orchestrator.py
```

### Run tests
```bash
pip install pytest pytest-asyncio
pytest test_orchestrator.py -v
```

### Check configuration
```bash
python -c "from config import Config; print(Config.get_all())"
```

### View logs in JSON format
```bash
python run_orchestrator.py | python -m json.tool
```

### Access help
```bash
python -c "from agents.orchestrator.main_orchestrator import DevOpsOrchestrator; help(DevOpsOrchestrator.execute_pipeline)"
```

---

## Next Steps

1. **Read Documentation**
   - [README.md](README.md) - Overview
   - [INSTALLATION.md](INSTALLATION.md) - Detailed setup
   - [API_REFERENCE.md](API_REFERENCE.md) - API details

2. **Explore Code**
   - Check `agents/reasoning_agents/` for agent implementation
   - Review `agents/orchestrator/main_orchestrator.py` for pipeline logic
   - Look at `test_orchestrator.py` for usage examples

3. **Customize**
   - Modify agents for your specific needs
   - Add custom reasoning logic
   - Extend with new agents

4. **Deploy**
   - Set up CI/CD pipeline
   - Configure Azure resources
   - Deploy to production

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -e .` |
| `AsyncIO errors` | Install `pytest-asyncio` |
| `Config not loading` | Check `.env` file exists |
| `Tests failing` | Run `pytest test_orchestrator.py -v` |

---

## Support

- See [INSTALLATION.md](INSTALLATION.md) for detailed setup
- See [API_REFERENCE.md](API_REFERENCE.md) for API documentation
- Check `test_orchestrator.py` for usage examples
