from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D

class LeNet:
	@staticmethod
	def build(input_shape, num_classes, weightsPath=None):
		# initialize the model
		model = Sequential()

		# first set of CONV => RELU => POOL
		model.add(Conv2D(6, kernel_size=(5,5), activation='relu', input_shape=input_shape))
		model.add(MaxPooling2D(pool_size=(2, 2)))

		# second set of CONV => RELU => POOL
		model.add(Conv2D(16, kernel_size=(5,5), activation='relu'))
		model.add(MaxPooling2D(pool_size=(2, 2)))

		# set of FC => RELU layers
		model.add(Flatten())
		model.add(Dense(120, activation='relu'))

		# softmax classifier
		model.add(Dropout(0.5))
		model.add(Dense(num_classes, activation='softmax'))

		# if a weights path is supplied (inicating that the model was
		# pre-trained), then load the weights
		if weightsPath is not None:
			model.load_weights(weightsPath)

		# return the constructed network architecture
		return model