import numpy as np
from matplotlib import pyplot as plt
y=np.random.rand(1000)
plt.hist(y,bins=50)
plt.show()