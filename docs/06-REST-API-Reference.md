# REST API Reference

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently open (no authentication required).  
**Coming soon**: JWT-based authentication.

## Endpoints

### Health Check

```http
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-15T13:00:00Z",
  "system": "Vault Nexus Eternal",
  "version": "1.0.0",
  "breath_cycle": 1234,
  "compliance": "TreatyHook™ OMNI-4321 §9.4.17"
}
```

### Store Data in 40D Hypercube

```http
POST /api/v1/store
Content-Type: application/json
```

**Request Body:**
```json
{
  "data": {
    "sector": "quantum_ai",
    "brand": "NVQLink",
    "product_type": "entanglement",
    "tech_stack": "CUDA-Q",
    "year": 2025,
    "quarter": 4,
    "quality_score": 0.95,
    "verified": true,
    "value": 1000.0
  }
}
```

**Response:**
```json
{
  "success": true,
  "genome": "a7f3c9e1d2b8f4a6...",
  "timestamp": "2025-12-15T13:00:00Z",
  "latency_ms": 12.34,
  "shanana_compliant": true,
  "care_15_applied": true
}
```

### Query 40D Hypercube

```http
POST /api/v1/query
Content-Type: application/json
```

**Request Body:**
```json
{
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
```

**Supported Operators:**
- `==` - Exact match (default)
- `>` - Greater than
- `<` - Less than
- `>=` - Greater than or equal
- `<=` - Less than or equal
- `in` - Member of array

**Response:**
```json
{
  "success": true,
  "count": 23,
  "results": [...],
  "latency_ms": 45.67,
  "shanana_compliant": true,
  "timestamp": "2025-12-15T13:00:00Z"
}
```

### Get Statistics

```http
GET /api/v1/stats
```

**Response:**
```json
{
  "total_stored": 13713,
  "total_queries": 5678,
  "care_redistributed": 15234.56,
  "avg_query_time": 0.045,
  "dimensions": 40,
  "care_mandate": 0.15,
  "care_pool": 15234.56,
  "free_capacity_percent": 87.7,
  "compliance": "TreatyHook™ OMNI-4321 §9.4.17",
  "api": {
    "uptime_seconds": 86400,
    "breath_cycles": 9600,
    "websocket_clients": 3
  }
}
```

### Trigger ELEPHANT_MEMORY Echo

```http
POST /api/v1/echo
Content-Type: application/json
```

**Request Body:**
```json
{
  "content": {
    "event": "NVQLink quantum entanglement demo",
    "importance": "critical",
    "category": "quantum",
    "timestamp": "2025-12-15T13:00:00Z"
  },
  "tags": ["quantum", "nvqlink", "demo"]
}
```

**Response:**
```json
{
  "success": true,
  "genome": "b8f4c9e2d3a7f5b6...",
  "phase": "INTAKE",
  "page": 1,
  "timestamp": "2025-12-15T13:00:00Z",
  "strength": 1.0,
  "decay_rate": 0.0
}
```

### Get Generational Wisdom

```http
GET /api/v1/wisdom?generation=5&tags=quantum,nvqlink&limit=100
```

**Query Parameters:**
- `generation` (optional): Specific generation number
- `tags` (optional): Comma-separated tags to filter
- `limit` (optional): Maximum memories to return (default: 100)

**Response:**
```json
{
  "success": true,
  "wisdom": {
    "total_generations": 12,
    "current_generation": 12,
    "generations": [...]
  },
  "memories": [...],
  "timestamp": "2025-12-15T13:00:00Z"
}
```

### Get ELEPHANT_MEMORY Statistics

```http
GET /api/v1/elephant/stats
```

**Response:**
```json
{
  "total_memories": 15234,
  "total_echoes": 45678,
  "total_generations": 12,
  "herd_validations": 8765,
  "phase_transitions": 23456,
  "avg_strength": 1.0,
  "pages": 46,
  "current_generation": 12,
  "loop_count": 89234,
  "decay_rate": 0.0,
  "memories_by_phase": {...},
  "top_tags": [...]
}
```

## WebSocket

### Real-Time Breath Updates

```
ws://localhost:8000/ws/realtime
```

**Client Messages:**
- `"ping"` - Heartbeat request
- `"stats"` - Request current statistics

**Server Messages:**

**Connection Established:**
```json
{
  "type": "connection_established",
  "breath_cycle": 1234,
  "timestamp": "2025-12-15T13:00:00Z",
  "message": "Connected to Vault Nexus Eternal real-time feed"
}
```

**Breath Phase Update:**
```json
{
  "phase": "PULSE",
  "cycle": 1234,
  "timestamp": "2025-12-15T13:00:00Z"
}
```

**Statistics Response:**
```json
{
  "type": "stats",
  "data": {
    "hypercube": {...},
    "elephant": {...},
    "breath_cycle": 1234
  },
  "timestamp": "2025-12-15T13:00:00Z"
}
```

**Heartbeat:**
```json
{
  "type": "heartbeat",
  "timestamp": "2025-12-15T13:00:00Z",
  "breath_cycle": 1234
}
```

## OpenAPI/Swagger

Interactive API documentation available at:

```
http://localhost:8000/docs
```

ReDoc alternative:

```
http://localhost:8000/redoc
```

## Rate Limiting

**Current**: No rate limiting  
**Coming Soon**: 100 requests/minute per IP

## Error Responses

### 400 Bad Request

```json
{
  "detail": "Invalid request format"
}
```

### 500 Internal Server Error

```json
{
  "detail": "Error message"
}
```

### 503 Service Unavailable

```json
{
  "detail": "Store40D not initialized"
}
```

---

**Base URL**: http://localhost:8000/api/v1  
**WebSocket**: ws://localhost:8000/ws/realtime  
**Docs**: http://localhost:8000/docs
