import pandas as pd
from strategies.base_strategy import BaseStrategy

class MeanReversionStrategy(BaseStrategy):
    def __init__(self, data: pd.DataFrame, window: int = 20):
        # initialize with data and moving average window
        super().__init__(data)
        self.window = window

    def generate_signals(self) -> pd.Series:
        # calculate the simple moving average
        self.data['sma'] = self.data['close'].rolling(window=self.window).mean()
        
        signals = pd.Series(index=self.data.index, data=0)
        
        # buy when price is below sma, sell when above
        signals[self.data['close'] < self.data['sma']] = 1
        signals[self.data['close'] > self.data['sma']] = -1
        
        return signals