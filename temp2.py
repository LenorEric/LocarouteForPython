import numpy as np

if __name__ == '__main__':
    a = np.array([1, 2, 3])
    c = np.float64(2)
    print(np.mean((a-c) ** 2))