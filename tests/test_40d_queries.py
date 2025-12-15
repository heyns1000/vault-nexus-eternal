"""
Test suite for 40D Hypercube queries

Tests multi-dimensional querying, operators, performance, and CARE-15 enforcement.
"""

import pytest
import sys
import os
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from core.store40d import Store40D


class TestBasicStorage:
    """Test basic storage operations."""
    
    def setup_method(self):
        """Create fresh hypercube for each test."""
        self.cube = Store40D(care_mandate=0.15)
    
    def test_store_single_brand(self):
        """Test storing a single brand."""
        data = {
            "sector": "quantum_ai",
            "brand": "TestBrand",
            "year": 2025,
            "quality_score": 0.95
        }
        
        genome = self.cube.store(data)
        
        assert genome is not None
        assert len(genome) == 64  # SHA-256 hex length
        assert self.cube.stats["total_stored"] == 1
    
    def test_store_multiple_brands(self):
        """Test storing multiple brands."""
        brands = [
            {"sector": "quantum_ai", "brand": "Brand1", "year": 2025},
            {"sector": "fintech", "brand": "Brand2", "year": 2024},
            {"sector": "healthtech", "brand": "Brand3", "year": 2025}
        ]
        
        for brand_data in brands:
            self.cube.store(brand_data)
        
        assert self.cube.stats["total_stored"] == 3
    
    def test_deduplication(self):
        """Test that identical data produces same genome."""
        data = {"sector": "quantum_ai", "brand": "TestBrand"}
        
        genome1 = self.cube.store(data)
        genome2 = self.cube.store(data)
        
        assert genome1 == genome2
        assert self.cube.stats["total_stored"] == 2  # Both stored but same genome


class TestExactMatchQueries:
    """Test exact match queries (== operator)."""
    
    def setup_method(self):
        """Set up test data."""
        self.cube = Store40D()
        
        # Store test brands
        self.brands = [
            {"sector": "quantum_ai", "brand": "QAI1", "year": 2025, "quality_score": 0.9},
            {"sector": "quantum_ai", "brand": "QAI2", "year": 2025, "quality_score": 0.85},
            {"sector": "fintech", "brand": "FIN1", "year": 2025, "quality_score": 0.95},
            {"sector": "quantum_ai", "brand": "QAI3", "year": 2024, "quality_score": 0.8},
        ]
        
        for brand in self.brands:
            self.cube.store(brand)
    
    def test_single_dimension_query(self):
        """Test query on single dimension."""
        results = self.cube.query({"sector": "quantum_ai"})
        
        assert len(results) == 3
        for result in results:
            assert result["data"]["sector"] == "quantum_ai"
    
    def test_multi_dimension_query(self):
        """Test query on multiple dimensions."""
        results = self.cube.query({
            "sector": "quantum_ai",
            "year": 2025
        })
        
        assert len(results) == 2
        for result in results:
            assert result["data"]["sector"] == "quantum_ai"
            assert result["data"]["year"] == 2025
    
    def test_no_matches(self):
        """Test query with no matches."""
        results = self.cube.query({"sector": "nonexistent"})
        
        assert len(results) == 0


class TestRangeQueries:
    """Test range queries (>, <, >=, <=)."""
    
    def setup_method(self):
        """Set up test data."""
        self.cube = Store40D()
        
        for i in range(10):
            self.cube.store({
                "sector": "test",
                "brand": f"Brand{i}",
                "quality_score": i * 0.1  # 0.0 to 0.9
            })
    
    def test_greater_than(self):
        """Test > operator."""
        results = self.cube.query(
            {"quality_score": 0.5},
            {"quality_score": ">"}
        )
        
        assert len(results) == 4  # 0.6, 0.7, 0.8, 0.9
        for result in results:
            assert result["data"]["quality_score"] > 0.5
    
    def test_greater_than_equal(self):
        """Test >= operator."""
        results = self.cube.query(
            {"quality_score": 0.5},
            {"quality_score": ">="}
        )
        
        assert len(results) == 5  # 0.5, 0.6, 0.7, 0.8, 0.9
        for result in results:
            assert result["data"]["quality_score"] >= 0.5
    
    def test_less_than(self):
        """Test < operator."""
        results = self.cube.query(
            {"quality_score": 0.5},
            {"quality_score": "<"}
        )
        
        assert len(results) == 5  # 0.0, 0.1, 0.2, 0.3, 0.4
        for result in results:
            assert result["data"]["quality_score"] < 0.5
    
    def test_less_than_equal(self):
        """Test <= operator."""
        results = self.cube.query(
            {"quality_score": 0.5},
            {"quality_score": "<="}
        )
        
        assert len(results) == 6  # 0.0, 0.1, 0.2, 0.3, 0.4, 0.5
        for result in results:
            assert result["data"]["quality_score"] <= 0.5


class TestInOperator:
    """Test 'in' operator for set membership."""
    
    def setup_method(self):
        """Set up test data."""
        self.cube = Store40D()
        
        sectors = ["quantum_ai", "fintech", "healthtech", "edtech"]
        for i, sector in enumerate(sectors):
            self.cube.store({
                "sector": sector,
                "brand": f"Brand{i}"
            })
    
    def test_in_operator(self):
        """Test 'in' operator."""
        results = self.cube.query(
            {"sector": ["quantum_ai", "fintech"]},
            {"sector": "in"}
        )
        
        assert len(results) == 2
        sectors = [r["data"]["sector"] for r in results]
        assert "quantum_ai" in sectors
        assert "fintech" in sectors
        assert "healthtech" not in sectors


class TestCARE15:
    """Test CARE-15 mandate enforcement."""
    
    def test_care_redistribution(self):
        """Test automatic CARE-15 redistribution."""
        cube = Store40D(care_mandate=0.15)
        
        cube.store({
            "brand": "TestBrand",
            "value": 1000.0
        })
        
        assert cube.care_pool == 150.0  # 15% of 1000
        assert cube.stats["care_redistributed"] == 150.0
    
    def test_care_accumulation(self):
        """Test CARE pool accumulates over multiple stores."""
        cube = Store40D(care_mandate=0.15)
        
        cube.store({"brand": "Brand1", "value": 1000.0})
        cube.store({"brand": "Brand2", "value": 2000.0})
        cube.store({"brand": "Brand3", "value": 500.0})
        
        expected_pool = (1000 + 2000 + 500) * 0.15
        assert cube.care_pool == expected_pool
    
    def test_no_value_no_care(self):
        """Test that entries without 'value' don't affect CARE pool."""
        cube = Store40D(care_mandate=0.15)
        
        cube.store({"brand": "TestBrand"})  # No 'value' field
        
        assert cube.care_pool == 0.0


class TestPerformance:
    """Test query performance (Shanana™ compliance)."""
    
    def test_shanana_latency(self):
        """Test queries complete in < 9s."""
        cube = Store40D()
        
        # Store 1000 brands
        for i in range(1000):
            cube.store({
                "sector": f"sector_{i % 10}",
                "brand": f"Brand{i}",
                "year": 2025
            })
        
        # Time query
        start = time.time()
        results = cube.query({"year": 2025})
        latency = time.time() - start
        
        assert latency < 9.0  # Shanana™ compliant
        assert len(results) == 1000
    
    def test_average_query_time_tracking(self):
        """Test that average query time is tracked."""
        cube = Store40D()
        
        cube.store({"brand": "Test"})
        
        cube.query({"brand": "Test"})
        cube.query({"brand": "Test"})
        
        assert cube.stats["total_queries"] == 2
        assert cube.stats["avg_query_time"] > 0


class TestExportImport:
    """Test export and import functionality."""
    
    def test_export_json(self, tmp_path):
        """Test exporting hypercube to JSON."""
        cube = Store40D()
        
        cube.store({"brand": "TestBrand", "value": 1000.0})
        
        export_path = tmp_path / "test_export.json"
        cube.export_json(str(export_path))
        
        assert export_path.exists()
    
    def test_import_json(self, tmp_path):
        """Test importing hypercube from JSON."""
        # Create and export
        cube1 = Store40D()
        cube1.store({"brand": "TestBrand", "value": 1000.0})
        
        export_path = tmp_path / "test_export.json"
        cube1.export_json(str(export_path))
        
        # Import to new cube
        cube2 = Store40D()
        cube2.import_json(str(export_path))
        
        assert cube2.stats["total_stored"] == 1
        results = cube2.query({"brand": "TestBrand"})
        assert len(results) == 1


class TestStatistics:
    """Test statistics tracking."""
    
    def test_get_stats(self):
        """Test get_stats returns complete information."""
        cube = Store40D(care_mandate=0.15)
        
        cube.store({"brand": "Test", "value": 1000.0})
        cube.query({"brand": "Test"})
        
        stats = cube.get_stats()
        
        assert "total_stored" in stats
        assert "total_queries" in stats
        assert "care_redistributed" in stats
        assert "avg_query_time" in stats
        assert "dimensions" in stats
        assert stats["dimensions"] == 40
        assert "care_mandate" in stats
        assert stats["care_mandate"] == 0.15
        assert "compliance" in stats
        assert "OMNI-4321" in stats["compliance"]


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_query(self):
        """Test query with no filters."""
        cube = Store40D()
        cube.store({"brand": "Test"})
        
        results = cube.query({})
        
        # Should return empty or all results (implementation dependent)
        assert isinstance(results, list)
    
    def test_none_dimension_values(self):
        """Test handling of None dimension values."""
        cube = Store40D()
        
        genome = cube.store({
            "brand": "TestBrand",
            "sector": None  # Explicitly None
        })
        
        assert genome is not None
        assert cube.stats["total_stored"] == 1
    
    def test_missing_dimensions(self):
        """Test storing with missing dimensions."""
        cube = Store40D()
        
        # Only 3 of 40 dimensions provided
        genome = cube.store({
            "brand": "MinimalBrand",
            "year": 2025,
            "verified": True
        })
        
        assert genome is not None
        results = cube.query({"brand": "MinimalBrand"})
        assert len(results) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
