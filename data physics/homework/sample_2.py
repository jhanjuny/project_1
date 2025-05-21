import numpy as np, matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d 
h = 0.1; MAX = 100; Error = 1.0E-8
x = np.arange(-1, 1+0.5*h, h)
y = np.arange(-1, 1+0.5*h, h)
X, Y = np.meshgrid(x, y)
Nx = np.size(X); Ny = np.size(Y)
phi = np.ones( (Nx, Ny)); phi *=0.1
phi[0,:] = phi[ -1,:] = 