from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    def __init__(self, data: pd.DataFrame):
        # store historical data for the strategy to process
        self.data = data

    @abstractmethod
    def generate_signals(self) -> pd.Series:
        # must be implemented by child classes to return buy or sell signals
        pass