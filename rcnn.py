
import keras
from keras.models import Model
import keras.backend as K
import tensorflow as tf

def residual_block(filters,block):
    if block == 0:
        stride = 2
    else:
        stride = 1

    def f(x):
        y = keras.layers.Conv2D(filters,(1,1),strides=stride)(x)
        y = keras.layers.BatchNormalization(axis=3)(y)
        y = keras.layers.Activation('relu')(y)

        y = keras.layers.Conv2D(filters,(3,3),padding='same')(y)
        y = keras.layers.BatchNormalization(axis=3)(y)
        y = keras.layers.Activation('relu')(y)

        y = keras.layers.Conv2D(4*filters,(1,1),strides=stride)(y)
        y = keras.layers.BatchNormalization(axis=3)(y)

        if block == 0:
            shortcut = keras.layers.Conv2D(4*filters,(1,1),strides=stride)(x)
            shortcut = keras.layers.BatchNormalization(axis=3)(shortcut)
        else:
            shortcut = x

        y = keras.layers.Add()([y,shortcut])
        y = keras.layers.Activation('relu')(y)
        return y
    return f

def resNet_Model(inputs):
    x = keras.layers.Conv2D(64,(3,3),padding='same')(inputs)
    x = keras.layers.BatchNormalization(axis=3)(x)
    x = keras.layers.Activation('relu')(x)

    filter = 64
    blocks = [3,6,4]
    for i,block_num in enumerate(blocks):
        for block_id in range(block_num):
            x = residual_block(filter,block_id)(x)
        filter *= 2
    return x

x = keras.layers.Input((64,64,3))
y = resNet_Model(x)
model = Model([x],[y])
print(model.summary())

def rpn_net(inputs,k):
    shared_map = keras.layers.Conv2D(256,(3,3),padding='same')(inputs)
    shared_map = keras.layers.Activation('linear')(shared_map)

    rpn_class = keras.layers.Conv2D(2*k,(1,1))(shared_map)
    rpn_class = keras.layers.Lambda(lambda x:tf.reshape(x,[tf.shape(x)[0],-1,2]))(rpn_class)
    rpn_class = keras.layers.Activation('linear')(rpn_class)
    rpn_prob = keras.layers.Activation('softmax')(rpn_class)

    y = keras.layers.Conv2D(4*k,(1,1))(shared_map)
    y = keras.layers.Activation('linear')(y)
    rpn_bbox = keras.layers.Lambda(lambda x:tf.reshape(x,[tf.shape(x)[0],-1,4]))(y)

    return rpn_class,rpn_prob,rpn_bbox


