import pandas as pd

data = pd.read_csv('dataset/global_ex.csv', index_col=0)
df = pd.DataFrame(data)

df.sort_values(by=['idGP', 'lap', 'position'], inplace=True)

grouped_df = df.groupby(['idGP', 'lap'])

for name, group in grouped_df:
    idGp, lap = name
    df.loc[(df['idGP'] == idGp) & (df['lap'] == lap),'driverPrev'] = group['driver'].shift(1, fill_value=group['driver'].iloc[0])
    df.loc[(df['idGP'] == idGp) & (df['lap'] == lap),'driverNext'] = group['driver'].shift(-1, fill_value=group['driver'].iloc[0])

    df.loc[(df['idGP'] == idGp) & (df['lap'] == lap),'teamPrev'] = group['team'].shift(1, fill_value=group['team'].iloc[0])
    df.loc[(df['idGP'] == idGp) & (df['lap'] == lap),'teamNext'] = group['team'].shift(-1,  fill_value=group['team'].iloc[0])

df['performance'] = df['performance'].fillna(0).astype(int)

print(df.head())

df.to_csv('dataset/global_ex-processed.csv', index=False)