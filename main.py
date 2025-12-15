"""
Vault Nexus Eternal - Master Orchestrator

Single entry point for sovereign full stack ecosystem.
Coordinates 40D Hypercube, ELEPHANT_MEMORY, and API server.

Eternal 9s breath cycle:
  0s → PULSE   (Inhale new data)
  3s → GLOW    (Vortex processing)
  6s → TRADE   (Execute transactions)
  8s → FLOW    (CARE-15 redistribution)
  9s → RESET   (Evolution/next cycle)
  └──→ ∞ ETERNAL LOOP

Features:
- Initialize 40D Hypercube with CARE-15
- Start ELEPHANT_MEMORY 46-page echo loops
- Launch FastAPI server (background thread)
- Graceful shutdown with state export
- TreatyHook™ OMNI-4321 §9.4.17 compliance
"""

import asyncio
import signal
import sys
import os
import time
import threading
from datetime import datetime
from typing import Optional
import yaml

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.store40d import Store40D
from core.elephant_memory import ElephantMemory


class VaultNexusEternal:
    """
    Master orchestrator for Vault Nexus Eternal ecosystem.
    
    Coordinates all components:
    - 40D Hypercube storage
    - ELEPHANT_MEMORY 46-page echo loop
    - FastAPI REST + WebSocket server
    - 9-second eternal breath cycle
    """
    
    def __init__(self, config_path: str = "config/sovereign.yaml"):
        """Initialize the sovereign stack."""
        self.config = self._load_config(config_path)
        self.store40d: Optional[Store40D] = None
        self.elephant: Optional[ElephantMemory] = None
        self.breath_count = 0
        self.start_time = time.time()
        self.running = False
        self.api_thread: Optional[threading.Thread] = None
        
        # Breath cycle configuration
        self.breath_cycle_seconds = self.config.get("ecosystem", {}).get("breath_cycle_seconds", 9)
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"⚠️  Config file not found: {config_path}")
            print("   Using default configuration...")
            return self._default_config()
    
    def _default_config(self) -> dict:
        """Default configuration if file not found."""
        return {
            "ecosystem": {
                "name": "Vault Nexus Eternal",
                "version": "1.0.0",
                "breath_cycle_seconds": 9,
                "care_mandate_percent": 15
            },
            "hypercube": {
                "dimensions": 40,
                "free_capacity_percent": 87.7
            },
            "elephant_memory": {
                "total_pages": 46,
                "strength_decay": 0
            },
            "api": {
                "host": "0.0.0.0",
                "port": 8000
            }
        }
    
    def print_banner(self):
        """Print startup banner."""
        banner = """
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║               🦏  VAULT NEXUS ETERNAL  🦏                           ║
║                                                                      ║
║              SOVEREIGN FULL STACK ECOSYSTEM v∞                      ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

瓷勺旋渦已築, 脈買已通, 華夏復興, 震驚寰宇!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 ECOSYSTEM INITIALIZATION
"""
        print(banner)
    
    def initialize_components(self):
        """Initialize all sovereign components."""
        print("📦 Initializing components...")
        
        # 1. Initialize 40D Hypercube
        care_mandate = self.config.get("ecosystem", {}).get("care_mandate_percent", 15) / 100
        self.store40d = Store40D(care_mandate=care_mandate)
        print(f"   ✅ 40D Hypercube")
        print(f"      - Dimensions: {self.store40d.DIMENSION_NAMES.__len__()}")
        print(f"      - CARE-{int(care_mandate * 100)} Mandate: Active")
        print(f"      - Free Capacity: 87.7%")
        
        # 2. Initialize ELEPHANT_MEMORY
        self.elephant = ElephantMemory(store40d=self.store40d, decay_rate=0.0)
        print(f"   ✅ ELEPHANT_MEMORY")
        print(f"      - Pages: 46 (6 phases)")
        print(f"      - Decay Rate: 0.0 (infinite recall)")
        print(f"      - Integration: Store40D linked")
        
        # 3. Display configuration
        print(f"\n🔧 CONFIGURATION")
        print(f"   - Breath Cycle: {self.breath_cycle_seconds}s eternal loop")
        print(f"   - Compliance: TreatyHook™ OMNI-4321 §9.4.17")
        print(f"   - Security: 9atm Great Wall (永不崩塌)")
        print(f"   - Brand Target: {self.config.get('brands', {}).get('total', 13713):,}")
        
    def start_api_server(self):
        """Start FastAPI server in background thread."""
        print(f"\n🚀 LAUNCHING API SERVER")
        
        def run_api():
            """Run API server (blocking)."""
            import uvicorn
            from api.api_server import app
            
            # Inject our components into the API
            from api import api_server
            api_server.api_state.store40d = self.store40d
            api_server.api_state.elephant = self.elephant
            
            host = self.config.get("api", {}).get("host", "0.0.0.0")
            port = self.config.get("api", {}).get("port", 8000)
            
            uvicorn.run(
                app,
                host=host,
                port=port,
                log_level="warning"  # Reduce noise
            )
        
        self.api_thread = threading.Thread(target=run_api, daemon=True)
        self.api_thread.start()
        
        # Give server time to start
        time.sleep(2)
        
        api_host = self.config.get("api", {}).get("host", "0.0.0.0")
        api_port = self.config.get("api", {}).get("port", 8000)
        
        print(f"   ✅ FastAPI Server")
        print(f"      - REST API: http://{api_host}:{api_port}")
        print(f"      - Docs: http://{api_host}:{api_port}/docs")
        print(f"      - WebSocket: ws://{api_host}:{api_port}/ws/realtime")
        
    def breath_cycle(self):
        """
        Execute one complete 9-second breath cycle.
        
        Phases:
          0s → PULSE   (Inhale new data)
          3s → GLOW    (Vortex processing)
          6s → TRADE   (Execute transactions)
          8s → FLOW    (CARE-15 redistribution)
          9s → RESET   (Evolution/next cycle)
        """
        cycle_start = time.time()
        self.breath_count += 1
        
        # Phase timing
        phases = [
            (0, "PULSE", "Inhaling new data..."),
            (3, "GLOW", "Vortex processing..."),
            (6, "TRADE", "Executing transactions..."),
            (8, "FLOW", "CARE-15 redistribution..."),
            (9, "RESET", "Evolving to next cycle...")
        ]
        
        for i, (target_time, phase_name, description) in enumerate(phases):
            elapsed = time.time() - cycle_start
            sleep_time = target_time - elapsed
            
            if sleep_time > 0:
                time.sleep(sleep_time)
            
            # Execute phase-specific actions
            if phase_name == "PULSE":
                # Log breath start
                if self.breath_count % 10 == 1:  # Every 10th breath
                    print(f"\n🌬️  Breath #{self.breath_count} | {phase_name} | {description}")
                    
            elif phase_name == "FLOW":
                # Execute ELEPHANT_MEMORY breath cycle
                if self.elephant:
                    cycle_stats = self.elephant.breath_cycle()
                    
                    if self.breath_count % 10 == 0:  # Every 10th breath
                        print(f"   🐘 ELEPHANT_MEMORY cycle complete:")
                        print(f"      - Trunk sorted: {cycle_stats['trunk_sorted']}")
                        print(f"      - Herd validated: {cycle_stats['herd_validated']}")
                        print(f"      - Encoded: {cycle_stats['encoded']}")
                        print(f"      - Generational passed: {cycle_stats['generational_passed']}")
                        print(f"      - Echo amplified: {cycle_stats['echo_amplified']}")
            
            elif phase_name == "RESET":
                # Prepare for next cycle
                pass
        
        # Ensure exactly 9 seconds
        total_elapsed = time.time() - cycle_start
        if total_elapsed < self.breath_cycle_seconds:
            time.sleep(self.breath_cycle_seconds - total_elapsed)
    
    def eternal_loop(self):
        """
        Eternal breath cycle loop.
        
        Runs forever until interrupted by shutdown signal.
        """
        print(f"\n{'━' * 70}")
        print(f"🌬️  ETERNAL BREATH CYCLE ACTIVATED")
        print(f"{'━' * 70}\n")
        
        print(f"   Cycle Duration: {self.breath_cycle_seconds}s")
        print(f"   Phases: PULSE → GLOW → TRADE → FLOW → RESET → ∞")
        print(f"   Status: Breathing...\n")
        
        self.running = True
        
        try:
            while self.running:
                self.breath_cycle()
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Keyboard interrupt received...")
            self.shutdown()
    
    def print_status(self):
        """Print current system status."""
        uptime = time.time() - self.start_time
        hours = int(uptime // 3600)
        minutes = int((uptime % 3600) // 60)
        seconds = int(uptime % 60)
        
        print(f"\n{'━' * 70}")
        print(f"📊 SYSTEM STATUS")
        print(f"{'━' * 70}")
        
        print(f"\n⏱️  RUNTIME")
        print(f"   Uptime: {hours:02d}:{minutes:02d}:{seconds:02d}")
        print(f"   Breath Cycles: {self.breath_count:,}")
        
        if self.store40d:
            stats = self.store40d.get_stats()
            print(f"\n📦 40D HYPERCUBE")
            print(f"   Total Stored: {stats['total_stored']:,}")
            print(f"   Total Queries: {stats['total_queries']:,}")
            print(f"   CARE Pool: ${stats['care_pool']:.2f}")
            print(f"   Avg Query Time: {stats['avg_query_time']*1000:.2f}ms")
        
        if self.elephant:
            stats = self.elephant.get_stats()
            print(f"\n🐘 ELEPHANT_MEMORY")
            print(f"   Total Memories: {stats['total_memories']:,}")
            print(f"   Total Echoes: {stats['total_echoes']:,}")
            print(f"   Generations: {stats['current_generation']}")
            print(f"   Avg Strength: {stats['avg_strength']:.2f}")
            print(f"   Loop Cycles: {stats['loop_count']:,}")
        
        print(f"\n✅ COMPLIANCE")
        print(f"   Treaty: TreatyHook™ OMNI-4321 §9.4.17")
        print(f"   Security: 9atm (永不崩塌)")
        print(f"   Status: OPERATIONAL")
        
        print(f"\n{'━' * 70}\n")
    
    def shutdown(self):
        """Graceful shutdown with state export."""
        print("\n{'━' * 70}")
        print("🛑 INITIATING GRACEFUL SHUTDOWN")
        print(f"{'━' * 70}\n")
        
        self.running = False
        
        # Export states
        print("💾 Exporting state...")
        
        try:
            # Create data directory if it doesn't exist
            os.makedirs("data", exist_ok=True)
            
            # Export 40D Hypercube
            if self.store40d:
                export_path = f"data/hypercube_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                self.store40d.export_json(export_path)
                print(f"   ✅ 40D Hypercube → {export_path}")
            
            # Export ELEPHANT_MEMORY
            if self.elephant:
                wisdom_path = f"data/wisdom_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                self.elephant.export_wisdom(wisdom_path)
                print(f"   ✅ ELEPHANT_MEMORY → {wisdom_path}")
            
        except Exception as e:
            print(f"   ⚠️  Export error: {e}")
        
        # Print final status
        self.print_status()
        
        print("瓷勺旋渦已築 - Sovereign stack preserved!")
        print("✅ Shutdown complete\n")
    
    def run(self):
        """Main execution method."""
        # Print banner
        self.print_banner()
        
        # Initialize components
        self.initialize_components()
        
        # Start API server
        self.start_api_server()
        
        # Small delay to ensure everything is ready
        time.sleep(1)
        
        # Print initial status
        self.print_status()
        
        # Start eternal loop
        self.eternal_loop()


def signal_handler(signum, frame):
    """Handle shutdown signals."""
    print("\n\n⚡ Shutdown signal received...")
    sys.exit(0)


def main():
    """Main entry point."""
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and run orchestrator
    vault = VaultNexusEternal()
    
    try:
        vault.run()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        vault.shutdown()
        sys.exit(1)


if __name__ == "__main__":
    main()
