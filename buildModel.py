import pandas as pd

data = pd.read_csv('dataset/global.csv', index_col=0)
df = pd.DataFrame(data)
df
df.sort_values(by=['idGP', 'lap', 'position'], inplace=True)
print(df)

grouped_df = df.groupby(['idGP', 'lap'])

for group in grouped_df:
     group[1].loc[:,'driverPrev'] = group[1]['driver'].shift(1)
     group[1].loc[:,'teamPrev'] = group[1]['team'].shift(1)
     group[1].loc[:,'driverNext'] = group[1]['driver'].shift(-1)
     group[1].loc[:,'teamNext'] = group[1]['team'].shift(-1)
     print(group)
     break

# df = grouped_df.apply(lambda x : x.reset_index())
# print(df)

# df = df.groupby(['idGP', 'driver'])

# for group in df:
#     group[1]['positionT-1'] = group[1]['position'].shift(1)
#     group[1]['positionT-2'] = group[1]['position'].shift(2)
#     group[1]['positionT-3'] = group[1]['position'].shift(3)
#     print(group)
#     break