import pandas as pd
import yfinance as yf
import os

from strategies.sma_crossover import SmaCrossoverStrategy
from strategies.mean_reversion import MeanReversionStrategy
from strategies.macd_strategy import MacdStrategy
from src.engine import ExecutionEngine
from src.visualisation import plot_multiple_equity_curves
from src.metrics import calculate_sharpe_ratio, calculate_max_drawdown

def fetch_real_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    # download historical data from yahoo finance
    print(f"downloading data for {ticker}...")
    data = yf.download(ticker, start=start_date, end=end_date)
    
    # drop any multi-level index complexities if they exist
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
        
    # standardize column names to lowercase to match our strategy logic
    data.columns = [col.lower() for col in data.columns]
    data = data.dropna()
    return data

if __name__ == "__main__":
    # 1. load market data
    ticker_symbol = "AAPL"
    market_data = fetch_real_data(ticker=ticker_symbol, start_date="2020-01-01", end_date="2024-01-01")
    
    # 2. define the professional strategies to test
    strategies = {
        "SMA Crossover (50/200)": SmaCrossoverStrategy(data=market_data.copy(), short_window=50, long_window=200),
        "Mean Reversion (Bollinger)": MeanReversionStrategy(data=market_data.copy(), window=20, num_std=2.0),
        "MACD (12/26/9)": MacdStrategy(data=market_data.copy())
    }
    
    results_curves = {}
    
    print("\n=== beginning comparative backtest ===")
    
    # 3. execute each strategy and collect results
    for name, strategy in strategies.items():
        print(f"processing {name}...")
        signals = strategy.generate_signals()
        
        engine = ExecutionEngine(
            data=market_data, 
            signals=signals, 
            initial_capital=10000.0,
            commission_rate=0.001, 
            slippage_rate=0.001
        )
        
        equity_curve = engine.run()
        results_curves[name] = equity_curve
        
        # calculate and print metrics
        sharpe = calculate_sharpe_ratio(equity_curve)
        mdd = calculate_max_drawdown(equity_curve)
        final_equity = equity_curve.iloc[-1]
        
        print(f"  final equity: ${final_equity:.2f} | sharpe: {sharpe:.2f} | mdd: {mdd * 100:.2f}%\n")
        
    # 4. plot and save results
    # ensure an assets directory exists to store the image cleanly
    os.makedirs("assets", exist_ok=True)
    save_location = "assets/comparison_chart.png"
    
    plot_multiple_equity_curves(
        curves=results_curves, 
        title=f"{ticker_symbol} Strategy Performance Comparison",
        save_path=save_location
    )