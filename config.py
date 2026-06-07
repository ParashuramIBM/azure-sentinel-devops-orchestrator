"""Configuration utilities for Azure Sentinel DevOps Orchestrator."""
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration from environment variables."""
    
    # Fabric IQ Settings
    FABRIC_WORKSPACE: str = os.getenv("FABRIC_WORKSPACE", "devops_orchestration")
    FABRIC_EVENTHOUSE: str = os.getenv("FABRIC_EVENTHOUSE", "devops_telemetry")
    
    # Foundry IQ Settings
    FOUNDRY_MODEL: str = os.getenv("FOUNDRY_MODEL", "gpt-4o-reasoning")
    FOUNDRY_KNOWLEDGE_BASE: str = os.getenv(
        "FOUNDRY_KNOWLEDGE_BASE",
        "foundry_integration/knowledge_bases/devops_runbooks.json"
    )
    
    # Azure Settings
    AZURE_SUBSCRIPTION_ID: Optional[str] = os.getenv("AZURE_SUBSCRIPTION_ID")
    AZURE_RESOURCE_GROUP: Optional[str] = os.getenv("AZURE_RESOURCE_GROUP")
    AZURE_TENANT_ID: Optional[str] = os.getenv("AZURE_TENANT_ID")
    
    # Logging Settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "json")
    
    # Application Settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    @classmethod
    def get_all(cls) -> dict:
        """Get all configuration values as a dictionary."""
        return {
            "fabric_workspace": cls.FABRIC_WORKSPACE,
            "fabric_eventhouse": cls.FABRIC_EVENTHOUSE,
            "foundry_model": cls.FOUNDRY_MODEL,
            "foundry_knowledge_base": cls.FOUNDRY_KNOWLEDGE_BASE,
            "azure_subscription_id": cls.AZURE_SUBSCRIPTION_ID,
            "azure_resource_group": cls.AZURE_RESOURCE_GROUP,
            "azure_tenant_id": cls.AZURE_TENANT_ID,
            "log_level": cls.LOG_LEVEL,
            "log_format": cls.LOG_FORMAT,
            "debug": cls.DEBUG,
        }
