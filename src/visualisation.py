import matplotlib.pyplot as plt
import pandas as pd

def plot_multiple_equity_curves(curves: dict, title: str = "strategy comparison", save_path: str = None):
    # plot multiple portfolio equity curves on a single chart for comparison
    plt.figure(figsize=(12, 7))
    
    # iterate through the dictionary and plot each curve
    for strategy_name, equity_curve in curves.items():
        plt.plot(equity_curve.index, equity_curve.values, label=strategy_name)
        
    plt.title(title)
    plt.xlabel("time")
    plt.ylabel("equity")
    plt.legend()
    plt.grid(True)
    
    # save the figure to the repository if a path is provided
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        print(f"chart successfully saved to {save_path}")
        
    plt.show()