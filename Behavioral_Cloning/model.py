import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.image as mpimg

from keras.layers import Dense, Flatten, Activation, MaxPooling2D, Lambda, Dropout
from keras.models import Sequential
from keras.layers.core import Lambda
from keras.layers import Conv2D, Cropping2D 
from keras.optimizers import SGD, Adam, RMSprop
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split


# read the csv file
driving_df = pd.read_csv('data/driving_log.csv')

# get the center, left, right camera images' filenames, and corresponding steering measurements
def get_images_filenames_measurements(dataframe):

    filenames = []
    measurements = []
    
    # correction is used for adjusting left and right camera images, the steering angle
    correction = 0.05

    for index, row in dataframe.iterrows():
        # get the center image filenames and measurements
        center_text = row[0]
        center_i = center_text.find('center')
        center_filename = center_text[center_i:]
        center_measure = float(row[3])
        filenames.append(center_filename)
        measurements.append(center_measure)
        # get the left image filenames and measurements
        left_text = row[1]
        left_i = left_text.find('left')
        left_filename = left_text[left_i:]
        left_measure = center_measure + correction
        filenames.append(left_filename)
        measurements.append(left_measure)
        # get the right image filenames and measurements
        right_text = row[2]
        right_i = right_text.find('right')
        right_filename = right_text[right_i:]
        right_measure = center_measure - correction
        filenames.append(right_filename)
        measurements.append(right_measure)
    
    return filenames, measurements


filenames, measurements = get_images_filenames_measurements(driving_df)

# I'll flip all the images, so I create the filenames for the flipped images first
flips_filenames = []

for each in filenames:
    flips_filenames.append('f'+each)

# adjust the original measurements to reflect the flipped images, by negating them    
flips_measurements = - np.asarray(measurements)

# concatenate the original images filenames with the created flipped filenames and measurements
total_filenames = np.append(np.asarray(filenames), np.asarray(flips_filenames))
total_measurements = np.append(np.asarray(measurements), np.asarray(flips_measurements))

# this function is used to flip all the images horizontally, and save them
def flip_images(data):
    
    for i in range(0, len(data)):
        filename = data[i]
        current_path = 'data/IMG/' + filename
        image = mpimg.imread(current_path)
        flipped_image = np.fliplr(image)
        plt.imsave('data1/IMG/'+'f'+filename, flipped_image)
        plt.close('all')
        
# flip the images horizontally
flip_images(total_filenames)

# define a generator to retrieve the images batch by batch, to save RAM
def generator(X_data, y_data, batch_size):
    
    num_samples = len(X_data)
    
    while True:
        for offset in range(0, num_samples, batch_size):
            batch_x = []
            batch_y = []
            X_data_range, y_data_range = X_data[offset:offset+batch_size], y_data[offset:offset+batch_size]
            
            # neglect the final batch if the images available is less than the batch size
            if len(X_data_range) < batch_size:
                break
            
            for i in range(0, batch_size):
                filename = X_data_range[i]
                current_path = 'data/IMG/' + filename
                batch_x_one = mpimg.imread(current_path)
                batch_x.append(batch_x_one)
                batch_y.append(y_data_range[i])
            
            batch_x = np.asarray(batch_x)
            batch_y = np.asarray(batch_y)
            # shuffle the data
            batch_x, batch_y = shuffle(batch_x, batch_y)
            
            yield batch_x, batch_y

# do the train test split, with 25% for testing
X_train, X_valid, y_train, y_valid = train_test_split(total_filenames, total_measurements, test_size=0.25, random_state=101)

# define the batch size and number of epochs
batch_size = 64
epochs = 1

# create generators
train_generator = generator(X_train, y_train, batch_size)
valid_generator = generator(X_valid, y_valid, batch_size)

# define optimizer
adam = Adam(lr=0.00003, beta_1=0.9, beta_2=0.999, decay=0.000003)

# create the model

model = Sequential()

# crop the some of the top and bottom to make image more relevant
model.add(Cropping2D(cropping=((50,20), (0,0)), input_shape=(160,320,3)))
# doing the normalizaton
model.add(Lambda(lambda x: x/255.0 - 0.5, input_shape=(90,320,3)))
# convolution layer 1, with input: 90x320x3, output: 90x320x15
model.add(Conv2D(filters=15, kernel_size=(5, 5), padding='same', subsample=(2, 2)))
# add non-linearity
model.add(Activation('relu'))
# maxpooling layer 1, with input: 90x320x15 output: 45x160x15, reduce overfitting
model.add(MaxPooling2D(pool_size=(2, 2), strides=(1, 1)))
# convolution layer 2, with input: 45x160x15, output: 45x160x64
model.add(Conv2D(filters=64, kernel_size=(5, 5), padding='same', subsample=(2, 2)))
# add non-linearity
model.add(Activation('relu'))
# maxpooling layer 2, with input: 45x160x64, output: 22x80x64, reduce overfitting
model.add(MaxPooling2D(pool_size=(2, 2), strides=(1, 1)))
# flatten the inputs, prepared for the fully connected layer
model.add(Flatten())
# fully connected layer 1, with input 22x80x64, output: 500
model.add(Dense(500))
# add non-linearity
model.add(Activation('relu'))
# apply regularization, with a dropout probability of 50%
model.add(Dropout(0.5))
# fully connected layer 2, with input 500, output: 50
model.add(Dense(50))
# add non-linearity
model.add(Activation('relu'))
# output layer, with input: 50, output 1
model.add(Dense(1))

model.compile(loss='mse', optimizer=adam, metrics=['accuracy'])
model.summary()

# train the model
model.fit_generator(train_generator, 
                    samples_per_epoch=len(X_train), 
                    steps_per_epoch=len(X_train)/batch_size,
                    validation_data=valid_generator,
                    validation_steps=len(X_valid)/batch_size,
                    verbose=1,
                    shuffle=True,
                    nb_epoch=epochs)

# save the model in h5 format
model.save('model.h5')