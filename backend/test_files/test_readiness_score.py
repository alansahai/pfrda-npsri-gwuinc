"""
Test script for retirement readiness scoring system
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1/forecast"

def test_readiness_score(test_name: str, payload: dict):
    """Test readiness score calculation"""
    print(f"\n{'='*60}")
    print(f"Test: {test_name}")
    print(f"{'='*60}")
    print(f"Request: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/readiness-score",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ SUCCESS")
            print(f"Score: {result['score']}/100")
            print(f"Label: {result['label']}")
            print(f"\nDetails:")
            for key, value in result['details'].items():
                print(f"  - {key}: {value}")
            print(f"\nRecommendation:")
            print(f"  {result['recommendation']}")
        else:
            print(f"\n❌ FAILED: {response.status_code}")
            print(f"Error: {response.text}")
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")


def main():
    """Run all test scenarios"""
    
    print("\n" + "="*60)
    print("RETIREMENT READINESS SCORING SYSTEM - TEST SUITE")
    print("="*60)
    
    # Test 1: Strong Outlook (High corpus, long horizon, conservative)
    test_readiness_score(
        "Strong Outlook - Excellent Readiness",
        {
            "median_corpus": 50000000,  # 5 crore
            "required_corpus": 40000000,  # 4 crore
            "years_to_retirement": 25,
            "risk_profile": "conservative"
        }
    )
    
    # Test 2: Moderate Confidence (Adequate corpus, medium horizon, moderate risk)
    test_readiness_score(
        "Moderate Confidence - On Track",
        {
            "median_corpus": 30000000,  # 3 crore
            "required_corpus": 35000000,  # 3.5 crore
            "years_to_retirement": 15,
            "risk_profile": "moderate"
        }
    )
    
    # Test 3: High Risk (Low corpus, short horizon, aggressive)
    test_readiness_score(
        "High Risk - Significant Shortfall",
        {
            "median_corpus": 10000000,  # 1 crore
            "required_corpus": 30000000,  # 3 crore
            "years_to_retirement": 5,
            "risk_profile": "aggressive"
        }
    )
    
    # Test 4: Edge case - Zero required corpus
    test_readiness_score(
        "Edge Case - No Target Set",
        {
            "median_corpus": 20000000,
            "required_corpus": 0,
            "years_to_retirement": 10,
            "risk_profile": "moderate"
        }
    )
    
    # Test 5: Moderate with short horizon
    test_readiness_score(
        "Moderate Risk - Short Timeline",
        {
            "median_corpus": 15000000,  # 1.5 crore
            "required_corpus": 20000000,  # 2 crore
            "years_to_retirement": 3,
            "risk_profile": "conservative"
        }
    )
    
    # Test 6: Strong with aggressive profile
    test_readiness_score(
        "Strong Outlook - Aggressive Strategy",
        {
            "median_corpus": 60000000,  # 6 crore
            "required_corpus": 45000000,  # 4.5 crore
            "years_to_retirement": 20,
            "risk_profile": "aggressive"
        }
    )
    
    print("\n" + "="*60)
    print("TEST SUITE COMPLETED")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
