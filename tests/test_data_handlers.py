import pytest
import pandas as pd
from datetime import datetime
from src.data_ingestion.battery_data import BatteryDataHandler
from src.data_ingestion.market_data import MarketDataHandler

@pytest.fixture
def battery_data_handler():
    """Create a battery data handler instance for testing."""
    return BatteryDataHandler("tests/test_data/battery_data.csv")

@pytest.fixture
def market_data_handler():
    """Create a market data handler instance for testing."""
    return MarketDataHandler("tests/test_data/market_data.csv")

def test_battery_data_loading(battery_data_handler):
    """Test battery data loading and basic properties."""
    data = battery_data_handler.load_data()
    
    # Check if data is loaded as DataFrame
    assert isinstance(data, pd.DataFrame)
    
    # Check required columns (excluding timestamp which is the index)
    required_columns = ['charge_power', 'discharge_power', 'state_of_charge']
    for col in required_columns:
        assert col in data.columns
        
    # Check data types
    assert pd.api.types.is_datetime64_any_dtype(data.index)
    assert pd.api.types.is_float_dtype(data['charge_power'])
    assert pd.api.types.is_float_dtype(data['discharge_power'])
    assert pd.api.types.is_float_dtype(data['state_of_charge'])
    
    # Check data ranges
    assert data['state_of_charge'].between(0, 100).all()
    assert (data['charge_power'] >= 0).all()
    assert (data['discharge_power'] >= 0).all()

def test_battery_monthly_summary(battery_data_handler):
    """Test battery monthly summary calculation."""
    month = datetime(2024, 3, 29)
    summary = battery_data_handler.get_monthly_summary(month)
    
    # Check summary structure
    assert isinstance(summary, dict)
    assert 'total_charge' in summary
    assert 'total_discharge' in summary
    assert 'avg_soc' in summary
    assert 'max_soc' in summary
    assert 'min_soc' in summary
    assert 'charge_cycles' in summary
    assert 'discharge_cycles' in summary
    
    # Check summary values
    assert summary['total_discharge'] > 0
    assert summary['min_soc'] <= summary['avg_soc'] <= summary['max_soc']

def test_market_data_loading(market_data_handler):
    """Test market data loading and basic properties."""
    data = market_data_handler.load_data()
    
    # Check if data is loaded as DataFrame
    assert isinstance(data, pd.DataFrame)
    
    # Check required columns
    assert 'price' in data.columns
    
    # Check data types
    assert pd.api.types.is_datetime64_any_dtype(data.index)
    assert pd.api.types.is_float_dtype(data['price'])
    
    # Check data validity
    assert (data['price'] >= 0).all()

def test_market_monthly_summary(market_data_handler):
    """Test market data monthly summary calculation."""
    month = datetime(2024, 3, 29)
    summary = market_data_handler.get_monthly_summary(month)
    
    # Check summary structure
    assert isinstance(summary, dict)
    assert 'avg_price' in summary
    assert 'max_price' in summary
    assert 'min_price' in summary
    assert 'price_std' in summary
    assert 'peak_hours' in summary
    assert 'off_peak_hours' in summary
    
    # Check summary values
    assert summary['min_price'] <= summary['avg_price'] <= summary['max_price']
    assert summary['peak_hours'] + summary['off_peak_hours'] == len(market_data_handler.data)

def test_data_alignment(battery_data_handler, market_data_handler):
    """Test that battery and market data can be aligned for analysis."""
    battery_data = battery_data_handler.load_data()
    market_data = market_data_handler.load_data()
    
    # Check timestamp alignment
    common_timestamps = battery_data.index.intersection(market_data.index)
    assert len(common_timestamps) > 0
    
    # Check data frequency (both 5min and 5T are valid in pandas)
    battery_freq = pd.infer_freq(battery_data.index)
    market_freq = pd.infer_freq(market_data.index)
    assert battery_freq in ['5T', '5min']
    assert market_freq in ['5T', '5min']
    assert battery_freq == market_freq  # Both should use the same format 