"""
Pydantic models for request/response validation
"""
from enum import Enum
from typing import Optional, Dict, List
from pydantic import BaseModel, Field, field_validator


class InsightSeverity(str, Enum):
    """Severity levels for insights"""
    INFO = "info"
    WARNING = "warning"
    POSITIVE = "positive"


class Insight(BaseModel):
    """Financial insight model"""
    title: str = Field(description="Insight title")
    message: str = Field(description="Detailed insight message")
    severity: InsightSeverity = Field(description="Severity level of the insight")


class RiskProfile(str, Enum):
    """Risk profile options for investment allocation"""
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


class RetirementInput(BaseModel):
    """Input parameters for retirement corpus calculation"""
    
    current_age: int = Field(
        ...,
        ge=18,
        le=65,
        description="Current age of the subscriber"
    )
    retirement_age: int = Field(
        ...,
        ge=40,
        le=70,
        description="Expected retirement age"
    )
    monthly_contribution: float = Field(
        ...,
        ge=500,
        le=200000,
        description="Monthly contribution amount in INR"
    )
    annual_income_growth: float = Field(
        default=5.0,
        ge=0,
        le=20,
        description="Expected annual income growth percentage"
    )
    risk_profile: RiskProfile = Field(
        default=RiskProfile.MODERATE,
        description="Investment risk profile"
    )
    monte_carlo_iterations: Optional[int] = Field(
        default=10000,
        ge=1000,
        le=50000,
        description="Number of Monte Carlo simulation iterations"
    )
    
    @field_validator('retirement_age')
    @classmethod
    def validate_retirement_age(cls, v, info):
        """Ensure retirement age is greater than current age"""
        if 'current_age' in info.data and v <= info.data['current_age']:
            raise ValueError('Retirement age must be greater than current age')
        return v
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "current_age": 30,
                    "retirement_age": 60,
                    "monthly_contribution": 5000,
                    "annual_income_growth": 5.0,
                    "risk_profile": "moderate",
                    "monte_carlo_iterations": 10000
                }
            ]
        }
    }


class PensionProjection(BaseModel):
    """Pension projection results"""
    
    percentile_10: float = Field(..., description="10th percentile corpus value")
    percentile_25: float = Field(..., description="25th percentile corpus value")
    percentile_50: float = Field(..., description="50th percentile (median) corpus value")
    percentile_75: float = Field(..., description="75th percentile corpus value")
    percentile_90: float = Field(..., description="90th percentile corpus value")
    mean: float = Field(..., description="Mean corpus value")
    std_deviation: float = Field(..., description="Standard deviation")


class PensionEstimate(BaseModel):
    """Monthly pension estimate based on corpus allocation"""
    
    lump_sum_amount: float = Field(..., description="Lump sum withdrawal amount")
    annuity_purchase_amount: float = Field(..., description="Amount allocated to annuity")
    monthly_pension_10th: float = Field(..., description="10th percentile monthly pension")
    monthly_pension_50th: float = Field(..., description="50th percentile monthly pension")
    monthly_pension_90th: float = Field(..., description="90th percentile monthly pension")


class RetirementForecastResponse(BaseModel):
    """Complete retirement forecast response"""
    
    input_parameters: RetirementInput
    investment_horizon_years: int
    total_contributions: float
    corpus_projection: PensionProjection
    pension_estimate: PensionEstimate
    risk_profile_details: Dict[str, float]
    insights: List[Insight] = Field(default=[], description="Intelligent financial insights")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "input_parameters": {
                        "current_age": 30,
                        "retirement_age": 60,
                        "monthly_contribution": 5000,
                        "annual_income_growth": 5.0,
                        "risk_profile": "moderate"
                    },
                    "investment_horizon_years": 30,
                    "total_contributions": 3000000.0,
                    "corpus_projection": {
                        "percentile_10": 8500000.0,
                        "percentile_50": 12000000.0,
                        "percentile_90": 16500000.0,
                        "mean": 12200000.0,
                        "std_deviation": 2500000.0
                    },
                    "pension_estimate": {
                        "lump_sum_amount": 4800000.0,
                        "annuity_purchase_amount": 7200000.0,
                        "monthly_pension_10th": 36000.0,
                        "monthly_pension_50th": 48000.0,
                        "monthly_pension_90th": 60000.0
                    },
                    "risk_profile_details": {
                        "min_return": 6.0,
                        "max_return": 8.0
                    }
                }
            ]
        }
    }


class ScenarioComparisonRequest(BaseModel):
    """Request for comparing multiple risk scenarios"""
    
    base_input: RetirementInput
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "base_input": {
                        "current_age": 30,
                        "retirement_age": 60,
                        "monthly_contribution": 5000,
                        "annual_income_growth": 5.0,
                        "risk_profile": "moderate"
                    }
                }
            ]
        }
    }


class ScenarioResult(BaseModel):
    """Single scenario result"""
    
    risk_profile: RiskProfile
    corpus_projection: PensionProjection
    pension_estimate: PensionEstimate


class ScenarioComparisonResponse(BaseModel):
    """Comparison of multiple risk scenarios"""
    
    scenarios: List[ScenarioResult]
    investment_horizon_years: int
    total_contributions: float
    insights: List[Insight] = Field(default=[], description="Comparative insights across scenarios")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "scenarios": [
                        {
                            "risk_profile": "conservative",
                            "corpus_projection": {
                                "percentile_10": 7000000.0,
                                "percentile_50": 9500000.0,
                                "percentile_90": 12000000.0,
                                "mean": 9600000.0,
                                "std_deviation": 1500000.0
                            },
                            "pension_estimate": {
                                "lump_sum_amount": 3800000.0,
                                "annuity_purchase_amount": 5700000.0,
                                "monthly_pension_10th": 28000.0,
                                "monthly_pension_50th": 38000.0,
                                "monthly_pension_90th": 48000.0
                            }
                        }
                    ],
                    "investment_horizon_years": 30,
                    "total_contributions": 3000000.0
                }
            ]
        }
    }


class ReversePensionRequest(BaseModel):
    """Request for reverse pension calculation (desired pension -> required contribution)"""
    
    current_age: int = Field(..., ge=18, le=65)
    retirement_age: int = Field(..., ge=40, le=70)
    desired_monthly_pension: float = Field(
        ...,
        ge=5000,
        le=500000,
        description="Desired monthly pension amount"
    )
    annual_income_growth: float = Field(default=5.0, ge=0, le=20)
    risk_profile: RiskProfile = Field(default=RiskProfile.MODERATE)
    
    @field_validator('retirement_age')
    @classmethod
    def validate_retirement_age(cls, v, info):
        if 'current_age' in info.data and v <= info.data['current_age']:
            raise ValueError('Retirement age must be greater than current age')
        return v


class ReversePensionResponse(BaseModel):
    """Response for reverse pension calculation"""
    
    required_monthly_contribution: float
    estimated_corpus_needed: float
    investment_horizon_years: int
    total_contributions_needed: float
    risk_profile: RiskProfile
    insights: List[Insight] = Field(default=[], description="Feasibility and strategy insights")
    strategic_suggestions: List[str] = Field(default=[], description="Strategic recommendations based on analysis")


class HealthCheckResponse(BaseModel):
    """Health check response"""
    
    status: str
    version: str
    timestamp: str


class ConfidenceInterval(BaseModel):
    """Confidence intervals for corpus projection"""
    
    confidence_50_percent: Dict[str, float] = Field(
        ...,
        description="50% confidence interval [p25, p75]"
    )
    confidence_80_percent: Dict[str, float] = Field(
        ...,
        description="80% confidence interval [p10, p90]"
    )
    percentile_25: float = Field(..., description="25th percentile value")
    percentile_75: float = Field(..., description="75th percentile value")


class ReadinessScoreBreakdown(BaseModel):
    """Readiness score breakdown details"""
    
    corpus_strength_score: float = Field(..., description="Component score for corpus strength")
    corpus_strength_weight: int = Field(..., description="Weight percentage (50%)")
    volatility_penalty_score: float = Field(..., description="Component score for downside protection")
    volatility_penalty_weight: int = Field(..., description="Weight percentage (30%)")
    time_horizon_score: float = Field(..., description="Component score for time benefit")
    time_horizon_weight: int = Field(..., description="Weight percentage (20%)")


class RetirementReadinessScore(BaseModel):
    """Retirement readiness assessment"""
    
    score: int = Field(..., ge=0, le=100, description="Readiness score 0-100")
    label: str = Field(..., description="Label: Strong Outlook, Moderate Confidence, or High Risk")
    explanation: str = Field(..., description="Detailed explanation of readiness score")
    recommendation: str = Field(..., description="Actionable recommendation")
    scoring_breakdown: ReadinessScoreBreakdown


class ReadinessScoreRequest(BaseModel):
    """Request for retirement readiness score calculation"""
    
    median_corpus: float = Field(
        ...,
        ge=0,
        description="Projected median corpus at retirement"
    )
    required_corpus: float = Field(
        ...,
        ge=0,
        description="Required corpus to meet pension target"
    )
    years_to_retirement: int = Field(
        ...,
        ge=1,
        le=50,
        description="Years until retirement"
    )
    risk_profile: RiskProfile = Field(
        description="Investment risk profile"
    )


class ReadinessScore(BaseModel):
    """Retirement readiness score with structured analysis"""
    
    score: int = Field(
        ge=0,
        le=100,
        description="Readiness score from 0 to 100"
    )
    label: str = Field(
        description="Readiness label: High Risk, Moderate Confidence, or Strong Outlook"
    )
    details: Dict[str, float] = Field(
        description="Breakdown of score components"
    )
    recommendation: str = Field(
        description="Actionable recommendation based on score"
    )


class VolatilityIndexRequest(BaseModel):
    """Request for volatility index calculation"""
    
    standard_deviation: float = Field(
        ...,
        ge=0,
        description="Standard deviation of corpus projections"
    )
    mean_corpus: float = Field(
        ...,
        gt=0,
        description="Mean corpus from projections"
    )


class VolatilityIndex(BaseModel):
    """Volatility index metric with risk classification"""
    
    volatility_percentage: float = Field(
        description="Coefficient of variation as percentage"
    )
    volatility_level: str = Field(
        description="Classification: low, medium, or high"
    )
    explanation: str = Field(
        description="Detailed explanation of volatility implications"
    )

class SensitivityRequest(BaseModel):
    """Request for contribution sensitivity analysis"""
    
    current_age: int = Field(..., ge=18, le=65, description="Current age")
    retirement_age: int = Field(..., ge=40, le=70, description="Target retirement age")
    monthly_contribution: float = Field(..., ge=500, le=200000, description="Current monthly contribution")
    annual_income_growth: float = Field(default=5.0, ge=0, le=20, description="Annual income growth %")
    risk_profile: RiskProfile = Field(default=RiskProfile.MODERATE, description="Risk profile")
    monte_carlo_iterations: Optional[int] = Field(default=10000, ge=1000, le=50000)
    
    @field_validator('retirement_age')
    @classmethod
    def validate_retirement_age(cls, v, info):
        if 'current_age' in info.data and v <= info.data['current_age']:
            raise ValueError('Retirement age must be greater than current age')
        return v


class DelayImpactRequest(BaseModel):
    """Request for retirement delay impact analysis"""
    
    current_age: int = Field(..., ge=18, le=65, description="Current age")
    planned_retirement_age: int = Field(..., ge=40, le=70, description="Currently planned retirement age")
    monthly_contribution: float = Field(..., ge=500, le=200000, description="Monthly contribution")
    annual_income_growth: float = Field(default=5.0, ge=0, le=20, description="Annual income growth %")
    risk_profile: RiskProfile = Field(default=RiskProfile.MODERATE, description="Risk profile")
    monte_carlo_iterations: Optional[int] = Field(default=10000, ge=1000, le=50000)
    
    @field_validator('planned_retirement_age')
    @classmethod
    def validate_retirement_age(cls, v, info):
        if 'current_age' in info.data and v <= info.data['current_age']:
            raise ValueError('Planned retirement age must be greater than current age')
        return v


class ErrorResponse(BaseModel):
    """Standard error response"""
    
    detail: str = Field(..., description="Error message")
    status_code: Optional[int] = Field(None, description="HTTP status code")