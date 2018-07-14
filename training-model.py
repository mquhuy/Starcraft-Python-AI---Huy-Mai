import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.callbacks import TensorBoard
import numpy as np
import os
import random

# Setting up the model structure
model = Sequential()

model.add(Conv2D(32, (3, 3), padding='same', input_shape = (176, 200, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.5))

model.add(Dense(4, activation='softmax'))

learning_rate = 0.0001
opt = keras.optimizers.adam(lr=learning_rate, decay=1e-6)

model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

# tensorboard = TensorBoard(log_dir = "logs/stage1")

# Loading the dataset
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

# Training and saving the model
model.fit(X, Y, batch_size=20, epochs=10)
model.save('trained_model.h5')
