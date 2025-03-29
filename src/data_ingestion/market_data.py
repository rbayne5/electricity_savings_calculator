import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class MarketDataHandler:
    def __init__(self, data_path: str):
        """
        Initialize the market data handler with a path to the market data file.
        
        Args:
            data_path (str): Path to the market data file (CSV/JSON)
        """
        self.data_path = data_path
        self.data = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Load and preprocess the market data.
        
        Returns:
            pd.DataFrame: Processed market data with datetime index
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
            raise Exception(f"Error loading market data: {str(e)}")
    
    def get_price_data(self) -> pd.Series:
        """
        Get the electricity price data.
        
        Returns:
            pd.Series: Time series of electricity prices
        """
        if self.data is None:
            self.load_data()
        return self.data['price']
    
    def get_monthly_summary(self, month: Optional[datetime] = None) -> Dict:
        """
        Get a summary of market prices for a specific month.
        
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
            'avg_price': month_data['price'].mean(),
            'max_price': month_data['price'].max(),
            'min_price': month_data['price'].min(),
            'price_std': month_data['price'].std(),
            'peak_hours': len(month_data[month_data['price'] > month_data['price'].mean()]),
            'off_peak_hours': len(month_data[month_data['price'] <= month_data['price'].mean()])
        }
    
    def get_price_periods(self) -> Dict[str, pd.Series]:
        """
        Get price data split into different time periods (peak, off-peak, etc.).
        
        Returns:
            Dict[str, pd.Series]: Dictionary of price data for different time periods
        """
        if self.data is None:
            self.load_data()
            
        mean_price = self.data['price'].mean()
        
        return {
            'peak': self.data[self.data['price'] > mean_price]['price'],
            'off_peak': self.data[self.data['price'] <= mean_price]['price']
        } 