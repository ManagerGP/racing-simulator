import pandas as pd
import tensorflow as tf
from tensorflow import keras

data = pd.read_csv('dataset/global_ex-processed.csv')
df = pd.DataFrame(data)

split_fraction = 0.715
train_split = int(split_fraction * int(df.shape[0]))

df.sort_values(by=['idGP', 'driver', 'lap'], inplace=True)

df.drop(columns=['idGP', 'out', 'windSpeed','humidity','pressure','windDir'], inplace=True)

for idx, col in enumerate(['driver', 'tyre', 'track', 'team', 'driverPrev', 'teamPrev', 'driverNext', 'teamNext']):
    df[col] = pd.Categorical(df[col])
    df[col] = df[col].cat.codes

print(df.head())

x_train = df 
y_train = x_train.pop('targetPosition')

g_dataset_train = keras.preprocessing.timeseries_dataset_from_array(
    x_train,
    y_train,
    sequence_length=5,
    sampling_rate=1,
    batch_size=1,
)

g_dataset_train = g_dataset_train.shuffle(len(g_dataset_train))

for feat, targ in g_dataset_train.take(5):
    print ('Features: {}, Target: {}'.format(feat, targ))

for batch in g_dataset_train.take(1):
    inputs, targets = batch

print("Input shape:", inputs.numpy().shape)
print("Target shape:", targets.numpy().shape)

inputs = keras.layers.Input(shape=(inputs.shape[1], inputs.shape[2]))
lstm_out = keras.layers.LSTM(32)(inputs)
outputs = keras.layers.Dense(1)(lstm_out)

model = keras.Model(inputs=inputs, outputs=outputs)
model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001), loss="mse", metrics=['accuracy'])
model.summary()

path_checkpoint = "model_checkpoint.h5"
es_callback = keras.callbacks.EarlyStopping(monitor="val_loss", min_delta=0, patience=5)

modelckpt_callback = keras.callbacks.ModelCheckpoint(
    monitor="val_loss",
    filepath=path_checkpoint,
    verbose=1,
    save_weights_only=False,
    save_best_only=True,
)

history = model.fit(
    g_dataset_train.take(int(len(g_dataset_train)*70/100)),
    epochs=15,
    validation_data=g_dataset_train.skip(int(len(g_dataset_train)*70/100)),
    callbacks=[es_callback, modelckpt_callback],
)


# for x, y in g_dataset_train.take(5):
#     print(x)
#     print(y)
#     print(model.predict(x)[0])