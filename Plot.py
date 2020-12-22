import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# The graph will take 2 values the time and the current capacity
def plot_graph(csv_file):
    headers = ['time','capacity']
    df = pd.read_csv(csv_file, names=headers)
    print(df)
    x = df['time']
    y = df['capacity']

    # plot
    plt.plot(x,y)
    # beautify the x-labels
    plt.gcf().autofmt_xdate()
    plt.show()


plot_graph("data.csv")