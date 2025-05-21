import numpy as np, matplotlib.pyplot as plt
q1 = 1
def E1(q, r1, x, y):
    X = x - r1[0]; Y = y - r1[1]
    denom = (np.sqrt(X**2+Y**2))**3
    return q*X/denom, q*Y/denom
r1 = np.array([-1.0, 0.0])

q2 = -1
def E2(q, r2, x, y):
    X = x - r2[0]; Y = y - r2[1]
    denom = (np.sqrt(X**2+Y**2))**3
    return q*X/denom, q*Y/denom
r2 = np.array([1.0, 0.0])

Nx, Ny = 10, 10
x = np.linspace(-5,5,Nx)
y = np.linspace(-5,5,Ny)
X, Y = np.meshgrid(x, y)

E_tot = E1(q1, r1, X, Y) + E2(q2, r2, X, Y)

Ex, Ey =E_tot[0], E_tot[1]
plt.streamplot(X, Y, Ex, Ey)
plt.xlabel('x')
plt.ylabel('y')
plt.show()