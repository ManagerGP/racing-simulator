import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


data = pd.read_csv('dataset/race3.csv', index_col=0)
startingLine = pd.DataFrame(data)

# startingLine['coef'] = startingLine['lap'] * startingLine['position']

for lap in range(3, 70):
    startingLine.loc[(startingLine['lap'] == lap), 'position'] =  np.arange(1, 21, dtype=int)

grouped_df = startingLine.groupby(['driver'])
for name, group in grouped_df:
    plt.plot(group['lap'], group['position'])

plt.title('Race', fontsize=14)
plt.xlabel('Lap', fontsize=14)
plt.ylabel('Position', fontsize=14)
plt.grid(True)
plt.show()

