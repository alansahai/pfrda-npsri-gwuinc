"""
Unit test for strategic suggestions in reverse calculator
"""
import sys
sys.path.insert(0, 'D:\\PFRDA\\backend')

from app.services.insight_generator import InsightGenerator
from app.models.schemas import RiskProfile


def test_strategic_scenario(name: str, required_contribution: float, years: int, risk: RiskProfile, required_corpus: float):
    """Test a specific strategic suggestion scenario"""
    print(f"\n{'='*80}")
    print(f"📊 Test: {name}")
    print(f"{'='*80}")
    print(f"Inputs:")
    print(f"  - Required Monthly Contribution: ₹{required_contribution:,.0f}")
    print(f"  - Years to Retirement: {years}")
    print(f"  - Risk Profile: {risk.value.upper()}")
    print(f"  - Required Corpus: ₹{required_corpus:,.0f}")
    
    generator = InsightGenerator()
    suggestions = generator.generate_strategic_suggestions(
        required_contribution=required_contribution,
        years_to_retirement=years,
        risk_profile=risk,
        required_corpus=required_corpus
    )
    
    print(f"\n💡 Strategic Suggestions ({len(suggestions)}):")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"\n  {i}. {suggestion}")


def main():
    print("\n" + "="*80)
    print("🎯 STRATEGIC SUGGESTIONS - REVERSE CALCULATOR TEST SUITE")
    print("="*80)
    
    # Test 1: High required contribution (> ₹30,000)
    test_strategic_scenario(
        "Rule 1: High Required Contribution",
        required_contribution=45000,  # > ₹30,000
        years=15,
        risk=RiskProfile.MODERATE,
        required_corpus=50000000  # 5 crore
    )
    
    # Test 2: Short timeline - Conservative
    test_strategic_scenario(
        "Rule 2a: Short Timeline + Conservative",
        required_contribution=20000,
        years=7,  # < 10 years
        risk=RiskProfile.CONSERVATIVE,
        required_corpus=30000000  # 3 crore
    )
    
    # Test 3: Short timeline - Moderate
    test_strategic_scenario(
        "Rule 2b: Short Timeline + Moderate",
        required_contribution=25000,
        years=8,  # < 10 years
        risk=RiskProfile.MODERATE,
        required_corpus=35000000  # 3.5 crore
    )
    
    # Test 4: Short timeline - Aggressive
    test_strategic_scenario(
        "Rule 2c: Short Timeline + Aggressive",
        required_contribution=18000,
        years=6,  # < 10 years
        risk=RiskProfile.AGGRESSIVE,
        required_corpus=28000000  # 2.8 crore
    )
    
    # Test 5: Aggressive risk profile (normal timeline)
    test_strategic_scenario(
        "Rule 3a: Aggressive Risk Profile",
        required_contribution=15000,
        years=20,
        risk=RiskProfile.AGGRESSIVE,
        required_corpus=60000000  # 6 crore
    )
    
    # Test 6: Aggressive + Very Short Timeline (CRITICAL)
    test_strategic_scenario(
        "Rule 3b: CRITICAL - Aggressive + Very Short Timeline",
        required_contribution=50000,  # High contribution + aggressive + short time
        years=3,  # < 5 years
        risk=RiskProfile.AGGRESSIVE,
        required_corpus=20000000  # 2 crore
    )
    
    # Test 7: Manageable contribution + short timeline
    test_strategic_scenario(
        "Edge Case: Manageable Contribution + Short Timeline",
        required_contribution=15000,  # <= ₹30,000
        years=8,  # < 10 years
        risk=RiskProfile.CONSERVATIVE,
        required_corpus=25000000  # 2.5 crore
    )
    
    # Test 8: Ideal scenario (no major triggers)
    test_strategic_scenario(
        "Ideal Scenario: Balanced Plan",
        required_contribution=12000,  # <= ₹30,000
        years=25,  # >= 10 years
        risk=RiskProfile.MODERATE,
        required_corpus=40000000  # 4 crore
    )
    
    # Test 9: Multiple triggers - High contribution + Short timeline + Aggressive
    test_strategic_scenario(
        "Multiple Triggers: High Contribution + Short Timeline + Aggressive",
        required_contribution=55000,  # > ₹30,000
        years=4,  # < 5 years (very short)
        risk=RiskProfile.AGGRESSIVE,
        required_corpus=18000000  # 1.8 crore
    )
    
    # Test 10: Boundary case - Exactly ₹30,000
    test_strategic_scenario(
        "Boundary Case: Exactly ₹30,000",
        required_contribution=30000,  # exactly ₹30,000
        years=15,
        risk=RiskProfile.CONSERVATIVE,
        required_corpus=35000000  # 3.5 crore
    )
    
    # Test 11: Boundary case - Exactly 10 years
    test_strategic_scenario(
        "Boundary Case: Exactly 10 Years",
        required_contribution=20000,
        years=10,  # exactly 10 years
        risk=RiskProfile.MODERATE,
        required_corpus=32000000  # 3.2 crore
    )
    
    print("\n" + "="*80)
    print("✅ ALL STRATEGIC SUGGESTION TESTS COMPLETED")
    print("="*80)
    
    # Summary
    print("\n" + "="*80)
    print("📋 STRATEGIC SUGGESTION RULES SUMMARY")
    print("="*80)
    print("Rule 1: Required SIP > ₹30,000")
    print("  → Suggest extending retirement age by 3 years")
    print()
    print("Rule 2: Years to Retirement < 10")
    print("  → Conservative: Suggest shifting to moderate risk")
    print("  → Moderate: Maximize contributions with moderate-aggressive allocation")
    print("  → Aggressive: Gradual shift to moderate to protect gains")
    print()
    print("Rule 3: Aggressive Risk Profile")
    print("  → Always suggest quarterly rebalancing due to high volatility")
    print("  → If years < 5: CRITICAL warning to shift 40-50% to conservative")
    print()
    print("Default: Balanced plan with no major concerns")
    print("  → Maintain discipline, review annually")
    print("="*80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
