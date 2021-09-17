import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
from tensorflow import keras


path_checkpoint = "model_checkpoint.h5"
model = keras.models.load_model(path_checkpoint)

data = pd.read_csv('dataset/global_ex-processed.csv')
df = pd.DataFrame(data)

df.sort_values(by=['idGP', 'driver', 'lap'], inplace=True)

df.drop(columns=['out', 'targetPosition', 'windSpeed','humidity','pressure','windDir'], inplace=True)

for idx, col in enumerate(['driver', 'tyre', 'track', 'team', 'driverPrev', 'teamPrev', 'driverNext', 'teamNext']):
    df[col] = pd.Categorical(df[col])
    df[col] = df[col].cat.codes

print(df.head())

startingLine = pd.DataFrame(columns=df.columns)
grouped_df = df.groupby(['idGP', 'driver'])
for name, group in grouped_df:
    if(name[0] == 25):
        startingLine = startingLine.append(group.iloc[0:5], ignore_index=True)

startingLine.drop(columns=['idGP'], inplace=True)
print(startingLine)

for i in range(6, 53):
    startingLine.sort_values(by=['driver', 'lap'], inplace=True)
    grouped_df = startingLine.groupby(['driver'])
    for name, group in grouped_df:
        # print(group[-1:]['out'].values[0])
        # prediction = model.predict(np.array([group[group.columns.difference(['out'])][-5:].values]).astype('float32'))
        prediction = model.predict(np.array([group[-5:].values]).astype('float32'))
        new_data = pd.DataFrame(group[-1:].values, columns=startingLine.columns)
        new_data['lap'] = i
        new_data['position'] = prediction
        # new_data['position'] = round(prediction[0][0], 1)
        new_data['tyreLap'] =  new_data['tyreLap']+1
        startingLine = startingLine.append(new_data, ignore_index=True)
    
    startingLine.sort_values(by=['lap', 'position'], inplace=True)
    # print(startingLine.loc[(startingLine['lap'] == i)]['position'])
    # print(np.arange(1, 21, dtype=int))
    # startingLine.loc[(startingLine['lap'] == i), 'position'] =  np.arange(1, 21, dtype=int)
    startingLine.loc[(startingLine['lap'] == i), 'driverPrev'] = startingLine.loc[(startingLine['lap'] == i), 'driver'].shift(1, fill_value=startingLine.loc[(startingLine['lap'] == i), 'driver'].iloc[0])
    startingLine.loc[(startingLine['lap'] == i), 'teamPrev'] = startingLine.loc[(startingLine['lap'] == i), 'team'].shift(1, fill_value=startingLine.loc[(startingLine['lap'] == i), 'team'].iloc[0])
    startingLine.loc[(startingLine['lap'] == i), 'driverNext'] = startingLine.loc[(startingLine['lap'] == i), 'driver'].shift(-1, fill_value=startingLine.loc[(startingLine['lap'] == i), 'driver'].iloc[0])
    startingLine.loc[(startingLine['lap'] == i), 'teamNext'] = startingLine.loc[(startingLine['lap'] == i), 'team'].shift(-1, fill_value=startingLine.loc[(startingLine['lap'] == i), 'team'].iloc[0])
    # startingLine.loc[(startingLine['lap'] == i), 'position'] =  np.arange(1, 21, dtype=int)
    print(startingLine.tail(20))

# #for lap in range(1, 70):
#     #startingLine.loc[(startingLine['lap'] == lap), 'position'] =  np.arange(1, 21, dtype=int)

startingLine.to_csv('dataset/race3.csv')


# # print(startingLine)
# #head = np.array([df.iloc[0:3], df.iloc[1:4], df.iloc[2:5], df.iloc[3:6]])

# # input = [
# #     [
# #         [29,   4,   2,  17,  17,  56,  34.7, 32.5,  0,   0,   3,  26,   7,  16, 6,  26,  14, ],
# #         [29,   5,   0,  17,  17,  59,  34.6, 32.5,  0,   0,   4,  26,   7,  16, 6,  26,  14, ],
# #         [29,   6,   0,  17,  17,  60,  34.6, 32.5,  0,   0,   5,  26,   7,  27, 14,  26,  14,]
# #     ]
# # ]
# # print(data)
# #print(np.array([data[-3:]]))
# # for i in range(3, 70):
# #     prediction = model.predict(np.array([data[-3:]]))
# #     # new_data = pd.DataFrame(data[-1:].values, columns=data.columns)
# #     # data = data.append(new_data, ignore_index=True)
# #     print(data)
# #     data.loc[i,'driver'] = data.loc[i-1,'driver']
# #     data.loc[i,'lap'] = i
# #     data.loc[i,'trackStatus'] = data.loc[i-1,'trackStatus']
# #     data.loc[i,'position'] = prediction
# #     data.loc[i,'grid'] = data.loc[i-1,'grid']
# #     data.loc[i,'performance'] = data.loc[i-1,'performance']
# #     data.loc[i,'trackTemp'] = data.loc[i-1,'trackTemp']
# #     data.loc[i,'airTemp'] = data.loc[i-1,'airTemp']
# #     data.loc[i,'raining'] = data.loc[i-1,'raining']
# #     data.loc[i,'tyre'] = data.loc[i-1,'tyre']
# #     data.loc[i,'tyreLap'] = data.loc[i-1,'tyreLap'] +1
# #     data.loc[i,'track'] = data.loc[i-1,'track']
# #     data.loc[i,'team'] = data.loc[i-1,'team']
# #     data.loc[i,'driverPrev'] = data.loc[i-1,'driverPrev']
# #     data.loc[i,'teamPrev'] = data.loc[i-1,'teamPrev']
# #     data.loc[i,'driverNext'] = data.loc[i-1,'driverNext']
# #     data.loc[i,'teamNext'] = data.loc[i-1,'teamNext']

# # print(data)
