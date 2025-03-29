import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class BatteryDataHandler:
    def __init__(self, data_path: str):
        """
        Initialize the battery data handler with a path to the battery data file.
        
        Args:
            data_path (str): Path to the battery data file (CSV/JSON)
        """
        self.data_path = data_path
        self.data = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Load and preprocess the battery data.
        
        Returns:
            pd.DataFrame: Processed battery data with datetime index
        """
        try:
            if self.data_path.endswith('.csv'):
                self.data = pd.read_csv(self.data_path)
            elif self.data_path.endswith('.json'):
                self.data = pd.read_json(self.data_path)
            else:
                raise ValueError("Unsupported file format. Please use CSV or JSON.")
                
            # Ensure datetime index
            if 'timestamp' in self.data.columns:
                self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
                self.data.set_index('timestamp', inplace=True)
                
            # Sort by timestamp
            self.data.sort_index(inplace=True)
            
            return self.data
            
        except Exception as e:
            raise Exception(f"Error loading battery data: {str(e)}")
    
    def get_charge_data(self) -> pd.Series:
        """
        Get the battery charging data.
        
        Returns:
            pd.Series: Time series of battery charging power
        """
        if self.data is None:
            self.load_data()
        return self.data['charge_power']
    
    def get_discharge_data(self) -> pd.Series:
        """
        Get the battery discharging data.
        
        Returns:
            pd.Series: Time series of battery discharging power
        """
        if self.data is None:
            self.load_data()
        return self.data['discharge_power']
    
    def get_soc_data(self) -> pd.Series:
        """
        Get the battery state of charge data.
        
        Returns:
            pd.Series: Time series of battery state of charge
        """
        if self.data is None:
            self.load_data()
        return self.data['state_of_charge']
    
    def get_monthly_summary(self, month: Optional[datetime] = None) -> Dict:
        """
        Get a summary of battery operations for a specific month.
        
        Args:
            month (datetime, optional): The month to summarize. If None, uses current month.
            
        Returns:
            Dict: Summary statistics for the specified month
        """
        if self.data is None:
            self.load_data()
            
        if month is None:
            month = datetime.now()
            
        month_start = month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if month.month == 12:
            month_end = month.replace(year=month.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            month_end = month.replace(month=month.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)
            
        month_data = self.data[month_start:month_end]
        
        return {
            'total_charge': month_data['charge_power'].sum(),
            'total_discharge': month_data['discharge_power'].sum(),
            'avg_soc': month_data['state_of_charge'].mean(),
            'max_soc': month_data['state_of_charge'].max(),
            'min_soc': month_data['state_of_charge'].min(),
            'charge_cycles': len(month_data[month_data['charge_power'] > 0]),
            'discharge_cycles': len(month_data[month_data['discharge_power'] > 0])
        } 