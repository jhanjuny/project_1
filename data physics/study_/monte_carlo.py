import numpy as np 
for N in 10**np.array([1,2,3,4,5,6,7,9,10]):
    x = np.random.rand(N)*2-1.0
    y = np.random.rand(N)*2-1.0
    ration = np.mean((x**2 + y**2)<1.0)
    print(N, ration*4)