"""
Unit tests for annuity_manager module
Tests corpus allocation and pension calculations with transparency
"""
import pytest
from app.services.annuity_manager import AnnuityManager
from app.core.exceptions import CalculationException


class TestAnnuityManager:
    """Test suite for AnnuityManager"""
    
    def test_allocate_corpus_default(self):
        """Test corpus allocation with default parameters (40% annuity, 60% lump sum)"""
        corpus = 1000000
        result = AnnuityManager.allocate_corpus(corpus)
        
        assert result["total_corpus"] == 1000000
        assert result["annuity_allocation_percent"] == 40
        assert result["lump_sum_allocation_percent"] == 60
        assert result["annuity_corpus"] == 400000
        assert result["lump_sum_amount"] == 600000
        assert result["annuity_rate_used"] == 6.0
    
    def test_allocate_corpus_custom(self):
        """Test corpus allocation with custom parameters"""
        corpus = 2000000
        result = AnnuityManager.allocate_corpus(
            corpus,
            annuity_allocation=0.5,
            annuity_rate=7.0
        )
        
        assert result["annuity_allocation_percent"] == 50
        assert result["lump_sum_allocation_percent"] == 50
        assert result["annuity_corpus"] == 1000000
        assert result["lump_sum_amount"] == 1000000
        assert result["annuity_rate_used"] == 7.0
    
    def test_calculate_monthly_pension_default(self):
        """Test monthly pension calculation with default allocation"""
        corpus = 1000000  # ₹1 crore
        result = AnnuityManager.calculate_monthly_pension(corpus)
        
        # With 40% allocation and 6% annuity rate:
        # Annuity corpus = 400,000
        # Monthly pension = (400,000 * 6 / 100) / 12 = 2,000
        assert result["monthly_pension"] == pytest.approx(2000, abs=1)
        assert result["lump_sum_amount"] == pytest.approx(600000, abs=1)
        assert result["annuity_corpus"] == pytest.approx(400000, abs=1)
        assert result["annuity_allocation_percent"] == 40
    
    def test_calculate_monthly_pension_custom_rate(self):
        """Test monthly pension with custom annuity rate"""
        corpus = 1200000
        result = AnnuityManager.calculate_monthly_pension(
            corpus,
            annuity_allocation=0.5,
            annuity_rate=8.0
        )
        
        # With 50% allocation and 8% rate:
        # Annuity corpus = 600,000
        # Monthly pension = (600,000 * 8 / 100) / 12 = 4,000
        assert result["monthly_pension"] == pytest.approx(4000, abs=1)
        assert result["lump_sum_amount"] == pytest.approx(600000, abs=1)
    
    def test_calculate_pension_range(self):
        """Test pension calculation across percentiles"""
        result = AnnuityManager.calculate_pension_range(
            p10_corpus=8000000,
            p50_corpus=12000000,
            p90_corpus=16000000
        )
        
        assert "p10" in result
        assert "p50" in result
        assert "p90" in result
        
        # P50 with 12M corpus and 6% rate, 40% allocation:
        # Monthly = (4.8M * 6/100) / 12 = 24,000
        assert result["p50"]["monthly_pension"] == pytest.approx(24000, abs=1)
        assert result["p50"]["annuity_allocation_percent"] == 40
        
        # P10 should have lower pension
        assert result["p10"]["monthly_pension"] < result["p50"]["monthly_pension"]
        # P90 should have higher pension
        assert result["p90"]["monthly_pension"] > result["p50"]["monthly_pension"]
    
    def test_allocate_zero_corpus(self):
        """Test allocation with zero corpus"""
        result = AnnuityManager.allocate_corpus(0)
        
        assert result["total_corpus"] == 0
        assert result["annuity_corpus"] == 0
        assert result["lump_sum_amount"] == 0
    
    def test_calculate_pension_zero_corpus(self):
        """Test pension calculation with zero corpus"""
        result = AnnuityManager.calculate_monthly_pension(0)
        
        assert result["monthly_pension"] == 0
        assert result["lump_sum_amount"] == 0
    
    def test_modular_separation(self):
        """Test that AnnuityManger is truly modular and reusable"""
        # Can be used independently
        allocation = AnnuityManager.allocate_corpus(5000000)
        pension = AnnuityManager.calculate_monthly_pension(5000000)
        range_calcs = AnnuityManager.calculate_pension_range(
            4000000, 5000000, 6000000
        )
        
        # All should work independently
        assert allocation["total_corpus"] == 5000000
        assert pension["monthly_pension"] > 0
        assert len(range_calcs) == 3
