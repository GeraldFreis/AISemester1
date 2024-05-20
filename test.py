import numpy as np

file = np.load("./assignment3-test-cases\op120.npz", mmap_mode='r')
print(file['arr_0'])

print("*" * 100)


file = np.load("output.npz", mmap_mode='r')
print(file['arr_0'])