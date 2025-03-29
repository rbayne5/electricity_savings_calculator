import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime
from ..data_ingestion.tariff_parser import TariffParser
from ..data_ingestion.battery_data import BatteryDataHandler
from ..data_ingestion.market_data import MarketDataHandler

class SavingsCalculator:
    def __init__(self, 
                 tariff_path: str,
                 battery_data_path: str,
                 market_data_path: str):
        """
        Initialize the savings calculator with paths to all required data.
        
        Args:
            tariff_path (str): Path to the tariff PDF file
            battery_data_path (str): Path to the battery data file
            market_data_path (str): Path to the market data file
        """
        self.tariff_parser = TariffParser(tariff_path)
        self.battery_handler = BatteryDataHandler(battery_data_path)
        self.market_handler = MarketDataHandler(market_data_path)
        
    def calculate_monthly_savings(self, month: Optional[datetime] = None) -> Dict:
        """
        Calculate monthly bill savings based on battery operations.
        
        Args:
            month (datetime, optional): The month to analyze. If None, uses current month.
            
        Returns:
            Dict: Detailed savings analysis for the specified month
        """
        if month is None:
            month = datetime.now()
            
        # Get tariff information
        tariff_data = self.tariff_parser.parse_pdf()
        rates = self.tariff_parser.get_rates()
        time_periods = self.tariff_parser.get_time_periods()
        
        # Get battery operations data
        battery_summary = self.battery_handler.get_monthly_summary(month)
        charge_data = self.battery_handler.get_charge_data()
        discharge_data = self.battery_handler.get_discharge_data()
        
        # Get market data
        market_summary = self.market_handler.get_monthly_summary(month)
        price_data = self.market_handler.get_price_data()
        
        # Calculate savings
        savings_breakdown = self._calculate_savings_breakdown(
            charge_data, discharge_data, price_data, rates, time_periods
        )
        
        savings_analysis = {
            'month': month.strftime('%Y-%m'),
            'battery_operations': battery_summary,
            'market_conditions': market_summary,
            'savings_breakdown': savings_breakdown,
            'total_savings': savings_breakdown['total_savings']
        }
        
        return savings_analysis
    
    def _calculate_savings_breakdown(self,
                                   charge_data: pd.Series,
                                   discharge_data: pd.Series,
                                   price_data: pd.Series,
                                   rates: List[Dict],
                                   time_periods: List[Dict]) -> Dict:
        """
        Calculate detailed savings breakdown by analyzing battery operations against prices.
        
        Args:
            charge_data (pd.Series): Battery charging data
            discharge_data (pd.Series): Battery discharging data
            price_data (pd.Series): Market price data
            rates (List[Dict]): Tariff rates
            time_periods (List[Dict]): Tariff time periods
            
        Returns:
            Dict: Detailed savings breakdown
        """
        # Align timestamps
        common_index = charge_data.index.intersection(discharge_data.index).intersection(price_data.index)
        charge_data = charge_data[common_index]
        discharge_data = discharge_data[common_index]
        price_data = price_data[common_index]
        
        # Calculate energy cost savings
        energy_cost_savings = self._calculate_energy_cost_savings(
            charge_data, discharge_data, price_data, rates, time_periods
        )
        
        # Calculate demand charge savings
        demand_charge_savings = self._calculate_demand_charge_savings(
            discharge_data, rates
        )
        
        # Calculate other savings (e.g., ancillary services, grid support)
        other_savings = self._calculate_other_savings(
            discharge_data, rates
        )
        
        # Calculate total savings
        total_savings = energy_cost_savings + demand_charge_savings + other_savings
        
        # Calculate percentage reductions
        total_energy_cost = (charge_data * price_data).sum()
        energy_cost_reduction = (energy_cost_savings / total_energy_cost * 100) if total_energy_cost > 0 else 0
        
        peak_demand = discharge_data.max()
        peak_demand_reduction = (peak_demand / (peak_demand + discharge_data.mean()) * 100) if peak_demand > 0 else 0
        
        return {
            'energy_cost_savings': energy_cost_savings,
            'demand_charge_savings': demand_charge_savings,
            'other_savings': other_savings,
            'total_savings': total_savings,
            'energy_cost_reduction': energy_cost_reduction,
            'peak_demand_reduction': peak_demand_reduction
        }
    
    def _calculate_energy_cost_savings(self,
                                     charge_data: pd.Series,
                                     discharge_data: pd.Series,
                                     price_data: pd.Series,
                                     rates: List[Dict],
                                     time_periods: List[Dict]) -> float:
        """Calculate energy cost savings from battery operations."""
        # Calculate cost without battery
        cost_without_battery = (discharge_data * price_data).sum()
        
        # Calculate cost with battery (charging at lower prices)
        cost_with_battery = (charge_data * price_data).sum()
        
        return cost_without_battery - cost_with_battery
    
    def _calculate_demand_charge_savings(self,
                                       discharge_data: pd.Series,
                                       rates: List[Dict]) -> float:
        """Calculate demand charge savings from peak demand reduction."""
        # Find peak demand rate from tariff
        peak_rate = next((rate['value'] for rate in rates if rate['type'] == 'demand_peak'), 0)
        
        # Calculate peak demand without battery
        peak_without_battery = discharge_data.max()
        
        # Calculate peak demand with battery (reduced)
        peak_with_battery = peak_without_battery * 0.8  # Assuming 20% peak reduction
        
        return (peak_without_battery - peak_with_battery) * peak_rate
    
    def _calculate_other_savings(self,
                               discharge_data: pd.Series,
                               rates: List[Dict]) -> float:
        """Calculate other savings (ancillary services, grid support, etc.)."""
        # This is a simplified calculation - in practice, this would be more complex
        # and would depend on the specific services provided and rates
        return 0.0  # Placeholder for future implementation 