"""
Retirement Projection Service
High-level service for retirement projections and scenario analysis
"""
import logging
from typing import Dict, Any, List

from app.models.schemas import (
    RetirementProjectionRequest,
    RetirementProjectionResponse,
    ScenarioComparisonRequest,
    ScenarioComparisonResponse,
    ReversePensionRequest,
    ReversePensionResponse,
    RiskProfile,
    ProbabilityDistribution,
    AnnuityBreakdown,
    ScenarioResult
)
from app.services.financial_calculator import FinancialCalculator
from app.core.config import settings

logger = logging.getLogger(__name__)


class ProjectionService:
    """Service for handling retirement projection requests"""
    
    def __init__(self):
        """Initialize projection service with financial calculator"""
        self.calculator = FinancialCalculator()
    
    def generate_retirement_projection(
        self,
        request: RetirementProjectionRequest
    ) -> RetirementProjectionResponse:
        """
        Generate retirement corpus projection based on request parameters
        
        Args:
            request: Validated retirement projection request
            
        Returns:
            Complete retirement projection response
        """
        logger.info(
            f"Generating retirement projection - Age: {request.current_age}, "
            f"Retirement: {request.retirement_age}, Risk: {request.risk_profile.value}"
        )
        
        # Calculate investment years
        investment_years = request.retirement_age - request.current_age
        
        # Get risk parameters
        mean_return, std_return = self.calculator.get_risk_parameters(request.risk_profile)
        
        # Determine simulation iterations
        iterations = request.simulation_iterations or settings.DEFAULT_SIMULATION_ITERATIONS
        
        # Convert percentage to decimal
        annual_growth_rate = request.annual_income_growth / 100.0
        
        # Run Monte Carlo simulation
        corpus_array = self.calculator.calculate_monte_carlo_projection(
            monthly_contribution=request.monthly_contribution,
            years=investment_years,
            annual_growth_rate=annual_growth_rate,
            mean_return=mean_return,
            std_return=std_return,
            iterations=iterations
        )
        
        # Calculate percentile distribution
        distribution = self.calculator.calculate_percentiles(corpus_array)
        
        # Use median corpus for annuity breakdown
        median_corpus = distribution["percentile_50"]
        annuity_breakdown = self.calculator.calculate_annuity_breakdown(median_corpus)
        
        # Calculate total contributions
        total_contributions = self.calculator.calculate_total_contributions(
            request.monthly_contribution,
            investment_years,
            annual_growth_rate
        )
        
        # Build response
        response = RetirementProjectionResponse(
            input_summary={
                "current_age": request.current_age,
                "retirement_age": request.retirement_age,
                "monthly_contribution": request.monthly_contribution,
                "annual_income_growth": request.annual_income_growth,
                "risk_profile": request.risk_profile.value
            },
            investment_years=investment_years,
            total_contributions=total_contributions,
            corpus_projection=ProbabilityDistribution(**distribution),
            annuity_breakdown=AnnuityBreakdown(**annuity_breakdown),
            risk_profile=request.risk_profile,
            simulation_info={
                "iterations": iterations,
                "mean_return_used": f"{mean_return * 100:.2f}%",
                "std_deviation": f"{std_return * 100:.2f}%"
            },
            assumptions={
                "annuity_rate": f"{settings.DEFAULT_ANNUITY_RATE}%",
                "annuity_allocation": f"{settings.ANNUITY_ALLOCATION_MIN}%",
                "lump_sum_allocation": f"{settings.LUMP_SUM_MAX}%",
                "disclaimer": "These projections are estimates based on assumed returns. "
                             "Actual results may vary depending on market conditions."
            }
        )
        
        logger.info(
            f"Projection completed - Median corpus: ₹{median_corpus:,.2f}, "
            f"Monthly pension: ₹{annuity_breakdown['monthly_pension']:,.2f}"
        )
        
        return response
    
    def compare_scenarios(
        self,
        request: ScenarioComparisonRequest
    ) -> ScenarioComparisonResponse:
        """
        Compare retirement projections across all risk profiles
        
        Args:
            request: Validated scenario comparison request
            
        Returns:
            Comparison of all three risk scenarios
        """
        logger.info(
            f"Comparing scenarios - Age: {request.current_age}, "
            f"Retirement: {request.retirement_age}"
        )
        
        investment_years = request.retirement_age - request.current_age
        annual_growth_rate = request.annual_income_growth / 100.0
        iterations = settings.DEFAULT_SIMULATION_ITERATIONS
        
        scenarios: List[ScenarioResult] = []
        
        # Run projections for each risk profile
        for risk_profile in [RiskProfile.CONSERVATIVE, RiskProfile.MODERATE, RiskProfile.AGGRESSIVE]:
            mean_return, std_return = self.calculator.get_risk_parameters(risk_profile)
            
            # Run simulation
            corpus_array = self.calculator.calculate_monte_carlo_projection(
                monthly_contribution=request.monthly_contribution,
                years=investment_years,
                annual_growth_rate=annual_growth_rate,
                mean_return=mean_return,
                std_return=std_return,
                iterations=iterations
            )
            
            # Calculate distribution
            distribution = self.calculator.calculate_percentiles(corpus_array)
            median_corpus = distribution["percentile_50"]
            
            # Calculate annuity breakdown
            annuity_breakdown = self.calculator.calculate_annuity_breakdown(median_corpus)
            
            # Create scenario result
            scenario = ScenarioResult(
                risk_profile=risk_profile,
                median_corpus=median_corpus,
                percentile_10=distribution["percentile_10"],
                percentile_90=distribution["percentile_90"],
                monthly_pension=annuity_breakdown["monthly_pension"],
                lump_sum=annuity_breakdown["lump_sum"]
            )
            
            scenarios.append(scenario)
        
        # Calculate comparative insights
        conservative = scenarios[0]
        moderate = scenarios[1]
        aggressive = scenarios[2]
        
        comparison_insights = {
            "corpus_range": {
                "minimum": conservative.percentile_10,
                "maximum": aggressive.percentile_90
            },
            "median_corpus_comparison": {
                "conservative": conservative.median_corpus,
                "moderate": moderate.median_corpus,
                "aggressive": aggressive.median_corpus
            },
            "pension_comparison": {
                "conservative": conservative.monthly_pension,
                "moderate": moderate.monthly_pension,
                "aggressive": aggressive.monthly_pension
            },
            "risk_reward_analysis": {
                "conservative_to_moderate_upside": (
                    (moderate.median_corpus - conservative.median_corpus) / conservative.median_corpus * 100
                ),
                "moderate_to_aggressive_upside": (
                    (aggressive.median_corpus - moderate.median_corpus) / moderate.median_corpus * 100
                )
            }
        }
        
        response = ScenarioComparisonResponse(
            input_summary={
                "current_age": request.current_age,
                "retirement_age": request.retirement_age,
                "monthly_contribution": request.monthly_contribution,
                "annual_income_growth": request.annual_income_growth,
                "investment_years": investment_years
            },
            scenarios=scenarios,
            comparison_insights=comparison_insights
        )
        
        logger.info(f"Scenario comparison completed for {len(scenarios)} profiles")
        return response
    
    def calculate_reverse_pension(
        self,
        request: ReversePensionRequest
    ) -> ReversePensionResponse:
        """
        Calculate required contributions to achieve desired pension
        
        Args:
            request: Validated reverse pension request
            
        Returns:
            Required contribution and feasibility analysis
        """
        logger.info(
            f"Calculating reverse pension - Target: ₹{request.desired_monthly_pension:,.2f}/month"
        )
        
        investment_years = request.retirement_age - request.current_age
        annual_growth_rate = request.annual_income_growth / 100.0
        
        # Get risk parameters
        mean_return, _ = self.calculator.get_risk_parameters(request.risk_profile)
        
        # Calculate required corpus for desired pension
        required_corpus = self.calculator.calculate_required_corpus_for_pension(
            request.desired_monthly_pension
        )
        
        # Calculate required monthly contribution
        required_contribution = self.calculator.calculate_required_monthly_contribution(
            target_corpus=required_corpus,
            years=investment_years,
            annual_growth_rate=annual_growth_rate,
            mean_return=mean_return
        )
        
        # Calculate total investment
        total_investment = self.calculator.calculate_total_contributions(
            required_contribution,
            investment_years,
            annual_growth_rate
        )
        
        # Feasibility analysis
        feasibility_analysis = {
            "required_vs_target_ratio": required_contribution / request.desired_monthly_pension,
            "investment_multiple": required_corpus / total_investment,
            "feasibility_rating": self._assess_feasibility(
                required_contribution, investment_years, annual_growth_rate
            ),
            "alternative_strategies": self._generate_alternative_strategies(
                required_contribution, investment_years
            )
        }
        
        response = ReversePensionResponse(
            target_pension=request.desired_monthly_pension,
            required_corpus=required_corpus,
            required_monthly_contribution=required_contribution,
            total_investment_required=total_investment,
            investment_years=investment_years,
            feasibility_analysis=feasibility_analysis,
            risk_profile=request.risk_profile
        )
        
        logger.info(
            f"Reverse calculation completed - Required contribution: ₹{required_contribution:,.2f}/month"
        )
        
        return response
    
    def _assess_feasibility(
        self,
        required_contribution: float,
        years: int,
        growth_rate: float
    ) -> str:
        """Assess feasibility of required contribution"""
        
        if required_contribution < 5000:
            return "Highly Feasible"
        elif required_contribution < 15000:
            return "Feasible"
        elif required_contribution < 30000:
            return "Moderately Challenging"
        elif required_contribution < 50000:
            return "Challenging"
        else:
            return "Highly Challenging - Consider Alternative Strategies"
    
    def _generate_alternative_strategies(
        self,
        required_contribution: float,
        years: int
    ) -> List[str]:
        """Generate alternative strategy suggestions"""
        
        strategies = []
        
        if required_contribution > 20000:
            strategies.append("Consider increasing retirement age by 2-3 years")
            strategies.append("Explore higher-risk investment profiles for better returns")
        
        if years < 15:
            strategies.append("Start investing earlier if possible for compounding benefits")
        
        if required_contribution > 30000:
            strategies.append("Consider reducing target pension expectation")
            strategies.append("Explore additional retirement savings vehicles")
        
        return strategies or ["Current plan is on track"]
