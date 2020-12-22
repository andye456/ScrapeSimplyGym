import requests
import pandas as pd
from matplotlib import pyplot as plt
import io

resp = requests.get("http://35.176.56.125:32766").content

headers = ['time', 'capacity']
df = pd.read_csv(io.StringIO(resp.decode('utf-8')), names=headers)
print(df)
x = df['time']
y = df['capacity']

# plot
plt.plot(x, y)
# beautify the x-labels
plt.gcf().autofmt_xdate()
plt.show()