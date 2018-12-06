
import numpy as np
import os
import random

from keras.models import Sequential, Model
from keras.layers import Dense, Flatten, Dropout, Reshape, Permute, Activation
from keras.layers import Convolution2D, MaxPooling3D, ConvLSTM2D
from keras import layers
from keras import Input
import scipy.io
import scipy.misc

N_CLASSES = 50
IMSIZE = (216, 216)
SequenceLength = 10
BatchSize = 2

def load_model():
    input_tensor = Input(shape = (SequenceLength, IMSIZE[0], IMSIZE[1], 3))

    x = layers.ConvLSTM2D(32, kernel_size=(7, 7), padding='valid', return_sequences=True)(input_tensor)
    x = layers.Activation('relu')(x)
    x = layers.MaxPooling3D(pool_size=(1, 2, 2))(x)

    x = layers.ConvLSTM2D(64, kernel_size=(5, 5), padding='valid', return_sequences=True)(x)
    x = layers.MaxPooling3D(pool_size=(1, 2, 2))(x)

    x = layers.ConvLSTM2D(96, kernel_size=(3, 3), padding='valid', return_sequences=True)(x)
    x = layers.Activation('relu')(x)
    x = layers.ConvLSTM2D(96, kernel_size=(3, 3), padding='valid', return_sequences=True)(x)
    x = layers.Activation('relu')(x)
    x = layers.ConvLSTM2D(96, kernel_size=(3, 3), padding='valid', return_sequences=True)(x)
    x = layers.MaxPooling3D(pool_size=(1, 2, 2))(x)

    x = layers.Dense(320)(x)
    x = layers.Activation('relu')(x)
    x = layers.Dropout(0.5)(x)

    out_shape = x.get_shape().as_list()
    x = layers.Reshape((SequenceLength, out_shape[2] * out_shape[3] * out_shape[4]))(x)
    x = layers.Bidirectional(layers.LSTM(64,return_sequences=True),merge_mode='concat')(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Flatten()(x)
    x = layers.Dense(128,activation='relu')(x)
    output_tensor = layers.Dense(N_CLASSES, activation='softmax')(x)

    model = Model(input_tensor,output_tensor)
    model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
    return model

def loadDataSet(folder = 'pic_data'):
    trainData = np.zeros([2500,SequenceLength,216,216,3],dtype='float16')
    trainLabel = []
    testData = np.zeros([1000,SequenceLength,216,216,3],dtype='float16')
    testLabel = []
    class_name = 0

    train_num = 0
    test_num = 0

    for k in os.listdir(folder):
        sample = random.sample(range(70),50)
        sample_cnt = 0
        folder2 = folder + '/' + str(k)
        class_label = np.zeros(N_CLASSES)
        for video_name in os.listdir(folder2):
            path = folder2 + "/" + str(video_name)
            class_label[class_name] = 1
            if sample_cnt in sample:
                for video_pic in os.listdir(path):
                    new_path = path + '/' + str(video_pic)
                    sample_len = np.sort(random.sample(range(400),SequenceLength))
                    cnt = 0
                    if cnt in sample_len:
                        image = scipy.misc.imread(new_path)
                        image = scipy.misc.imresize(image, [216, 216])
                        image = np.reshape(image, (1,216,216,3))
                        trainData[train_num][cnt] = image
                        cnt += 1
                trainLabel.append(class_label)
                train_num += 1
            else:
                for video_pic in os.listdir(path):
                    new_path = path + '/' + str(video_pic)
                    sample_len = np.sort(random.sample(range(400),SequenceLength))
                    cnt = 0
                    if cnt in sample_len:
                        image = scipy.misc.imread(new_path)
                        image = scipy.misc.imresize(image, [216, 216])
                        image = np.reshape(image, (1,216,216,3))
                        testData[test_num][cnt] = image
                        cnt += 1
                testLabel.append(class_label)
                test_num += 1
            sample_cnt += 1
        print(class_name,"----FINISH----")
        class_name += 1

    trainLabel = np.array(trainLabel,dtype=float)
    testLabel = np.array(testLabel,dtype=float)
    return trainData,trainLabel,testData,testLabel

trainData,trainLabel,testData,testLabel = loadDataSet()
print(trainData.shape,testData.shape)

model = load_model()
message = model.fit(
    trainData,
    trainLabel,
    epochs=1000,
    batch_size=BatchSize,
    validation_data=(testData,testLabel)
)
