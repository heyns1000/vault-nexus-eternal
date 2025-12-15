"""
ELEPHANT_MEMORY - 46-Page Echo Loop System

Bio-inspired infinite recall system based on elephant matriarch memory.
Memories never decay, wisdom passes through generations.

6 Phases across 46 Pages:
1. INTAKE (Pages 1-8): Sensory absorption
2. TRUNK_SORT (Pages 9-16): Categorization and prioritization
3. HERD_CONSENSUS (Pages 17-24): Social validation
4. MEMORY_ENCODE (Pages 25-32): Deep embedding
5. GENERATIONAL_PASS (Pages 33-40): Wisdom transfer
6. ECHO_AMPLIFY (Pages 41-46): Reinforcement and recall

Integration with Store40D for persistent storage.
Strength rating never decays (bio-inspired eternal memory).
"""

import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, deque
from dataclasses import dataclass, field, asdict
import hashlib


@dataclass
class Memory:
    """A single memory unit in the ELEPHANT_MEMORY system."""
    
    content: Dict[str, Any]
    timestamp: str
    genome: str
    strength: float = 1.0
    phase: str = "INTAKE"
    page: int = 1
    generation: int = 0
    herd_validations: int = 0
    echo_count: int = 0
    tags: List[str] = field(default_factory=list)
    associations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert memory to dictionary."""
        return asdict(self)


class ElephantMemory:
    """
    46-Page ELEPHANT_MEMORY Echo Loop System
    
    Bio-inspired infinite recall with generational wisdom transfer.
    Integrated with Store40D for persistent 40-dimensional storage.
    
    Key Features:
    - 46 pages organized into 6 phases
    - Memories never decay (strength remains constant)
    - Generational wisdom accumulation
    - Echo amplification for reinforcement
    - Herd consensus for social validation
    - Integration with 40D hypercube
    """
    
    TOTAL_PAGES = 46
    
    PHASES = {
        "INTAKE": list(range(1, 9)),           # Pages 1-8
        "TRUNK_SORT": list(range(9, 17)),      # Pages 9-16
        "HERD_CONSENSUS": list(range(17, 25)), # Pages 17-24
        "MEMORY_ENCODE": list(range(25, 33)),  # Pages 25-32
        "GENERATIONAL_PASS": list(range(33, 41)), # Pages 33-40
        "ECHO_AMPLIFY": list(range(41, 47))    # Pages 41-46
    }
    
    def __init__(self, store40d=None, decay_rate: float = 0.0):
        """
        Initialize ELEPHANT_MEMORY system.
        
        Args:
            store40d: Optional Store40D instance for persistent storage
            decay_rate: Memory decay rate (default 0.0 = never decays)
        """
        self.store40d = store40d
        self.decay_rate = decay_rate  # Bio-inspired: elephants never forget
        
        # Memory storage organized by pages
        self.pages: Dict[int, List[Memory]] = {i: [] for i in range(1, self.TOTAL_PAGES + 1)}
        
        # Index for fast lookup
        self.genome_index: Dict[str, Memory] = {}
        self.tag_index: Dict[str, List[str]] = defaultdict(list)
        
        # Generational wisdom archive
        self.generations: List[Dict[str, Any]] = []
        self.current_generation = 0
        
        # Statistics
        self.stats = {
            "total_memories": 0,
            "total_echoes": 0,
            "total_generations": 0,
            "herd_validations": 0,
            "phase_transitions": 0,
            "avg_strength": 1.0
        }
        
        # Echo loop state
        self.loop_active = False
        self.loop_count = 0
        self.last_breath = time.time()
        
    def _compute_genome(self, content: Dict[str, Any]) -> str:
        """Generate SHA-256 genome hash for memory content."""
        canonical = json.dumps(content, sort_keys=True)
        return hashlib.sha256(canonical.encode()).hexdigest()
    
    def ingest(self, content: Dict[str, Any], tags: Optional[List[str]] = None) -> str:
        """
        Ingest new memory through INTAKE phase (Pages 1-8).
        
        Args:
            content: Memory content as dictionary
            tags: Optional tags for categorization
            
        Returns:
            genome: SHA-256 hash identifier
        """
        # Compute genome
        genome = self._compute_genome(content)
        
        # Check if memory already exists
        if genome in self.genome_index:
            # Strengthen existing memory
            self.genome_index[genome].echo_count += 1
            self.stats["total_echoes"] += 1
            return genome
        
        # Create new memory
        memory = Memory(
            content=content,
            timestamp=datetime.utcnow().isoformat(),
            genome=genome,
            strength=1.0,
            phase="INTAKE",
            page=1,
            generation=self.current_generation,
            tags=tags or [],
            associations=[]
        )
        
        # Store in first INTAKE page
        self.pages[1].append(memory)
        self.genome_index[genome] = memory
        
        # Update tag index
        for tag in memory.tags:
            self.tag_index[tag].append(genome)
        
        self.stats["total_memories"] += 1
        
        # Integrate with Store40D if available
        if self.store40d:
            self._store_in_40d(memory)
        
        return genome
    
    def _store_in_40d(self, memory: Memory):
        """Store memory in 40D hypercube for persistent storage."""
        if not self.store40d:
            return
        
        # Map memory to 40D coordinates
        data_40d = {
            **memory.content,
            "genome": memory.genome,
            "elephant_phase": memory.phase,
            "elephant_page": memory.page,
            "elephant_generation": memory.generation,
            "elephant_strength": memory.strength,
            "timestamp": memory.timestamp
        }
        
        self.store40d.store(data_40d)
    
    def trunk_sort(self):
        """
        TRUNK_SORT phase (Pages 9-16): Categorize and prioritize memories.
        
        Moves memories from INTAKE to TRUNK_SORT based on strength and relevance.
        """
        moved_count = 0
        
        # Process memories in INTAKE pages
        for intake_page in self.PHASES["INTAKE"]:
            memories_to_move = []
            
            for memory in self.pages[intake_page]:
                if memory.phase == "INTAKE":
                    # Evaluate for promotion to TRUNK_SORT
                    if memory.strength >= 0.5 or memory.echo_count > 0:
                        memory.phase = "TRUNK_SORT"
                        memory.page = 9  # First TRUNK_SORT page
                        memories_to_move.append(memory)
                        moved_count += 1
            
            # Move memories
            for memory in memories_to_move:
                self.pages[intake_page].remove(memory)
                self.pages[9].append(memory)
        
        if moved_count > 0:
            self.stats["phase_transitions"] += moved_count
        
        return moved_count
    
    def herd_consensus(self):
        """
        HERD_CONSENSUS phase (Pages 17-24): Social validation of memories.
        
        Simulates elephant herd validation where memories are strengthened
        through social reinforcement.
        """
        validated_count = 0
        
        # Process memories in TRUNK_SORT pages
        for trunk_page in self.PHASES["TRUNK_SORT"]:
            memories_to_validate = []
            
            for memory in self.pages[trunk_page]:
                if memory.phase == "TRUNK_SORT":
                    # Simulate herd validation
                    memory.herd_validations += 1
                    
                    # Strengthen based on validation
                    if memory.herd_validations >= 2:
                        memory.phase = "HERD_CONSENSUS"
                        memory.page = 17  # First HERD_CONSENSUS page
                        memory.strength = min(1.0, memory.strength + 0.1)
                        memories_to_validate.append(memory)
                        validated_count += 1
                        self.stats["herd_validations"] += 1
            
            # Move memories
            for memory in memories_to_validate:
                self.pages[trunk_page].remove(memory)
                self.pages[17].append(memory)
        
        return validated_count
    
    def memory_encode(self):
        """
        MEMORY_ENCODE phase (Pages 25-32): Deep embedding of validated memories.
        
        Creates permanent encoding with associations and connections.
        """
        encoded_count = 0
        
        # Process memories in HERD_CONSENSUS pages
        for consensus_page in self.PHASES["HERD_CONSENSUS"]:
            memories_to_encode = []
            
            for memory in self.pages[consensus_page]:
                if memory.phase == "HERD_CONSENSUS":
                    # Deep encoding: find associations
                    associations = self._find_associations(memory)
                    memory.associations = associations
                    
                    # Promote to MEMORY_ENCODE
                    memory.phase = "MEMORY_ENCODE"
                    memory.page = 25  # First MEMORY_ENCODE page
                    memory.strength = 1.0  # Full strength after encoding
                    memories_to_encode.append(memory)
                    encoded_count += 1
            
            # Move memories
            for memory in memories_to_encode:
                self.pages[consensus_page].remove(memory)
                self.pages[25].append(memory)
        
        return encoded_count
    
    def _find_associations(self, memory: Memory, max_associations: int = 5) -> List[str]:
        """Find associated memories based on content similarity and tags."""
        associations = []
        
        # Find memories with overlapping tags
        for tag in memory.tags:
            related_genomes = self.tag_index.get(tag, [])
            for genome in related_genomes:
                if genome != memory.genome and genome not in associations:
                    associations.append(genome)
                    if len(associations) >= max_associations:
                        break
            if len(associations) >= max_associations:
                break
        
        return associations
    
    def generational_pass(self):
        """
        GENERATIONAL_PASS phase (Pages 33-40): Transfer wisdom to next generation.
        
        Creates generational wisdom snapshots for long-term preservation.
        """
        passed_count = 0
        
        # Process memories in MEMORY_ENCODE pages
        for encode_page in self.PHASES["MEMORY_ENCODE"]:
            memories_to_pass = []
            
            for memory in self.pages[encode_page]:
                if memory.phase == "MEMORY_ENCODE":
                    # Promote to GENERATIONAL_PASS
                    memory.phase = "GENERATIONAL_PASS"
                    memory.page = 33  # First GENERATIONAL_PASS page
                    memories_to_pass.append(memory)
                    passed_count += 1
            
            # Move memories
            for memory in memories_to_pass:
                self.pages[encode_page].remove(memory)
                self.pages[33].append(memory)
        
        # Create generational snapshot if enough memories passed
        if passed_count > 10:
            self._create_generation_snapshot()
        
        return passed_count
    
    def _create_generation_snapshot(self):
        """Create a snapshot of current generation wisdom."""
        generation_wisdom = {
            "generation": self.current_generation,
            "timestamp": datetime.utcnow().isoformat(),
            "total_memories": self.stats["total_memories"],
            "avg_strength": self._calculate_avg_strength(),
            "top_tags": self._get_top_tags(10),
            "memory_count_by_phase": self._count_by_phase()
        }
        
        self.generations.append(generation_wisdom)
        self.current_generation += 1
        self.stats["total_generations"] += 1
    
    def echo_amplify(self):
        """
        ECHO_AMPLIFY phase (Pages 41-46): Reinforce and amplify memories.
        
        Final phase that strengthens memories through echo reinforcement.
        """
        amplified_count = 0
        
        # Process memories in GENERATIONAL_PASS pages
        for gen_page in self.PHASES["GENERATIONAL_PASS"]:
            memories_to_amplify = []
            
            for memory in self.pages[gen_page]:
                if memory.phase == "GENERATIONAL_PASS":
                    # Amplify through echo
                    memory.echo_count += 1
                    memory.phase = "ECHO_AMPLIFY"
                    memory.page = 41  # First ECHO_AMPLIFY page
                    memories_to_amplify.append(memory)
                    amplified_count += 1
                    self.stats["total_echoes"] += 1
            
            # Move memories
            for memory in memories_to_amplify:
                self.pages[gen_page].remove(memory)
                self.pages[41].append(memory)
        
        return amplified_count
    
    def breath_cycle(self):
        """
        Execute one complete breath cycle through all 6 phases.
        
        Returns:
            dict: Statistics from this breath cycle
        """
        cycle_stats = {
            "trunk_sorted": self.trunk_sort(),
            "herd_validated": self.herd_consensus(),
            "encoded": self.memory_encode(),
            "generational_passed": self.generational_pass(),
            "echo_amplified": self.echo_amplify()
        }
        
        self.loop_count += 1
        self.last_breath = time.time()
        
        return cycle_stats
    
    def recall(self, genome: Optional[str] = None, tags: Optional[List[str]] = None, 
               phase: Optional[str] = None, limit: int = 100) -> List[Memory]:
        """
        Recall memories based on criteria.
        
        Args:
            genome: Specific memory genome to recall
            tags: List of tags to filter by
            phase: Specific phase to filter by
            limit: Maximum number of memories to return
            
        Returns:
            List of matching memories
        """
        if genome:
            # Direct genome lookup
            memory = self.genome_index.get(genome)
            return [memory] if memory else []
        
        results = []
        
        # Collect all memories
        for page_memories in self.pages.values():
            for memory in page_memories:
                # Filter by tags
                if tags and not any(tag in memory.tags for tag in tags):
                    continue
                
                # Filter by phase
                if phase and memory.phase != phase:
                    continue
                
                results.append(memory)
                
                if len(results) >= limit:
                    break
            
            if len(results) >= limit:
                break
        
        # Sort by strength and echo count
        results.sort(key=lambda m: (m.strength, m.echo_count), reverse=True)
        
        return results[:limit]
    
    def get_generational_wisdom(self, generation: Optional[int] = None) -> Dict[str, Any]:
        """
        Retrieve generational wisdom archive.
        
        Args:
            generation: Specific generation number (None for all)
            
        Returns:
            Wisdom data for requested generation(s)
        """
        if generation is not None:
            for gen_data in self.generations:
                if gen_data["generation"] == generation:
                    return gen_data
            return {}
        
        return {
            "total_generations": len(self.generations),
            "current_generation": self.current_generation,
            "generations": self.generations
        }
    
    def _calculate_avg_strength(self) -> float:
        """Calculate average strength across all memories."""
        if self.stats["total_memories"] == 0:
            return 0.0
        
        total_strength = 0.0
        count = 0
        
        for page_memories in self.pages.values():
            for memory in page_memories:
                total_strength += memory.strength
                count += 1
        
        return total_strength / count if count > 0 else 0.0
    
    def _get_top_tags(self, limit: int = 10) -> List[Tuple[str, int]]:
        """Get most frequently used tags."""
        tag_counts = [(tag, len(genomes)) for tag, genomes in self.tag_index.items()]
        tag_counts.sort(key=lambda x: x[1], reverse=True)
        return tag_counts[:limit]
    
    def _count_by_phase(self) -> Dict[str, int]:
        """Count memories by phase."""
        counts = defaultdict(int)
        
        for page_memories in self.pages.values():
            for memory in page_memories:
                counts[memory.phase] += 1
        
        return dict(counts)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics."""
        return {
            **self.stats,
            "pages": self.TOTAL_PAGES,
            "current_generation": self.current_generation,
            "loop_count": self.loop_count,
            "avg_strength": self._calculate_avg_strength(),
            "memories_by_phase": self._count_by_phase(),
            "top_tags": self._get_top_tags(10),
            "decay_rate": self.decay_rate
        }
    
    def export_wisdom(self, filepath: str):
        """Export generational wisdom to JSON file."""
        export_data = {
            "metadata": {
                "exported_at": datetime.utcnow().isoformat(),
                "system": "ELEPHANT_MEMORY",
                "version": "1.0.0",
                "pages": self.TOTAL_PAGES
            },
            "stats": self.get_stats(),
            "generations": self.generations,
            "memories": [memory.to_dict() for page_memories in self.pages.values() 
                        for memory in page_memories]
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
    
    def import_wisdom(self, filepath: str):
        """Import generational wisdom from JSON file."""
        with open(filepath, 'r') as f:
            import_data = json.load(f)
        
        # Restore generations
        self.generations = import_data.get("generations", [])
        
        # Restore memories
        for memory_dict in import_data.get("memories", []):
            memory = Memory(**memory_dict)
            self.pages[memory.page].append(memory)
            self.genome_index[memory.genome] = memory
            
            for tag in memory.tags:
                self.tag_index[tag].append(memory.genome)


# Example usage
if __name__ == "__main__":
    print("🐘 ELEPHANT_MEMORY - 46-Page Echo Loop - Initializing...")
    
    # Create ELEPHANT_MEMORY system
    elephant = ElephantMemory(decay_rate=0.0)
    
    # Ingest some sample memories
    memories = [
        {"event": "NVQLink announced", "importance": "critical", "category": "quantum"},
        {"event": "CARE-15 mandate activated", "importance": "high", "category": "compliance"},
        {"event": "40D Hypercube deployed", "importance": "critical", "category": "technical"}
    ]
    
    for mem_content in memories:
        genome = elephant.ingest(mem_content, tags=[mem_content.get("category", "general")])
        print(f"✅ Ingested memory: {genome[:16]}... ({mem_content.get('event', 'unknown')})")
    
    # Execute breath cycle
    print("\n🌬️ Executing breath cycle through all 6 phases...")
    cycle_stats = elephant.breath_cycle()
    print(f"   TRUNK_SORT: {cycle_stats['trunk_sorted']} memories")
    print(f"   HERD_CONSENSUS: {cycle_stats['herd_validated']} memories")
    print(f"   MEMORY_ENCODE: {cycle_stats['encoded']} memories")
    print(f"   GENERATIONAL_PASS: {cycle_stats['generational_passed']} memories")
    print(f"   ECHO_AMPLIFY: {cycle_stats['echo_amplified']} memories")
    
    # Recall memories
    recalled = elephant.recall(tags=["quantum"])
    print(f"\n🧠 Recalled {len(recalled)} quantum-related memories")
    
    # Statistics
    stats = elephant.get_stats()
    print(f"\n📊 Statistics:")
    print(f"   Total memories: {stats['total_memories']}")
    print(f"   Total echoes: {stats['total_echoes']}")
    print(f"   Current generation: {stats['current_generation']}")
    print(f"   Avg strength: {stats['avg_strength']:.2f} (never decays!)")
    
    print("\n瓷勺旋渦已築 - ELEPHANT_MEMORY operational! 🐘")
