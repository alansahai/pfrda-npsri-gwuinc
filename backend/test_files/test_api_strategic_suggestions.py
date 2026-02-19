"""
API Example: Enhanced Reverse Calculator with Strategic Suggestions
Demonstrates the new strategic_suggestions feature
"""
import requests
import json


BASE_URL = "http://localhost:8000/api/v1/forecast"


def test_reverse_calculator_with_suggestions(test_name: str, payload: dict):
    """Test reverse calculator with strategic suggestions"""
    print(f"\n{'='*80}")
    print(f"Test: {test_name}")
    print(f"{'='*80}")
    print(f"Request:")
    for key, value in payload.items():
        print(f"  - {key}: {value}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/reverse-pension",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ SUCCESS")
            print(f"\n📊 CALCULATION RESULTS:")
            print(f"  Required Monthly Contribution: ₹{result['required_monthly_contribution']:,.0f}")
            print(f"  Estimated Corpus Needed: ₹{result['estimated_corpus_needed']:,.0f}")
            print(f"  Investment Horizon: {result['investment_horizon_years']} years")
            print(f"  Total Contributions Needed: ₹{result['total_contributions_needed']:,.0f}")
            print(f"  Risk Profile: {result['risk_profile'].upper()}")
            
            print(f"\n💡 STRATEGIC SUGGESTIONS ({len(result['strategic_suggestions'])}):")
            for i, suggestion in enumerate(result['strategic_suggestions'], 1):
                print(f"\n  {i}. {suggestion}")
            
            if result.get('insights'):
                print(f"\n📈 INSIGHTS ({len(result['insights'])}):")
                for insight in result['insights']:
                    emoji = "⚠️" if insight['severity'] == "warning" else "✅" if insight['severity'] == "positive" else "ℹ️"
                    print(f"\n  {emoji} {insight['title']}")
                    print(f"     {insight['message'][:100]}...")
        else:
            print(f"\n❌ FAILED: {response.status_code}")
            print(f"Error: {response.text}")
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")


def main():
    print("\n" + "="*80)
    print("🎯 ENHANCED REVERSE CALCULATOR WITH STRATEGIC SUGGESTIONS")
    print("="*80)
    
    # Scenario 1: High Required Contribution
    test_reverse_calculator_with_suggestions(
        "Scenario 1: High Required Contribution (> ₹30,000)",
        {
            "current_age": 40,
            "retirement_age": 55,
            "desired_monthly_pension": 80000,
            "risk_profile": "moderate",
            "annual_income_growth": 5.0
        }
    )
    
    # Scenario 2: Short Timeline + Conservative
    test_reverse_calculator_with_suggestions(
        "Scenario 2: Short Timeline + Conservative Risk",
        {
            "current_age": 53,
            "retirement_age": 60,
            "desired_monthly_pension": 50000,
            "risk_profile": "conservative",
            "annual_income_growth": 4.0
        }
    )
    
    # Scenario 3: Aggressive + Short Timeline (CRITICAL)
    test_reverse_calculator_with_suggestions(
        "Scenario 3: CRITICAL - Aggressive + Very Short Timeline",
        {
            "current_age": 57,
            "retirement_age": 60,
            "desired_monthly_pension": 60000,
            "risk_profile": "aggressive",
            "annual_income_growth": 5.0
        }
    )
    
    # Scenario 4: Ideal Balanced Plan
    test_reverse_calculator_with_suggestions(
        "Scenario 4: Ideal Balanced Plan",
        {
            "current_age": 30,
            "retirement_age": 60,
            "desired_monthly_pension": 50000,
            "risk_profile": "moderate",
            "annual_income_growth": 6.0
        }
    )
    
    # Scenario 5: Multiple Triggers
    test_reverse_calculator_with_suggestions(
        "Scenario 5: Multiple Triggers - High Contribution + Short + Aggressive",
        {
            "current_age": 56,
            "retirement_age": 60,
            "desired_monthly_pension": 100000,
            "risk_profile": "aggressive",
            "annual_income_growth": 5.0
        }
    )
    
    print("\n" + "="*80)
    print("✅ ALL API TESTS COMPLETED")
    print("="*80)
    
    print("\n" + "="*80)
    print("📋 STRATEGIC SUGGESTION RULES")
    print("="*80)
    print("""
Rule 1: Required SIP > ₹30,000
  → Suggest extending retirement age by 3 years

Rule 2: Years to Retirement < 10
  → Tailored suggestions based on risk profile:
     • Conservative: Suggest shifting to moderate risk
     • Moderate: Maximize contributions with moderate-aggressive allocation
     • Aggressive: Gradual shift to moderate to protect gains

Rule 3: Aggressive Risk Profile
  → Always suggest quarterly rebalancing due to high volatility
  → If years < 5: CRITICAL warning to shift 40-50% to conservative assets

Additional Logic:
  → Manageable contribution + short timeline: Emphasize consistency
  → No major triggers: Maintain discipline, review annually
""")
    print("="*80)
    
    print("\n" + "="*80)
    print("📚 RESPONSE STRUCTURE")
    print("="*80)
    print("""
{
  "required_monthly_contribution": float,
  "estimated_corpus_needed": float,
  "investment_horizon_years": int,
  "total_contributions_needed": float,
  "risk_profile": string,
  "insights": [
    {
      "title": string,
      "message": string,
      "severity": "info" | "warning" | "positive"
    }
  ],
  "strategic_suggestions": [string]  // ← NEW FEATURE
}
""")
    print("="*80 + "\n")


if __name__ == "__main__":
    print("\n⚠️  NOTE: This test requires the FastAPI server to be running.")
    print("   Start the server with: uvicorn app.main:app --reload")
    print("   Then run this script.\n")
    
    try:
        # Quick health check
        response = requests.get(f"{BASE_URL.replace('/api/v1/forecast', '')}/health", timeout=2)
        if response.status_code == 200:
            print("✅ Server is running. Starting tests...\n")
            main()
        else:
            print("❌ Server responded but health check failed.")
    except requests.exceptions.RequestException:
        print("❌ Server is not running. Please start the server first.")
        print("   Command: cd backend && uvicorn app.main:app --reload\n")
