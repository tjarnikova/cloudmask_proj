import numpy as np

import numpy as np
import matplotlib.pyplot as plt

def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t)

t1 = np.arange(0.0, 5.0, 0.1)
t2 = np.arange(0.0, 5.0, 0.02)

plt.figure(1)
plt.subplot(211)
plt.plot(t1, f(t1), 'bo', t2, f(t2), 'k')

plt.subplot(212)
plt.plot(t2, np.cos(2*np.pi*t2), 'r--')
plt.show()


# y = np.zeros((3,4))

# xlim = [0, 2]
# ylim = [3, 4]
# res = 1
# x_bins=np.arange(xlim[0], xlim[1], res)
# y_bins=np.arange(ylim[0], ylim[1], res) 
# print(x_bins)

# raw_x = np.array([[0.5, 1.9, 1.2], [0.2, 0.1, 2]])
# print(np.ravel(raw_x))

# x_indices=np.searchsorted(x_bins, np.ravel(raw_x), 'right')
# print(x_indices)
# x_array=np.zeros([len(y_bins), len(x_bins)], dtype=np.float)
# print(x_array)

count = 0 

for i in range(0,2):
	for j in range(0,3):
		count = count+1
		print count






















# y = [3,4]
# print(y)
# print(y[0])

# z = x.shape[0]
# q = x.shape[1]


# print(x)


# for i in range(0,z):
# 	for j in range(0,q):
# 		b = x[i,j]
# 		print b
# 		if i > 1 and i < 3:
# 			x[i,j] = 4


# print (x)
#z = np.searchsorted(x,:)
#print(z)
#w = x[1,2]
#print(w)

#y = x[1,:]
#print(y)