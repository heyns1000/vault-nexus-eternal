"""Vault Nexus Eternal - API Layer

FastAPI REST + WebSocket Server
Real-time Breath Cycle Updates
OpenAPI Documentation
"""

__version__ = "1.0.0"

from .api_server import create_app

__all__ = ["create_app"]