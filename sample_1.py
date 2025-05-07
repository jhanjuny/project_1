import numpy as np, matplotlib.pyplot as plt
q = 1
def potential (q, r0, x, y):
  X = x - r0[0]; Y = y - r0[1]
  denom = (np.sqrt(X**2 + Y**2))**2
  return q/denom
r0 = np.array([0.0, 0.0])
Nx, Ny = 10, 10
x = np.linspace(-1, 1, Nx)
y = np.linspace(-1, 1, Ny)
X, Y = np.meshgrid(x, y)
Phi = potential(q, r0, X, Y)
plt.contour(X, Y, Phi)
plt.xlabel("x")
plt.ylabel("y")
plt.show()