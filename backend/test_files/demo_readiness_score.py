"""
Quick Demo: Retirement Readiness Scoring System
This system is already fully operational!
"""
import sys
sys.path.insert(0, 'D:\\PFRDA\\backend')

from app.services.insight_generator import InsightGenerator
from app.models.schemas import RiskProfile


def demo_readiness_score():
    """Demonstrate the retirement readiness scoring system"""
    
    print("\n" + "="*70)
    print("🎯 RETIREMENT READINESS SCORING SYSTEM - QUICK DEMO")
    print("="*70)
    
    generator = InsightGenerator()
    
    # Example 1: Strong Outlook
    print("\n" + "="*70)
    print("Example 1: Strong Outlook (90/100)")
    print("="*70)
    result1 = generator.calculate_readiness_score(
        median_corpus=50000000,      # ₹5 crore projected
        required_corpus=40000000,    # ₹4 crore needed
        years_to_retirement=25,      # Long timeline
        risk_profile=RiskProfile.CONSERVATIVE  # Stable approach
    )
    print(f"Score: {result1['score']}/100")
    print(f"Label: {result1['label']}")
    print(f"Details:")
    for key, val in result1['details'].items():
        print(f"  • {key}: {val}")
    print(f"\nRecommendation: {result1['recommendation']}")
    
    # Example 2: Moderate Confidence
    print("\n" + "="*70)
    print("Example 2: Moderate Confidence (62/100)")
    print("="*70)
    result2 = generator.calculate_readiness_score(
        median_corpus=30000000,      # ₹3 crore projected
        required_corpus=35000000,    # ₹3.5 crore needed
        years_to_retirement=12,      # Medium timeline
        risk_profile=RiskProfile.MODERATE
    )
    print(f"Score: {result2['score']}/100")
    print(f"Label: {result2['label']}")
    print(f"Details:")
    for key, val in result2['details'].items():
        print(f"  • {key}: {val}")
    print(f"\nRecommendation: {result2['recommendation']}")
    
    # Example 3: High Risk
    print("\n" + "="*70)
    print("Example 3: High Risk (35/100)")
    print("="*70)
    result3 = generator.calculate_readiness_score(
        median_corpus=10000000,      # ₹1 crore projected
        required_corpus=30000000,    # ₹3 crore needed
        years_to_retirement=5,       # Short timeline
        risk_profile=RiskProfile.AGGRESSIVE  # High volatility
    )
    print(f"Score: {result3['score']}/100")
    print(f"Label: {result3['label']}")
    print(f"Details:")
    for key, val in result3['details'].items():
        print(f"  • {key}: {val}")
    print(f"\nRecommendation: {result3['recommendation']}")
    
    # Show scoring breakdown
    print("\n" + "="*70)
    print("📊 SCORING BREAKDOWN (Total: 100 points)")
    print("="*70)
    print("""
1. CORPUS ADEQUACY (60 points)
   • Compares projected vs required corpus
   • Formula: (median_corpus / required_corpus) × 60
   • Capped at 60 points maximum

2. RISK STABILITY (20 points)
   • Conservative: 20 points (most stable)
   • Moderate: 15 points
   • Aggressive: 10 points (highest volatility)

3. TIME HORIZON (20 points)
   • 21+ years: 20 points
   • 11-20 years: 15 points
   • 6-10 years: 10 points
   • 1-5 years: 5 points

LABELS:
   • 0-40: "High Risk" - Urgent action needed
   • 41-70: "Moderate Confidence" - On track with adjustments
   • 71-100: "Strong Outlook" - Excellent readiness
""")
    print("="*70)
    
    # API Usage
    print("\n" + "="*70)
    print("🌐 API ENDPOINT USAGE")
    print("="*70)
    print("""
POST /api/v1/forecast/readiness-score

Request Body:
{
  "median_corpus": 50000000,
  "required_corpus": 40000000,
  "years_to_retirement": 25,
  "risk_profile": "conservative"
}

Response:
{
  "score": 100,
  "label": "Strong Outlook",
  "details": {
    "corpus_adequacy_score": 60.0,
    "risk_stability_score": 20,
    "time_horizon_score": 20,
    "adequacy_ratio": 1.25
  },
  "recommendation": "Excellent readiness. Your projected corpus..."
}
""")
    print("="*70)
    
    # Python Example
    print("\n" + "="*70)
    print("🐍 PYTHON API CLIENT EXAMPLE")
    print("="*70)
    print("""
import requests

response = requests.post(
    "http://localhost:8000/api/v1/forecast/readiness-score",
    json={
        "median_corpus": 50000000,
        "required_corpus": 40000000,
        "years_to_retirement": 25,
        "risk_profile": "conservative"
    }
)

result = response.json()
print(f"Readiness Score: {result['score']}/100")
print(f"Label: {result['label']}")
print(f"Recommendation: {result['recommendation']}")
""")
    print("="*70 + "\n")


if __name__ == "__main__":
    demo_readiness_score()
