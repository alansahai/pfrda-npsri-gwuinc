"""
Retirement delay impact simulator
Simulates the financial benefit of delaying retirement
"""
from typing import Dict, List
from app.services.monte_carlo_simulator import MonteCarloSimulator
from app.services.annuity_manager import AnnuityManager
from app.core.logging_config import get_logger
from app.core.exceptions import CalculationException

logger = get_logger(__name__)


class DelaySimulator:
    """Simulates impact of retirement delay on corpus and pension"""
    
    # Standard delay scenarios (years)
    DEFAULT_DELAY_SCENARIOS = [1, 2, 5]
    
    @staticmethod
    def simulate_retirement_delay(
        base_retirement_age: int,
        current_age: int,
        monthly_contribution: float,
        risk_profile: str,
        annual_income_growth: float = 0.0,
        delay_years: List[int] = None,
        iterations: int = None
    ) -> Dict:
        """
        Simulate impact of delaying retirement on corpus and pension
        
        Args:
            base_retirement_age: Original planned retirement age
            current_age: Current age
            monthly_contribution: Current monthly contribution
            risk_profile: Investment risk profile
            annual_income_growth: Annual contribution growth
            delay_years: Years to delay (default [1, 2, 5])
            iterations: MC simulation iterations
        
        Returns:
            Dictionary with:
                - base_scenario: Original retirement age projection
                - delay_scenarios: +1yr, +2yr, +5yr projections
                - benefit_analysis: Additional corpus, pension increase
        """
        try:
            if delay_years is None:
                delay_years = DelaySimulator.DEFAULT_DELAY_SCENARIOS
            
            simulator = MonteCarloSimulator()
            
            # Run base scenario (original retirement age)
            base_years = base_retirement_age - current_age
            logger.info(f"Simulating delay analysis: base age={base_retirement_age}, years={base_years}")
            
            base_results = simulator.simulate_retirement_corpus(
                monthly_contribution=monthly_contribution,
                years=base_years,
                risk_profile=risk_profile,
                annual_income_growth=annual_income_growth,
                iterations=iterations
            )
            
            # Calculate base pension
            base_pension = AnnuityManager.calculate_monthly_pension(
                base_results["percentile_50"]
            )
            
            # Run delay scenarios
            delay_results = []
            
            for delay in delay_years:
                new_retirement_age = base_retirement_age + delay
                new_horizon_years = new_retirement_age - current_age
                
                scenario_results = simulator.simulate_retirement_corpus(
                    monthly_contribution=monthly_contribution,
                    years=new_horizon_years,
                    risk_profile=risk_profile,
                    annual_income_growth=annual_income_growth,
                    iterations=iterations
                )
                
                # Calculate pension for delay scenario
                delay_pension = AnnuityManager.calculate_monthly_pension(
                    scenario_results["percentile_50"]
                )
                
                # Calculate benefits
                impact = {
                    "delay_years": delay,
                    "new_retirement_age": new_retirement_age,
                    "investment_horizon_years": new_horizon_years,
                    "corpus_projection": scenario_results,
                    "pension_estimate": delay_pension,
                    "benefit_analysis": {
                        "additional_corpus_p50": scenario_results["percentile_50"] - base_results["percentile_50"],
                        "additional_corpus_percentage": (
                            (scenario_results["percentile_50"] - base_results["percentile_50"]) /
                            base_results["percentile_50"] * 100
                        ) if base_results["percentile_50"] > 0 else 0,
                        "monthly_pension_increase": delay_pension["monthly_pension"] - base_pension["monthly_pension"],
                        "monthly_pension_percentage_increase": (
                            (delay_pension["monthly_pension"] - base_pension["monthly_pension"]) /
                            base_pension["monthly_pension"] * 100
                        ) if base_pension["monthly_pension"] > 0 else 0,
                        "additional_working_years": delay,
                        "additional_compilation_benefit_percent": (
                            ((scenario_results["percentile_50"] - base_results["percentile_50"]) /
                            base_results["percentile_50"] - (delay / base_years)) * 100
                        ) if base_results["percentile_50"] > 0 else 0
                    }
                }
                delay_results.append(impact)
                
                logger.info(
                    f"Delay +{delay}yr: retirement at {new_retirement_age}, corpus p50={scenario_results['percentile_50']:.2f}, "
                    f"pension_increase={impact['benefit_analysis']['monthly_pension_percentage_increase']:.1f}%"
                )
            
            return {
                "base_scenario": {
                    "retirement_age": base_retirement_age,
                    "investment_horizon_years": base_years,
                    "corpus_projection": base_results,
                    "pension_estimate": base_pension
                },
                "delay_scenarios": delay_results,
                "analysis_metadata": {
                    "current_age": current_age,
                    "monthly_contribution": monthly_contribution,
                    "risk_profile": risk_profile,
                    "annual_income_growth": annual_income_growth,
                    "scenarios_tested": delay_years
                }
            }
        
        except Exception as e:
            logger.error(f"Error in delay impact simulation: {str(e)}")
            raise CalculationException(
                "Failed to simulate retirement delay impact",
                details={"error": str(e)}
            )
