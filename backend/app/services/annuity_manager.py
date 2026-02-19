"""
Modular annuity and pension allocation service
Handles corpus allocation, annuity purchase, and monthly pension calculations
"""
from typing import Dict, Tuple
from app.core.config import settings
from app.core.logging_config import get_logger
from app.core.exceptions import CalculationException

logger = get_logger(__name__)


class AnnuityManager:
    """Manages annuity allocation and pension calculations with transparency"""
    
    @staticmethod
    def allocate_corpus(
        corpus: float,
        annuity_allocation: float = None,
        annuity_rate: float = None
    ) -> Dict[str, float]:
        """
        Allocate corpus between annuity and lump sum
        
        Args:
            corpus: Total retirement corpus
            annuity_allocation: Percentage of corpus for annuity (0-1), default 40%
            annuity_rate: Annual annuity rate (%), default 6%
        
        Returns:
            Dictionary with:
                - total_corpus: Input corpus
                - annuity_allocation_percent: Allocation percentage (40% standard)
                - lump_sum_allocation_percent: Allocation percentage (60% standard)
                - annuity_corpus: Amount dedicated to annuity
                - lump_sum_amount: Lump sum withdrawal
                - annuity_rate_used: Actual annuity rate applied
        """
        try:
            if annuity_allocation is None:
                annuity_allocation = settings.CORPUS_ANNUITY_ALLOCATION
            
            if annuity_rate is None:
                annuity_rate = settings.DEFAULT_ANNUITY_RATE
            
            lump_sum_allocation = 1 - annuity_allocation
            
            annuity_corpus = corpus * annuity_allocation
            lump_sum = corpus * lump_sum_allocation
            
            return {
                "total_corpus": corpus,
                "annuity_allocation_percent": annuity_allocation * 100,
                "lump_sum_allocation_percent": lump_sum_allocation * 100,
                "annuity_corpus": annuity_corpus,
                "lump_sum_amount": lump_sum,
                "annuity_rate_used": annuity_rate
            }
        
        except Exception as e:
            logger.error(f"Error allocating corpus: {str(e)}")
            raise CalculationException(
                "Failed to allocate corpus between annuity and lump sum",
                details={"error": str(e)}
            )
    
    @staticmethod
    def calculate_monthly_pension(
        corpus: float,
        annuity_allocation: float = None,
        annuity_rate: float = None
    ) -> Dict[str, float]:
        """
        Calculate monthly pension from corpus with transparency
        
        Args:
            corpus: Total retirement corpus
            annuity_allocation: Percentage allocated to annuity (default 40%)
            annuity_rate: Annual annuity rate percentage (default 6%)
        
        Returns:
            Dictionary with:
                - monthly_pension: Monthly income from annuity
                - lump_sum_amount: Available lump sum
                - annuity_corpus: Amount used for annuity
                - annuity_rate_used: Rate applied
        """
        try:
            allocation = AnnuityManager.allocate_corpus(
                corpus,
                annuity_allocation,
                annuity_rate
            )
            
            annuity_corpus = allocation["annuity_corpus"]
            annuity_rate_used = allocation["annuity_rate_used"]
            
            monthly_pension = (annuity_corpus * annuity_rate_used / 100) / 12
            
            return {
                "monthly_pension": monthly_pension,
                "lump_sum_amount": allocation["lump_sum_amount"],
                "annuity_corpus": annuity_corpus,
                "annuity_rate_used": annuity_rate_used,
                "annuity_allocation_percent": allocation["annuity_allocation_percent"],
                "lump_sum_allocation_percent": allocation["lump_sum_allocation_percent"]
            }
        
        except Exception as e:
            logger.error(f"Error calculating monthly pension: {str(e)}")
            raise CalculationException(
                "Failed to calculate monthly pension",
                details={"error": str(e)}
            )
    
    @staticmethod
    def calculate_pension_range(
        p10_corpus: float,
        p50_corpus: float,
        p90_corpus: float,
        annuity_allocation: float = None,
        annuity_rate: float = None
    ) -> Dict[str, Dict[str, float]]:
        """
        Calculate pension for different percentiles
        
        Args:
            p10_corpus: 10th percentile corpus
            p50_corpus: 50th percentile corpus
            p90_corpus: 90th percentile corpus
            annuity_allocation: Percentage for annuity
            annuity_rate: Annual annuity rate
        
        Returns:
            Dictionary with p10, p50, p90 pension breakdowns
        """
        try:
            percentiles = {
                "p10": AnnuityManager.calculate_monthly_pension(p10_corpus, annuity_allocation, annuity_rate),
                "p50": AnnuityManager.calculate_monthly_pension(p50_corpus, annuity_allocation, annuity_rate),
                "p90": AnnuityManager.calculate_monthly_pension(p90_corpus, annuity_allocation, annuity_rate)
            }
            return percentiles
        
        except Exception as e:
            logger.error(f"Error calculating pension range: {str(e)}")
            raise CalculationException(
                "Failed to calculate pension range",
                details={"error": str(e)}
            )
