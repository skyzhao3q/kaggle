import numpy as np
import pandas as pd
import cv2
import os

data = pd.read_csv('data/test.csv')
images = data.iloc[:,:].values
images = images.astype(np.float)

image_size = images.shape[1]
image_w = image_h = np.ceil(np.sqrt(image_size)).astype(np.uint8)

for i in range(len(images)):
    image = images[i]
    image = image.reshape(image_w, image_h)
    filePath = "data/test/" + str(i) + ".jpg"
    cv2.imwrite(filePath, image)
    print(i)

print("END")