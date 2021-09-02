import numpy as np
import tensorflow as tf
import itertools
import json
import math
import matplotlib.pyplot as plt
import sys
from decimal import Decimal


def retrieve_test_samples(data_set: dict,
                          min_sequence_length: int=3,
                          max_sequence_length: int=-1,
                          max_test_data_length: int=-1) -> dict:
    print("Data-set samples before filtering:", len(data_set.keys()))
    if max_sequence_length > 0:
        result = dict(
            (key, value) for key, value in data_set.items() if max_sequence_length >= len(value) >= min_sequence_length)
    else:
        result = dict((key, value) for key, value in data_set.items() if len(value) >= min_sequence_length)
    if len(result.keys()) > max_test_data_length > 0:
        result = dict(itertools.islice(result.items(), max_test_data_length))
    print("Data-set samples after filtering:", len(result.keys()))
    return result


def process_data_set(trajectories_map: dict, length: int):
    # This holds our extracted sequences
    trajectories = []

    # This holds the targets (the follow-up characters)
    next_gates = []

    for trajectory in trajectories_map.values():
        for i in range(0, len(trajectory) - length):
            trajectories.append(trajectory[i: i + length])
            next_gates.append(trajectory[i + length])
    print('Extracted trajectory:', len(trajectories))

    # List of unique gates in the data-set
    gates = sorted(list(set(itertools.chain.from_iterable(trajectories_map.values()))))
    print('Unique gates:', len(gates))

    # Dictionary mapping unique gate to their index in `gates`
    gates_index = dict((gate, gates.index(gate)) for gate in gates)

    return (trajectories, next_gates, gates_index, gates)


def one_hot_encoding(samples: list, classifications: list, labels_index: dict, labels: list):
    x = np.zeros((len(samples), len(samples[0]), len(labels)), dtype=np.bool)
    y = np.zeros((len(samples), len(labels)), dtype=np.bool)

    for i, sample in enumerate(samples):
        for t, observation in enumerate(sample):
            x[i, t, labels_index[observation]] = 1
        y[i, labels_index[classifications[i]]] = 1

    return (x, y)


def build_model(x: list, y: list, fold: int=1, epochs: int=1, csv_logger: tf.keras.callbacks.CSVLogger=object):
    for e in range(0, fold):
        num_samples_fold = len(x) // fold
        tf.logging.set_verbosity(tf.logging.INFO)
        rnn = tf.keras.models.Sequential()
        rnn.add(tf.keras.layers.LSTM(256, activation='tanh', input_shape=(len(x[0]), len(y[0]))))
        rnn.add(tf.keras.layers.Dense(len(y[0]), activation='softmax'))
        optimizer = tf.keras.optimizers.RMSprop()
        rnn.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        rnn.summary()

        history = rnn.fit(x[num_samples_fold*e:], y[num_samples_fold*e:],
                batch_size=512,
                epochs=epochs,
                validation_data=(x[:num_samples_fold*(fold-e)], y[:num_samples_fold*(fold-e)]),
                callbacks=[csv_logger])

        return (rnn, history)


def sample(predictions, temp=1.0):
    predictions = np.asarray(predictions).astype('float64')
    predictions = np.log(predictions) / temp
    exp_predictions = np.exp(predictions)
    predictions = exp_predictions / np.sum(exp_predictions)
    probabilities = np.random.multinomial(1, predictions, 1)
    return np.argmax(probabilities)


def probability_gap(predictions, next_gate_index: int):
    predictions = np.asarray(predictions).astype('float64')
    max_gate_index = np.argmax(predictions)
    return predictions[max_gate_index] - predictions[next_gate_index]
