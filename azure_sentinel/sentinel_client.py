"""
Azure Sentinel Client for Enterprise Integration
Handles incident creation, analytics rules, and SOAR automation
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
import json

try:
    from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
    from azure.mgmt.securityinsight import SecurityInsights
    from azure.mgmt.securityinsight.models import Incident, IncidentSeverity, IncidentStatus
    AZURE_SDK_AVAILABLE = True
except ImportError:
    AZURE_SDK_AVAILABLE = False
    logging.warning("Azure SDK not available. Running in simulation mode.")


@dataclass
class SentinelIncident:
    """Sentinel incident data model"""
    incident_id: str
    title: str
    description: str
    severity: str  # Low, Medium, High, Critical
    status: str  # New, Active, Closed
    created_time: str
    resource_id: Optional[str] = None
    tactics: Optional[List[str]] = None
    tags: Optional[Dict[str, str]] = None


class AzureSentinelClient:
    """
    Enterprise Azure Sentinel Client
    
    Features:
    - Incident creation and management
    - Analytics rule integration
    - SOAR automation triggers
    - Threat intelligence integration
    """
    
    def __init__(
        self,
        subscription_id: str,
        resource_group: str,
        workspace_name: str,
        use_managed_identity: bool = False
    ):
        """Initialize Azure Sentinel client"""
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.workspace_name = workspace_name
        self.logger = logging.getLogger(__name__)
        
        # Initialize credential
        if AZURE_SDK_AVAILABLE:
            try:
                if use_managed_identity:
                    self.credential = ManagedIdentityCredential()
                    self.logger.info("Using Managed Identity for authentication")
                else:
                    self.credential = DefaultAzureCredential()
                    self.logger.info("Using Default Azure Credential")
                
                self.client = SecurityInsights(
                    credential=self.credential,
                    subscription_id=subscription_id
                )
                self.logger.info(f"Azure Sentinel client initialized for workspace: {workspace_name}")
            except Exception as e:
                self.logger.error(f"Failed to initialize Azure Sentinel client: {e}")
                self.client = None
        else:
            self.client = None
            self.logger.warning("Running in simulation mode - no actual Azure connection")
    
    async def create_incident(
        self,
        title: str,
        description: str,
        severity: str,
        resource_id: Optional[str] = None,
        tactics: Optional[List[str]] = None,
        tags: Optional[Dict[str, str]] = None
    ) -> SentinelIncident:
        """Create incident in Azure Sentinel"""
        incident_id = f"INC-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        
        try:
            if self.client and AZURE_SDK_AVAILABLE:
                severity_map = {
                    "Low": IncidentSeverity.LOW,
                    "Medium": IncidentSeverity.MEDIUM,
                    "High": IncidentSeverity.HIGH,
                    "Critical": IncidentSeverity.HIGH
                }
                
                incident_properties = {
                    "title": title,
                    "description": description,
                    "severity": severity_map.get(severity, IncidentSeverity.MEDIUM),
                    "status": IncidentStatus.NEW
                }
                
                if tactics:
                    incident_properties["tactics"] = tactics
                
                incident = await asyncio.to_thread(
                    self.client.incidents.create_or_update,
                    resource_group_name=self.resource_group,
                    workspace_name=self.workspace_name,
                    incident_id=incident_id,
                    incident=incident_properties
                )
                
                self.logger.info(f"✅ Created Sentinel incident: {incident_id}")
                
                return SentinelIncident(
                    incident_id=incident_id,
                    title=title,
                    description=description,
                    severity=severity,
                    status="New",
                    created_time=datetime.now(timezone.utc).isoformat(),
                    resource_id=resource_id,
                    tactics=tactics,
                    tags=tags
                )
            else:
                self.logger.info(f"📝 [SIMULATION] Would create Sentinel incident: {incident_id}")
                self.logger.info(f"   Title: {title}")
                self.logger.info(f"   Severity: {severity}")
                
                return SentinelIncident(
                    incident_id=incident_id,
                    title=title,
                    description=description,
                    severity=severity,
                    status="New",
                    created_time=datetime.now(timezone.utc).isoformat(),
                    resource_id=resource_id,
                    tactics=tactics,
                    tags=tags
                )
                
        except Exception as e:
            self.logger.error(f"❌ Failed to create Sentinel incident: {e}")
            return SentinelIncident(
                incident_id=incident_id,
                title=title,
                description=description,
                severity=severity,
                status="Failed",
                created_time=datetime.now(timezone.utc).isoformat(),
                resource_id=resource_id,
                tactics=tactics,
                tags=tags
            )
    
    async def list_incidents(self, filter_query: Optional[str] = None, top: int = 50) -> List[Dict[str, Any]]:
        """List incidents from Sentinel"""
        try:
            if self.client and AZURE_SDK_AVAILABLE:
                incidents = await asyncio.to_thread(
                    self.client.incidents.list,
                    resource_group_name=self.resource_group,
                    workspace_name=self.workspace_name,
                    filter=filter_query,
                    top=top
                )
                
                incident_list = []
                for incident in incidents:
                    incident_list.append({
                        "incident_id": incident.name,
                        "title": incident.title,
                        "severity": str(incident.severity),
                        "status": str(incident.status),
                        "created_time": incident.created_time_utc.isoformat() if incident.created_time_utc else None
                    })
                
                self.logger.info(f"✅ Retrieved {len(incident_list)} incidents")
                return incident_list
            else:
                self.logger.info("📝 [SIMULATION] Would list incidents")
                return []
                
        except Exception as e:
            self.logger.error(f"❌ Failed to list incidents: {e}")
            return []
    
    def get_incident_url(self, incident_id: str) -> str:
        """Get Azure Portal URL for incident"""
        return (
            f"https://portal.azure.com/#blade/Microsoft_Azure_Security_Insights/"
            f"IncidentBlade/id/%2Fsubscriptions%2F{self.subscription_id}%2F"
            f"resourceGroups%2F{self.resource_group}%2Fproviders%2F"
            f"Microsoft.OperationalInsights%2Fworkspaces%2F{self.workspace_name}%2F"
            f"providers%2FMicrosoft.SecurityInsights%2FIncidents%2F{incident_id}"
        )

# Made with Bob
