import pandas as pd
from strategies.base_strategy import BaseStrategy

class MeanReversionStrategy(BaseStrategy):
    def __init__(self, data: pd.DataFrame, window: int = 20, num_std: float = 2.0):
        # initialize with data, moving average window, and standard deviation multiplier
        super().__init__(data)
        self.window = window
        self.num_std = num_std

    def generate_signals(self) -> pd.Series:
        # calculate the simple moving average and rolling standard deviation
        self.data['sma'] = self.data['close'].rolling(window=self.window).mean()
        self.data['std_dev'] = self.data['close'].rolling(window=self.window).std()
        
        # calculate upper and lower bollinger bands
        self.data['upper_band'] = self.data['sma'] + (self.data['std_dev'] * self.num_std)
        self.data['lower_band'] = self.data['sma'] - (self.data['std_dev'] * self.num_std)
        
        # create an empty signal series defaulting to hold
        signals = pd.Series(index=self.data.index, data=0)
        
        # generate buy signal when price crosses below the lower band
        buy_condition = (self.data['close'] < self.data['lower_band']) & (self.data['close'].shift(1) >= self.data['lower_band'].shift(1))
        signals[buy_condition] = 1
        
        # generate sell signal when price crosses above the upper band
        sell_condition = (self.data['close'] > self.data['upper_band']) & (self.data['close'].shift(1) <= self.data['upper_band'].shift(1))
        signals[sell_condition] = -1
        
        return signals