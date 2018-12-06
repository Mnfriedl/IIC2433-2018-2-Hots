"""File to merge different .csv's of data, in case you used differente PC's to parse the data
"""


import pandas as pd

data1 = pd.read_csv('data1.csv')
data2 = pd.read_csv('data2.csv')
data3 = pd.read_csv('data3.csv')

total_data = pd.concat([data1, data2, data3])

total_data.to_csv('data.csv')
