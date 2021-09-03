import pandas as pd

data = pd.read_csv('dataset/global.csv', index_col=0)
df = pd.DataFrame(data)

df.sort_values(by=['idGP', 'lap', 'position'], inplace=True)

grouped_df = df.groupby(['idGP', 'lap'])

for name, group in grouped_df:
     df.loc[(df['idGP'] == name[0]) & (df['lap'] == name[1]),'driverPrev'] = group['driver'].shift(1, fill_value=group['driver'].iloc[0])
     df.loc[(df['idGP'] == name[0]) & (df['lap'] == name[1]),'teamPrev'] = group['team'].shift(1, fill_value=group['team'].iloc[0])
     df.loc[(df['idGP'] == name[0]) & (df['lap'] == name[1]),'driverNext'] = group['driver'].shift(-1, fill_value=group['driver'].iloc[0])
     df.loc[(df['idGP'] == name[0]) & (df['lap'] == name[1]),'teamNext'] = group['team'].shift(-1,  fill_value=group['team'].iloc[0])

print(df.head())

df.sort_values(by=['idGP', 'driver', 'lap'], inplace=True)
grouped_df = df.groupby(['idGP', 'driver'])


for name, group in grouped_df:
     df.loc[(df['idGP'] == name[0]) & (df['driver'] == name[1]),'positionT-1'] = group['position'].shift(1, fill_value=group['position'].iloc[0])
     df.loc[(df['idGP'] == name[0]) & (df['driver'] == name[1]),'positionT-2'] = group['position'].shift(2, fill_value=group['position'].iloc[0])
     df.loc[(df['idGP'] == name[0]) & (df['driver'] == name[1]),'positionT-3'] = group['position'].shift(3, fill_value=group['position'].iloc[0])

df['performance'] = df['performance'].fillna(0).astype(int)
df['positionT-1'] = df['positionT-1'].astype(int)
df['positionT-2'] = df['positionT-2'].astype(int)
df['positionT-3'] = df['positionT-3'].astype(int)
print(df.head())

df.sort_values(by=['idGP', 'lap', 'position'], inplace=True)
df.to_csv('dataset/global-processed.csv')