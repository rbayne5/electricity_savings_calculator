import pytest
from datetime import datetime
from src.analysis.savings_calculator import SavingsCalculator

@pytest.fixture
def calculator():
    """Create a SavingsCalculator instance for testing."""
    return SavingsCalculator(
        tariff_path="tests/test_data/tariff.pdf",
        battery_data_path="tests/test_data/battery_data.csv",
        market_data_path="tests/test_data/market_data.csv"
    )

def test_savings_calculation(calculator):
    """Test monthly savings calculation."""
    month = datetime(2024, 3, 29)
    savings = calculator.calculate_monthly_savings(month)
    
    # Check savings analysis structure
    assert isinstance(savings, dict)
    assert 'month' in savings
    assert 'battery_operations' in savings
    assert 'market_conditions' in savings
    assert 'savings_breakdown' in savings
    assert 'total_savings' in savings
    
    # Check savings breakdown structure
    breakdown = savings['savings_breakdown']
    assert 'arbitrage_opportunities' in breakdown
    assert 'total_savings' in breakdown
    assert 'number_of_opportunities' in breakdown
    assert 'average_savings_per_opportunity' in breakdown
    
    # Check savings values
    assert savings['total_savings'] >= 0
    assert breakdown['total_savings'] >= 0
    assert breakdown['number_of_opportunities'] >= 0
    if breakdown['number_of_opportunities'] > 0:
        assert breakdown['average_savings_per_opportunity'] > 0

def test_savings_breakdown_calculation(calculator):
    """Test the detailed savings breakdown calculation."""
    month = datetime(2024, 3, 29)
    savings = calculator.calculate_monthly_savings(month)
    breakdown = savings['savings_breakdown']
    
    # Check arbitrage opportunities
    for opp in breakdown['arbitrage_opportunities']:
        assert isinstance(opp, dict)
        assert 'timestamp' in opp
        assert 'charge_price' in opp
        assert 'discharge_price' in opp
        assert 'price_difference' in opp
        assert 'energy' in opp
        
        # Verify arbitrage logic
        assert opp['discharge_price'] > opp['charge_price']
        assert opp['price_difference'] == opp['discharge_price'] - opp['charge_price']
        assert opp['energy'] > 0
    
    # Verify total savings calculation
    calculated_total = sum(opp['price_difference'] * opp['energy'] 
                         for opp in breakdown['arbitrage_opportunities'])
    assert abs(calculated_total - breakdown['total_savings']) < 0.01  # Allow for small floating-point differences 