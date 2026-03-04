import pandas as pd
import yfinance as yf
from strategies.breakout_strategy import BreakoutStrategy
from src.engine import ExecutionEngine
from src.visualisation import plot_equity_curve

def fetch_real_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    # download historical data from yahoo finance
    print(f"downloading data for {ticker}...")
    data = yf.download(ticker, start=start_date, end=end_date)
    
    # drop any multi-level index complexities if they exist
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
        
    # standardize column names to lowercase to match our strategy logic
    data.columns = [col.lower() for col in data.columns]
    
    # drop any rows with missing data to prevent calculation errors
    data = data.dropna()
    
    return data

if __name__ == "__main__":
    # 1. load real market data
    market_data = fetch_real_data(ticker="BTC-USD", start_date="2023-01-01", end_date="2024-01-01")
    
    # 2. instantiate strategy and generate signals
    print("generating breakout signals...")
    strategy = BreakoutStrategy(data=market_data, window=20)
    signals = strategy.generate_signals()
    
    # 3. run the execution engine with realistic transaction costs
    print("running backtest engine with transaction costs and slippage...")
    
    # setting commission to 0.08% and slippage to 0.1% as an example
    engine = ExecutionEngine(
        data=market_data, 
        signals=signals, 
        initial_capital=10000.0,
        commission_rate=0.0008, 
        slippage_rate=0.001
    )
    equity_curve = engine.run()
    
    # 4. view results
    print("backtest complete. plotting results.")
    plot_equity_curve(equity_curve, title="BTC-USD Breakout Strategy (Friction Adjusted)")