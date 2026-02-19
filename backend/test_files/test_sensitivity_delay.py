"""
Unit tests for sensitivity_analyzer and delay_simulator modules
Tests contribution sensitivity and retirement delay impact analysis
"""
import pytest  
from app.services.sensitivity_analyzer import SensitivityAnalyzer
from app.services.delay_simulator import DelaySimulator
from app.models.schemas import RiskProfile


class TestSensitivityAnalyzer:
    """Test suite for SensitivityAnalyzer"""
    
    def test_sensitivity_has_base_scenario(self):
        """Test that sensitivity analysis includes base scenario"""
        result = SensitivityAnalyzer.analyze_contribution_sensitivity(
            base_monthly_contribution=10000,
            years=30,
            risk_profile=RiskProfile.MODERATE,
            iterations=1000
        )
        
        assert "base_scenario" in result
        assert result["base_scenario"]["monthly_contribution"] == 10000
        assert "corpus_projection" in result["base_scenario"]
    
    def test_sensitivity_scenarios_exist(self):
        """Test that sensitivity scenarios are generated"""
        result = SensitivityAnalyzer.analyze_contribution_sensitivity(
            base_monthly_contribution=10000,
            years=30,
            risk_profile=RiskProfile.MODERATE,
            iterations=1000
        )
        
        assert "sensitivity_scenarios" in result
        assert len(result["sensitivity_scenarios"]) == 3  # Default: +5%, +10%, +20%
    
    def test_sensitivity_improvement_monotonic(self):
        """Test that higher contributions lead to higher corpus"""
        result = SensitivityAnalyzer.analyze_contribution_sensitivity(
            base_monthly_contribution=10000,
            years=30,
            risk_profile=RiskProfile.MODERATE,
            iterations=1000
        )
        
        base_p50 = result["base_scenario"]["corpus_projection"]["percentile_50"]
        
        prev_p50 = base_p50
        for scenario in result["sensitivity_scenarios"]:
            current_p50 = scenario["corpus_projection"]["percentile_50"]
            # Higher contribution should lead to higher corpus (monotonic increase)
            assert current_p50 > prev_p50
            prev_p50 = current_p50
    
    def test_sensitivity_impact_calculation(self):
        """Test that impact metrics are calculated"""
        result = SensitivityAnalyzer.analyze_contribution_sensitivity(
            base_monthly_contribution=10000,
            years=30,
            risk_profile=RiskProfile.MODERATE,
            iterations=1000
        )
        
        for scenario in result["sensitivity_scenarios"]:
            assert "impact_vs_base" in scenario
            impact = scenario["impact_vs_base"]
            
            assert "p50_difference" in impact
            assert "p50_percentage_gain" in impact
            
            # Gain should be positive for higher contributions
            assert impact["p50_difference"] > 0
            assert impact["p50_percentage_gain"] > 0
    
    def test_sensitivity_custom_scenarios(self):
        """Test sensitivity with custom scenario percentages"""
        result = SensitivityAnalyzer.analyze_contribution_sensitivity(
            base_monthly_contribution=10000,
            years=30,
            risk_profile=RiskProfile.MODERATE,
            scenarios=[3, 15],
            iterations=1000
        )
        
        assert len(result["sensitivity_scenarios"]) == 2
        assert result["sensitivity_scenarios"][0]["contribution_increase_percent"] == 3
        assert result["sensitivity_scenarios"][1]["contribution_increase_percent"] == 15
    
    def test_sensitivity_metadata(self):
        """Test that analysis metadata is present"""
        result = SensitivityAnalyzer.analyze_contribution_sensitivity(
            base_monthly_contribution=10000,
            years=30,
            risk_profile=RiskProfile.AGGRESSIVE,
            annual_income_growth=3.5,
            iterations=2000
        )
        
        metadata = result["analysis_metadata"]
        assert metadata["investment_horizon_years"] == 30
        assert metadata["risk_profile"] == RiskProfile.AGGRESSIVE
        assert metadata["annual_income_growth"] == 3.5


class TestDelaySimulator:
    """Test suite for DelaySimulator"""
    
    def test_delay_has_base_scenario(self):
        """Test that delay analysis includes base retirement scenario"""
        result = DelaySimulator.simulate_retirement_delay(
            base_retirement_age=60,
            current_age=35,
            monthly_contribution=10000,
            risk_profile=RiskProfile.MODERATE,
            iterations=1000
        )
        
        assert "base_scenario" in result
        assert result["base_scenario"]["retirement_age"] == 60
        assert result["base_scenario"]["investment_horizon_years"] == 25
    
    def test_delay_scenarios_generated(self):
        """Test that delay scenarios are generated"""
        result = DelaySimulator.simulate_retirement_delay(
            base_retirement_age=60,
            current_age=35,
            monthly_contribution=10000,
            risk_profile=RiskProfile.MODERATE,
            iterations=1000
        )
        
        assert "delay_scenarios" in result
        assert len(result["delay_scenarios"]) == 3  # Default: +1yr, +2yr, +5yr
    
    def test_delay_corpus_improvement(self):
        """Test that delaying retirement increases corpus"""
        result = DelaySimulator.simulate_retirement_delay(
            base_retirement_age=60,
            current_age=35,
            monthly_contribution=10000,
            risk_profile=RiskProfile.MODERATE,
            iterations=1000
        )
        
        base_p50 = result["base_scenario"]["corpus_projection"]["percentile_50"]
        
        prev_corpus = base_p50
        for scenario in result["delay_scenarios"]:
            current_corpus = scenario["corpus_projection"]["percentile_50"]
            # More years = larger corpus
            assert current_corpus > prev_corpus
            prev_corpus = current_corpus
    
    def test_delay_pension_improvement(self):
        """Test that delaying retirement increases monthly pension"""
        result = DelaySimulator.simulate_retirement_delay(
            base_retirement_age=60,
            current_age=35,
            monthly_contribution=10000,
            risk_profile=RiskProfile.MODERATE,
            iterations=1000
        )
        
        base_pension = result["base_scenario"]["pension_estimate"]["monthly_pension"]
        
        for scenario in result["delay_scenarios"]:
            delayed_pension = scenario["pension_estimate"]["monthly_pension"]
            # More corpus = higher pension
            assert delayed_pension > base_pension
    
    def test_delay_benefit_analysis(self):
        """Test that benefit analysis metrics are calculated"""
        result = DelaySimulator.simulate_retirement_delay(
            base_retirement_age=60,
            current_age=35,
            monthly_contribution=10000,
            risk_profile=RiskProfile.MODERATE,
            iterations=1000
        )
        
        for scenario in result["delay_scenarios"]:
            benefits = scenario["benefit_analysis"]
            
            assert "additional_corpus_p50" in benefits
            assert "additional_corpus_percentage" in benefits
            assert "monthly_pension_increase" in benefits
            assert "monthly_pension_percentage_increase" in benefits
            assert "additional_working_years" in benefits
            
            # Adding years should increase corpus
            assert benefits["additional_corpus_p50"] > 0
            assert benefits["additional_corpus_percentage"] > 0
    
    def test_delay_retirement_age_progression(self):
        """Test that retirement ages increase correctly"""
        result = DelaySimulator.simulate_retirement_delay(
            base_retirement_age=60,
            current_age=35,
            monthly_contribution=10000,
            risk_profile=RiskProfile.MODERATE,
            iterations=1000
        )
        
        ages = [scenario["new_retirement_age"] for scenario in result["delay_scenarios"]]
        # Should be 61, 62, 65
        assert ages == [61, 62, 65]
    
    def test_delay_custom_scenarios(self):
        """Test delay analysis with custom delay periods"""
        result = DelaySimulator.simulate_retirement_delay(
            base_retirement_age=60,
            current_age=40,
            monthly_contribution=10000,
            risk_profile=RiskProfile.MODERATE,
            delay_years=[1, 3],
            iterations=1000
        )
        
        assert len(result["delay_scenarios"]) == 2
        assert result["delay_scenarios"][0]["delay_years"] == 1
        assert result["delay_scenarios"][1]["delay_years"] == 3
    
    def test_delay_metadata(self):
        """Test that analysis metadata is present"""
        result = DelaySimulator.simulate_retirement_delay(
            base_retirement_age=60,
            current_age=35,
            monthly_contribution=10000,
            risk_profile=RiskProfile.CONSERVATIVE,
            annual_income_growth=4.0,
            iterations=2000
        )
        
        metadata = result["analysis_metadata"]
        assert metadata["current_age"] == 35
        assert metadata["monthly_contribution"] == 10000
        assert metadata["risk_profile"] == RiskProfile.CONSERVATIVE
        assert metadata["annual_income_growth"] == 4.0
