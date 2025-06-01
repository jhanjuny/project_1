import numpy as np
import matplotlib.pyplot as plt

# 물리 상수
alpha = 0.01  # 열확산계수 (m^2/s)

# 시뮬레이션 설정
L = 1.0         # 막대 길이 (m)
Nx = 50         # 공간 격자 수
dx = L / (Nx-1) # 공간 간격
T_total = 1.0   # 시뮬레이션 총 시간 (s)
dt = 0.0005     # 시간 간격
Nt = int(T_total / dt)  # 시간 단계 수

# 안정 조건 확인
s = alpha * dt / dx**2
assert s <= 0.5, f"불안정! s = {s:.3f} > 0.5"

T = np.zeros(Nx)        # 현재 시간의 온도 분포
T_new = np.zeros(Nx)    # 다음 시간의 온도 분포
T[int(Nx/2)] = 100.0     # 중앙에만 열 줌


history = []

for n in range(Nt):
    for i in range(1, Nx-1):
        T_new[i] = T[i] + s * (T[i+1] - 2*T[i] + T[i-1])
    T[:] = T_new[:]

    if n % 100 == 0:  # 결과 저장 (간격 맞춰서)
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
