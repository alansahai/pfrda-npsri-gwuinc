"""
Unit test for readiness scoring logic
"""
import sys
sys.path.insert(0, 'D:\\PFRDA\\backend')

from app.services.insight_generator import InsightGenerator
from app.models.schemas import RiskProfile

def test_scenario(name: str, median: float, required: float, years: int, risk: RiskProfile):
    """Test a specific scenario"""
    print(f"\n{'='*70}")
    print(f"📊 Test: {name}")
    print(f"{'='*70}")
    print(f"Inputs:")
    print(f"  - Median Corpus: ₹{median:,.0f}")
    print(f"  - Required Corpus: ₹{required:,.0f}")
    print(f"  - Years to Retirement: {years}")
    print(f"  - Risk Profile: {risk.value}")
    
    generator = InsightGenerator()
    result = generator.calculate_readiness_score(
        median_corpus=median,
        required_corpus=required,
        years_to_retirement=years,
        risk_profile=risk
    )
    
    print(f"\n📈 Results:")
    print(f"  Score: {result['score']}/100")
    print(f"  Label: {result['label']}")
    print(f"\n📊 Score Breakdown:")
    for key, value in result['details'].items():
        print(f"  - {key}: {value}")
    print(f"\n💡 Recommendation:")
    print(f"  {result['recommendation']}")


def main():
    print("\n" + "="*70)
    print("🎯 RETIREMENT READINESS SCORING SYSTEM - UNIT TEST")
    print("="*70)
    
    # Test 1: Strong Outlook
    test_scenario(
        "Strong Outlook - Well Prepared",
        median=50000000,     # 5 crore
        required=40000000,   # 4 crore
        years=25,
        risk=RiskProfile.CONSERVATIVE
    )
    
    # Test 2: Moderate Confidence
    test_scenario(
        "Moderate Confidence - Slight Gap",
        median=30000000,     # 3 crore
        required=38000000,   # 3.8 crore
        years=15,
        risk=RiskProfile.MODERATE
    )
    
    # Test 3: High Risk - Short Timeline
    test_scenario(
        "High Risk - Critical Shortfall",
        median=10000000,     # 1 crore
        required=30000000,   # 3 crore
        years=5,
        risk=RiskProfile.AGGRESSIVE
    )
    
    # Test 4: Moderate with Very Long Horizon
    test_scenario(
        "Moderate - Long Timeline Advantage",
        median=25000000,     # 2.5 crore
        required=30000000,   # 3 crore
        years=30,
        risk=RiskProfile.MODERATE
    )
    
    # Test 5: High Risk - Conservative with Gap
    test_scenario(
        "High Risk - Conservative Underperforming",
        median=15000000,     # 1.5 crore
        required=40000000,   # 4 crore
        years=8,
        risk=RiskProfile.CONSERVATIVE
    )
    
    # Test 6: Strong - Aggressive Well Funded
    test_scenario(
        "Strong Outlook - Aggressive Overachieving",
        median=80000000,     # 8 crore
        required=50000000,   # 5 crore
        years=20,
        risk=RiskProfile.AGGRESSIVE
    )
    
    # Test 7: Edge Case - Exact Match
    test_scenario(
        "Moderate - Exactly On Target",
        median=35000000,     # 3.5 crore
        required=35000000,   # 3.5 crore
        years=12,
        risk=RiskProfile.MODERATE
    )
    
    # Test 8: Edge Case - Very Short Timeline
    test_scenario(
        "High Risk - Near Retirement",
        median=20000000,     # 2 crore
        required=25000000,   # 2.5 crore
        years=2,
        risk=RiskProfile.CONSERVATIVE
    )
    
    print("\n" + "="*70)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
