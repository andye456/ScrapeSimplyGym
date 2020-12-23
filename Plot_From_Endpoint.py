import requests
import pandas as pd
from matplotlib import pyplot as plt
import io

resp = requests.get("http://35.176.56.125:32766/data.csv").content

headers = ['time', 'capacity']
# Creates the dataframe from the csv data, skips the header text values.
df = pd.read_csv(io.StringIO(resp.decode('utf-8')), names=headers, skiprows=1)
print(df)
x = df['time']
y = df['capacity']

# plot
plt.plot(x, y)
# beautify the x-labels
plt.gcf().autofmt_xdate()
ax = plt.gca()

# Only display every 10th value to prevent overlap
labels=ax.get_xaxis().get_ticklabels()
for label in range(len(labels)):
    if label % 10 != 0:
        labels[label].set_visible(False)
plt.show()