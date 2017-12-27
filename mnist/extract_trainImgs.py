import numpy as np
import pandas as pd
import cv2
import os

data = pd.read_csv('data/train.csv')
images = data.iloc[:,1:].values
images = images.astype(np.float)

image_size = images.shape[1]
image_w = image_h = np.ceil(np.sqrt(image_size)).astype(np.uint8)

labels = data.iloc[:,0].values

for i in range(len(labels)):
    image = images[i]
    image = image.reshape(image_w, image_h)
    label = labels[i]
    dirPath = "data/train/" + str(label) 
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)
    filePath = dirPath + "/" + str(i) + ".jpg"
    cv2.imwrite(filePath, image)
    print(i)

print("END")