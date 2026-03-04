import pandas as pd
from strategies.base_strategy import BaseStrategy

class MacdStrategy(BaseStrategy):
    def __init__(self, data: pd.DataFrame, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9):
        # initialize with data and standard macd periods
        super().__init__(data)
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period

    def generate_signals(self) -> pd.Series:
        # calculate fast and slow exponential moving averages
        ema_fast = self.data['close'].ewm(span=self.fast_period, adjust=False).mean()
        ema_slow = self.data['close'].ewm(span=self.slow_period, adjust=False).mean()
        
        # calculate the macd line and the signal line
        self.data['macd'] = ema_fast - ema_slow
        self.data['signal_line'] = self.data['macd'].ewm(span=self.signal_period, adjust=False).mean()
        
        # create an empty signal series defaulting to hold
        signals = pd.Series(index=self.data.index, data=0)
        
        # generate buy signal when macd crosses above signal line
        buy_condition = (self.data['macd'] > self.data['signal_line']) & (self.data['macd'].shift(1) <= self.data['signal_line'].shift(1))
        signals[buy_condition] = 1
        
        # generate sell signal when macd crosses below signal line
        sell_condition = (self.data['macd'] < self.data['signal_line']) & (self.data['macd'].shift(1) >= self.data['signal_line'].shift(1))
        signals[sell_condition] = -1
        
        return signals