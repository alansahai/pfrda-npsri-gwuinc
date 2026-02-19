"""
Retirement readiness score analyzer
Generates readiness scores with transparent breakdown and recommendations
"""
from typing import Dict
from app.core.logging_config import get_logger
from app.core.exceptions import CalculationException

logger = get_logger(__name__)


class ReadinessAnalyzer:
    """Analyzes retirement readiness with transparent scoring breakdown"""
    
    # Readiness thresholds
    STRONG_OUTLOOK_MIN = 75
    MODERATE_CONFIDENCE_MIN = 50
    HIGH_RISK_MIN = 0
    
    @staticmethod
    def calculate_readiness_score(
        median_corpus: float,
        p10_corpus: float,
        p90_corpus: float,
        years_to_retirement: int,
        required_corpus: float = None,
        risk_profile: str = None
    ) -> Dict:
        """
        Calculate readiness score with breakdown transparency
        
        Args:
            median_corpus: 50th percentile corpus projection
            p10_corpus: 10th percentile corpus (downside scenario)
            p90_corpus: 90th percentile corpus (upside scenario)
            years_to_retirement: Years until retirement
            required_corpus: Minimum corpus needed (optional benchmark)
            risk_profile: Investment risk profile
        
        Returns:
            Dictionary with:
                - score: 0-100 readiness score
                - label: "Strong Outlook", "Moderate Confidence", or "High Risk"
                - breakdown: Component scores with weights
                - explanation: Text explanation of score
                - recommendation: Actionable recommendation
        """
        try:
            # Component 1: Corpus Strength (50% weight)
            # How well positioned is the median corpus?
            corpus_strength = ReadinessAnalyzer._calculate_corpus_strength(
                median_corpus,
                required_corpus
            )
            
            # Component 2: Downside Protection (30% weight)
            # How safe is the p10 scenario?
            downside_weight = ReadinessAnalyzer._calculate_downside_protection(
                p10_corpus,
                p90_corpus,
                median_corpus
            )
            
            # Component 3: Time Horizon (20% weight)
            # More years = more compounding opportunity
            time_weight = ReadinessAnalyzer._calculate_time_benefit(
                years_to_retirement
            )
            
            # Weighted score
            weighted_score = (
                corpus_strength * 0.50 +
                downside_weight * 0.30 +
                time_weight * 0.20
            )
            
            # Round to integer
            final_score = int(round(weighted_score))
            final_score = max(0, min(100, final_score))
            
            # Determine label
            if final_score >= ReadinessAnalyzer.STRONG_OUTLOOK_MIN:
                label = "Strong Outlook"
            elif final_score >= ReadinessAnalyzer.MODERATE_CONFIDENCE_MIN:
                label = "Moderate Confidence"
            else:
                label = "High Risk"
            
            # Generate explanation
            explanation = ReadinessAnalyzer._generate_explanation(
                final_score,
                label,
                corpus_strength,
                downside_weight,
                time_weight
            )
            
            # Generate recommendation
            recommendation = ReadinessAnalyzer._generate_recommendation(
                label,
                corpus_strength,
                downside_weight,
                time_weight
            )
            
            return {
                "score": final_score,
                "label": label,
                "explanation": explanation,
                "recommendation": recommendation,
                "scoring_breakdown": {
                    "corpus_strength_score": round(corpus_strength, 1),
                    "corpus_strength_weight": 50,
                    "volatility_penalty_score": round(downside_weight, 1),
                    "volatility_penalty_weight": 30,
                    "time_horizon_score": round(time_weight, 1),
                    "time_horizon_weight": 20
                }
            }
        
        except Exception as e:
            logger.error(f"Error calculating readiness score: {str(e)}")
            raise CalculationException(
                "Failed to calculate retirement readiness score",
                details={"error": str(e)}
            )
    
    @staticmethod
    def _calculate_corpus_strength(median_corpus: float, required_corpus: float = None) -> float:
        """Score based on median corpus adequacy"""
        if required_corpus is None or required_corpus <= 0:
            # If no benchmark, use median corpus size as proxy
            # Assume 50L is 'adequate' for typical Indian retirement
            required_corpus = 5000000
        
        ratio = median_corpus / required_corpus
        
        if ratio >= 1.2:
            return 100
        elif ratio >= 1.0:
            return 90
        elif ratio >= 0.8:
            return 70
        elif ratio >= 0.6:
            return 50
        elif ratio >= 0.4:
            return 30
        else:
            return 10
    
    @staticmethod
    def _calculate_downside_protection(p10_corpus: float, p90_corpus: float, median_corpus: float) -> float:
        """Score based on distribution width (volatility protection)"""
        if median_corpus == 0:
            return 50
        
        # Coefficient of variation using percentiles
        distribution_width = (p90_corpus - p10_corpus) / (2 * median_corpus) if median_corpus > 0 else 0.5
        
        # Lower width = better protection
        if distribution_width < 0.3:
            return 95  # Tight distribution = very safe
        elif distribution_width < 0.5:
            return 80
        elif distribution_width < 0.7:
            return 65
        elif distribution_width < 0.9:
            return 50
        else:
            return 35
    
    @staticmethod
    def _calculate_time_benefit(years_to_retirement: int) -> float:
        """Score based on investment horizon"""
        if years_to_retirement >= 25:
            return 100  # Excellent time for compounding
        elif years_to_retirement >= 20:
            return 90
        elif years_to_retirement >= 15:
            return 75
        elif years_to_retirement >= 10:
            return 60
        elif years_to_retirement >= 5:
            return 40
        else:
            return 20
    
    @staticmethod
    def _generate_explanation(score: int, label: str, corpus: float, volatility: float, time: float) -> str:
        """Generate human-readable explanation"""
        if label == "Strong Outlook":
            return (
                f"Your retirement projection is strong with a score of {score}/100. "
                f"The median corpus is substantial (corpus strength: {corpus:.0f}%), and you have "
                f"adequate time to benefit from compounding. The downside scenario remains reasonable, "
                f"providing cushion against adverse market conditions."
            )
        elif label == "Moderate Confidence":
            return (
                f"Your retirement readiness score is {score}/100, indicating moderate confidence. "
                f"The projected corpus aligns with your likely requirements (corpus strength: {corpus:.0f}%), "
                f"though there is limited buffer (volatility score: {volatility:.0f}%). Continue your current contribution plan "
                f"and monitor progress periodically."
            )
        else:
            return (
                f"Your readiness score of {score}/100 suggests high risk. The projected corpus "
                f"(corpus strength: {corpus:.0f}%) falls short of typical retirement needs. "
                f"Consider increasing contributions, extending work years (time value: {time:.0f}%), "
                f"or reviewing expense assumptions."
            )
    
    @staticmethod
    def _generate_recommendation(label: str, corpus: float, volatility: float, time: float) -> str:
        """Generate actionable recommendation"""
        if label == "Strong Outlook":
            return "Continue current savings plan. Consider consulting a financial advisor for tax optimization and post-retirement income strategies."
        elif label == "Moderate Confidence":
            if corpus < 70:
                return "Increase monthly contributions by 10-20% if possible to strengthen corpus. Review investment allocation for optimal risk-return balance."
            elif time < 60:
                return "With limited time remaining, focus on capital preservation. Consider shifting to dividend-yielding investments."
            else:
                return "Monitor annually and adjust contributions as income grows. Stay the course with consistent investing discipline."
        else:
            recommendations = []
            if corpus < 50:
                recommendations.append("Increase contributions significantly (20%+ if feasible)")
            if time > 60:
                recommendations.append(f"Work 2-3 additional years (time horizon boost to {time:.0f}%)")
            if volatility < 50:
                recommendations.append("Your projections are uncertain—seek professional financial guidance")
            recommendation = "; ".join(recommendations) if recommendations else "Seek professional financial advisory guidance"
            return f"Action needed: {recommendation}."
