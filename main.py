#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path
from src.analysis.savings_calculator import SavingsCalculator

def format_currency(amount: float) -> str:
    """Format a number as currency."""
    return f"${amount:,.2f}"

def format_percentage(value: float) -> str:
    """Format a number as a percentage."""
    return f"{value:.1f}%"

def display_savings_analysis(savings: dict):
    """Display the savings analysis in a formatted way."""
    print("\n=== Battery Asset Bill Savings Analysis ===")
    print(f"Analysis Period: {savings['month']}")
    
    print("\nBattery Operations Summary:")
    print("-" * 40)
    battery_ops = savings['battery_operations']
    print(f"Total Energy Charged: {battery_ops['total_charge']:.2f} kWh")
    print(f"Total Energy Discharged: {battery_ops['total_discharge']:.2f} kWh")
    print(f"Average State of Charge: {format_percentage(battery_ops['avg_soc'])}")
    print(f"Number of Charge Cycles: {battery_ops['charge_cycles']}")
    print(f"Number of Discharge Cycles: {battery_ops['discharge_cycles']}")

    print("\nMarket Conditions:")
    print("-" * 40)
    market_cond = savings['market_conditions']
    print(f"Average Price: {format_currency(market_cond['avg_price'])}/kWh")
    print(f"Peak Price: {format_currency(market_cond['max_price'])}/kWh")
    print(f"Off-Peak Price: {format_currency(market_cond['min_price'])}/kWh")
    print(f"Peak Hours: {market_cond['peak_hours']}")
    print(f"Off-Peak Hours: {market_cond['off_peak_hours']}")

    print("\nBill Savings Summary:")
    print("-" * 40)
    breakdown = savings['savings_breakdown']
    print(f"Total Bill Savings: {format_currency(breakdown['total_savings'])}")
    print(f"Energy Cost Reduction: {format_percentage(breakdown['energy_cost_reduction'])}")
    print(f"Peak Demand Reduction: {format_percentage(breakdown['peak_demand_reduction'])}")
    
    if breakdown['total_savings'] > 0:
        print("\nSavings Breakdown by Component:")
        print("-" * 40)
        print(f"Energy Cost Savings: {format_currency(breakdown['energy_cost_savings'])}")
        print(f"Demand Charge Savings: {format_currency(breakdown['demand_charge_savings'])}")
        print(f"Other Savings: {format_currency(breakdown['other_savings'])}")

def save_savings_analysis(savings: dict, output_path: str):
    """Save the savings analysis to a JSON file."""
    with open(output_path, 'w') as f:
        json.dump(savings, f, indent=2, default=str)
    print(f"\nAnalysis saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Calculate monthly bill savings for battery assets')
    parser.add_argument('--tariff', required=True, help='Path to the tariff PDF file')
    parser.add_argument('--battery-data', required=True, help='Path to the battery data file (CSV/JSON)')
    parser.add_argument('--market-data', required=True, help='Path to the market data file (CSV/JSON)')
    parser.add_argument('--month', help='Month to analyze (YYYY-MM format)')
    parser.add_argument('--output', help='Output file path for the analysis (JSON format)')
    
    args = parser.parse_args()
    
    # Parse month if provided
    month = None
    if args.month:
        try:
            month = datetime.strptime(args.month, '%Y-%m')
        except ValueError:
            print("Error: Month must be in YYYY-MM format")
            return
    
    # Validate input files
    for file_path in [args.tariff, args.battery_data, args.market_data]:
        if not Path(file_path).exists():
            print(f"Error: File not found: {file_path}")
            return
    
    try:
        # Initialize calculator
        calculator = SavingsCalculator(
            tariff_path=args.tariff,
            battery_data_path=args.battery_data,
            market_data_path=args.market_data
        )
        
        # Calculate savings
        savings = calculator.calculate_monthly_savings(month)
        
        # Display results
        display_savings_analysis(savings)
        
        # Save results if output path provided
        if args.output:
            save_savings_analysis(savings, args.output)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return

if __name__ == "__main__":
    main() 