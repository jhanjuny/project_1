import numpy as np
import matplotlib.pyplot as plt

alpha = 0.01

L = 1.0
Nx = 50
dx = L / (Nx-1)
T_total = 1.0
dt = 0.0005
Nt = int(T_total / dt)

s = alpha * dt / dx**2
assert s <= 0.5, f"불안정! s = {s:.3f} > 0.5"

T = np.zeros(Nx)
T_new = np.zeros(Nx)
T[int(Nx/2)] = 100.0

history = []

for n in range(Nt):
    for i in range(1, Nx-1):
        T_new[i] = T[i] + s * (T[i+1] - 2*T[i] + T[i-1])
    T[:] = T_new[:]
    history.append(T.copy())

import matplotlib.animation as animation

fig, ax = plt.subplots()
line, = ax.plot(np.linspace(0, L, Nx), history[0])
ax.set_ylim(0, 110)

def update(frame):
    line.set_ydata(history[frame])
    return line,

ani = animation.FuncAnimation(fig, update, frames=len(history), interval=50)
plt.title("1D Heat Equation Simulation")
plt.xlabel("Position (x)")
plt.ylabel("Temperature (T)")
plt.show()