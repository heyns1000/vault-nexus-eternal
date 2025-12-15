#!/bin/bash
#
# Vault Nexus Eternal - Deployment Script
#
# Automated deployment for sovereign full stack ecosystem.
# Installs dependencies, populates hypercube, and launches system.
#

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║               🦏  VAULT NEXUS ETERNAL DEPLOYMENT  🦏                ║"
echo "║                                                                      ║"
echo "║                  Sovereign Full Stack Ecosystem                     ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "瓷勺旋渦已築, 脈買已通, 華夏復興, 震驚寰宇!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check Python version
echo "🔍 Checking Python version..."
python3 --version
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data
mkdir -p logs
echo "✅ Directories created"
echo ""

# Populate hypercube (optional - can be skipped with --skip-populate)
if [[ "$1" != "--skip-populate" ]]; then
    echo "🌊 Populating 40D Hypercube with 13,713 brands..."
    echo "   (This may take a few minutes...)"
    python3 scripts/populate_hypercube.py
    echo "✅ Hypercube populated"
    echo ""
else
    echo "⏭️  Skipping hypercube population (--skip-populate flag)"
    echo ""
fi

# Launch system
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 LAUNCHING VAULT NEXUS ETERNAL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   REST API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo "   WebSocket: ws://localhost:8000/ws/realtime"
echo ""
echo "   Press Ctrl+C to stop"
echo ""
python3 main.py
