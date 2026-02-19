"""
Monte Carlo simulation service for retirement forecasting
"""
import numpy as np
from typing import Dict, Tuple

from app.core.config import settings
from app.core.logging_config import get_logger
from app.core.exceptions import CalculationException
from app.models.schemas import RiskProfile
from app.services.financial_calculator import FinancialCalculator

logger = get_logger(__name__)


class MonteCarloSimulator:
    """Monte Carlo simulation engine for probabilistic retirement forecasting"""
    
    def __init__(self, seed: int = None):
        """Initialize simulator with optional random seed for reproducibility"""
        self.seed = seed
        if seed is not None:
            np.random.seed(seed)
    
    def simulate_retirement_corpus(
        self,
        monthly_contribution: float,
        years: int,
        risk_profile: RiskProfile,
        annual_income_growth: float = 0.0,
        iterations: int = None
    ) -> Dict[str, float]:
        """
        Run Monte Carlo simulation for retirement corpus
        
        Args:
            monthly_contribution: Initial monthly contribution
            years: Investment horizon in years
            risk_profile: Investment risk profile
            annual_income_growth: Annual growth in contribution (%)
            iterations: Number of simulation iterations
        
        Returns:
            Dictionary with statistical results (mean, std, percentiles)
        """
        try:
            if iterations is None:
                iterations = settings.DEFAULT_MONTE_CARLO_ITERATIONS
            
            # Validate iterations
            if iterations > settings.MAX_MONTE_CARLO_ITERATIONS:
                iterations = settings.MAX_MONTE_CARLO_ITERATIONS
                logger.warning(
                    f"Iterations capped at {settings.MAX_MONTE_CARLO_ITERATIONS}"
                )
            
            # Get return range for risk profile
            min_return, max_return = FinancialCalculator.get_risk_profile_returns(
                risk_profile
            )
            
            logger.info(
                f"Starting Monte Carlo simulation: {iterations} iterations, "
                f"{years} years, risk={risk_profile.value}"
            )
            
            # Run simulations
            results = np.zeros(iterations)
            
            for i in range(iterations):
                # Generate random annual returns for each year
                annual_returns = np.random.uniform(
                    min_return,
                    max_return,
                    size=years
                )
                
                corpus = self._simulate_single_path(
                    monthly_contribution,
                    years,
                    annual_returns,
                    annual_income_growth
                )
                results[i] = corpus
            
            # Calculate statistics
            statistics = {
                "mean": float(np.mean(results)),
                "std_deviation": float(np.std(results)),
                "percentile_10": float(np.percentile(results, 10)),
                "percentile_25": float(np.percentile(results, 25)),
                "percentile_50": float(np.percentile(results, 50)),
                "percentile_75": float(np.percentile(results, 75)),
                "percentile_90": float(np.percentile(results, 90)),
                "min": float(np.min(results)),
                "max": float(np.max(results)),
            }
            
            logger.info(
                f"Simulation completed: mean={statistics['mean']:.2f}, "
                f"median={statistics['percentile_50']:.2f}"
            )
            
            return statistics
        
        except Exception as e:
            logger.error(f"Monte Carlo simulation failed: {str(e)}", exc_info=True)
            raise CalculationException(
                "Monte Carlo simulation failed",
                details={"error": str(e)}
            )
    
    def _simulate_single_path(
        self,
        initial_contribution: float,
        years: int,
        annual_returns: np.ndarray,
        annual_income_growth: float
    ) -> float:
        """
        Simulate a single path of corpus accumulation
        
        Args:
            initial_contribution: Starting monthly contribution
            years: Investment horizon
            annual_returns: Array of annual return rates for each year
            annual_income_growth: Annual contribution growth rate
        
        Returns:
            Final corpus value
        """
        corpus = 0.0
        monthly_growth_rate = annual_income_growth / 100 / 12
        
        for year in range(years):
            annual_return = annual_returns[year]
            monthly_return = annual_return / 100 / 12
            
            for month in range(12):
                # Calculate contribution for this month
                total_months = year * 12 + month
                contribution = initial_contribution * (1 + monthly_growth_rate) ** total_months
                
                # Add contribution and apply return
                corpus = (corpus + contribution) * (1 + monthly_return)
        
        return corpus
    
    def simulate_pension_scenarios(
        self,
        monthly_contribution: float,
        years: int,
        annual_income_growth: float = 0.0,
        iterations: int = None
    ) -> Dict[RiskProfile, Dict[str, float]]:
        """
        Simulate all three risk scenarios for comparison
        
        Returns:
            Dictionary mapping risk profiles to their simulation results
        """
        try:
            scenarios = {}
            
            for risk_profile in RiskProfile:
                logger.info(f"Simulating {risk_profile.value} scenario")
                results = self.simulate_retirement_corpus(
                    monthly_contribution=monthly_contribution,
                    years=years,
                    risk_profile=risk_profile,
                    annual_income_growth=annual_income_growth,
                    iterations=iterations
                )
                scenarios[risk_profile] = results
            
            return scenarios
        
        except Exception as e:
            logger.error(f"Scenario simulation failed: {str(e)}", exc_info=True)
            raise CalculationException(
                "Failed to simulate multiple scenarios",
                details={"error": str(e)}
            )
    
    def calculate_confidence_interval(
        self,
        results: np.ndarray,
        confidence_level: float = 0.95
    ) -> Tuple[float, float]:
        """
        Calculate confidence interval for simulation results
        
        Args:
            results: Array of simulation results
            confidence_level: Confidence level (default 95%)
        
        Returns:
            Tuple of (lower_bound, upper_bound)
        """
        alpha = 1 - confidence_level
        lower_percentile = (alpha / 2) * 100
        upper_percentile = (1 - alpha / 2) * 100
        
        lower_bound = np.percentile(results, lower_percentile)
        upper_bound = np.percentile(results, upper_percentile)
        
        return float(lower_bound), float(upper_bound)
