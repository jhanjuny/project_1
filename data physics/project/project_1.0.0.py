import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 열 확산 계수 및 격자 설정
alpha = 0.01
Lx, Ly, Lz = 1.0, 1.0, 1.0
Nx, Ny, Nz = 20, 20, 20
dx = Lx / (Nx - 1)
dt = 0.0005
T_total = 0.05
Nt = int(T_total / dt)

# 안정 조건 확인 (6방향으로 확산하므로 1/6)
s = alpha * dt / dx**2
assert s <= 1/6, f"불안정! s = {s:.3f} > 1/6"

# 초기 온도 배열
T = np.zeros((Nx, Ny, Nz))
T_new = np.zeros_like(T)
T[Nx//2, Ny//2, Nz//2] = 100.0  # 중앙만 뜨겁게

# 결과 저장: 중앙 z 단면만 저장
history = []

for n in range(Nt):
    for i in range(1, Nx-1):
        for j in range(1, Ny-1):
            for k in range(1, Nz-1):
                T_new[i, j, k] = T[i, j, k] + s * (
                    T[i+1, j, k] + T[i-1, j, k] +
                    T[i, j+1, k] + T[i, j-1, k] +
                    T[i, j, k+1] + T[i, j, k-1] -
                    6 * T[i, j, k]
                )
    T, T_new = T_new, T

    if n % 10 == 0:
        history.append(T[:, :, Nz//2].copy())

# 시각화 (중앙 z 단면)
fig, ax = plt.subplots()
img = ax.imshow(history[0], cmap='hot', origin='lower', extent=[0, Lx, 0, Ly])
ax.set_title("3D Heat Diffusion (Z-Slice)")
plt.colorbar(img)

def update(frame):
    img.set_data(history[frame])
    return [img]

ani = FuncAnimation(fig, update, frames=len(history), interval=100)
plt.show()
