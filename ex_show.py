import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import bar_chart_race as bcr

data = pd.read_csv('dataset/race3.csv', index_col=0)
startingLine = pd.DataFrame(data)

# startingLine['coef'] = startingLine['lap'] * startingLine['position']

for lap in range(3, 53):
    startingLine.loc[(startingLine['lap'] == lap), 'position'] =  np.arange(1, 21, dtype=int)

grouped_df = startingLine.groupby(['driver'])
for name, group in grouped_df:
    plt.plot(group['lap'], group['position'])

plt.title('Race', fontsize=14)
plt.xlabel('Lap', fontsize=14)
plt.ylabel('Position', fontsize=14, )
plt.grid(False)
plt.gca().invert_yaxis()
plt.show()

barChartDf = pd.DataFrame()
grouped_df = startingLine.groupby(['driver'])
for name, group in grouped_df:
    print(name)
    barChartDf[name] = (1/group['position'].values) * group['lap'].values

print(barChartDf.tail(20))

bcr.bar_chart_race(
    df=barChartDf,
    filename='test.mp4',
    orientation='h',
    sort='desc',
    n_bars=20,
    fixed_order=False,
    fixed_max=True,
    steps_per_period=4,
    interpolate_period=True,
    label_bars=True,
    bar_size=.95,
    perpendicular_bar_func='median',
    period_length=52,
    figsize=(5, 3),
    dpi=144,
    cmap='dark12',
    title='Race',
    title_size='',
    bar_label_size=7,
    tick_label_size=7,
    scale='log',
    writer=None,
    fig=None,
    bar_kwargs={'alpha': .7},
    filter_column_colors=False)  
