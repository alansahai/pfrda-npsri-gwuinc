"""
Insight Generation Service
Generates intelligent financial insights from retirement projection data
"""
from typing import List, Dict, Any
from enum import Enum
import logging

from app.models.schemas import RiskProfile

logger = logging.getLogger(__name__)


class InsightSeverity(str, Enum):
    """Severity levels for insights"""
    INFO = "info"
    WARNING = "warning"
    POSITIVE = "positive"


class InsightGenerator:
    """Generates intelligent insights from retirement projection data"""
    
    def generate_insights(
        self,
        p10: float,
        p50: float,
        p90: float,
        total_contributions: float,
        years_to_retirement: int,
        risk_profile: RiskProfile
    ) -> List[Dict[str, Any]]:
        """
        Generate comprehensive insights from projection data
        
        Args:
            p10: 10th percentile corpus value
            p50: 50th percentile (median) corpus value
            p90: 90th percentile corpus value
            total_contributions: Total amount contributed over investment period
            years_to_retirement: Number of years until retirement
            risk_profile: Investment risk profile
            
        Returns:
            List of insight objects with title, message, and severity
        """
        insights = []
        
        # 1. Risk Interpretation & Variability
        insights.extend(self._generate_risk_interpretation(p10, p50, p90))
        
        # 2. Contribution vs Corpus Insight
        insights.extend(self._generate_contribution_insight(
            p50, total_contributions, years_to_retirement
        ))
        
        # 3. Risk Warning
        insights.extend(self._generate_risk_warning(p10, p50, p90, risk_profile))
        
        # 4. Confidence Statements
        insights.extend(self._generate_confidence_statements(p10, p50, p90))
        
        # 5. Investment Horizon Insight
        insights.extend(self._generate_horizon_insight(years_to_retirement))
        
        # 6. Goal Achievement Insight
        insights.extend(self._generate_goal_insight(p50, total_contributions))
        
        logger.info(f"Generated {len(insights)} insights for projection")
        return insights
    
    def _generate_risk_interpretation(
        self,
        p10: float,
        p50: float,
        p90: float
    ) -> List[Dict[str, Any]]:
        """Generate insights about risk and variability"""
        insights = []
        
        # Calculate variability
        range_value = p90 - p10
        variability_pct = (range_value / p50) * 100
        
        # Format currency values
        p10_formatted = self._format_currency(p10)
        p50_formatted = self._format_currency(p50)
        p90_formatted = self._format_currency(p90)
        
        # Risk interpretation insight
        if variability_pct < 30:
            severity = InsightSeverity.POSITIVE
            variability_desc = "relatively stable"
        elif variability_pct < 50:
            severity = InsightSeverity.INFO
            variability_desc = "moderate"
        else:
            severity = InsightSeverity.WARNING
            variability_desc = "significant"
        
        insights.append({
            "title": "Projection Range Analysis",
            "message": (
                f"Your retirement corpus projection shows a {variability_desc} range. "
                f"In a conservative scenario (10th percentile), you could accumulate {p10_formatted}, "
                f"while in an optimistic scenario (90th percentile), it could reach {p90_formatted}. "
                f"The median projection is {p50_formatted}."
            ),
            "severity": severity.value
        })
        
        # Variability percentage insight
        if variability_pct > 40:
            insights.append({
                "title": "Market Volatility Notice",
                "message": (
                    f"Your portfolio exhibits {variability_pct:.1f}% variability between "
                    f"conservative and optimistic scenarios. This indicates significant market risk. "
                    f"Consider diversifying your investments or adopting a more conservative strategy "
                    f"if you prefer more predictable outcomes."
                ),
                "severity": InsightSeverity.WARNING.value
            })
        
        return insights
    
    def _generate_contribution_insight(
        self,
        median_corpus: float,
        total_contributions: float,
        years: int
    ) -> List[Dict[str, Any]]:
        """Generate insights about contributions vs final corpus"""
        insights = []
        
        # Calculate returns generated
        returns_generated = median_corpus - total_contributions
        returns_multiple = median_corpus / total_contributions if total_contributions > 0 else 0
        returns_pct = ((median_corpus - total_contributions) / total_contributions * 100) if total_contributions > 0 else 0
        
        median_formatted = self._format_currency(median_corpus)
        contributions_formatted = self._format_currency(total_contributions)
        returns_formatted = self._format_currency(returns_generated)
        
        # Compounding impact insight
        if returns_multiple >= 3:
            severity = InsightSeverity.POSITIVE
            impact_desc = "excellent"
        elif returns_multiple >= 2:
            severity = InsightSeverity.POSITIVE
            impact_desc = "strong"
        else:
            severity = InsightSeverity.INFO
            impact_desc = "moderate"
        
        insights.append({
            "title": "Power of Compounding",
            "message": (
                f"You will contribute a total of {contributions_formatted} over {years} years. "
                f"Through the power of compounding, your median projected corpus is {median_formatted}. "
                f"This means your investments could generate approximately {returns_formatted} "
                f"in returns ({returns_pct:.0f}% growth), demonstrating the {impact_desc} impact "
                f"of long-term investing."
            ),
            "severity": severity.value
        })
        
        return insights
    
    def _generate_risk_warning(
        self,
        p10: float,
        p50: float,
        p90: float,
        risk_profile: RiskProfile
    ) -> List[Dict[str, Any]]:
        """Generate risk-specific warnings"""
        insights = []
        
        # Calculate downside risk
        downside_risk_pct = ((p50 - p10) / p50) * 100
        
        # Risk profile specific warnings
        if risk_profile == RiskProfile.AGGRESSIVE and downside_risk_pct > 35:
            insights.append({
                "title": "Aggressive Portfolio Alert",
                "message": (
                    f"Your aggressive investment strategy has a {downside_risk_pct:.1f}% downside risk. "
                    f"While this offers higher growth potential, there's also significant volatility. "
                    f"In unfavorable market conditions, your corpus could be substantially lower than "
                    f"the median projection. Ensure you're comfortable with this level of risk."
                ),
                "severity": InsightSeverity.WARNING.value
            })
        
        elif risk_profile == RiskProfile.CONSERVATIVE:
            upside_potential_pct = ((p90 - p50) / p50) * 100
            if upside_potential_pct > 30:
                insights.append({
                    "title": "Conservative Growth Opportunity",
                    "message": (
                        f"While your conservative strategy minimizes risk, you're potentially "
                        f"leaving {upside_potential_pct:.1f}% upside on the table compared to "
                        f"moderate or aggressive strategies. If you have a longer investment "
                        f"horizon, consider gradually increasing your risk exposure."
                    ),
                    "severity": InsightSeverity.INFO.value
                })
        
        return insights
    
    def _generate_confidence_statements(
        self,
        p10: float,
        p50: float,
        p90: float
    ) -> List[Dict[str, Any]]:
        """Generate probability-based confidence statements"""
        insights = []
        
        p50_formatted = self._format_currency(p50)
        p90_formatted = self._format_currency(p90)
        p10_formatted = self._format_currency(p10)
        
        # 50% confidence statement
        insights.append({
            "title": "Probability Assessment",
            "message": (
                f"There is a 50% probability that your retirement corpus will exceed {p50_formatted}, "
                f"and a 10% probability it could reach {p90_formatted} or more. "
                f"Conversely, there is a 10% chance it may be {p10_formatted} or less. "
                f"These projections help you understand the range of potential outcomes."
            ),
            "severity": InsightSeverity.INFO.value
        })
        
        return insights
    
    def _generate_horizon_insight(
        self,
        years: int
    ) -> List[Dict[str, Any]]:
        """Generate insights based on investment horizon"""
        insights = []
        
        if years >= 25:
            insights.append({
                "title": "Long Investment Horizon Advantage",
                "message": (
                    f"With {years} years until retirement, you have a substantial investment horizon. "
                    f"This allows your investments to weather market volatility and benefit from "
                    f"long-term compounding. Consider maintaining or even increasing your equity "
                    f"exposure to maximize growth potential."
                ),
                "severity": InsightSeverity.POSITIVE.value
            })
        elif years <= 10:
            insights.append({
                "title": "Approaching Retirement",
                "message": (
                    f"With only {years} years until retirement, you're in the critical phase of "
                    f"your investment journey. Consider gradually shifting to more conservative "
                    f"investments to protect your accumulated corpus from market volatility. "
                    f"It's also a good time to finalize your retirement income strategy."
                ),
                "severity": InsightSeverity.INFO.value
            })
        
        return insights
    
    def _generate_goal_insight(
        self,
        median_corpus: float,
        total_contributions: float
    ) -> List[Dict[str, Any]]:
        """Generate insights about goal achievement"""
        insights = []
        
        # Calculate if corpus growth is on track
        returns_multiple = median_corpus / total_contributions if total_contributions > 0 else 0
        
        if returns_multiple >= 2.5:
            insights.append({
                "title": "Strong Growth Trajectory",
                "message": (
                    f"Your investment plan shows strong growth potential with an expected return "
                    f"multiple of {returns_multiple:.1f}x. This suggests you're on track to build "
                    f"a substantial retirement corpus. Continue with disciplined contributions and "
                    f"periodic reviews to stay on course."
                ),
                "severity": InsightSeverity.POSITIVE.value
            })
        elif returns_multiple < 1.5:
            insights.append({
                "title": "Growth Optimization Opportunity",
                "message": (
                    f"Your projected return multiple ({returns_multiple:.1f}x) suggests room for "
                    f"improvement. Consider increasing your monthly contributions, extending your "
                    f"investment horizon, or adopting a slightly more aggressive investment strategy "
                    f"to enhance your retirement corpus."
                ),
                "severity": InsightSeverity.WARNING.value
            })
        
        return insights
    
    def _format_currency(self, amount: float) -> str:
        """Format amount as Indian currency with proper notation"""
        if amount >= 10000000:  # 1 crore or more
            crores = amount / 10000000
            return f"₹{crores:.2f} crore"
        elif amount >= 100000:  # 1 lakh or more
            lakhs = amount / 100000
            return f"₹{lakhs:.2f} lakh"
        else:
            return f"₹{amount:,.0f}"
    
    def generate_scenario_comparison_insights(
        self,
        conservative_median: float,
        moderate_median: float,
        aggressive_median: float,
        years: int
    ) -> List[Dict[str, Any]]:
        """Generate insights for scenario comparison"""
        insights = []
        
        conservative_formatted = self._format_currency(conservative_median)
        moderate_formatted = self._format_currency(moderate_median)
        aggressive_formatted = self._format_currency(aggressive_median)
        
        # Compare conservative to moderate
        conservative_to_moderate_diff = moderate_median - conservative_median
        conservative_to_moderate_pct = (conservative_to_moderate_diff / conservative_median) * 100
        
        # Compare moderate to aggressive
        moderate_to_aggressive_diff = aggressive_median - moderate_median
        moderate_to_aggressive_pct = (moderate_to_aggressive_diff / moderate_median) * 100
        
        insights.append({
            "title": "Risk vs Reward Comparison",
            "message": (
                f"Moving from Conservative to Moderate strategy could increase your corpus by "
                f"{self._format_currency(conservative_to_moderate_diff)} "
                f"({conservative_to_moderate_pct:.1f}%). "
                f"Further moving to Aggressive strategy could add another "
                f"{self._format_currency(moderate_to_aggressive_diff)} "
                f"({moderate_to_aggressive_pct:.1f}%). "
                f"However, higher returns come with increased volatility."
            ),
            "severity": InsightSeverity.INFO.value
        })
        
        # Long horizon recommendation
        if years >= 20:
            insights.append({
                "title": "Long Horizon Strategy Recommendation",
                "message": (
                    f"With {years} years until retirement, you can afford to take more risk. "
                    f"A Moderate or Aggressive strategy could significantly boost your corpus "
                    f"while allowing time to recover from market downturns. "
                    f"Consider your risk tolerance and gradually shift to conservative as you "
                    f"approach retirement."
                ),
                "severity": InsightSeverity.POSITIVE.value
            })
        
        return insights
    
    def generate_reverse_calculator_insights(
        self,
        target_pension: float,
        required_contribution: float,
        required_corpus: float,
        total_investment: float,
        years: int
    ) -> List[Dict[str, Any]]:
        """Generate insights for reverse pension calculator"""
        insights = []
        
        target_formatted = self._format_currency(target_pension)
        contribution_formatted = self._format_currency(required_contribution)
        corpus_formatted = self._format_currency(required_corpus)
        investment_formatted = self._format_currency(total_investment)
        
        # Feasibility assessment
        contribution_to_pension_ratio = required_contribution / target_pension
        
        if contribution_to_pension_ratio <= 0.15:
            severity = InsightSeverity.POSITIVE
            feasibility = "highly achievable"
        elif contribution_to_pension_ratio <= 0.25:
            severity = InsightSeverity.POSITIVE
            feasibility = "achievable"
        elif contribution_to_pension_ratio <= 0.40:
            severity = InsightSeverity.INFO
            feasibility = "moderately challenging"
        else:
            severity = InsightSeverity.WARNING
            feasibility = "challenging"
        
        insights.append({
            "title": "Target Pension Feasibility",
            "message": (
                f"To achieve your target monthly pension of {target_formatted}, "
                f"you need to contribute {contribution_formatted} per month for {years} years. "
                f"This is {feasibility} given the contribution-to-pension ratio of "
                f"{contribution_to_pension_ratio:.1%}."
            ),
            "severity": severity.value
        })
        
        # Investment vs corpus comparison
        returns_multiple = required_corpus / total_investment if total_investment > 0 else 0
        
        insights.append({
            "title": "Required Investment Growth",
            "message": (
                f"You will need to invest a total of {investment_formatted} over {years} years "
                f"to build a corpus of {corpus_formatted}. "
                f"This requires a return multiple of {returns_multiple:.1f}x through market growth "
                f"and compounding. This is based on your selected risk profile assumptions."
            ),
            "severity": InsightSeverity.INFO.value
        })
        
        # Alternative suggestions if challenging
        if contribution_to_pension_ratio > 0.40:
            insights.append({
                "title": "Alternative Strategies",
                "message": (
                    f"The required contribution is relatively high. Consider: "
                    f"(1) Extending your retirement age by 2-3 years, "
                    f"(2) Adopting a higher-risk investment strategy for better returns, "
                    f"(3) Adjusting your target pension expectation, or "
                    f"(4) Starting with a smaller target and gradually increasing contributions."
                ),
                "severity": InsightSeverity.WARNING.value
            })
        
        return insights
    
    def generate_strategic_suggestions(
        self,
        required_contribution: float,
        years_to_retirement: int,
        risk_profile: RiskProfile,
        required_corpus: float
    ) -> List[str]:
        """
        Generate strategic suggestions based on reverse calculator analysis
        
        Rules:
        1. If required SIP > ₹30,000: Suggest increasing retirement age
        2. If years_to_retirement < 10: Suggest moderate risk shift
        3. If aggressive risk + high expected volatility: Suggest rebalancing
        
        Args:
            required_contribution: Required monthly contribution amount
            years_to_retirement: Years until retirement
            risk_profile: Selected investment risk profile
            required_corpus: Required corpus to achieve pension target
        
        Returns:
            List of strategic suggestions
        """
        suggestions = []
        
        # Rule 1: High required contribution
        if required_contribution > 30000:
            contribution_formatted = self._format_currency(required_contribution)
            additional_years_needed = 3  # Suggest 3 additional years
            
            suggestions.append(
                f"Your required monthly contribution of {contribution_formatted} is quite high. "
                f"Consider extending your retirement age by {additional_years_needed} years, which could "
                f"significantly reduce your monthly burden while allowing more time for wealth accumulation."
            )
        
        # Rule 2: Short time horizon
        if years_to_retirement < 10:
            if risk_profile == RiskProfile.CONSERVATIVE:
                suggestions.append(
                    f"With only {years_to_retirement} years to retirement and a conservative approach, "
                    f"your growth potential is limited. Consider shifting to a moderate risk profile "
                    f"to achieve better returns and reduce the required contribution amount."
                )
            elif risk_profile == RiskProfile.MODERATE:
                suggestions.append(
                    f"Your {years_to_retirement}-year timeline is relatively short. Maximize your contributions "
                    f"in these critical years and consider keeping a moderate-to-aggressive allocation "
                    f"to capture growth opportunities while time is still on your side."
                )
            else:  # AGGRESSIVE
                suggestions.append(
                    f"With {years_to_retirement} years remaining, your aggressive strategy carries significant risk. "
                    f"Consider a balanced approach: maintain some aggressive exposure for growth, "
                    f"but start gradually shifting to moderate allocations to protect gains."
                )
        
        # Rule 3: Aggressive risk profile with potential high volatility
        if risk_profile == RiskProfile.AGGRESSIVE:
            # Aggressive profile typically has high volatility (standard assumption)
            # Expected volatility for aggressive is ~40-50% based on return ranges
            suggestions.append(
                "Your aggressive risk profile may result in high portfolio volatility (30%+ variation). "
                "Consider periodic rebalancing to maintain your target allocation and reduce downside risk. "
                "Review your portfolio quarterly and rebalance when any asset class deviates by more than 5% "
                "from its target weight."
            )
            
            # Additional suggestion if both aggressive AND short timeline
            if years_to_retirement < 5:
                suggestions.append(
                    "CRITICAL: Combining aggressive risk with a very short timeline is highly risky. "
                    "Consider immediately shifting 40-50% of your portfolio to conservative assets "
                    "(bonds, fixed deposits) to provide a safety cushion as retirement approaches."
                )
        
        # Additional suggestion if contribution is manageable but years are limited
        if required_contribution <= 30000 and years_to_retirement < 10 and not suggestions:
            suggestions.append(
                f"Your required contribution is manageable at {self._format_currency(required_contribution)}, "
                f"but with only {years_to_retirement} years remaining, consistency is critical. "
                f"Set up automatic monthly transfers and avoid skipping contributions to stay on track."
            )
        
        # Default suggestion if no specific triggers
        if not suggestions:
            suggestions.append(
                "Your retirement plan appears balanced. Maintain disciplined contributions, "
                "review your progress annually, and adjust as needed based on life changes or market conditions."
            )
        
        return suggestions
    
    def calculate_readiness_score(
        self,
        median_corpus: float,
        required_corpus: float,
        years_to_retirement: int,
        risk_profile: RiskProfile
    ) -> Dict[str, any]:
        """
        Calculate retirement readiness score from 0 to 100
        
        Scoring components:
        1. Corpus adequacy (60%): Compare projected vs required corpus
        2. Risk stability (20%): Penalize high volatility profiles
        3. Time horizon (20%): Reward longer investment periods
        
        Args:
            median_corpus: Projected median corpus at retirement
            required_corpus: Required corpus to meet pension target
            years_to_retirement: Years until retirement
            risk_profile: Investment risk profile
        
        Returns:
            Dictionary with score, label, details, and recommendation
        """
        # Component 1: Corpus Adequacy Score (0-60 points)
        if required_corpus > 0:
            adequacy_ratio = median_corpus / required_corpus
            adequacy_score = min(adequacy_ratio * 60, 60)
        else:
            adequacy_score = 60  # No target set, assume adequate
        
        # Component 2: Risk Stability Score (0-20 points)
        # Lower risk = higher stability score
        risk_scores = {
            RiskProfile.CONSERVATIVE: 20,
            RiskProfile.MODERATE: 15,
            RiskProfile.AGGRESSIVE: 10
        }
        stability_score = risk_scores.get(risk_profile, 15)
        
        # Component 3: Time Horizon Score (0-20 points)
        # More time = better recovery potential
        if years_to_retirement >= 21:
            horizon_score = 20
        elif years_to_retirement >= 11:
            horizon_score = 15
        elif years_to_retirement >= 6:
            horizon_score = 10
        else:
            horizon_score = 5
        
        # Calculate total score
        total_score = int(adequacy_score + stability_score + horizon_score)
        
        # Determine label
        if total_score >= 71:
            label = "Strong Outlook"
        elif total_score >= 41:
            label = "Moderate Confidence"
        else:
            label = "High Risk"
        
        # Generate recommendation
        recommendation = self._generate_readiness_recommendation(
            total_score,
            adequacy_ratio if required_corpus > 0 else 1.0,
            years_to_retirement,
            risk_profile
        )
        
        return {
            "score": total_score,
            "label": label,
            "details": {
                "corpus_adequacy_score": round(adequacy_score, 2),
                "risk_stability_score": stability_score,
                "time_horizon_score": horizon_score,
                "adequacy_ratio": round(adequacy_ratio if required_corpus > 0 else 1.0, 2)
            },
            "recommendation": recommendation
        }
    
    def _generate_readiness_recommendation(
        self,
        score: int,
        adequacy_ratio: float,
        years: int,
        risk_profile: RiskProfile
    ) -> str:
        """Generate actionable recommendation based on readiness score"""
        
        if score >= 71:
            # Strong Outlook - but differentiate by adequacy ratio
            if adequacy_ratio >= 1.0:
                return (
                    "Excellent readiness. Your projected corpus exceeds your target. "
                    "Continue your current investment strategy and review annually to maintain alignment with goals."
                )
            elif adequacy_ratio >= 0.85:
                return (
                    "Good readiness. You're nearly on target with a slight shortfall. "
                    "Consider modest contribution increases of 5-10% to close the gap and build a safety buffer."
                )
            else:
                return (
                    "On track but with a noticeable gap. Your strong time horizon and stable risk profile work in your favor. "
                    "Increase contributions by 10-15% or optimize investment allocation to reach your target."
                )
        
        elif score >= 41:
            if adequacy_ratio < 0.8:
                return (
                    "Moderate readiness, but corpus may fall short of target. "
                    "Consider increasing monthly contributions by 15-20% or extending your retirement timeline by 2-3 years."
                )
            elif years < 10:
                return (
                    "Moderate readiness with limited time horizon. "
                    "Focus on maximizing contributions now and consider a more aggressive investment approach if appropriate."
                )
            else:
                return (
                    "Good trajectory. Monitor your progress quarterly and adjust contributions "
                    "as your income grows to ensure you stay on track."
                )
        
        else:  # High Risk (0-40)
            if adequacy_ratio < 0.5:
                return (
                    "Significant gap between projected and required corpus. "
                    "URGENT: Increase contributions by at least 50%, consider delaying retirement by 5+ years, "
                    "or reassess your pension target expectations."
                )
            elif years < 5:
                return (
                    "Critical: Very short timeline with inadequate corpus projection. "
                    "Immediate action needed: Maximize contributions, consider part-time work post-retirement, "
                    "or delay retirement to allow more accumulation time."
                )
            elif risk_profile == RiskProfile.CONSERVATIVE:
                return (
                    "Your conservative approach may limit growth potential. "
                    "Consider shifting to a moderate risk profile to boost returns, "
                    "and increase monthly contributions by 30-40%."
                )
            else:
                return (
                    "High risk of retirement income shortfall. "
                    "Develop a comprehensive catch-up strategy: increase contributions substantially, "
                    "extend your working years, and seek professional financial advice."
                )
    
    def calculate_volatility_index(
        self,
        standard_deviation: float,
        mean_corpus: float
    ) -> Dict[str, any]:
        """
        Calculate volatility index using coefficient of variation
        
        The coefficient of variation (CV) expresses standard deviation as a 
        percentage of the mean, providing a normalized measure of volatility.
        
        Classification:
        - Low volatility: CV < 15% (stable, predictable)
        - Medium volatility: CV 15-30% (moderate uncertainty)
        - High volatility: CV > 30% (significant variability)
        
        Args:
            standard_deviation: Standard deviation of corpus projections
            mean_corpus: Mean corpus value from simulations
        
        Returns:
            Dictionary with volatility_percentage, volatility_level, and explanation
        """
        # Calculate coefficient of variation as percentage
        volatility_percentage = (standard_deviation / mean_corpus) * 100
        
        # Classify volatility level
        if volatility_percentage < 15:
            volatility_level = "low"
            risk_description = "stable and predictable"
            recommendation = (
                "Your retirement projections show low variability, indicating a stable investment path. "
                "This suggests consistent growth with minimal downside risk. Continue your disciplined "
                "approach and maintain regular contributions."
            )
        elif volatility_percentage <= 30:
            volatility_level = "medium"
            risk_description = "moderately uncertain"
            recommendation = (
                "Your projections show moderate volatility, which is typical for balanced portfolios. "
                "While there's some variability in outcomes, this level of volatility is manageable. "
                "Consider diversifying further if risk tolerance is low, or maintain current strategy "
                "if comfortable with moderate fluctuations."
            )
        else:
            volatility_level = "high"
            risk_description = "highly variable"
            recommendation = (
                "High volatility indicates significant uncertainty in retirement outcomes. "
                "This could be due to an aggressive investment strategy or long time horizons amplifying variance. "
                "Consider: (1) Rebalancing toward more stable assets if near retirement, "
                "(2) Increasing contribution consistency to reduce reliance on market timing, or "
                "(3) Accepting higher volatility if you have time and risk tolerance."
            )
        
        # Generate detailed explanation
        mean_formatted = self._format_currency(mean_corpus)
        std_formatted = self._format_currency(standard_deviation)
        
        explanation = (
            f"Your retirement corpus projections have a volatility index of {volatility_percentage:.1f}%, "
            f"classified as {volatility_level} volatility. With a mean corpus of {mean_formatted} "
            f"and standard deviation of {std_formatted}, your outcomes are {risk_description}. "
            f"{recommendation}"
        )
        
        return {
            "volatility_percentage": round(volatility_percentage, 2),
            "volatility_level": volatility_level,
            "explanation": explanation
        }
