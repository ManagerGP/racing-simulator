import pandas as pd
import tensorflow as tf

data = pd.read_csv('dataset/global-processed.csv', index_col=0)
df = pd.DataFrame(data)

print(df.head())
print(df.dtypes)

for idx, col in enumerate(['driver', 'tyre', 'track', 'team', 'driverPrev', 'teamPrev', 'driverNext', 'teamNext']):
    df[col] = pd.Categorical(df[col])
    df[col] = df[col].cat.codes

print(df.head())

df.drop(columns=['idGP', 'out', 'targetPosition'], inplace=True)

model = tf.keras.models.load_model('my_model')

for data in df.head(5).values:
    print(data)
    print(model.predict(data))