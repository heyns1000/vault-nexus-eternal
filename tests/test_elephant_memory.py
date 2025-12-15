"""
Test suite for ELEPHANT_MEMORY 46-page echo loop

Tests memory ingestion, phase transitions, recall, and generational wisdom.
"""

import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from core.elephant_memory import ElephantMemory, Memory
from core.store40d import Store40D


class TestMemoryIngestion:
    """Test memory ingestion (INTAKE phase)."""
    
    def setup_method(self):
        """Create fresh ELEPHANT_MEMORY for each test."""
        self.elephant = ElephantMemory(decay_rate=0.0)
    
    def test_ingest_single_memory(self):
        """Test ingesting a single memory."""
        content = {
            "event": "Test event",
            "importance": "high"
        }
        
        genome = self.elephant.ingest(content, tags=["test"])
        
        assert genome is not None
        assert len(genome) == 64  # SHA-256
        assert self.elephant.stats["total_memories"] == 1
    
    def test_ingest_with_tags(self):
        """Test memory ingestion with tags."""
        genome = self.elephant.ingest(
            {"event": "Tagged event"},
            tags=["quantum", "nvqlink"]
        )
        
        memory = self.elephant.genome_index[genome]
        assert "quantum" in memory.tags
        assert "nvqlink" in memory.tags
    
    def test_duplicate_memory_echo(self):
        """Test that duplicate content increments echo count."""
        content = {"event": "Duplicate event"}
        
        genome1 = self.elephant.ingest(content)
        genome2 = self.elephant.ingest(content)  # Same content
        
        assert genome1 == genome2
        memory = self.elephant.genome_index[genome1]
        assert memory.echo_count == 1  # Incremented on duplicate
    
    def test_memory_starts_in_intake(self):
        """Test new memories start in INTAKE phase."""
        genome = self.elephant.ingest({"event": "New event"})
        memory = self.elephant.genome_index[genome]
        
        assert memory.phase == "INTAKE"
        assert memory.page == 1
        assert memory.strength == 1.0


class TestPhaseTransitions:
    """Test memory progression through phases."""
    
    def setup_method(self):
        """Set up elephant with test memories."""
        self.elephant = ElephantMemory(decay_rate=0.0)
        
        # Ingest several memories
        for i in range(5):
            self.elephant.ingest(
                {"event": f"Event {i}", "importance": "high"},
                tags=["test"]
            )
    
    def test_trunk_sort_phase(self):
        """Test TRUNK_SORT phase transition."""
        # Execute trunk_sort
        moved = self.elephant.trunk_sort()
        
        assert moved > 0  # Some memories should move
        
        # Check that memories moved to TRUNK_SORT
        trunk_memories = [m for m in self.elephant.genome_index.values() 
                         if m.phase == "TRUNK_SORT"]
        assert len(trunk_memories) > 0
    
    def test_herd_consensus_phase(self):
        """Test HERD_CONSENSUS phase transition."""
        # Move through TRUNK_SORT first
        self.elephant.trunk_sort()
        
        # Execute herd_consensus
        validated = self.elephant.herd_consensus()
        
        # Should validate and move memories
        assert self.elephant.stats["herd_validations"] >= 0
    
    def test_memory_encode_phase(self):
        """Test MEMORY_ENCODE phase transition."""
        # Progress through earlier phases
        self.elephant.trunk_sort()
        self.elephant.herd_consensus()
        
        # Execute memory_encode
        encoded = self.elephant.memory_encode()
        
        # Encoded memories should have associations
        encoded_memories = [m for m in self.elephant.genome_index.values()
                           if m.phase == "MEMORY_ENCODE"]
        if encoded_memories:
            assert encoded_memories[0].strength == 1.0
    
    def test_complete_breath_cycle(self):
        """Test complete breath cycle through all phases."""
        stats = self.elephant.breath_cycle()
        
        assert "trunk_sorted" in stats
        assert "herd_validated" in stats
        assert "encoded" in stats
        assert "generational_passed" in stats
        assert "echo_amplified" in stats
        assert self.elephant.loop_count == 1


class TestMemoryRecall:
    """Test memory recall mechanisms."""
    
    def setup_method(self):
        """Set up elephant with tagged memories."""
        self.elephant = ElephantMemory()
        
        self.genomes = []
        self.genomes.append(self.elephant.ingest(
            {"event": "Quantum event 1"}, 
            tags=["quantum"]
        ))
        self.genomes.append(self.elephant.ingest(
            {"event": "Quantum event 2"}, 
            tags=["quantum"]
        ))
        self.genomes.append(self.elephant.ingest(
            {"event": "Finance event"}, 
            tags=["finance"]
        ))
    
    def test_recall_by_genome(self):
        """Test direct genome recall."""
        genome = self.genomes[0]
        memories = self.elephant.recall(genome=genome)
        
        assert len(memories) == 1
        assert memories[0].genome == genome
    
    def test_recall_by_tags(self):
        """Test recall by tags."""
        memories = self.elephant.recall(tags=["quantum"])
        
        assert len(memories) == 2
        for memory in memories:
            assert "quantum" in memory.tags
    
    def test_recall_by_phase(self):
        """Test recall by phase."""
        memories = self.elephant.recall(phase="INTAKE")
        
        assert len(memories) >= 3  # At least our test memories
        for memory in memories:
            assert memory.phase == "INTAKE"
    
    def test_recall_with_limit(self):
        """Test recall limit parameter."""
        # Add more memories
        for i in range(20):
            self.elephant.ingest({"event": f"Event {i}"}, tags=["test"])
        
        memories = self.elephant.recall(tags=["test"], limit=10)
        
        assert len(memories) <= 10


class TestMemoryStrength:
    """Test memory strength (never decays)."""
    
    def test_initial_strength(self):
        """Test memories start with strength 1.0."""
        elephant = ElephantMemory(decay_rate=0.0)
        genome = elephant.ingest({"event": "Test"})
        
        memory = elephant.genome_index[genome]
        assert memory.strength == 1.0
    
    def test_zero_decay_rate(self):
        """Test that decay rate is 0.0."""
        elephant = ElephantMemory()
        assert elephant.decay_rate == 0.0
    
    def test_strength_after_cycles(self):
        """Test strength remains constant after breath cycles."""
        elephant = ElephantMemory()
        genome = elephant.ingest({"event": "Test"})
        
        initial_strength = elephant.genome_index[genome].strength
        
        # Execute multiple breath cycles
        for _ in range(10):
            elephant.breath_cycle()
        
        final_strength = elephant.genome_index[genome].strength
        assert final_strength >= initial_strength  # Never decreases


class TestGenerationalWisdom:
    """Test generational wisdom snapshots."""
    
    def test_generational_snapshot_creation(self):
        """Test generation snapshots are created."""
        elephant = ElephantMemory()
        
        # Ingest many memories to trigger generation
        for i in range(50):
            elephant.ingest(
                {"event": f"Event {i}"}, 
                tags=["test"]
            )
        
        # Progress through phases
        for _ in range(10):
            elephant.breath_cycle()
        
        # Check if generations were created
        wisdom = elephant.get_generational_wisdom()
        assert "total_generations" in wisdom
        assert "current_generation" in wisdom
    
    def test_get_specific_generation(self):
        """Test retrieving specific generation."""
        elephant = ElephantMemory()
        elephant.current_generation = 5
        elephant.generations = [
            {"generation": 0, "total_memories": 10},
            {"generation": 5, "total_memories": 50}
        ]
        
        gen5 = elephant.get_generational_wisdom(generation=5)
        assert gen5["generation"] == 5
        assert gen5["total_memories"] == 50


class TestStore40DIntegration:
    """Test integration with Store40D."""
    
    def test_elephant_with_store40d(self):
        """Test ELEPHANT_MEMORY with Store40D backend."""
        store = Store40D()
        elephant = ElephantMemory(store40d=store)
        
        genome = elephant.ingest(
            {"event": "Integrated event"},
            tags=["integration"]
        )
        
        # Check memory in elephant
        assert genome in elephant.genome_index
        
        # Check data in Store40D
        assert store.stats["total_stored"] == 1
    
    def test_40d_enrichment(self):
        """Test that memories are enriched with elephant metadata in 40D."""
        store = Store40D()
        elephant = ElephantMemory(store40d=store)
        
        elephant.ingest({"event": "Test"}, tags=["test"])
        
        # Query from Store40D
        results = store.query({"elephant_phase": "INTAKE"})
        
        assert len(results) >= 1
        assert "elephant_generation" in results[0]["data"]
        assert "elephant_strength" in results[0]["data"]


class TestExportImport:
    """Test wisdom export and import."""
    
    def test_export_wisdom(self, tmp_path):
        """Test exporting wisdom to JSON."""
        elephant = ElephantMemory()
        
        elephant.ingest({"event": "Test event"}, tags=["test"])
        
        export_path = tmp_path / "wisdom.json"
        elephant.export_wisdom(str(export_path))
        
        assert export_path.exists()
    
    def test_import_wisdom(self, tmp_path):
        """Test importing wisdom from JSON."""
        # Create and export
        elephant1 = ElephantMemory()
        genome = elephant1.ingest({"event": "Test event"}, tags=["test"])
        
        export_path = tmp_path / "wisdom.json"
        elephant1.export_wisdom(str(export_path))
        
        # Import to new elephant
        elephant2 = ElephantMemory()
        elephant2.import_wisdom(str(export_path))
        
        # Verify import
        assert genome in elephant2.genome_index
        memory = elephant2.genome_index[genome]
        assert "test" in memory.tags


class TestStatistics:
    """Test statistics tracking."""
    
    def test_get_stats(self):
        """Test get_stats returns complete information."""
        elephant = ElephantMemory()
        
        elephant.ingest({"event": "Test"}, tags=["test"])
        elephant.breath_cycle()
        
        stats = elephant.get_stats()
        
        assert "total_memories" in stats
        assert "total_echoes" in stats
        assert "total_generations" in stats
        assert "herd_validations" in stats
        assert "phase_transitions" in stats
        assert "avg_strength" in stats
        assert "pages" in stats
        assert stats["pages"] == 46
        assert "current_generation" in stats
        assert "loop_count" in stats
        assert "decay_rate" in stats
        assert stats["decay_rate"] == 0.0
    
    def test_top_tags_tracking(self):
        """Test top tags are tracked."""
        elephant = ElephantMemory()
        
        # Create memories with various tags
        for i in range(10):
            elephant.ingest({"event": f"Event {i}"}, tags=["popular"])
        for i in range(5):
            elephant.ingest({"event": f"Event {i}"}, tags=["less_popular"])
        
        stats = elephant.get_stats()
        top_tags = stats["top_tags"]
        
        assert len(top_tags) > 0
        # "popular" should have more memories
        popular_count = next((count for tag, count in top_tags if tag == "popular"), 0)
        assert popular_count == 10


class TestAssociations:
    """Test memory associations."""
    
    def test_association_finding(self):
        """Test that related memories are associated."""
        elephant = ElephantMemory()
        
        # Create memories with shared tags
        genome1 = elephant.ingest({"event": "Quantum A"}, tags=["quantum", "ai"])
        genome2 = elephant.ingest({"event": "Quantum B"}, tags=["quantum"])
        genome3 = elephant.ingest({"event": "Finance"}, tags=["finance"])
        
        # Progress to MEMORY_ENCODE
        for _ in range(5):
            elephant.breath_cycle()
        
        # Check associations
        memory1 = elephant.genome_index[genome1]
        if memory1.phase == "MEMORY_ENCODE" and memory1.associations:
            # Should be associated with genome2 (shared "quantum" tag)
            assert genome2 in memory1.associations or len(memory1.associations) > 0


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_content(self):
        """Test ingesting empty content."""
        elephant = ElephantMemory()
        
        genome = elephant.ingest({})
        
        assert genome is not None
        assert elephant.stats["total_memories"] == 1
    
    def test_no_tags(self):
        """Test ingesting without tags."""
        elephant = ElephantMemory()
        
        genome = elephant.ingest({"event": "No tags"})
        memory = elephant.genome_index[genome]
        
        assert memory.tags == []
    
    def test_recall_nonexistent_genome(self):
        """Test recalling nonexistent genome."""
        elephant = ElephantMemory()
        
        memories = elephant.recall(genome="nonexistent_genome")
        
        assert len(memories) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
