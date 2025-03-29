import argparse
import json
from datetime import datetime
from analysis.savings_calculator import SavingsCalculator
from visualization.reporting import generate_report

def main():
    parser = argparse.ArgumentParser(description='Calculate monthly bill savings for battery assets')
    parser.add_argument('--tariff', required=True, help='Path to the tariff PDF file')
    parser.add_argument('--battery-data', required=True, help='Path to the battery data file (CSV/JSON)')
    parser.add_argument('--market-data', required=True, help='Path to the market data file (CSV/JSON)')
    parser.add_argument('--month', help='Month to analyze (YYYY-MM format)')
    parser.add_argument('--output', default='savings_report.json', help='Output file path for the report')
    
    args = parser.parse_args()
    
    # Parse month if provided
    month = None
    if args.month:
        try:
            month = datetime.strptime(args.month, '%Y-%m')
        except ValueError:
            print("Error: Month must be in YYYY-MM format")
            return
    
    # Initialize calculator
    calculator = SavingsCalculator(
        tariff_path=args.tariff,
        battery_data_path=args.battery_data,
        market_data_path=args.market_data
    )
    
    # Calculate savings
    savings_analysis = calculator.calculate_monthly_savings(month)
    
    # Get optimization recommendations
    recommendations = calculator.get_optimization_recommendations(month)
    
    # Combine results
    results = {
        'savings_analysis': savings_analysis,
        'optimization_recommendations': recommendations
    }
    
    # Save results to file
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    # Generate and display summary
    print("\nSavings Analysis Summary:")
    print(f"Month: {savings_analysis['month']}")
    print(f"Total Savings: ${savings_analysis['savings_breakdown']['total_savings']:.2f}")
    print(f"Number of Arbitrage Opportunities: {savings_analysis['savings_breakdown']['number_of_opportunities']}")
    print(f"\nDetailed report saved to: {args.output}")
    
    # Generate visualization
    generate_report(results, f"{args.output.replace('.json', '_report.html')}")

if __name__ == '__main__':
    main()
