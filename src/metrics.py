import numpy as np
import pandas as pd

def calculate_sharpe_ratio(equity_curve: pd.Series, risk_free_rate: float = 0.0, periods: int = 252) -> float:
    # compute daily percentage returns directly from the equity curve
    daily_returns = equity_curve.pct_change().dropna()
    
    # calculate the mean and standard deviation of those daily returns
    mean_return = daily_returns.mean()
    std_dev = daily_returns.std()
    
    # avoid division by zero if the strategy never traded and has zero volatility
    if std_dev == 0.0 or pd.isna(std_dev):
        return 0.0
        
    # compute the daily sharpe ratio and scale it to an annualized figure
    daily_sharpe = (mean_return - risk_free_rate) / std_dev
    annualized_sharpe = daily_sharpe * np.sqrt(periods)
    
    return annualized_sharpe

def calculate_max_drawdown(equity_curve: pd.Series) -> float:
    # compute the running maximum of the portfolio value
    rolling_max = equity_curve.cummax()
    
    # calculate the percentage drop from the highest peak seen so far
    drawdowns = (equity_curve - rolling_max) / rolling_max
    
    # locate the most extreme negative percentage drop
    max_drawdown = drawdowns.min()
    
    return max_drawdown