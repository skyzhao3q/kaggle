from keras.initializers import TruncatedNormal, Constant
from keras.models import Sequential
from keras.optimizers import SGD
from keras.layers import Input, Dropout, Flatten, Conv2D, MaxPooling2D, Dense, Activation, BatchNormalization
from keras.callbacks import Callback, EarlyStopping
from keras.utils.np_utils import to_categorical

def conv2d(filters, kernel_size, strides=1, bias_init=1, **kwargs):
    trunc = TruncatedNormal(mean=0.0, stddev=0.01)
    cnst = Constant(value=bias_init)
    return Conv2D(
        filters,
        kernel_size,
        strides=strides,
        padding='same',
        activation='relu',
        kernel_initializer=trunc,
        bias_initializer=cnst,
        **kwargs
    )

def dense(units, **kwargs):
    trunc = TruncatedNormal(mean=0.0, stddev=0.01)
    cnst = Constant(value=1)
    return Dense(
        units,
        activation='tanh',
        kernel_initializer=trunc,
        bias_initializer=cnst,
        **kwargs
    )

def AlexNet():
    model = Sequential()

    # 第1畳み込み層
    model.add(conv2d(96, 11, strides=(4,4), bias_init=0, input_shape=(ROWS, COLS, 3)))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
    model.add(BatchNormalization())

    # 第２畳み込み層
    model.add(conv2d(256, 5, bias_init=1))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
    model.add(BatchNormalization())

    # 第３~5畳み込み層
    model.add(conv2d(384, 3, bias_init=0))
    model.add(conv2d(384, 3, bias_init=1))
    model.add(conv2d(256, 3, bias_init=1))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
    model.add(BatchNormalization())

    # 密結合層
    model.add(Flatten())
    model.add(dense(4096))
    model.add(Dropout(0.5))
    model.add(dense(4096))
    model.add(Dropout(0.5))

    # 読み出し層
    model.add(Dense(2, activation='softmax'))

    model.compile(optimizer=SGD(lr=0.01), loss='categorical_crossentropy', metrics=['accuracy'])
    return model