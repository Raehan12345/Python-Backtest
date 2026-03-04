import pandas as pd
import numpy as np
from strategies.base_strategy import BaseStrategy

class SmaCrossoverStrategy(BaseStrategy):
    def __init__(self, data: pd.DataFrame, short_window: int = 50, long_window: int = 200):
        # initialize with data and the two moving average windows
        super().__init__(data)
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self) -> pd.Series:
        # calculate the short and long simple moving averages
        self.data['short_mavg'] = self.data['close'].rolling(window=self.short_window, min_periods=1).mean()
        self.data['long_mavg'] = self.data['close'].rolling(window=self.long_window, min_periods=1).mean()
        
        # create an empty signal series defaulting to hold
        signals = pd.Series(index=self.data.index, data=0)
        
        # generate a buy signal when the short moving average crosses above the long moving average
        buy_condition = (self.data['short_mavg'] > self.data['long_mavg']) & (self.data['short_mavg'].shift(1) <= self.data['long_mavg'].shift(1))
        signals[buy_condition] = 1
        
        # generate a sell signal when the short moving average crosses below the long moving average
        sell_condition = (self.data['short_mavg'] < self.data['long_mavg']) & (self.data['short_mavg'].shift(1) >= self.data['long_mavg'].shift(1))
        signals[sell_condition] = -1
        
        return signals