# Battery Asset Savings Calculator

A Python-based tool for calculating monthly bill savings for battery asset owners by analyzing electricity tariffs, battery operations, and market pricing data.

## Features

- PDF tariff data ingestion and parsing
- Battery charge/discharge data analysis
- Electricity market pricing integration
- Monthly bill savings calculation
- Detailed reporting and visualization

## Project Structure

```
electricity_savings_calculator/
├── src/
│   ├── data_ingestion/
│   │   ├── tariff_parser.py      # PDF tariff data parsing
│   │   ├── battery_data.py       # Battery operations data handling
│   │   └── market_data.py        # Market pricing data integration
│   ├── analysis/
│   │   ├── savings_calculator.py # Core savings calculation logic
│   │   └── optimization.py       # Battery operation optimization
│   └── visualization/
│       └── reporting.py          # Results visualization and reporting
├── tests/                        # Unit and integration tests
├── data/                         # Sample data and configuration files
├── requirements.txt              # Project dependencies
└── README.md                     # Project documentation
```

## Requirements

- Python 3.8+
- PDF parsing libraries (PyPDF2/pdfplumber)
- Data analysis libraries (pandas, numpy)
- Visualization libraries (matplotlib, plotly)
- Testing framework (pytest)

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Prepare your input data:
   - Electricity tariff PDF
   - Battery operation data (CSV/JSON format)
   - Market pricing data

2. Run the calculator:
   ```bash
   python src/main.py --tariff path/to/tariff.pdf --battery-data path/to/battery_data.csv --market-data path/to/market_data.csv
   ```

3. View the generated reports and savings analysis

## Output

The tool generates:
- Monthly bill savings calculations
- Battery operation optimization recommendations
- Visual reports showing savings breakdown
- Exportable CSV/PDF reports

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License
