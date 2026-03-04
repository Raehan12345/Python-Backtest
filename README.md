# Python Trading Strategy Backtester

A custom-built, event-driven backtesting engine written in Python. This project simulates algorithmic trading strategies against historical data, accounting for realistic market conditions including transaction costs and slippage.

## Features
* Modular architecture separating strategy logic from execution
* Realistic order filling simulation
* Comprehensive performance metrics including Sharpe Ratio and Max Drawdown
* Visualization tools for equity curves and trade analysis

## Installation
1. Clone the repository.
2. Create a virtual environment.
3. Install dependencies via `pip install -r requirements.txt`.

## Usage
Run `main.py` to execute a sample backtest using the defined strategies. Add historical data to the `data/` directory before running.