import matplotlib.pyplot as plt
import pandas as pd

def plot_equity_curve(equity_curve: pd.Series, title: str = "strategy equity curve"):
    # plot the portfolio equity over time
    plt.figure(figsize=(10, 6))
    plt.plot(equity_curve.index, equity_curve.values, label='portfolio value')
    plt.title(title)
    plt.xlabel("time")
    plt.ylabel("equity")
    plt.legend()
    plt.grid(True)
    plt.show()