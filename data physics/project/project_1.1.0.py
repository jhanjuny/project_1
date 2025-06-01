# 코드 재실행: 2D 열전도 방정식 시뮬레이션 (절연 경계 조건)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 시뮬레이션 파라미터 설정
alpha = 0.1
Lx, Ly = 1.0, 1.0
Nx, Ny = 50, 50
dx = Lx / (Nx - 1)
dy = Ly / (Ny - 1)
dt = 0.0005
T_total = 1.0
Nt = int(T_total / dt)

# 안정 조건
s = alpha * dt / dx**2
assert s <= 0.25, f"불안정! s = {s:.3f} > 0.25"

# 초기 조건: 중앙만 뜨겁게
T = np.zeros((Nx, Ny))
T_new = np.zeros_like(T)

T[Nx // 2, Ny // 2] = 1000.0

# 결과 저장용 리스트
history = []

# 시간 루프
for n in range(Nt):
    for i in range(1, Nx - 1):
        for j in range(1, Ny - 1):
            T_new[i, j] = T[i, j] + s * (
                T[i+1, j] + T[i-1, j] + T[i, j+1] + T[i, j-1] - 4*T[i, j]
            )

 

    T[:] = T_new[:]

    if n % 10 == 0:
        history.append(T.copy())

# 시각화
fig, ax = plt.subplots()
img = ax.imshow(history[0], cmap='hot', origin='lower', extent=[0, Lx, 0, Ly])
ax.set_title("2D Heat Diffusion")
plt.colorbar(img)

def update(frame):
    img.set_data(history[frame])
    return [img]

ani = FuncAnimation(fig, update, frames=len(history), interval=1000)
plt.show()
ani
