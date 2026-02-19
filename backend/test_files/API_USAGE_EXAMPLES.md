# API Usage Examples - Retirement Intelligence Engine

## Overview
This document demonstrates how to use the new analytical endpoints for retirement planning.

## Base URL
```
http://localhost:8000/api/v1/forecast
```

---

## 1. Retirement Readiness Score

### Endpoint
`POST /api/v1/forecast/readiness-score`

### Purpose
Calculates a comprehensive readiness score (0-100) based on corpus adequacy, risk stability, and time horizon.

### Scoring Components
- **Corpus Adequacy (60%)**: Projected corpus vs required corpus
- **Risk Stability (20%)**: Penalty for high-volatility profiles
- **Time Horizon (20%)**: Bonus for longer investment periods

### Score Classification
- **71-100**: Strong Outlook
- **41-70**: Moderate Confidence
- **0-40**: High Risk

### Request Example
```json
{
  "median_corpus": 50000000,
  "required_corpus": 40000000,
  "years_to_retirement": 25,
  "risk_profile": "conservative"
}
```

### Response Example
```json
{
  "score": 100,
  "label": "Strong Outlook",
  "details": {
    "corpus_adequacy_score": 60.0,
    "risk_stability_score": 20,
    "time_horizon_score": 20,
    "adequacy_ratio": 1.25
  },
  "recommendation": "Excellent readiness. Your projected corpus exceeds your target. Continue your current investment strategy and review annually to maintain alignment with goals."
}
```

### Python Example
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/forecast/readiness-score",
    json={
        "median_corpus": 30000000,      # ₹3 crore
        "required_corpus": 35000000,    # ₹3.5 crore
        "years_to_retirement": 15,
        "risk_profile": "moderate"
    }
)

result = response.json()
print(f"Readiness Score: {result['score']}/100")
print(f"Label: {result['label']}")
print(f"Recommendation: {result['recommendation']}")
```

### cURL Example
```bash
curl -X POST "http://localhost:8000/api/v1/forecast/readiness-score" \
  -H "Content-Type: application/json" \
  -d '{
    "median_corpus": 50000000,
    "required_corpus": 40000000,
    "years_to_retirement": 25,
    "risk_profile": "conservative"
  }'
```

---

## 2. Volatility Index

### Endpoint
`POST /api/v1/forecast/volatility-index`

### Purpose
Calculates the coefficient of variation (CV) to measure portfolio volatility as a normalized percentage.

### Volatility Classification
- **Low (<15%)**: Stable and predictable
- **Medium (15-30%)**: Moderate uncertainty
- **High (>30%)**: Significant variability

### Request Example
```json
{
  "standard_deviation": 10000000,
  "mean_corpus": 50000000
}
```

### Response Example
```json
{
  "volatility_percentage": 20.0,
  "volatility_level": "medium",
  "explanation": "Your retirement corpus projections have a volatility index of 20.0%, classified as medium volatility. With a mean corpus of ₹5.00 crore and standard deviation of ₹1.00 crore, your outcomes are moderately uncertain. Your projections show moderate volatility, which is typical for balanced portfolios. While there's some variability in outcomes, this level of volatility is manageable. Consider diversifying further if risk tolerance is low, or maintain current strategy if comfortable with moderate fluctuations."
}
```

### Python Example
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/forecast/volatility-index",
    json={
        "standard_deviation": 3000000,   # ₹30 lakh
        "mean_corpus": 30000000          # ₹3 crore
    }
)

result = response.json()
print(f"Volatility: {result['volatility_percentage']:.2f}%")
print(f"Level: {result['volatility_level'].upper()}")
print(f"\nExplanation:\n{result['explanation']}")
```

### cURL Example
```bash
curl -X POST "http://localhost:8000/api/v1/forecast/volatility-index" \
  -H "Content-Type: application/json" \
  -d '{
    "standard_deviation": 10000000,
    "mean_corpus": 50000000
  }'
```

---

## 3. Combined Analysis Workflow

### Step 1: Get Initial Forecast
```python
import requests

# Get retirement forecast
forecast = requests.post(
    "http://localhost:8000/api/v1/forecast/retirement",
    json={
        "current_age": 30,
        "retirement_age": 60,
        "monthly_contribution": 10000,
        "annual_income_growth": 5.0,
        "risk_profile": "moderate",
        "monte_carlo_iterations": 10000
    }
).json()

# Extract key metrics
median_corpus = forecast["corpus_projection"]["percentile_50"]
mean_corpus = forecast["corpus_projection"]["mean"]
std_deviation = forecast["corpus_projection"]["std_deviation"]
monthly_pension = forecast["pension_estimate"]["monthly_pension_50th"]
```

### Step 2: Calculate Volatility
```python
# Analyze volatility
volatility = requests.post(
    "http://localhost:8000/api/v1/forecast/volatility-index",
    json={
        "standard_deviation": std_deviation,
        "mean_corpus": mean_corpus
    }
).json()

print(f"\n📊 VOLATILITY ANALYSIS")
print(f"Volatility Index: {volatility['volatility_percentage']:.2f}%")
print(f"Risk Level: {volatility['volatility_level'].upper()}")
```

### Step 3: Calculate Readiness Score
```python
# Assume target pension of ₹50,000/month
# Required corpus = (50000 * 12 * 100) / 6% annuity rate
target_monthly_pension = 50000
required_corpus = (target_monthly_pension * 12 * 100) / 6

# Get readiness score
readiness = requests.post(
    "http://localhost:8000/api/v1/forecast/readiness-score",
    json={
        "median_corpus": median_corpus,
        "required_corpus": required_corpus,
        "years_to_retirement": 30,
        "risk_profile": "moderate"
    }
).json()

print(f"\n🎯 RETIREMENT READINESS")
print(f"Score: {readiness['score']}/100")
print(f"Label: {readiness['label']}")
print(f"Recommendation: {readiness['recommendation']}")
```

### Step 4: Comprehensive Report
```python
print(f"\n" + "="*70)
print("RETIREMENT READINESS COMPREHENSIVE REPORT")
print("="*70)
print(f"\n📈 PROJECTIONS")
print(f"  Median Corpus: ₹{median_corpus:,.0f}")
print(f"  Required Corpus: ₹{required_corpus:,.0f}")
print(f"  Expected Monthly Pension: ₹{monthly_pension:,.0f}")

print(f"\n📊 VOLATILITY ANALYSIS")
print(f"  Index: {volatility['volatility_percentage']:.2f}%")
print(f"  Level: {volatility['volatility_level'].upper()}")

print(f"\n🎯 READINESS ASSESSMENT")
print(f"  Score: {readiness['score']}/100")
print(f"  Label: {readiness['label']}")
print(f"  Corpus Adequacy: {readiness['details']['adequacy_ratio']:.2%}")

print(f"\n💡 KEY INSIGHTS")
for insight in forecast.get('insights', []):
    print(f"  • {insight['title']}: {insight['message'][:100]}...")

print(f"\n✅ RECOMMENDATION")
print(f"  {readiness['recommendation']}")
print("="*70)
```

---

## 4. Risk Profile Comparison

### Workflow: Compare all risk profiles with volatility analysis

```python
import requests

risk_profiles = ["conservative", "moderate", "aggressive"]
results = {}

for profile in risk_profiles:
    # Get forecast
    forecast = requests.post(
        "http://localhost:8000/api/v1/forecast/retirement",
        json={
            "current_age": 35,
            "retirement_age": 60,
            "monthly_contribution": 15000,
            "risk_profile": profile
        }
    ).json()
    
    # Calculate volatility
    volatility = requests.post(
        "http://localhost:8000/api/v1/forecast/volatility-index",
        json={
            "standard_deviation": forecast["corpus_projection"]["std_deviation"],
            "mean_corpus": forecast["corpus_projection"]["mean"]
        }
    ).json()
    
    results[profile] = {
        "median_corpus": forecast["corpus_projection"]["percentile_50"],
        "volatility": volatility["volatility_percentage"],
        "volatility_level": volatility["volatility_level"]
    }

# Compare results
print("\n" + "="*70)
print("RISK PROFILE VOLATILITY COMPARISON")
print("="*70)
print(f"{'Profile':<15} {'Median Corpus':<20} {'Volatility':<15} {'Level':<10}")
print("-"*70)
for profile, data in results.items():
    print(f"{profile.capitalize():<15} ₹{data['median_corpus']:>15,.0f} {data['volatility']:>10.2f}% {data['volatility_level'].upper():<10}")
print("="*70)
```

---

## 5. API Documentation

Visit the interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Error Handling

All endpoints return standard HTTP status codes:

- **200**: Success
- **400**: Bad Request (validation error)
- **500**: Internal Server Error

### Error Response Example
```json
{
  "detail": "Validation error: mean_corpus must be greater than 0"
}
```

### Python Error Handling
```python
try:
    response = requests.post(url, json=payload)
    response.raise_for_status()  # Raise exception for 4xx/5xx
    result = response.json()
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e.response.status_code}")
    print(f"Detail: {e.response.json()['detail']}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {str(e)}")
```
