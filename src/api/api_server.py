"""
FastAPI REST + WebSocket Server

Sovereign API for Vault Nexus Eternal ecosystem.
Provides REST endpoints and real-time WebSocket for 40D Hypercube and ELEPHANT_MEMORY.

Endpoints:
- POST /api/v1/store - Store data in 40D Hypercube
- POST /api/v1/query - Multi-dimensional queries
- GET /api/v1/stats - Hypercube statistics
- POST /api/v1/echo - Trigger ELEPHANT_MEMORY ingestion
- GET /api/v1/wisdom - Retrieve generational wisdom
- GET /api/v1/health - Health check
- WebSocket /ws/realtime - Live breath cycle updates

Features:
- OpenAPI/Swagger docs at /docs
- CORS enabled for dashboard integration
- TreatyHook™ OMNI-4321 §9.4.17 compliant
- <9s response latency (Shanana™)
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import asyncio
import json
import time
from datetime import datetime
from contextlib import asynccontextmanager


# Import core components
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.store40d import Store40D
from core.elephant_memory import ElephantMemory


# Pydantic models for request/response validation
class StoreRequest(BaseModel):
    """Request model for storing data in 40D Hypercube."""
    data: Dict[str, Any] = Field(..., description="Data to store with 40D coordinates")
    
    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "sector": "quantum_ai",
                    "brand": "NVQLink",
                    "product_type": "entanglement",
                    "tech_stack": "CUDA-Q",
                    "year": 2025,
                    "quarter": 4,
                    "quality_score": 0.95,
                    "verified": True,
                    "value": 1000.0
                }
            }
        }


class QueryRequest(BaseModel):
    """Request model for multi-dimensional queries."""
    filters: Dict[str, Any] = Field(..., description="Filter criteria by dimension")
    operators: Optional[Dict[str, str]] = Field(None, description="Operators for each dimension")
    limit: Optional[int] = Field(100, description="Maximum results to return")
    
    class Config:
        json_schema_extra = {
            "example": {
                "filters": {
                    "sector": "quantum_ai",
                    "year": 2025,
                    "quality_score": 0.8
                },
                "operators": {
                    "quality_score": ">="
                },
                "limit": 50
            }
        }


class EchoRequest(BaseModel):
    """Request model for ELEPHANT_MEMORY echo/ingestion."""
    content: Dict[str, Any] = Field(..., description="Memory content to ingest")
    tags: Optional[List[str]] = Field(None, description="Tags for categorization")
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": {
                    "event": "NVQLink quantum entanglement demo",
                    "importance": "critical",
                    "category": "quantum",
                    "timestamp": "2025-12-15T13:00:00Z"
                },
                "tags": ["quantum", "nvqlink", "demo"]
            }
        }


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: str
    system: str
    version: str
    breath_cycle: int
    compliance: str


# Global state
class APIState:
    """Global API state container."""
    def __init__(self):
        self.store40d: Optional[Store40D] = None
        self.elephant: Optional[ElephantMemory] = None
        self.websocket_clients: List[WebSocket] = []
        self.breath_count: int = 0
        self.start_time: float = time.time()
        self.breath_task: Optional[asyncio.Task] = None


api_state = APIState()


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - startup and shutdown."""
    # Startup
    print("🦏 Vault Nexus Eternal API - Starting up...")
    
    # Initialize core components
    api_state.store40d = Store40D(care_mandate=0.15)
    api_state.elephant = ElephantMemory(store40d=api_state.store40d, decay_rate=0.0)
    
    print("✅ 40D Hypercube initialized")
    print("✅ ELEPHANT_MEMORY initialized (46 pages)")
    
    # Start breath cycle background task
    api_state.breath_task = asyncio.create_task(breath_cycle_loop())
    print("✅ Breath cycle started (9s eternal loop)")
    
    print("🌬️ API ready - Sovereign stack breathing!")
    
    yield
    
    # Shutdown
    print("\n🛑 Shutting down gracefully...")
    
    # Cancel breath cycle
    if api_state.breath_task:
        api_state.breath_task.cancel()
        try:
            await api_state.breath_task
        except asyncio.CancelledError:
            pass
    
    # Close all websockets
    for client in api_state.websocket_clients:
        await client.close()
    
    print("✅ Shutdown complete - State preserved")


# Create FastAPI app
app = FastAPI(
    title="Vault Nexus Eternal API",
    description="Sovereign Full Stack Ecosystem - 40D Hypercube + ELEPHANT_MEMORY",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware for dashboard integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Background task: 9-second breath cycle
async def breath_cycle_loop():
    """
    Eternal 9-second breath cycle loop.
    
    Phases:
    0s - PULSE: Inhale new data
    3s - GLOW: Vortex processing
    6s - TRADE: Execute transactions
    8s - FLOW: CARE-15 redistribution
    9s - RESET: Evolution/next cycle
    """
    while True:
        try:
            api_state.breath_count += 1
            cycle_start = time.time()
            
            # Broadcast breath start to websockets
            await broadcast_breath_update({
                "phase": "PULSE",
                "cycle": api_state.breath_count,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            # PULSE phase (0-3s)
            await asyncio.sleep(3)
            
            # GLOW phase (3-6s)
            await broadcast_breath_update({
                "phase": "GLOW",
                "cycle": api_state.breath_count,
                "timestamp": datetime.utcnow().isoformat()
            })
            await asyncio.sleep(3)
            
            # TRADE phase (6-8s)
            await broadcast_breath_update({
                "phase": "TRADE",
                "cycle": api_state.breath_count,
                "timestamp": datetime.utcnow().isoformat()
            })
            await asyncio.sleep(2)
            
            # FLOW phase (8-9s) - Execute ELEPHANT_MEMORY breath
            await broadcast_breath_update({
                "phase": "FLOW",
                "cycle": api_state.breath_count,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            if api_state.elephant:
                cycle_stats = api_state.elephant.breath_cycle()
                await broadcast_breath_update({
                    "phase": "FLOW_COMPLETE",
                    "elephant_stats": cycle_stats,
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            await asyncio.sleep(1)
            
            # RESET phase
            await broadcast_breath_update({
                "phase": "RESET",
                "cycle": api_state.breath_count,
                "next_cycle": api_state.breath_count + 1,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            # Ensure exactly 9 seconds
            elapsed = time.time() - cycle_start
            if elapsed < 9:
                await asyncio.sleep(9 - elapsed)
                
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"❌ Breath cycle error: {e}")
            await asyncio.sleep(9)


async def broadcast_breath_update(message: Dict[str, Any]):
    """Broadcast breath update to all connected websocket clients."""
    disconnected = []
    
    for client in api_state.websocket_clients:
        try:
            await client.send_json(message)
        except:
            disconnected.append(client)
    
    # Remove disconnected clients
    for client in disconnected:
        api_state.websocket_clients.remove(client)


# REST API Endpoints

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Vault Nexus Eternal API",
        "version": "1.0.0",
        "status": "operational",
        "compliance": "TreatyHook™ OMNI-4321 §9.4.17",
        "breath_cycle": "9s eternal",
        "docs": "/docs",
        "websocket": "/ws/realtime"
    }


@app.get("/api/v1/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns system status and compliance information.
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        system="Vault Nexus Eternal",
        version="1.0.0",
        breath_cycle=api_state.breath_count,
        compliance="TreatyHook™ OMNI-4321 §9.4.17"
    )


@app.post("/api/v1/store", tags=["40D Hypercube"])
async def store_data(request: StoreRequest):
    """
    Store data in 40D Hypercube.
    
    Auto-enforces CARE-15 mandate (15% redistribution).
    Returns genome hash for stored data.
    """
    if not api_state.store40d:
        raise HTTPException(status_code=503, detail="Store40D not initialized")
    
    start_time = time.time()
    
    try:
        genome = api_state.store40d.store(request.data)
        query_time = time.time() - start_time
        
        return {
            "success": True,
            "genome": genome,
            "timestamp": datetime.utcnow().isoformat(),
            "latency_ms": round(query_time * 1000, 2),
            "shanana_compliant": query_time < 9,
            "care_15_applied": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/query", tags=["40D Hypercube"])
async def query_data(request: QueryRequest):
    """
    Multi-dimensional query on 40D Hypercube.
    
    Supports operators: ==, >, <, >=, <=, in
    Returns matching data points with <9s latency (Shanana™).
    """
    if not api_state.store40d:
        raise HTTPException(status_code=503, detail="Store40D not initialized")
    
    start_time = time.time()
    
    try:
        results = api_state.store40d.query(
            filters=request.filters,
            operators=request.operators
        )
        
        # Apply limit
        if request.limit:
            results = results[:request.limit]
        
        query_time = time.time() - start_time
        
        return {
            "success": True,
            "count": len(results),
            "results": results,
            "latency_ms": round(query_time * 1000, 2),
            "shanana_compliant": query_time < 9,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/stats", tags=["40D Hypercube"])
async def get_stats():
    """
    Get 40D Hypercube statistics.
    
    Returns comprehensive stats including CARE-15 redistribution.
    """
    if not api_state.store40d:
        raise HTTPException(status_code=503, detail="Store40D not initialized")
    
    try:
        stats = api_state.store40d.get_stats()
        
        # Add API-level stats
        uptime = time.time() - api_state.start_time
        stats["api"] = {
            "uptime_seconds": round(uptime, 2),
            "breath_cycles": api_state.breath_count,
            "websocket_clients": len(api_state.websocket_clients)
        }
        
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/echo", tags=["ELEPHANT_MEMORY"])
async def trigger_echo(request: EchoRequest):
    """
    Trigger ELEPHANT_MEMORY ingestion (echo).
    
    Ingests content into 46-page echo loop system.
    Returns genome hash for ingested memory.
    """
    if not api_state.elephant:
        raise HTTPException(status_code=503, detail="ELEPHANT_MEMORY not initialized")
    
    try:
        genome = api_state.elephant.ingest(
            content=request.content,
            tags=request.tags
        )
        
        return {
            "success": True,
            "genome": genome,
            "phase": "INTAKE",
            "page": 1,
            "timestamp": datetime.utcnow().isoformat(),
            "strength": 1.0,
            "decay_rate": 0.0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/wisdom", tags=["ELEPHANT_MEMORY"])
async def get_wisdom(
    generation: Optional[int] = Query(None, description="Specific generation number"),
    tags: Optional[str] = Query(None, description="Comma-separated tags to filter"),
    limit: int = Query(100, description="Maximum memories to return")
):
    """
    Retrieve generational wisdom from ELEPHANT_MEMORY.
    
    Can filter by generation number or tags.
    Returns generational archive and memory snapshots.
    """
    if not api_state.elephant:
        raise HTTPException(status_code=503, detail="ELEPHANT_MEMORY not initialized")
    
    try:
        # Get generational wisdom
        wisdom = api_state.elephant.get_generational_wisdom(generation)
        
        # Get memories if tags specified
        memories = []
        if tags:
            tag_list = [t.strip() for t in tags.split(",")]
            recalled = api_state.elephant.recall(tags=tag_list, limit=limit)
            memories = [m.to_dict() for m in recalled]
        
        return {
            "success": True,
            "wisdom": wisdom,
            "memories": memories,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/elephant/stats", tags=["ELEPHANT_MEMORY"])
async def get_elephant_stats():
    """
    Get ELEPHANT_MEMORY statistics.
    
    Returns comprehensive stats across all 46 pages and 6 phases.
    """
    if not api_state.elephant:
        raise HTTPException(status_code=503, detail="ELEPHANT_MEMORY not initialized")
    
    try:
        stats = api_state.elephant.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# WebSocket endpoint for real-time updates
@app.websocket("/ws/realtime")
async def websocket_realtime(websocket: WebSocket):
    """
    WebSocket endpoint for real-time breath cycle updates.
    
    Broadcasts:
    - Breath cycle phase transitions (PULSE→GLOW→TRADE→FLOW→RESET)
    - ELEPHANT_MEMORY statistics
    - 40D Hypercube metrics
    """
    await websocket.accept()
    api_state.websocket_clients.append(websocket)
    
    try:
        # Send initial state
        await websocket.send_json({
            "type": "connection_established",
            "breath_cycle": api_state.breath_count,
            "timestamp": datetime.utcnow().isoformat(),
            "message": "Connected to Vault Nexus Eternal real-time feed"
        })
        
        # Keep connection alive and handle client messages
        while True:
            try:
                # Wait for client messages (keep-alive)
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                
                # Echo back or handle specific commands
                if data == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": datetime.utcnow().isoformat()
                    })
                elif data == "stats":
                    stats = {
                        "hypercube": api_state.store40d.get_stats() if api_state.store40d else {},
                        "elephant": api_state.elephant.get_stats() if api_state.elephant else {},
                        "breath_cycle": api_state.breath_count
                    }
                    await websocket.send_json({
                        "type": "stats",
                        "data": stats,
                        "timestamp": datetime.utcnow().isoformat()
                    })
                    
            except asyncio.TimeoutError:
                # Send periodic heartbeat
                await websocket.send_json({
                    "type": "heartbeat",
                    "timestamp": datetime.utcnow().isoformat(),
                    "breath_cycle": api_state.breath_count
                })
                
    except WebSocketDisconnect:
        api_state.websocket_clients.remove(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        if websocket in api_state.websocket_clients:
            api_state.websocket_clients.remove(websocket)


# Example usage and testing
if __name__ == "__main__":
    import uvicorn
    
    print("🦏 Starting Vault Nexus Eternal API Server...")
    print("📡 REST API: http://0.0.0.0:8000")
    print("📚 Docs: http://0.0.0.0:8000/docs")
    print("🔌 WebSocket: ws://0.0.0.0:8000/ws/realtime")
    print("\n瓷勺旋渦已築 - API Server launching!")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
