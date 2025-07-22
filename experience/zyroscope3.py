import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go

def gyro_motion_3d(I, omega_disk, M, r, theta0_deg=30, phi0_deg=0, psi0_deg=0, dtheta_dt0_deg=0, g=9.81, T=10, n_steps=1000):
    # 각도 -> 라디안 변환
    theta0 = np.deg2rad(theta0_deg)
    phi0 = np.deg2rad(phi0_deg)
    psi0 = np.deg2rad(psi0_deg)
    dtheta_dt0 = np.deg2rad(dtheta_dt0_deg)

    t = np.linspace(0, T, n_steps)
    L = I * omega_disk
    tau = M * g * r
    Omega = tau / L   # 세차 각속도

    # Nutation(장동) 주기 (harmonic approx)
    omega_n = np.sqrt(M * g * r / I)
    # θ(t) = θ₀ + (dθ/dt₀ / ωₙ) * sin(ωₙ t)
    theta = theta0 + (dtheta_dt0 / omega_n) * np.sin(omega_n * t)
    phi = Omega * t + phi0
    psi = omega_disk * t + psi0

    # 방향벡터(단위벡터)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)

    # 크기*벡터(L로 스케일)
    x = L * x
    y = L * y
    z = L * z

    return x, y, z, t, theta, phi

# ===== 입력 =====
I = 0.012           # 관성모멘트 (kg*m^2)
omega_disk = 200   # 각속도 (rad/s)
M = 0.1           # 무게추 (kg)
r = 0.17           # 거리 (m)
theta0_deg = 90    # 초기 회전축 각도
phi0_deg = 0       # 세차각 시작값
psi0_deg = 0       # 고유회전 초기값
dtheta_dt0_deg = 0.1 # θ 방향 초기 각속도(축을 미는 효과, deg/s)
T = 100             # 시뮬레이션 시간(초)
n_steps = 1500     # 플롯 해상도

# 궤적 계산
x, y, z, t, theta, phi = gyro_motion_3d(
    I, omega_disk, M, r,
    theta0_deg=theta0_deg, phi0_deg=phi0_deg, psi0_deg=psi0_deg,
    dtheta_dt0_deg=dtheta_dt0_deg,
    T=T, n_steps=n_steps
)

# ---- 기존 Matplotlib 3D 플롯 ----
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, label='Gyroscope Trajectory (세차+장동)', linewidth=2)
ax.scatter([0], [0], [0], color='red', s=40, label='Origin')
ax.set_xlabel('X (각운동량 단위)')
ax.set_ylabel('Y (각운동량 단위)')
ax.set_zlabel('Z (각운동량 단위)')
ax.set_title('자이로스코프 세차+장동운동 3D 시뮬레이션')
ax.legend()
plt.tight_layout()
plt.show()

# ---- Plotly 3D 플롯 추가 ----
fig3 = go.Figure()
fig3.add_trace(go.Scatter3d(x=x, y=y, z=z,
    mode='lines',
    line=dict(width=6, color='royalblue'),
    name='Gyroscope Trajectory'))
fig3.add_trace(go.Scatter3d(x=[0], y=[0], z=[0],
    mode='markers', marker=dict(size=6, color='red'), name='Origin'))
fig3.update_layout(
    scene = dict(
        xaxis_title='X (각운동량 단위)',
        yaxis_title='Y (각운동량 단위)',
        zaxis_title='Z (각운동량 단위)'
    ),
    title='자이로스코프 세차+장동운동 3D 시뮬레이션 (Plotly)',
    legend=dict(x=0.8, y=0.9)
)
fig3.show()

# ---- 2D 장동/세차 그래프 (Matplotlib) ----
fig2, axs = plt.subplots(2, 1, figsize=(8, 5), sharex=True)
axs[0].plot(t, np.rad2deg(theta), label='θ (장동, deg)')
axs[0].set_ylabel('θ (deg)')
axs[0].legend()
axs[0].grid(True)
axs[1].plot(t, np.rad2deg(phi), label='φ (세차, deg)', color='g')
axs[1].set_ylabel('φ (deg)')
axs[1].set_xlabel('Time (s)')
axs[1].legend()
axs[1].grid(True)
plt.suptitle('장동(θ), 세차(φ) 각도 변화')
plt.tight_layout()
plt.show()