import pytest
from src.data_ingestion.tariff_parser import TariffParser
from src.data_ingestion.battery_data import BatteryDataHandler
from src.data_ingestion.market_data import MarketDataHandler
from src.data_ingestion.caiso_api import CAISOAPI
from src.analysis.savings_calculator import SavingsCalculator
from src.visualization.reporting import generate_report

def test_imports():
    """Test that all required modules can be imported."""
    assert TariffParser is not None
    assert BatteryDataHandler is not None
    assert MarketDataHandler is not None
    assert CAISOAPI is not None
    assert SavingsCalculator is not None
    assert generate_report is not None

def test_caiso_api_initialization():
    """Test CAISO API initialization."""
    api = CAISOAPI()
    assert api.base_url == "http://oasis.caiso.com/oasisapi"
    assert api.config is not None
    assert isinstance(api.config, dict)

def test_savings_calculator_initialization():
    """Test SavingsCalculator initialization."""
    calculator = SavingsCalculator(
        tariff_path="test_data/tariff.pdf",
        battery_data_path="test_data/battery_data.csv",
        market_data_path="test_data/market_data.csv"
    )
    assert calculator.tariff_parser is not None
    assert calculator.battery_handler is not None
    assert calculator.market_handler is not None 