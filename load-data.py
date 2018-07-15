# Loading the dataset
import numpy as np
import os
import random

list_files = os.listdir('train_data')
np.random.shuffle(list_files)
X = []
Y = []
for train_data_file in list_files:
    data = np.load('train_data/' + train_data_file)
    Y.append(np.stack(data[:, 0]))
    X.append(np.stack(data[:, 1]))

Y = np.vstack(Y)
X = np.vstack(X)
np.save('X.npy', X)
np.save('Y.npy', Y)
