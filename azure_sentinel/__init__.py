"""
Azure Sentinel Integration Module
Enterprise-grade incident management and SOAR automation
"""

from .sentinel_client import AzureSentinelClient, SentinelIncident, create_sentinel_incident

__all__ = [
    'AzureSentinelClient',
    'SentinelIncident',
    'create_sentinel_incident'
]

__version__ = '1.0.0'

# Made with Bob
