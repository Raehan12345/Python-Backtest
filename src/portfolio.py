import pandas as pd

class Portfolio:
    def __init__(self, initial_capital: float):
        # initialize with starting capital and no positions
        self.initial_capital = initial_capital
        self.current_cash = initial_capital
        self.positions = 0
        self.equity_curve = []

    def update(self, price: float, action: str, quantity: int, commission_rate: float = 0.0, slippage_rate: float = 0.0):
        # process buying and selling with realistic market friction
        if action == 'buy':
            # slippage increases the price you pay
            fill_price = price * (1 + slippage_rate)
            trade_value = fill_price * quantity
            commission = trade_value * commission_rate
            total_cost = trade_value + commission
            
            # only execute if we have enough cash to cover the asset, slippage, and fees
            if self.current_cash >= total_cost:
                self.positions += quantity
                self.current_cash -= total_cost
                
        elif action == 'sell' and self.positions >= quantity:
            # slippage decreases the price you receive
            fill_price = price * (1 - slippage_rate)
            trade_value = fill_price * quantity
            commission = trade_value * commission_rate
            total_revenue = trade_value - commission
            
            self.positions -= quantity
            self.current_cash += total_revenue
            
        # record current total equity
        # we value current open positions at the current market price, not the fill price
        current_equity = self.current_cash + (self.positions * price)
        self.equity_curve.append(current_equity)

    def get_equity_curve(self) -> pd.Series:
        # return the recorded equity as a pandas series
        return pd.Series(self.equity_curve)