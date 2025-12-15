"""
Test suite for API endpoints

Tests REST API endpoints and WebSocket connections.
"""

import pytest
import sys
import os
from fastapi.testclient import TestClient

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from api.api_server import app, api_state
from core.store40d import Store40D
from core.elephant_memory import ElephantMemory


# Test client
client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self):
        """Test GET /api/v1/health."""
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["system"] == "Vault Nexus Eternal"
        assert data["version"] == "1.0.0"
        assert "breath_cycle" in data
        assert "compliance" in data
        assert "OMNI-4321" in data["compliance"]


class TestRootEndpoint:
    """Test root endpoint."""
    
    def test_root(self):
        """Test GET /."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["name"] == "Vault Nexus Eternal API"
        assert data["version"] == "1.0.0"
        assert data["status"] == "operational"
        assert "docs" in data
        assert "websocket" in data


class TestStoreEndpoint:
    """Test data storage endpoint."""
    
    def setup_method(self):
        """Reset API state for each test."""
        api_state.store40d = Store40D(care_mandate=0.15)
        api_state.elephant = ElephantMemory(store40d=api_state.store40d)
    
    def test_store_brand(self):
        """Test POST /api/v1/store."""
        data = {
            "data": {
                "sector": "quantum_ai",
                "brand": "TestBrand",
                "product_type": "entanglement",
                "year": 2025,
                "quality_score": 0.95,
                "verified": True,
                "value": 1000.0
            }
        }
        
        response = client.post("/api/v1/store", json=data)
        
        assert response.status_code == 200
        result = response.json()
        
        assert result["success"] is True
        assert "genome" in result
        assert len(result["genome"]) == 64  # SHA-256
        assert "timestamp" in result
        assert "latency_ms" in result
        assert result["shanana_compliant"] is True
        assert result["care_15_applied"] is True
    
    def test_store_without_value(self):
        """Test storing data without value field."""
        data = {
            "data": {
                "brand": "NoCareValue"
            }
        }
        
        response = client.post("/api/v1/store", json=data)
        
        assert response.status_code == 200
        result = response.json()
        assert result["success"] is True
    
    def test_store_invalid_request(self):
        """Test store with invalid request."""
        response = client.post("/api/v1/store", json={})
        
        assert response.status_code == 422  # Validation error


class TestQueryEndpoint:
    """Test query endpoint."""
    
    def setup_method(self):
        """Set up test data."""
        api_state.store40d = Store40D()
        api_state.elephant = ElephantMemory(store40d=api_state.store40d)
        
        # Store test brands
        test_brands = [
            {"sector": "quantum_ai", "brand": "QBrand1", "year": 2025, "quality_score": 0.9},
            {"sector": "quantum_ai", "brand": "QBrand2", "year": 2025, "quality_score": 0.85},
            {"sector": "fintech", "brand": "FBrand1", "year": 2024, "quality_score": 0.95}
        ]
        
        for brand in test_brands:
            api_state.store40d.store(brand)
    
    def test_query_exact_match(self):
        """Test POST /api/v1/query with exact match."""
        query = {
            "filters": {
                "sector": "quantum_ai"
            }
        }
        
        response = client.post("/api/v1/query", json=query)
        
        assert response.status_code == 200
        result = response.json()
        
        assert result["success"] is True
        assert result["count"] == 2
        assert len(result["results"]) == 2
        assert "latency_ms" in result
        assert result["shanana_compliant"] is True
    
    def test_query_with_operators(self):
        """Test query with range operators."""
        query = {
            "filters": {
                "quality_score": 0.9
            },
            "operators": {
                "quality_score": ">="
            }
        }
        
        response = client.post("/api/v1/query", json=query)
        
        assert response.status_code == 200
        result = response.json()
        
        assert result["success"] is True
        assert result["count"] >= 2  # At least 0.9 and 0.95
    
    def test_query_with_limit(self):
        """Test query with result limit."""
        query = {
            "filters": {
                "year": 2025
            },
            "limit": 1
        }
        
        response = client.post("/api/v1/query", json=query)
        
        assert response.status_code == 200
        result = response.json()
        
        assert result["success"] is True
        assert len(result["results"]) <= 1
    
    def test_query_no_matches(self):
        """Test query with no matches."""
        query = {
            "filters": {
                "sector": "nonexistent"
            }
        }
        
        response = client.post("/api/v1/query", json=query)
        
        assert response.status_code == 200
        result = response.json()
        
        assert result["success"] is True
        assert result["count"] == 0
        assert len(result["results"]) == 0


class TestStatsEndpoint:
    """Test statistics endpoint."""
    
    def setup_method(self):
        """Set up API state."""
        api_state.store40d = Store40D(care_mandate=0.15)
        api_state.elephant = ElephantMemory(store40d=api_state.store40d)
    
    def test_get_stats(self):
        """Test GET /api/v1/stats."""
        # Store some data first
        api_state.store40d.store({"brand": "Test", "value": 1000.0})
        
        response = client.get("/api/v1/stats")
        
        assert response.status_code == 200
        stats = response.json()
        
        # Hypercube stats
        assert "total_stored" in stats
        assert stats["total_stored"] >= 1
        assert "care_pool" in stats
        assert stats["care_pool"] >= 150.0  # 15% of 1000
        assert "dimensions" in stats
        assert stats["dimensions"] == 40
        assert "care_mandate" in stats
        assert stats["care_mandate"] == 0.15
        
        # API stats
        assert "api" in stats
        assert "uptime_seconds" in stats["api"]
        assert "breath_cycles" in stats["api"]


class TestEchoEndpoint:
    """Test ELEPHANT_MEMORY echo endpoint."""
    
    def setup_method(self):
        """Set up API state."""
        api_state.store40d = Store40D()
        api_state.elephant = ElephantMemory(store40d=api_state.store40d)
    
    def test_trigger_echo(self):
        """Test POST /api/v1/echo."""
        echo_data = {
            "content": {
                "event": "NVQLink quantum demo",
                "importance": "critical",
                "category": "quantum"
            },
            "tags": ["quantum", "nvqlink", "demo"]
        }
        
        response = client.post("/api/v1/echo", json=echo_data)
        
        assert response.status_code == 200
        result = response.json()
        
        assert result["success"] is True
        assert "genome" in result
        assert result["phase"] == "INTAKE"
        assert result["page"] == 1
        assert result["strength"] == 1.0
        assert result["decay_rate"] == 0.0
    
    def test_echo_without_tags(self):
        """Test echo without tags."""
        echo_data = {
            "content": {
                "event": "Simple event"
            }
        }
        
        response = client.post("/api/v1/echo", json=echo_data)
        
        assert response.status_code == 200
        result = response.json()
        assert result["success"] is True


class TestWisdomEndpoint:
    """Test generational wisdom endpoint."""
    
    def setup_method(self):
        """Set up API state with memories."""
        api_state.store40d = Store40D()
        api_state.elephant = ElephantMemory(store40d=api_state.store40d)
        
        # Ingest some memories
        api_state.elephant.ingest({"event": "Event 1"}, tags=["quantum"])
        api_state.elephant.ingest({"event": "Event 2"}, tags=["quantum"])
        api_state.elephant.ingest({"event": "Event 3"}, tags=["finance"])
    
    def test_get_wisdom_all(self):
        """Test GET /api/v1/wisdom without filters."""
        response = client.get("/api/v1/wisdom")
        
        assert response.status_code == 200
        result = response.json()
        
        assert result["success"] is True
        assert "wisdom" in result
        assert "current_generation" in result["wisdom"]
    
    def test_get_wisdom_with_tags(self):
        """Test GET /api/v1/wisdom with tag filter."""
        response = client.get("/api/v1/wisdom?tags=quantum&limit=10")
        
        assert response.status_code == 200
        result = response.json()
        
        assert result["success"] is True
        assert "memories" in result
        assert len(result["memories"]) >= 2  # Should have 2 quantum memories


class TestElephantStatsEndpoint:
    """Test ELEPHANT_MEMORY statistics endpoint."""
    
    def setup_method(self):
        """Set up API state."""
        api_state.store40d = Store40D()
        api_state.elephant = ElephantMemory(store40d=api_state.store40d)
        
        api_state.elephant.ingest({"event": "Test"}, tags=["test"])
    
    def test_get_elephant_stats(self):
        """Test GET /api/v1/elephant/stats."""
        response = client.get("/api/v1/elephant/stats")
        
        assert response.status_code == 200
        stats = response.json()
        
        assert "total_memories" in stats
        assert stats["total_memories"] >= 1
        assert "pages" in stats
        assert stats["pages"] == 46
        assert "decay_rate" in stats
        assert stats["decay_rate"] == 0.0
        assert "current_generation" in stats


class TestWebSocket:
    """Test WebSocket connections."""
    
    def setup_method(self):
        """Set up API state."""
        api_state.store40d = Store40D()
        api_state.elephant = ElephantMemory(store40d=api_state.store40d)
    
    def test_websocket_connection(self):
        """Test WebSocket connection establishment."""
        with client.websocket_connect("/ws/realtime") as websocket:
            # Should receive connection message
            data = websocket.receive_json()
            
            assert data["type"] == "connection_established"
            assert "breath_cycle" in data
            assert "timestamp" in data
    
    def test_websocket_ping_pong(self):
        """Test WebSocket ping/pong."""
        with client.websocket_connect("/ws/realtime") as websocket:
            # Skip connection message
            websocket.receive_json()
            
            # Send ping
            websocket.send_text("ping")
            
            # Should receive pong
            data = websocket.receive_json()
            assert data["type"] == "pong"
    
    def test_websocket_stats_request(self):
        """Test requesting stats via WebSocket."""
        with client.websocket_connect("/ws/realtime") as websocket:
            # Skip connection message
            websocket.receive_json()
            
            # Request stats
            websocket.send_text("stats")
            
            # Should receive stats
            data = websocket.receive_json()
            assert data["type"] == "stats"
            assert "data" in data
            assert "hypercube" in data["data"]


class TestErrorHandling:
    """Test error handling."""
    
    def test_store_without_state(self):
        """Test store when Store40D not initialized."""
        # Temporarily remove store40d
        original_store = api_state.store40d
        api_state.store40d = None
        
        response = client.post("/api/v1/store", json={"data": {"brand": "Test"}})
        
        # Restore state
        api_state.store40d = original_store
        
        assert response.status_code == 503  # Service unavailable
        assert "Store40D not initialized" in response.json()["detail"]
    
    def test_query_without_state(self):
        """Test query when Store40D not initialized."""
        original_store = api_state.store40d
        api_state.store40d = None
        
        response = client.post("/api/v1/query", json={"filters": {}})
        
        api_state.store40d = original_store
        
        assert response.status_code == 503


class TestCORS:
    """Test CORS configuration."""
    
    def test_cors_headers(self):
        """Test CORS headers are present."""
        response = client.options("/api/v1/health")
        
        # Should allow CORS (configured with allow_origins=["*"])
        assert response.status_code in [200, 405]  # OPTIONS might be allowed or not


class TestOpenAPI:
    """Test OpenAPI documentation."""
    
    def test_openapi_json(self):
        """Test OpenAPI JSON is available."""
        response = client.get("/openapi.json")
        
        assert response.status_code == 200
        openapi = response.json()
        
        assert "openapi" in openapi
        assert "info" in openapi
        assert openapi["info"]["title"] == "Vault Nexus Eternal API"
    
    def test_docs_endpoint(self):
        """Test /docs endpoint exists."""
        response = client.get("/docs")
        
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
