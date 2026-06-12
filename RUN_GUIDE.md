# 🚀 Complete Run Guide - Azure Sentinel DevOps Orchestrator

## Enterprise Implementation with Working Steps

This guide provides complete, tested steps to run the Azure Sentinel DevOps Orchestrator in your environment.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start (5 minutes)](#quick-start-5-minutes)
3. [Full Enterprise Setup (90 minutes)](#full-enterprise-setup-90-minutes)
4. [Verification Steps](#verification-steps)
5. [Troubleshooting](#troubleshooting)
6. [Production Deployment](#production-deployment)

---

## Prerequisites

### Required Software
- ✅ Python 3.11 or higher
- ✅ Git
- ✅ Azure CLI (`az`) - [Install](https://docs.microsoft.com/cli/azure/install-azure-cli)
- ✅ Active Azure Subscription

### Required Access
- ✅ Azure Subscription Contributor role
- ✅ Permission to create Resource Groups
- ✅ Permission to enable Microsoft Sentinel

### System Requirements
- ✅ Windows 10/11, macOS, or Linux
- ✅ 4GB RAM minimum
- ✅ 2GB free disk space

---

## Quick Start (5 minutes)

### Step 1: Clone and Setup

```bash
# Clone repository
git clone https://github.com/yourusername/azure-sentinel-devops-orchestrator.git
cd azure-sentinel-devops-orchestrator

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your editor (notepad, vim, nano, etc.)
notepad .env  # Windows
nano .env     # Linux/Mac
```

**Minimal .env configuration for local testing:**
```bash
# Local Testing Mode (no Azure required)
SENTINEL_ENABLED=false
LOG_LEVEL=INFO
LOG_FORMAT=json

# Optional: Add Azure credentials later
AZURE_SUBSCRIPTION_ID=
AZURE_RESOURCE_GROUP=
AZURE_TENANT_ID=
```

### Step 3: Run the Orchestrator

```bash
# Run in local/simulation mode
python run_orchestrator.py
```

**Expected Output:**
```
🚀 Starting DevOps Orchestrator Pipeline
✅ Security scan completed - Status: approved
✅ Deployment evaluation completed - Safe: True
✅ Monitoring configuration completed
✅ Telemetry ingested - 4 events
✅ Pipeline execution successful!

Pipeline Result: {'status': 'success', 'deployment_plan': {...}, 'monitoring_config': {...}}
```

### Step 4: Run Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest test_orchestrator.py -v

# Run with coverage
pytest test_orchestrator.py -v --cov=agents --cov-report=html
```

---

## Full Enterprise Setup (90 minutes)

### Phase 1: Azure Infrastructure (30 minutes)

#### 1.1 Login to Azure

```bash
# Login to Azure
az login

# List subscriptions
az account list --output table

# Set active subscription
az account set --subscription "YOUR_SUBSCRIPTION_NAME_OR_ID"

# Verify current subscription
az account show --output table
```

#### 1.2 Create Resource Group

```bash
# Create resource group
az group create \
  --name sentinel-devops-rg \
  --location eastus \
  --tags Environment=Production Project=DevOpsOrchestrator

# Verify creation
az group show --name sentinel-devops-rg --output table
```

#### 1.3 Create Log Analytics Workspace

```bash
# Create Log Analytics workspace
az monitor log-analytics workspace create \
  --resource-group sentinel-devops-rg \
  --workspace-name sentinel-devops-workspace \
  --location eastus \
  --sku PerGB2018

# Get Workspace ID (save this!)
WORKSPACE_ID=$(az monitor log-analytics workspace show \
  --resource-group sentinel-devops-rg \
  --workspace-name sentinel-devops-workspace \
  --query customerId -o tsv)

echo "Workspace ID: $WORKSPACE_ID"

# Get Workspace Key (save this!)
WORKSPACE_KEY=$(az monitor log-analytics workspace get-shared-keys \
  --resource-group sentinel-devops-rg \
  --workspace-name sentinel-devops-workspace \
  --query primarySharedKey -o tsv)

echo "Workspace Key: $WORKSPACE_KEY"

# IMPORTANT: Save these values for later!
```

#### 1.4 Enable Microsoft Sentinel

**Option A: Using Azure CLI**
```bash
# Enable Sentinel
az sentinel onboard \
  --resource-group sentinel-devops-rg \
  --workspace-name sentinel-devops-workspace
```

**Option B: Using Azure Portal**
1. Go to [Azure Portal](https://portal.azure.com)
2. Search for "Microsoft Sentinel"
3. Click "+ Create"
4. Select workspace: `sentinel-devops-workspace`
5. Click "Add"
6. Wait for deployment (2-3 minutes)

#### 1.5 Verify Setup

```bash
# Verify resource group
az group show --name sentinel-devops-rg

# Verify workspace
az monitor log-analytics workspace show \
  --resource-group sentinel-devops-rg \
  --workspace-name sentinel-devops-workspace

# List all resources in group
az resource list \
  --resource-group sentinel-devops-rg \
  --output table
```

---

### Phase 2: Application Configuration (15 minutes)

#### 2.1 Update Environment File

Edit `.env` file with your Azure credentials:

```bash
# Azure Sentinel Configuration
AZURE_SUBSCRIPTION_ID=your-subscription-id-here
AZURE_RESOURCE_GROUP=sentinel-devops-rg
AZURE_TENANT_ID=your-tenant-id-here
AZURE_WORKSPACE_ID=your-workspace-id-from-step-1.3
AZURE_WORKSPACE_KEY=your-workspace-key-from-step-1.3

# Sentinel Configuration
SENTINEL_WORKSPACE_NAME=sentinel-devops-workspace
SENTINEL_ENABLED=true

# Fabric IQ Configuration (Optional)
FABRIC_WORKSPACE=devops_orchestration
FABRIC_EVENTHOUSE=devops_telemetry

# Foundry IQ Configuration
FOUNDRY_MODEL=gpt-4o-reasoning
FOUNDRY_KNOWLEDGE_BASE=foundry_integration/knowledge_bases/devops_runbooks.json

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE=logs/orchestrator.log

# Performance Configuration
MAX_CONCURRENT_OPERATIONS=50
EVENT_BATCH_SIZE=100
TELEMETRY_FLUSH_INTERVAL=60
DEBUG=false
```

#### 2.2 Get Azure Tenant ID

```bash
# Get tenant ID
az account show --query tenantId -o tsv
```

#### 2.3 Get Subscription ID

```bash
# Get subscription ID
az account show --query id -o tsv
```

#### 2.4 Create Logs Directory

```bash
# Create logs directory
mkdir -p logs

# On Windows:
mkdir logs
```

---

### Phase 3: Azure Sentinel Configuration (20 minutes)

#### 3.1 Create Custom Log Table

**Navigate to Azure Portal:**
1. Go to Log Analytics Workspace → `sentinel-devops-workspace`
2. Click "Tables" → "Create" → "New custom log (DCR-based)"
3. Use the following schema:

**Or use Azure CLI:**
```bash
# Create custom table
az monitor log-analytics workspace table create \
  --resource-group sentinel-devops-rg \
  --workspace-name sentinel-devops-workspace \
  --name DevOpsTelemetry_CL \
  --columns '[
    {"name":"TimeGenerated","type":"datetime"},
    {"name":"AgentName","type":"string"},
    {"name":"Action","type":"string"},
    {"name":"ResourceId","type":"string"},
    {"name":"Success","type":"boolean"},
    {"name":"ResponseTimeMs","type":"int"},
    {"name":"ErrorCode","type":"string"},
    {"name":"ReasoningTrace","type":"string"},
    {"name":"Severity","type":"string"},
    {"name":"DeploymentId","type":"string"}
  ]'
```

#### 3.2 Create Analytics Rules

**Rule 1: Failed Deployment Detection**

1. Navigate to: Sentinel → Analytics → Create → Scheduled query rule
2. Name: `Multiple Deployment Failures`
3. Severity: High
4. Query:

```kql
DevOpsTelemetry_CL
| where TimeGenerated > ago(5m)
| where AgentName == "IntelligentDeploymentAgent"
| where Success == false
| summarize FailureCount = count() by ResourceId, ErrorCode
| where FailureCount > 3
| project 
    TimeGenerated = now(),
    AlertName = "Multiple Deployment Failures Detected",
    Severity = "High",
    ResourceId,
    ErrorCode,
    FailureCount
```

5. Query scheduling:
   - Run query every: 5 minutes
   - Lookup data from the last: 5 minutes
6. Alert threshold: Greater than 0
7. Click "Create"

**Rule 2: Security Violation Detection**

1. Create new rule
2. Name: `Security Compliance Violation`
3. Severity: High
4. Query:

```kql
DevOpsTelemetry_CL
| where TimeGenerated > ago(5m)
| where AgentName == "SecurityComplianceAgent"
| where Success == false
| where Severity in ("High", "Critical")
| project 
    TimeGenerated,
    AlertName = "Security Compliance Violation",
    Severity,
    ResourceId,
    ReasoningTrace
```

5. Same scheduling as Rule 1
6. Click "Create"

**Rule 3: Agent Performance Degradation**

1. Create new rule
2. Name: `Agent Performance Degradation`
3. Severity: Medium
4. Query:

```kql
DevOpsTelemetry_CL
| where TimeGenerated > ago(15m)
| summarize AvgResponseTime = avg(ResponseTimeMs) by AgentName
| where AvgResponseTime > 5000
| project 
    TimeGenerated = now(),
    AlertName = "Agent Performance Degradation",
    Severity = "Medium",
    AgentName,
    AvgResponseTimeMs = AvgResponseTime
```

5. Run every 15 minutes, lookup last 15 minutes
6. Click "Create"

#### 3.3 Create Automation Rule (Optional)

1. Navigate to: Sentinel → Automation → Create → Automation rule
2. Name: `Auto-Remediate Deployment Failures`
3. Trigger: When incident is created
4. Conditions:
   - Incident title contains: "Deployment Failure"
   - Severity equals: High
5. Actions:
   - Add comment: "Automated remediation initiated by orchestrator"
   - Change status to: Active
6. Click "Create"

---

### Phase 4: Run and Verify (15 minutes)

#### 4.1 Install Azure SDK Dependencies

```bash
# Install Azure SDK packages
pip install azure-identity azure-mgmt-securityinsight azure-monitor-ingestion
```

#### 4.2 Verify Installation

```bash
# Test imports
python -c "
from agents.orchestrator.main_orchestrator import DevOpsOrchestrator
from azure_sentinel import AzureSentinelClient
from config import Config
print('✅ All imports successful!')
print(f'Sentinel Enabled: {Config.SENTINEL_ENABLED}')
print(f'Workspace: {Config.SENTINEL_WORKSPACE_NAME}')
"
```

#### 4.3 Run Orchestrator with Azure Integration

```bash
# Run orchestrator
python run_orchestrator.py
```

**Expected Output with Azure Integration:**
```
🚀 Starting DevOps Orchestrator Pipeline
🔐 Authenticating with Azure...
✅ Azure Sentinel client initialized
✅ Security scan completed - Status: approved
✅ Deployment evaluation completed - Safe: True
✅ Monitoring configuration completed
📊 Sending telemetry to Azure Log Analytics...
✅ Telemetry sent successfully
✅ Pipeline execution successful!
```

#### 4.4 Verify Telemetry in Azure

**Option A: Azure Portal**
1. Go to Log Analytics Workspace
2. Click "Logs"
3. Run query:

```kql
DevOpsTelemetry_CL
| where TimeGenerated > ago(1h)
| project TimeGenerated, AgentName, Action, Success, ResponseTimeMs
| order by TimeGenerated desc
| take 50
```

**Option B: Azure CLI**
```bash
# Query logs
az monitor log-analytics query \
  --workspace $WORKSPACE_ID \
  --analytics-query "DevOpsTelemetry_CL | where TimeGenerated > ago(1h) | take 10" \
  --output table
```

#### 4.5 Check Sentinel Incidents

**Azure Portal:**
1. Navigate to Microsoft Sentinel
2. Click "Incidents"
3. You should see incidents created by the orchestrator (if any failures occurred)

**Azure CLI:**
```bash
# List incidents
az sentinel incident list \
  --resource-group sentinel-devops-rg \
  --workspace-name sentinel-devops-workspace \
  --output table
```

---

### Phase 5: Run Tests (10 minutes)

#### 5.1 Run Unit Tests

```bash
# Run all tests
pytest test_orchestrator.py -v

# Run specific test class
pytest test_orchestrator.py::TestOrchestrator -v

# Run with detailed output
pytest test_orchestrator.py -v -s
```

#### 5.2 Run Integration Tests

```bash
# Run integration tests (requires Azure connection)
pytest test_orchestrator.py -v -m integration

# Run with coverage
pytest test_orchestrator.py -v --cov=agents --cov=azure_sentinel --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser
```

#### 5.3 Verify Test Results

Expected output:
```
test_orchestrator.py::TestSecurityAgent::test_scan_pipeline PASSED
test_orchestrator.py::TestDeploymentAgent::test_evaluate_deployment PASSED
test_orchestrator.py::TestMonitoringAgent::test_configure_observability PASSED
test_orchestrator.py::TestIncidentAgent::test_create_incident PASSED
test_orchestrator.py::TestOrchestrator::test_execute_pipeline PASSED
test_orchestrator.py::TestFabricIQClient::test_ingest_events PASSED

======================== 10 passed in 5.23s ========================
```

---

## Verification Steps

### 1. Verify Azure Resources

```bash
# Check resource group
az group show --name sentinel-devops-rg --output table

# Check Log Analytics workspace
az monitor log-analytics workspace show \
  --resource-group sentinel-devops-rg \
  --workspace-name sentinel-devops-workspace \
  --output table

# Check Sentinel status
az sentinel show \
  --resource-group sentinel-devops-rg \
  --workspace-name sentinel-devops-workspace \
  --output table
```

### 2. Verify Telemetry Flow

```kql
// Run in Log Analytics Workspace → Logs

// Check if data is flowing
DevOpsTelemetry_CL
| where TimeGenerated > ago(1h)
| summarize Count = count() by AgentName
| order by Count desc

// Check success rate
DevOpsTelemetry_CL
| where TimeGenerated > ago(24h)
| summarize 
    Total = count(),
    Successful = countif(Success == true),
    Failed = countif(Success == false)
| extend SuccessRate = round(100.0 * Successful / Total, 2)
```

### 3. Verify Analytics Rules

```bash
# List analytics rules
az sentinel alert-rule list \
  --resource-group sentinel-devops-rg \
  --workspace-name sentinel-devops-workspace \
  --output table
```

### 4. Test Incident Creation

```python
# Create test_incident.py
import asyncio
from azure_sentinel import AzureSentinelClient
from config import Config

async def test_incident():
    client = AzureSentinelClient(
        subscription_id=Config.AZURE_SUBSCRIPTION_ID,
        resource_group=Config.AZURE_RESOURCE_GROUP,
        workspace_name=Config.SENTINEL_WORKSPACE_NAME
    )
    
    incident = await client.create_incident(
        title="Test Incident - DevOps Orchestrator",
        description="This is a test incident created by the orchestrator",
        severity="Medium",
        tactics=["Execution", "Persistence"]
    )
    
    print(f"✅ Created incident: {incident.incident_id}")
    print(f"   Portal URL: {client.get_incident_url(incident.incident_id)}")

asyncio.run(test_incident())
```

Run:
```bash
python test_incident.py
```

---

## Troubleshooting

### Issue 1: Authentication Errors

**Error:** `DefaultAzureCredential failed to retrieve a token`

**Solution:**
```bash
# Re-login to Azure
az login

# Clear Azure CLI cache
az account clear
az login

# Verify authentication
az account show
```

### Issue 2: Telemetry Not Appearing

**Error:** Data not showing in Log Analytics

**Solution:**
```bash
# Check workspace connection
az monitor log-analytics workspace show \
  --resource-group sentinel-devops-rg \
  --workspace-name sentinel-devops-workspace

# Verify workspace ID in .env matches
echo $WORKSPACE_ID

# Check if table exists
az monitor log-analytics workspace table show \
  --resource-group sentinel-devops-rg \
  --workspace-name sentinel-devops-workspace \
  --name DevOpsTelemetry_CL
```

### Issue 3: Module Import Errors

**Error:** `ModuleNotFoundError: No module named 'azure_sentinel'`

**Solution:**
```bash
# Reinstall in development mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Linux/Mac
set PYTHONPATH=%PYTHONPATH%;%CD%  # Windows CMD
```

### Issue 4: Permission Denied

**Error:** `AuthorizationFailed: The client does not have authorization`

**Solution:**
```bash
# Grant required permissions
az role assignment create \
  --assignee $(az account show --query user.name -o tsv) \
  --role "Azure Sentinel Contributor" \
  --resource-group sentinel-devops-rg

# Verify role assignment
az role assignment list \
  --resource-group sentinel-devops-rg \
  --output table
```

### Issue 5: Sentinel Not Enabled

**Error:** `Sentinel workspace not found`

**Solution:**
```bash
# Enable Sentinel
az sentinel onboard \
  --resource-group sentinel-devops-rg \
  --workspace-name sentinel-devops-workspace

# Verify
az sentinel show \
  --resource-group sentinel-devops-rg \
  --workspace-name sentinel-devops-workspace
```

---

## Production Deployment

### Option 1: Azure App Service

```bash
# Create App Service Plan
az appservice plan create \
  --name sentinel-orchestrator-plan \
  --resource-group sentinel-devops-rg \
  --sku P1V2 \
  --is-linux

# Create Web App
az webapp create \
  --name sentinel-orchestrator-app \
  --resource-group sentinel-devops-rg \
  --plan sentinel-orchestrator-plan \
  --runtime "PYTHON:3.11"

# Configure app settings
az webapp config appsettings set \
  --name sentinel-orchestrator-app \
  --resource-group sentinel-devops-rg \
  --settings \
    AZURE_SUBSCRIPTION_ID="$AZURE_SUBSCRIPTION_ID" \
    AZURE_WORKSPACE_ID="$WORKSPACE_ID" \
    SENTINEL_ENABLED="true"

# Deploy code
zip -r deploy.zip . -x "*.git*" -x "*__pycache__*" -x "*.venv*"

az webapp deployment source config-zip \
  --name sentinel-orchestrator-app \
  --resource-group sentinel-devops-rg \
  --src deploy.zip
```

### Option 2: Azure Container Instances

```bash
# Build Docker image
docker build -t sentinel-orchestrator:latest .

# Push to Azure Container Registry
az acr create --name sentinelorchestrator --resource-group sentinel-devops-rg --sku Basic
az acr login --name sentinelorchestrator
docker tag sentinel-orchestrator:latest sentinelorchestrator.azurecr.io/orchestrator:latest
docker push sentinelorchestrator.azurecr.io/orchestrator:latest

# Deploy to ACI
az container create \
  --name sentinel-orchestrator \
  --resource-group sentinel-devops-rg \
  --image sentinelorchestrator.azurecr.io/orchestrator:latest \
  --cpu 2 \
  --memory 4 \
  --environment-variables \
    AZURE_SUBSCRIPTION_ID="$AZURE_SUBSCRIPTION_ID" \
    SENTINEL_ENABLED="true"
```

---

## Next Steps

1. ✅ **Customize Agents** - Modify agents in `agents/reasoning_agents/` for your use case
2. ✅ **Add Custom Rules** - Create additional Sentinel analytics rules
3. ✅ **Configure Dashboards** - Build monitoring dashboards in Azure Portal
4. ✅ **Set Up CI/CD** - Implement automated deployment pipeline
5. ✅ **Enable Monitoring** - Configure Application Insights
6. ✅ **Train Team** - Conduct training sessions for operations team

---

## Support

- 📧 Email: support@example.com
- 💬 Slack: #devops-orchestrator
- 📚 Documentation: [Full Docs](./README.md)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/azure-sentinel-devops-orchestrator/issues)

---

**Last Updated:** 2026-06-12  
**Version:** 1.0.0  
**Status:** Production Ready ✅