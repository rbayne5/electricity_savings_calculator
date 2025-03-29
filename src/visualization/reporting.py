import plotly.graph_objects as go
import plotly.express as px
from typing import Dict
import pandas as pd
from datetime import datetime

def generate_report(results: Dict, output_path: str):
    """
    Generate an HTML report with visualizations of the savings analysis.
    
    Args:
        results (Dict): Combined results from savings analysis and recommendations
        output_path (str): Path to save the HTML report
    """
    savings_analysis = results['savings_analysis']
    recommendations = results['optimization_recommendations']
    
    # Create HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Battery Asset Savings Report - {savings_analysis['month']}</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .section {{ margin-bottom: 30px; }}
            h1, h2 {{ color: #333; }}
            .summary-box {{ 
                background-color: #f5f5f5;
                padding: 20px;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Battery Asset Savings Report</h1>
            <div class="summary-box">
                <h2>Summary</h2>
                <p>Month: {savings_analysis['month']}</p>
                <p>Total Savings: ${savings_analysis['savings_breakdown']['total_savings']:.2f}</p>
                <p>Number of Arbitrage Opportunities: {savings_analysis['savings_breakdown']['number_of_opportunities']}</p>
            </div>
            
            <div class="section">
                <h2>Battery Operations</h2>
                <div id="battery_operations"></div>
            </div>
            
            <div class="section">
                <h2>Market Conditions</h2>
                <div id="market_conditions"></div>
            </div>
            
            <div class="section">
                <h2>Optimization Recommendations</h2>
                <div id="recommendations"></div>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Create visualizations
    battery_ops_fig = create_battery_operations_plot(savings_analysis)
    market_conditions_fig = create_market_conditions_plot(savings_analysis)
    recommendations_fig = create_recommendations_plot(recommendations)
    
    # Add plotly figures to HTML
    html_content = html_content.replace(
        '<div id="battery_operations"></div>',
        f'<div id="battery_operations">{battery_ops_fig.to_html(full_html=False)}</div>'
    )
    
    html_content = html_content.replace(
        '<div id="market_conditions"></div>',
        f'<div id="market_conditions">{market_conditions_fig.to_html(full_html=False)}</div>'
    )
    
    html_content = html_content.replace(
        '<div id="recommendations"></div>',
        f'<div id="recommendations">{recommendations_fig.to_html(full_html=False)}</div>'
    )
    
    # Save HTML file
    with open(output_path, 'w') as f:
        f.write(html_content)

def create_battery_operations_plot(savings_analysis: Dict) -> go.Figure:
    """Create a plot showing battery operations."""
    battery_ops = savings_analysis['battery_operations']
    
    fig = go.Figure()
    
    # Add charge and discharge bars
    fig.add_trace(go.Bar(
        name='Charge',
        x=['Total'],
        y=[battery_ops['total_charge']],
        marker_color='blue'
    ))
    
    fig.add_trace(go.Bar(
        name='Discharge',
        x=['Total'],
        y=[battery_ops['total_discharge']],
        marker_color='red'
    ))
    
    fig.update_layout(
        title='Battery Operations Summary',
        barmode='group',
        yaxis_title='Energy (kWh)'
    )
    
    return fig

def create_market_conditions_plot(savings_analysis: Dict) -> go.Figure:
    """Create a plot showing market conditions."""
    market_conditions = savings_analysis['market_conditions']
    
    fig = go.Figure()
    
    # Add price range
    fig.add_trace(go.Box(
        name='Price Range',
        q1=[market_conditions['avg_price'] - market_conditions['price_std']],
        median=[market_conditions['avg_price']],
        q3=[market_conditions['avg_price'] + market_conditions['price_std']],
        lowerfence=[market_conditions['min_price']],
        upperfence=[market_conditions['max_price']],
        boxpoints='all'
    ))
    
    fig.update_layout(
        title='Market Price Distribution',
        yaxis_title='Price ($/kWh)'
    )
    
    return fig

def create_recommendations_plot(recommendations: Dict) -> go.Figure:
    """Create a plot showing optimization recommendations."""
    # Create a sunburst chart for recommendations
    fig = go.Figure(go.Sunburst(
        ids=[
            'root',
            'charging', 'discharging', 'utilization', 'cost',
            'charging_times', 'charging_pattern', 'charging_efficiency',
            'discharging_times', 'discharging_pattern', 'discharging_efficiency',
            'utilization_rate', 'capacity', 'maintenance',
            'tariff', 'market', 'reduction'
        ],
        labels=[
            'Recommendations',
            'Charging Strategy', 'Discharging Strategy', 'Battery Utilization', 'Cost Optimization',
            'Optimal Times', 'Pattern', 'Efficiency',
            'Optimal Times', 'Pattern', 'Efficiency',
            'Rate', 'Capacity', 'Maintenance',
            'Tariff', 'Market', 'Reduction'
        ],
        parents=[
            '',
            'root', 'root', 'root', 'root',
            'charging', 'charging', 'charging',
            'discharging', 'discharging', 'discharging',
            'utilization', 'utilization', 'utilization',
            'cost', 'cost', 'cost'
        ]
    ))
    
    fig.update_layout(
        title='Optimization Recommendations Structure',
        width=800,
        height=600
    )
    
    return fig 