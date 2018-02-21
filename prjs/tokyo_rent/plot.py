import numpy as np
import random
from matplotlib import pyplot as plt

data = np.random.normal(0, 20, 1000)
bins = np.arange(-100, 100, 5)
plt.xlim([min(data)-5, max(data)+5])
plt.hist(data, bins=bins, alpha=0.5)
plt.title('Random Gaussian data (fixed bin size)')
plt.xlabel('variable X (bin size 5')
plt.ylabel('count')
plt.show()