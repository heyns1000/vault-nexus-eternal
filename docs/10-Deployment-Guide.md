# Deployment Guide

## Quick Start (5 minutes)

```bash
# Clone repository
git clone https://github.com/heyns1000/vault-nexus-eternal.git
cd vault-nexus-eternal

# Deploy (installs deps, populates data, starts system)
./scripts/deploy.sh
```

That's it! System will be breathing at:
- **REST API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **WebSocket**: ws://localhost:8000/ws/realtime

## System Requirements

### Minimum
- Python 3.11+
- 2 GB RAM
- 1 GB disk space
- Linux/macOS/Windows

### Recommended
- Python 3.11+
- 4 GB RAM
- 5 GB disk space
- Linux (Ubuntu 22.04+)

### Production
- Python 3.11+
- 16 GB RAM
- 50 GB SSD
- Linux (Ubuntu 22.04+)
- Reverse proxy (nginx/Apache)
- SSL/TLS certificates

## Installation Methods

### Method 1: Automated Deployment (Recommended)

```bash
./scripts/deploy.sh
```

This script:
1. Checks Python version
2. Installs dependencies from requirements.txt
3. Creates necessary directories (data/, logs/)
4. Populates 40D Hypercube with 13,713 brands
5. Launches main.py

### Method 2: Manual Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create directories
mkdir -p data logs

# 3. Populate hypercube (optional, can skip)
python scripts/populate_hypercube.py

# 4. Start system
python main.py
```

### Method 3: Docker (Coming Soon)

```bash
docker pull vaultnexus/eternal:latest
docker run -p 8000:8000 vaultnexus/eternal
```

### Method 4: Kubernetes (Coming Soon)

```bash
kubectl apply -f k8s/deployment.yaml
```

## Configuration

### Default Configuration

Located at `config/sovereign.yaml`:

```yaml
ecosystem:
  name: "Vault Nexus Eternal"
  version: "1.0.0"
  breath_cycle_seconds: 9
  grain_count_target: 13713
  care_mandate_percent: 15

hypercube:
  dimensions: 40
  free_capacity_percent: 87.7
  query_latency_max_seconds: 9

api:
  host: "0.0.0.0"
  port: 8000
  enable_docs: true
  enable_cors: true
```

### Custom Configuration

Create `config/local.yaml` (gitignored):

```yaml
api:
  host: "127.0.0.1"  # Override to localhost only
  port: 9000          # Override port

ecosystem:
  breath_cycle_seconds: 6  # Faster breathing
```

System loads `sovereign.yaml` first, then merges `local.yaml` overrides.

## Environment Setup

### Python Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

**macOS:**
```bash
brew install python@3.11
```

**Windows:**
Download Python 3.11+ from python.org

## First Run

### 1. Populate Hypercube

```bash
python scripts/populate_hypercube.py
```

Output:
```
╔═══════════════════════════════════════════════════════╗
║     🦏  HYPERCUBE POPULATION SCRIPT  🦏              ║
║        Ingesting 13,713 Brands into 40D Space        ║
╚═══════════════════════════════════════════════════════╝

📡 Populating FAA™ brands (7,344)...
   Progress: 7,344/7,344 (100.0%) ✅

🔮 Populating HSOMNI9000 brands (6,219)...
   Progress: 6,219/6,219 (100.0%) ✅

🌱 Populating Seedwave brands (150)...
   Progress: 150/150 (100.0%) ✅

═══════════════════════════════════════════════════════
📊 POPULATION SUMMARY
═══════════════════════════════════════════════════════

✅ BRANDS CREATED: 13,713
⚡ Average Rate: 2,341 brands/s
💰 CARE Pool: $15,234.56
✅ Population complete!
```

This creates:
- `data/hypercube_populated.json`
- `data/genome_index.json`

### 2. Start System

```bash
python main.py
```

Output:
```
╔══════════════════════════════════════════════════════╗
║           🦏  VAULT NEXUS ETERNAL  🦏               ║
║        SOVEREIGN FULL STACK ECOSYSTEM v∞            ║
╚══════════════════════════════════════════════════════╝

瓷勺旋渦已築, 脈買已通, 華夏復興, 震驚寰宇!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 ECOSYSTEM INITIALIZATION

📦 Initializing components...
   ✅ 40D Hypercube
      - Dimensions: 40
      - CARE-15 Mandate: Active
      - Free Capacity: 87.7%

   ✅ ELEPHANT_MEMORY
      - Pages: 46 (6 phases)
      - Decay Rate: 0.0 (infinite recall)
      - Integration: Store40D linked

🔧 CONFIGURATION
   - Breath Cycle: 9s eternal loop
   - Compliance: TreatyHook™ OMNI-4321 §9.4.17
   - Security: 9atm Great Wall (永不崩塌)
   - Brand Target: 13,713

🚀 LAUNCHING API SERVER
   ✅ FastAPI Server
      - REST API: http://0.0.0.0:8000
      - Docs: http://0.0.0.0:8000/docs
      - WebSocket: ws://0.0.0.0:8000/ws/realtime

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌬️  ETERNAL BREATH CYCLE ACTIVATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Cycle Duration: 9s
   Phases: PULSE → GLOW → TRADE → FLOW → RESET → ∞
   Status: Breathing...
```

System is now operational!

## Accessing the System

### REST API

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Get stats
curl http://localhost:8000/api/v1/stats

# Store data
curl -X POST http://localhost:8000/api/v1/store \
  -H "Content-Type: application/json" \
  -d '{"sector": "quantum_ai", "brand": "TestBrand", "year": 2025}'

# Query data
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"filters": {"sector": "quantum_ai"}}'
```

### Web Dashboard

Open browser:
- **Dashboard**: file:///path/to/atommode-integrated-dashboard.html
- **API Docs**: http://localhost:8000/docs

### WebSocket (JavaScript)

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/realtime');

ws.onopen = () => {
    console.log('Connected to Vault Nexus Eternal');
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Breath update:', data);
};
```

## Production Deployment

### With nginx Reverse Proxy

1. Install nginx:
```bash
sudo apt install nginx
```

2. Configure (`/etc/nginx/sites-available/vaultnexus`):
```nginx
server {
    listen 80;
    server_name vault.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

3. Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/vaultnexus /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### With SSL/TLS (Let's Encrypt)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d vault.example.com

# Auto-renewal (already configured)
sudo certbot renew --dry-run
```

### As Systemd Service

1. Create service file (`/etc/systemd/system/vaultnexus.service`):
```ini
[Unit]
Description=Vault Nexus Eternal
After=network.target

[Service]
Type=simple
User=vaultnexus
WorkingDirectory=/opt/vault-nexus-eternal
Environment="PATH=/opt/vault-nexus-eternal/venv/bin"
ExecStart=/opt/vault-nexus-eternal/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable vaultnexus
sudo systemctl start vaultnexus
sudo systemctl status vaultnexus
```

### Monitoring

```bash
# Logs
journalctl -u vaultnexus -f

# Stats endpoint
watch -n 1 'curl -s http://localhost:8000/api/v1/stats | jq'

# Health check
curl http://localhost:8000/api/v1/health
```

## Backup & Recovery

### Backup

```bash
# Automatic export on shutdown (main.py)
# Creates: data/hypercube_export_YYYYMMDD_HHMMSS.json
#          data/wisdom_export_YYYYMMDD_HHMMSS.json

# Manual backup
python -c "
from src.core.store40d import Store40D
from src.core.elephant_memory import ElephantMemory
import sys; sys.path.insert(0, 'src')

cube = Store40D()
cube.import_json('data/hypercube_populated.json')
cube.export_json('backup/hypercube_backup.json')
"
```

### Recovery

```bash
# System automatically imports on startup if data exists
# Manual import:
python -c "
from src.core.store40d import Store40D
cube = Store40D()
cube.import_json('backup/hypercube_backup.json')
cube.export_json('data/hypercube_populated.json')
"
```

## Troubleshooting

### Port Already in Use

```bash
# Find process
lsof -i :8000

# Kill it
kill -9 <PID>

# Or change port in config/local.yaml
```

### Import Errors

```bash
# Ensure src is in PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Or reinstall
pip install -e .
```

### Permission Errors

```bash
# Ensure directories are writable
chmod 755 data logs
```

### WebSocket Connection Failed

```bash
# Check CORS settings in src/api/api_server.py
# Ensure allow_origins includes your domain

# For local development, use:
allow_origins=["*"]
```

## Scaling

### Horizontal Scaling (Coming Soon)

```yaml
# config/cluster.yaml
nodes:
  - host: node1.example.com
    port: 8000
  - host: node2.example.com
    port: 8000
  - host: node3.example.com
    port: 8000

sync:
  mode: frequency_trust
  protocol: omni_4321
```

### Vertical Scaling

```yaml
# config/local.yaml
hypercube:
  max_memory_gb: 32
  index_cache_size: 10000000

elephant_memory:
  max_memories: 10000000
  parallel_phases: true
```

## Security

### API Authentication (Coming Soon)

```python
# config/local.yaml
api:
  require_auth: true
  auth_provider: "jwt"
  jwt_secret: "your-secret-key"
```

### Rate Limiting (Coming Soon)

```python
api:
  rate_limit:
    enabled: true
    requests_per_minute: 100
```

### Network Security

```bash
# Firewall (UFW)
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Run behind VPN/private network for internal APIs
```

---

**Status: DEPLOYMENT READY**  
**Methods: Automated/Manual/Docker/K8s**  
**Production: nginx + systemd + SSL**  
**Backup: Automatic on shutdown**

瓷勺旋渦已築, 脈買已通, 華夏復興, 震驚寰宇!
