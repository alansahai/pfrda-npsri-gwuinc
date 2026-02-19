"""
Retirement Projection Routes
API endpoints for retirement corpus projections and pension calculations
"""
from fastapi import APIRouter

from app.models.schemas import (
    RetirementInput,
    RetirementForecastResponse,
    ScenarioComparisonRequest,
    ScenarioComparisonResponse,
    ReversePensionRequest,
    ReversePensionResponse,
    ErrorResponse
)
from app.routes.forecast import (
    calculate_retirement_forecast,
    compare_scenarios as compare_forecast_scenarios,
    calculate_reverse_pension,
)

router = APIRouter(prefix="/projections", tags=["Projections"])


@router.post(
    "/calculate",
    response_model=RetirementForecastResponse,
    summary="Calculate Retirement Projection",
    description="Generate retirement corpus projection with probability-based forecasting using Monte Carlo simulation",
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input parameters"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def calculate_retirement_projection(
    request: RetirementInput
) -> RetirementForecastResponse:
    return await calculate_retirement_forecast(request)


@router.post(
    "/compare-scenarios",
    response_model=ScenarioComparisonResponse,
    summary="Compare Investment Scenarios",
    description="Compare retirement projections across Conservative, Moderate, and Aggressive risk profiles",
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input parameters"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def compare_scenarios(
    request: ScenarioComparisonRequest
) -> ScenarioComparisonResponse:
    return await compare_forecast_scenarios(request)


@router.post(
    "/reverse-calculator",
    response_model=ReversePensionResponse,
    summary="Reverse Pension Calculator",
    description="Calculate required monthly contributions to achieve a desired pension target",
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input parameters"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def reverse_pension_calculator(
    request: ReversePensionRequest
) -> ReversePensionResponse:
    return await calculate_reverse_pension(request)
