"""
Contribution sensitivity analysis service
Simulates impact of contribution increase scenarios on retirement corpus
"""
from typing import Dict, List
from app.services.monte_carlo_simulator import MonteCarloSimulator
from app.core.logging_config import get_logger
from app.core.exceptions import CalculationException

logger = get_logger(__name__)


class SensitivityAnalyzer:
    """Analyzes impact of contribution changes on retirement outcomes"""
    
    # Standard sensitivity scenarios (percentage increases)
    DEFAULT_SCENARIOS = [5, 10, 20]
    
    @staticmethod
    def analyze_contribution_sensitivity(
        base_monthly_contribution: float,
        years: int,
        risk_profile: str,
        annual_income_growth: float = 0.0,
        scenarios: List[int] = None,
        iterations: int = None
    ) -> Dict:
        """
        Analyze impact of contribution increases on final corpus
        
        Args:
            base_monthly_contribution: Current monthly contribution
            years: Investment horizon
            risk_profile: Conservative, Moderate, or Aggressive
            annual_income_growth: Annual contribution growth rate
            scenarios: Contribution increase percentages (default [5, 10, 20])
            iterations: MC simulation iterations
        
        Returns:
            Dictionary with:
                - base_scenario: Original projection (0% increase)
                - sensitivity_scenarios: +5%, +10%, +20% projections
                - impact_analysis: corpus gain, percentage improvement
        """
        try:
            if scenarios is None:
                scenarios = SensitivityAnalyzer.DEFAULT_SCENARIOS
            
            simulator = MonteCarloSimulator()
            
            # Run base scenario
            logger.info(f"Running sensitivity analysis: base={base_monthly_contribution}")
            
            base_results = simulator.simulate_retirement_corpus(
                monthly_contribution=base_monthly_contribution,
                years=years,
                risk_profile=risk_profile,
                annual_income_growth=annual_income_growth,
                iterations=iterations
            )
            
            # Run sensitivity scenarios
            sensitivity_results = []
            
            for increase_pct in scenarios:
                adjusted_contribution = base_monthly_contribution * (1 + increase_pct / 100)
                
                scenario_results = simulator.simulate_retirement_corpus(
                    monthly_contribution=adjusted_contribution,
                    years=years,
                    risk_profile=risk_profile,
                    annual_income_growth=annual_income_growth,
                    iterations=iterations
                )
                
                # Calculate impact
                impact = {
                    "contribution_increase_percent": increase_pct,
                    "adjusted_monthly_contribution": adjusted_contribution,
                    "corpus_projection": scenario_results,
                    "impact_vs_base": {
                        "p10_difference": scenario_results["percentile_10"] - base_results["percentile_10"],
                        "p50_difference": scenario_results["percentile_50"] - base_results["percentile_50"],
                        "p90_difference": scenario_results["percentile_90"] - base_results["percentile_90"],
                        "p50_percentage_gain": (
                            (scenario_results["percentile_50"] - base_results["percentile_50"]) / 
                            base_results["percentile_50"] * 100
                        ) if base_results["percentile_50"] > 0 else 0
                    }
                }
                sensitivity_results.append(impact)
                
                logger.info(
                    f"Sensitivity +{increase_pct}%: p50 corpus = {scenario_results['percentile_50']:.2f}, "
                    f"gain = {impact['impact_vs_base']['p50_percentage_gain']:.1f}%"
                )
            
            return {
                "base_scenario": {
                    "monthly_contribution": base_monthly_contribution,
                    "corpus_projection": base_results
                },
                "sensitivity_scenarios": sensitivity_results,
                "analysis_metadata": {
                    "investment_horizon_years": years,
                    "risk_profile": risk_profile,
                    "annual_income_growth": annual_income_growth,
                    "scenarios_tested": scenarios
                }
            }
        
        except Exception as e:
            logger.error(f"Error in sensitivity analysis: {str(e)}")
            raise CalculationException(
                "Failed to analyze contribution sensitivity",
                details={"error": str(e)}
            )
