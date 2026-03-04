import pandas as pd
from strategies.base_strategy import BaseStrategy

class BreakoutStrategy(BaseStrategy):
    def __init__(self, data: pd.DataFrame, window: int = 20):
        # initialize with data and the lookback window for the breakout
        super().__init__(data)
        self.window = window

    def generate_signals(self) -> pd.Series:
        # calculate rolling highs and lows for the channel
        self.data['rolling_high'] = self.data['close'].rolling(window=self.window).max()
        self.data['rolling_low'] = self.data['close'].rolling(window=self.window).min()
        
        # create an empty signal series
        signals = pd.Series(index=self.data.index, data=0)
        
        # generate buy signal when price breaks above the rolling high
        # this is particularly effective for high volatility assets like btc or eth
        buy_condition = self.data['close'] >= self.data['rolling_high'].shift(1)
        signals[buy_condition] = 1
        
        # generate sell signal when price breaks below the rolling low
        sell_condition = self.data['close'] <= self.data['rolling_low'].shift(1)
        signals[sell_condition] = -1
        
        return signals