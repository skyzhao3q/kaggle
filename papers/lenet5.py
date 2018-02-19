from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.utils import np_utils

def Lenet5():
    model = Sequential()
    '''
    [C1] Conv
    input_shape: 32*32
    kernel_size: 5*5
    kernel_sum : 6
    stride: 1
    pading: -
    '''
    model.add(Conv2D(32, (5,5),strides=(1,1),input_shape(28,28,1),padding='valid',activation='relu',kernel_initializer='form'))
    '''
    [S2] Pooling
    input_shape: 28*28
    kernel_size: 5*5
    kernel_sum : 6
    stride: 1
    pading: -
    '''
    '''
    [C3] Conv
    input_shape: 32*32
    kernel_size: 5*5
    kernel_sum : 6
    stride: 1
    pading: -
    '''
    '''
    [S4] Pooling
    input_shape: 28*28
    kernel_size: 5*5
    kernel_sum : 6
    stride: 1
    pading: -
    '''
    '''
    [C5] Conv
    input_shape: 32*32
    kernel_size: 5*5
    kernel_sum : 6
    stride: 1
    pading: -
    '''
    '''
    [F6] Full
    '''