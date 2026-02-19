"""
Financial calculation service for retirement corpus and pension estimation
"""
import numpy as np
from typing import Tuple, Dict

from app.core.config import settings
from app.core.logging_config import get_logger
from app.core.exceptions import CalculationException
from app.models.schemas import RiskProfile

logger = get_logger(__name__)


class FinancialCalculator:
    """Service for financial calculations related to retirement planning"""
    
    @staticmethod
    def get_risk_profile_returns(risk_profile: RiskProfile) -> Tuple[float, float]:
        """Get return range for a given risk profile"""
        risk_ranges = {
            RiskProfile.CONSERVATIVE: (
                settings.CONSERVATIVE_RETURN_MIN,
                settings.CONSERVATIVE_RETURN_MAX
            ),
            RiskProfile.MODERATE: (
                settings.MODERATE_RETURN_MIN,
                settings.MODERATE_RETURN_MAX
            ),
            RiskProfile.AGGRESSIVE: (
                settings.AGGRESSIVE_RETURN_MIN,
                settings.AGGRESSIVE_RETURN_MAX
            ),
        }
        return risk_ranges[risk_profile]
    
    @staticmethod
    def calculate_corpus_deterministic(
        monthly_contribution: float,
        years: int,
        annual_return_rate: float,
        annual_income_growth: float = 0.0
    ) -> float:
        """
        Calculate retirement corpus using deterministic formula
        
        Args:
            monthly_contribution: Initial monthly contribution
            years: Investment horizon in years
            annual_return_rate: Expected annual return rate (%)
            annual_income_growth: Annual growth in contribution (%)
        
        Returns:
            Total corpus at retirement
        """
        try:
            monthly_rate = annual_return_rate / 100 / 12
            months = years * 12
            
            if annual_income_growth == 0:
                # Simple future value of annuity
                if monthly_rate == 0:
                    corpus = monthly_contribution * months
                else:
                    corpus = monthly_contribution * (
                        ((1 + monthly_rate) ** months - 1) / monthly_rate
                    )
            else:
                # Growing annuity formula
                monthly_growth_rate = annual_income_growth / 100 / 12
                corpus = 0
                
                for month in range(months):
                    contribution = monthly_contribution * (1 + monthly_growth_rate) ** month
                    future_value = contribution * (1 + monthly_rate) ** (months - month)
                    corpus += future_value
            
            return corpus
        
        except Exception as e:
            logger.error(f"Error in deterministic corpus calculation: {str(e)}")
            raise CalculationException(
                "Failed to calculate retirement corpus",
                details={"error": str(e)}
            )
    
    @staticmethod
    def calculate_total_contributions(
        initial_monthly_contribution: float,
        years: int,
        annual_income_growth: float = 0.0
    ) -> float:
        """Calculate total contributions over investment period"""
        try:
            months = years * 12
            monthly_growth_rate = annual_income_growth / 100 / 12
            
            if annual_income_growth == 0:
                return initial_monthly_contribution * months
            
            total = 0
            for month in range(months):
                contribution = initial_monthly_contribution * (1 + monthly_growth_rate) ** month
                total += contribution
            
            return total
        
        except Exception as e:
            logger.error(f"Error calculating total contributions: {str(e)}")
            raise CalculationException(
                "Failed to calculate total contributions",
                details={"error": str(e)}
            )
    
    @staticmethod
    def calculate_monthly_pension(
        corpus: float,
        annuity_rate: float = None,
        corpus_allocation: float = None
    ) -> Tuple[float, float, float]:
        """
        Calculate monthly pension from corpus
        
        Args:
            corpus: Total retirement corpus
            annuity_rate: Annual annuity rate (%)
            corpus_allocation: Percentage of corpus allocated to annuity (0-1)
        
        Returns:
            Tuple of (lump_sum, annuity_amount, monthly_pension)
        """
        try:
            if annuity_rate is None:
                annuity_rate = settings.DEFAULT_ANNUITY_RATE
            
            if corpus_allocation is None:
                corpus_allocation = settings.CORPUS_ANNUITY_ALLOCATION
            
            # Calculate allocation
            annuity_corpus = corpus * corpus_allocation
            lump_sum = corpus * (1 - corpus_allocation)
            
            # Calculate monthly pension from annuity
            monthly_pension = (annuity_corpus * annuity_rate / 100) / 12
            
            return lump_sum, annuity_corpus, monthly_pension
        
        except Exception as e:
            logger.error(f"Error calculating pension: {str(e)}")
            raise CalculationException(
                "Failed to calculate pension estimate",
                details={"error": str(e)}
            )
    
    @staticmethod
    def reverse_calculate_required_contribution(
        desired_monthly_pension: float,
        years: int,
        annual_return_rate: float,
        annual_income_growth: float = 0.0,
        annuity_rate: float = None,
        corpus_allocation: float = None
    ) -> Tuple[float, float]:
        """
        Reverse calculate required monthly contribution for desired pension
        
        Args:
            desired_monthly_pension: Target monthly pension amount
            years: Investment horizon in years
            annual_return_rate: Expected annual return rate (%)
            annual_income_growth: Annual growth in contribution (%)
            annuity_rate: Annual annuity rate (%)
            corpus_allocation: Percentage allocated to annuity
        
        Returns:
            Tuple of (required_monthly_contribution, required_corpus)
        """
        try:
            if annuity_rate is None:
                annuity_rate = settings.DEFAULT_ANNUITY_RATE
            
            if corpus_allocation is None:
                corpus_allocation = settings.CORPUS_ANNUITY_ALLOCATION
            
            # Calculate required annuity corpus
            required_annuity_corpus = (desired_monthly_pension * 12 * 100) / annuity_rate
            
            # Calculate total required corpus
            required_total_corpus = required_annuity_corpus / corpus_allocation
            
            # Use binary search to find required contribution
            min_contribution = 100
            max_contribution = 500000
            tolerance = 100  # INR 100 tolerance
            
            for _ in range(100):  # Max iterations
                mid_contribution = (min_contribution + max_contribution) / 2
                
                calculated_corpus = FinancialCalculator.calculate_corpus_deterministic(
                    mid_contribution,
                    years,
                    annual_return_rate,
                    annual_income_growth
                )
                
                if abs(calculated_corpus - required_total_corpus) < tolerance:
                    return mid_contribution, required_total_corpus
                
                if calculated_corpus < required_total_corpus:
                    min_contribution = mid_contribution
                else:
                    max_contribution = mid_contribution
            
            # Return best estimate if not converged
            return mid_contribution, required_total_corpus
        
        except Exception as e:
            logger.error(f"Error in reverse calculation: {str(e)}")
            raise CalculationException(
                "Failed to calculate required contribution",
                details={"error": str(e)}
            )
