import pandas as pd
import tensorflow as tf

def get_compiled_model():
  model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(1)
  ])

  model.compile(optimizer='adam',
                loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                metrics=['accuracy'])
  return model

data = pd.read_csv('dataset/global-processed.csv', index_col=0)
df = pd.DataFrame(data)

print(df.head())
print(df.dtypes)

for idx, col in enumerate(['driver', 'tyre', 'track', 'team', 'driverPrev', 'teamPrev', 'driverNext', 'teamNext']):
    df[col] = pd.Categorical(df[col])
    df[col] = df[col].cat.codes

print(df.head())

df.drop(columns=['idGP'], inplace=True)

targetOut = df.pop('out')

targetPos = df.pop('targetPosition')
dataset = tf.data.Dataset.from_tensor_slices((df.values, targetPos.values))

print(dataset)

for feat, targ in dataset.take(5):
  print ('Features: {}, Target: {}'.format(feat, targ))

train_dataset = dataset.shuffle(len(df)).batch(1)

# model = get_compiled_model()
# model.fit(train_dataset, epochs=15)

# # Save the entire model as a SavedModel.
# model.save('my_model')
