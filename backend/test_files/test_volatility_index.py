"""
Unit test for volatility index calculation
"""
import sys
sys.path.insert(0, 'D:\\PFRDA\\backend')

from app.services.insight_generator import InsightGenerator


def test_volatility_scenario(name: str, std_dev: float, mean: float):
    """Test a specific volatility scenario"""
    print(f"\n{'='*70}")
    print(f"📊 Test: {name}")
    print(f"{'='*70}")
    print(f"Inputs:")
    print(f"  - Mean Corpus: ₹{mean:,.0f}")
    print(f"  - Standard Deviation: ₹{std_dev:,.0f}")
    
    generator = InsightGenerator()
    result = generator.calculate_volatility_index(
        standard_deviation=std_dev,
        mean_corpus=mean
    )
    
    print(f"\n📈 Results:")
    print(f"  Volatility Percentage: {result['volatility_percentage']:.2f}%")
    print(f"  Volatility Level: {result['volatility_level'].upper()}")
    print(f"\n💡 Explanation:")
    print(f"  {result['explanation']}")


def main():
    print("\n" + "="*70)
    print("📉 VOLATILITY INDEX CALCULATION - UNIT TEST")
    print("="*70)
    
    # Test 1: Low Volatility - Conservative profile
    test_volatility_scenario(
        "Low Volatility - Stable Conservative Portfolio",
        std_dev=3000000,      # 30 lakh
        mean=30000000         # 3 crore
    )
    
    # Test 2: Medium Volatility - Balanced portfolio
    test_volatility_scenario(
        "Medium Volatility - Moderate Risk Portfolio",
        std_dev=10000000,     # 1 crore
        mean=50000000         # 5 crore
    )
    
    # Test 3: High Volatility - Aggressive strategy
    test_volatility_scenario(
        "High Volatility - Aggressive Growth Portfolio",
        std_dev=25000000,     # 2.5 crore
        mean=60000000         # 6 crore
    )
    
    # Test 4: Very Low Volatility - Ultra conservative
    test_volatility_scenario(
        "Very Low Volatility - Ultra Stable",
        std_dev=2000000,      # 20 lakh
        mean=40000000         # 4 crore
    )
    
    # Test 5: Extremely High Volatility - Speculative
    test_volatility_scenario(
        "Extremely High Volatility - Speculative Strategy",
        std_dev=40000000,     # 4 crore
        mean=80000000         # 8 crore
    )
    
    # Test 6: Boundary case - Exactly 15%
    test_volatility_scenario(
        "Boundary Case - Low/Medium Threshold (15%)",
        std_dev=7500000,      # 75 lakh
        mean=50000000         # 5 crore
    )
    
    # Test 7: Boundary case - Exactly 30%
    test_volatility_scenario(
        "Boundary Case - Medium/High Threshold (30%)",
        std_dev=15000000,     # 1.5 crore
        mean=50000000         # 5 crore
    )
    
    # Test 8: Small corpus, low volatility
    test_volatility_scenario(
        "Small Corpus - Low Volatility",
        std_dev=500000,       # 5 lakh
        mean=5000000          # 50 lakh
    )
    
    # Test 9: Large corpus, medium volatility
    test_volatility_scenario(
        "Large Corpus - Medium Volatility",
        std_dev=30000000,     # 3 crore
        mean=150000000        # 15 crore
    )
    
    print("\n" + "="*70)
    print("✅ ALL VOLATILITY INDEX TESTS COMPLETED")
    print("="*70)
    
    # Summary table
    print("\n" + "="*70)
    print("📊 VOLATILITY CLASSIFICATION REFERENCE")
    print("="*70)
    print("Level      | Range      | Description")
    print("-" * 70)
    print("LOW        | < 15%      | Stable, predictable outcomes")
    print("MEDIUM     | 15-30%     | Moderate uncertainty, typical for balanced portfolios")
    print("HIGH       | > 30%      | Significant variability, aggressive strategies")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
