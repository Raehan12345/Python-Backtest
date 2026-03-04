import pandas as pd
from src.portfolio import Portfolio

class ExecutionEngine:
    def __init__(self, data: pd.DataFrame, signals: pd.Series, initial_capital: float = 10000.0, commission_rate: float = 0.001, slippage_rate: float = 0.001):
        # setup the engine with market data, signals, capital, and friction parameters
        self.data = data
        self.signals = signals
        self.commission_rate = commission_rate
        self.slippage_rate = slippage_rate
        self.portfolio = Portfolio(initial_capital)

    def run(self) -> pd.Series:
        # iterate through the data to simulate trading step by step
        for i in range(len(self.data)):
            current_price = self.data['close'].iloc[i]
            current_signal = self.signals.iloc[i]
            
            # execute trades based on signals while applying friction
            if current_signal == 1:
                self.portfolio.update(
                    price=current_price, 
                    action='buy', 
                    quantity=1, 
                    commission_rate=self.commission_rate, 
                    slippage_rate=self.slippage_rate
                )
            elif current_signal == -1:
                self.portfolio.update(
                    price=current_price, 
                    action='sell', 
                    quantity=1, 
                    commission_rate=self.commission_rate, 
                    slippage_rate=self.slippage_rate
                )
            else:
                # hold position but update the equity curve to reflect mark-to-market value
                self.portfolio.update(
                    price=current_price, 
                    action='hold', 
                    quantity=0, 
                    commission_rate=0.0, 
                    slippage_rate=0.0
                )
                
        return self.portfolio.get_equity_curve()