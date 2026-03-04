import numpy as np
import pandas as pd

def calculate_sharpe_ratio(returns_series: pd.Series, risk_free_rate: float = 0.0, periods: int = 252) -> float:
    # calculate the annualized sharpe ratio
    # periods represents the trading days in a year for daily data
    
    mean_return = returns_series.mean()
    std_dev = returns_series.std()
    
    # handle cases where volatility is zero to avoid division by zero
    if std_dev == 0:
        return 0.0
        
    # calculate daily sharpe and annualize it
    daily_sharpe = (mean_return - risk_free_rate) / std_dev
    annualized_sharpe = daily_sharpe * np.sqrt(periods)
    
    return annualized_sharpe

def calculate_max_drawdown(equity_curve: pd.Series) -> float:
    # calculate the maximum peak-to-trough drop in the equity curve
    
    rolling_max = equity_curve.cummax()
    drawdowns = (equity_curve - rolling_max) / rolling_max
    max_drawdown = drawdowns.min()
    
    return max_drawdown