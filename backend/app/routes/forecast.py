"""
Retirement forecasting and pension calculation endpoints
"""
from fastapi import APIRouter, HTTPException

from app.core.logging_config import get_logger
from app.core.exceptions import ValidationException, CalculationException
from app.models.schemas import (
    RetirementInput,
    RetirementForecastResponse,
    ScenarioComparisonRequest,
    ScenarioComparisonResponse,
    ReversePensionRequest,
    ReversePensionResponse,
    PensionProjection,
    PensionEstimate,
    ScenarioResult,
    RiskProfile,
    Insight,
    InsightSeverity,
    ReadinessScoreRequest,
    ReadinessScore,
    VolatilityIndexRequest,
    VolatilityIndex,
    ConfidenceInterval,
    SensitivityRequest,
    DelayImpactRequest
)
from app.services.monte_carlo_simulator import MonteCarloSimulator
from app.services.financial_calculator import FinancialCalculator
from app.services.insight_generator import InsightGenerator
from app.services.annuity_manager import AnnuityManager
from app.services.readiness_analyzer import ReadinessAnalyzer
from app.services.sensitivity_analyzer import SensitivityAnalyzer
from app.services.delay_simulator import DelaySimulator

router = APIRouter(prefix="/forecast", tags=["Forecast"])
logger = get_logger(__name__)

# Initialize insight generator
insight_generator = InsightGenerator()


@router.post("/retirement", response_model=RetirementForecastResponse)
async def calculate_retirement_forecast(input_data: RetirementInput):
    """
    Calculate retirement corpus and pension forecast using Monte Carlo simulation
    
    Args:
        input_data: Retirement planning input parameters
    
    Returns:
        Complete retirement forecast with corpus projections and pension estimates
    """
    try:
        logger.info(
            f"Processing retirement forecast: age={input_data.current_age}, "
            f"retirement={input_data.retirement_age}, "
            f"contribution={input_data.monthly_contribution}"
        )
        
        # Calculate investment horizon
        years = input_data.retirement_age - input_data.current_age
        
        # Run Monte Carlo simulation
        simulator = MonteCarloSimulator()
        simulation_results = simulator.simulate_retirement_corpus(
            monthly_contribution=input_data.monthly_contribution,
            years=years,
            risk_profile=input_data.risk_profile,
            annual_income_growth=input_data.annual_income_growth,
            iterations=input_data.monte_carlo_iterations
        )
        
        # Calculate total contributions
        total_contributions = FinancialCalculator.calculate_total_contributions(
            initial_monthly_contribution=input_data.monthly_contribution,
            years=years,
            annual_income_growth=input_data.annual_income_growth
        )
        
        # Use new AnnuityManager for transparent pension calculations
        pension_range = AnnuityManager.calculate_pension_range(
            p10_corpus=simulation_results["percentile_10"],
            p50_corpus=simulation_results["percentile_50"],
            p90_corpus=simulation_results["percentile_90"]
        )
        
        # Get risk profile details
        min_return, max_return = FinancialCalculator.get_risk_profile_returns(
            input_data.risk_profile
        )
        
        # Generate insights
        insights = insight_generator.generate_insights(
            p10=simulation_results["percentile_10"],
            p50=simulation_results["percentile_50"],
            p90=simulation_results["percentile_90"],
            total_contributions=total_contributions,
            years_to_retirement=years,
            risk_profile=input_data.risk_profile
        )
        
        # Build response with extended fields
        response = RetirementForecastResponse(
            input_parameters=input_data,
            investment_horizon_years=years,
            total_contributions=total_contributions,
            corpus_projection=PensionProjection(
                percentile_10=simulation_results["percentile_10"],
                percentile_25=simulation_results["percentile_25"],
                percentile_50=simulation_results["percentile_50"],
                percentile_75=simulation_results["percentile_75"],
                percentile_90=simulation_results["percentile_90"],
                mean=simulation_results["mean"],
                std_deviation=simulation_results["std_deviation"]
            ),
            pension_estimate=PensionEstimate(
                lump_sum_amount=pension_range["p50"]["lump_sum_amount"],
                annuity_purchase_amount=pension_range["p50"]["annuity_corpus"],
                monthly_pension_10th=pension_range["p10"]["monthly_pension"],
                monthly_pension_50th=pension_range["p50"]["monthly_pension"],
                monthly_pension_90th=pension_range["p90"]["monthly_pension"]
            ),
            risk_profile_details={
                "min_return": min_return,
                "max_return": max_return
            },
            insights=insights
        )
        
        logger.info(
            f"Forecast completed: corpus_median={simulation_results['percentile_50']:.2f}, "
            f"pension_median={pension_range['p50']['monthly_pension']:.2f}"
        )
        
        return response
    
    except ValidationException as e:
        logger.error(f"Validation error: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except CalculationException as e:
        logger.error(f"Calculation error: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except Exception as e:
        logger.error(f"Unexpected error in retirement forecast: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/scenario-comparison", response_model=ScenarioComparisonResponse)
async def compare_scenarios(request: ScenarioComparisonRequest):
    """
    Compare retirement forecasts across all three risk profiles
    
    Args:
        request: Base retirement parameters
    
    Returns:
        Comparison of conservative, moderate, and aggressive scenarios
    """
    try:
        logger.info("Processing scenario comparison request")
        
        base_input = request.base_input
        years = base_input.retirement_age - base_input.current_age
        
        # Calculate total contributions (same for all scenarios)
        total_contributions = FinancialCalculator.calculate_total_contributions(
            initial_monthly_contribution=base_input.monthly_contribution,
            years=years,
            annual_income_growth=base_input.annual_income_growth
        )
        
        # Run simulations for all risk profiles
        simulator = MonteCarloSimulator()
        scenario_results = []
        
        for risk_profile in RiskProfile:
            logger.info(f"Simulating {risk_profile.value} scenario")
            
            # Run simulation
            simulation_results = simulator.simulate_retirement_corpus(
                monthly_contribution=base_input.monthly_contribution,
                years=years,
                risk_profile=risk_profile,
                annual_income_growth=base_input.annual_income_growth,
                iterations=base_input.monte_carlo_iterations
            )
            
            # Use new AnnuityManager for pension calculations
            pension_range = AnnuityManager.calculate_pension_range(
                p10_corpus=simulation_results["percentile_10"],
                p50_corpus=simulation_results["percentile_50"],
                p90_corpus=simulation_results["percentile_90"]
            )
            
            # Add to results
            scenario_results.append(
                ScenarioResult(
                    risk_profile=risk_profile,
                    corpus_projection=PensionProjection(
                        percentile_10=simulation_results["percentile_10"],
                        percentile_25=simulation_results["percentile_25"],
                        percentile_50=simulation_results["percentile_50"],
                        percentile_75=simulation_results["percentile_75"],
                        percentile_90=simulation_results["percentile_90"],
                        mean=simulation_results["mean"],
                        std_deviation=simulation_results["std_deviation"]
                    ),
                    pension_estimate=PensionEstimate(
                        lump_sum_amount=pension_range["p50"]["lump_sum_amount"],
                        annuity_purchase_amount=pension_range["p50"]["annuity_corpus"],
                        monthly_pension_10th=pension_range["p10"]["monthly_pension"],
                        monthly_pension_50th=pension_range["p50"]["monthly_pension"],
                        monthly_pension_90th=pension_range["p90"]["monthly_pension"]
                    )
                )
            )
        
        # Generate comparison insights
        insights = insight_generator.generate_scenario_comparison_insights(
            scenario_results
        )
        
        response = ScenarioComparisonResponse(
            scenarios=scenario_results,
            investment_horizon_years=years,
            total_contributions=total_contributions,
            insights=insights
        )
        
        logger.info("Scenario comparison completed successfully")
        return response
    
    except Exception as e:
        logger.error(f"Error in scenario comparison: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to compare scenarios")


@router.post("/reverse-pension", response_model=ReversePensionResponse)
async def calculate_reverse_pension(request: ReversePensionRequest):
    """
    Calculate required monthly contribution for desired pension (reverse calculator)
    
    Args:
        request: Desired pension and retirement parameters
    
    Returns:
        Required monthly contribution and estimated corpus needed
    """
    try:
        logger.info(
            f"Processing reverse pension calculation: "
            f"desired_pension={request.desired_monthly_pension}"
        )
        
        years = request.retirement_age - request.current_age
        
        # Get expected return for risk profile
        min_return, max_return = FinancialCalculator.get_risk_profile_returns(
            request.risk_profile
        )
        expected_return = (min_return + max_return) / 2  # Use midpoint
        
        # Calculate required contribution
        required_contribution, required_corpus = (
            FinancialCalculator.reverse_calculate_required_contribution(
                desired_monthly_pension=request.desired_monthly_pension,
                years=years,
                annual_return_rate=expected_return,
                annual_income_growth=request.annual_income_growth
            )
        )
        
        # Calculate total contributions needed
        total_contributions = FinancialCalculator.calculate_total_contributions(
            initial_monthly_contribution=required_contribution,
            years=years,
            annual_income_growth=request.annual_income_growth
        )
        
        # Generate reverse calculator insights
        insights = insight_generator.generate_reverse_calculator_insights(
            required_contribution=required_contribution,
            desired_pension=request.desired_monthly_pension,
            years=years,
            risk_profile=request.risk_profile
        )
        
        # Generate strategic suggestions
        strategic_suggestions = insight_generator.generate_strategic_suggestions(
            required_contribution=required_contribution,
            years_to_retirement=years,
            risk_profile=request.risk_profile,
            required_corpus=required_corpus
        )
        
        response = ReversePensionResponse(
            required_monthly_contribution=required_contribution,
            estimated_corpus_needed=required_corpus,
            investment_horizon_years=years,
            total_contributions_needed=total_contributions,
            risk_profile=request.risk_profile,
            insights=insights,
            strategic_suggestions=strategic_suggestions
        )
        
        logger.info(
            f"Reverse calculation completed: "
            f"required_contribution={required_contribution:.2f}"
        )
        
        return response
    
    except Exception as e:
        logger.error(f"Error in reverse pension calculation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to calculate required contribution"
        )


@router.post("/readiness-score", response_model=ReadinessScore)
async def calculate_readiness_score(request: ReadinessScoreRequest):
    """
    Calculate retirement readiness score (0-100) with structured analysis
    
    Scoring components:
    - Corpus adequacy (60%): Projected corpus vs required corpus
    - Risk stability (20%): Volatility penalty for aggressive profiles
    - Time horizon (20%): Bonus for longer investment periods
    
    Args:
        request: Readiness score calculation parameters
    
    Returns:
        Readiness score with label, details, and recommendation
    """
    try:
        logger.info(
            f"Calculating readiness score: median={request.median_corpus:.2f}, "
            f"required={request.required_corpus:.2f}, years={request.years_to_retirement}"
        )
        
        # Calculate readiness score
        score_data = insight_generator.calculate_readiness_score(
            median_corpus=request.median_corpus,
            required_corpus=request.required_corpus,
            years_to_retirement=request.years_to_retirement,
            risk_profile=request.risk_profile
        )
        
        response = ReadinessScore(**score_data)
        
        logger.info(
            f"Readiness score calculated: score={score_data['score']}, "
            f"label={score_data['label']}"
        )
        
        return response
    
    except Exception as e:
        logger.error(f"Error calculating readiness score: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to calculate readiness score"
        )


@router.post("/volatility-index", response_model=VolatilityIndex)
async def calculate_volatility_index(request: VolatilityIndexRequest):
    """
    Calculate volatility index using coefficient of variation
    
    Returns normalized volatility measure (std dev as % of mean) with classification:
    - Low: <15% (stable, predictable)
    - Medium: 15-30% (moderate uncertainty)
    - High: >30% (significant variability)
    
    Args:
        request: Volatility index calculation parameters
    
    Returns:
        Volatility percentage, level classification, and detailed explanation
    """
    try:
        logger.info(
            f"Calculating volatility index: std_dev={request.standard_deviation:.2f}, "
            f"mean={request.mean_corpus:.2f}"
        )
        
        # Calculate volatility index
        volatility_data = insight_generator.calculate_volatility_index(
            standard_deviation=request.standard_deviation,
            mean_corpus=request.mean_corpus
        )
        
        response = VolatilityIndex(**volatility_data)
        
        logger.info(
            f"Volatility index calculated: {volatility_data['volatility_percentage']:.2f}%, "
            f"level={volatility_data['volatility_level']}"
        )
        
        return response
    
    except Exception as e:
        logger.error(f"Error calculating volatility index: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to calculate volatility index"
        )

@router.post("/sensitivity-analysis")
async def sensitivity_analysis(request: SensitivityRequest):
    """
    Analyze impact of contribution increases on retirement corpus
    
    Simulates contribution increases of +5%, +10%, and +20% to show
    the impact on final corpus and pension amounts.
    
    Args:
        request: Current parameters with age, retirement age, contribution, risk profile
    
    Returns:
        Sensitivity analysis showing base and adjusted scenarios with impact metrics
    """
    try:
        logger.info(
            f"Processing sensitivity analysis: age={request.current_age}, "
            f"contribution={request.monthly_contribution}"
        )
        
        years = request.retirement_age - request.current_age
        
        result = SensitivityAnalyzer.analyze_contribution_sensitivity(
            base_monthly_contribution=request.monthly_contribution,
            years=years,
            risk_profile=request.risk_profile,
            annual_income_growth=request.annual_income_growth,
            iterations=request.monte_carlo_iterations
        )
        
        logger.info(
            f"Sensitivity analysis completed: {len(result['sensitivity_scenarios'])} scenarios analyzed"
        )
        
        return result
    
    except CalculationException as e:
        logger.error(f"Calculation error in sensitivity: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except Exception as e:
        logger.error(f"Error in sensitivity analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to analyze contribution sensitivity"
        )


@router.post("/delay-impact")
async def retirement_delay_impact(request: DelayImpactRequest):
    """
    Simulate impact of delaying retirement on corpus and pension
    
    Shows the financial benefit of working 1, 2, or 5 years longer,
    including additional compounding and contributions.
    
    Args:
        request: Current parameters with age, continuation, retirement age target
    
    Returns:
        Delay impact analysis showing base scenario and delay scenarios with benefits
    """
    try:
        logger.info(
            f"Processing delay impact analysis: current_age={request.current_age}, "
            f"planned_retirement_age={request.planned_retirement_age}"
        )
        
        result = DelaySimulator.simulate_retirement_delay(
            base_retirement_age=request.planned_retirement_age,
            current_age=request.current_age,
            monthly_contribution=request.monthly_contribution,
            risk_profile=request.risk_profile,
            annual_income_growth=request.annual_income_growth,
            iterations=request.monte_carlo_iterations
        )
        
        logger.info(
            f"Delay impact analysis completed: {len(result['delay_scenarios'])} scenarios analyzed"
        )
        
        return result
    
    except CalculationException as e:
        logger.error(f"Calculation error in delay analysis: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except Exception as e:
        logger.error(f"Error in delay impact analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to analyze retirement delay impact"
        )