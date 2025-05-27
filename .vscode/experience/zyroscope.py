import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def gyro_motion_3d(I, omega_disk, M, r, theta0_deg=30, phi0_deg=0, psi0_deg=0, nutation_amp_deg=5, g=9.81, T=10, n_steps=1000):
    """
    I: 관성모멘트 (kg*m^2)
    omega_disk: 관성원판 각속도 (rad/s)
    M: 무게추 질량 (kg)
    r: 무게추 작용 거리 (m)
    theta0_deg: 초기 z축과 이루는 각 (deg)
    phi0_deg: 초기 세차각 (deg)
    psi0_deg: 회전자 고유 회전의 초기각 (deg)
    nutation_amp_deg: 장동운동(궤적의 위아래 흔들림) 최대 진폭 (deg)
    g: 중력가속도 (m/s^2)
    T: 전체 시간 (s)
    n_steps: 스텝수
    """
    # 각도 -> 라디안 변환
    theta0 = np.deg2rad(theta0_deg)
    phi0 = np.deg2rad(phi0_deg)
    psi0 = np.deg2rad(psi0_deg)
    nutation_amp = np.deg2rad(nutation_amp_deg)

    t = np.linspace(0, T, n_steps)
    L = I * omega_disk
    tau = M * g * r
    Omega = tau / L   # 세차 각속도

    # Nutation(장동) 주기는 harmonic approximation에서:  omega_n ~ sqrt(Mgr/I)
    omega_n = np.sqrt(M * g * r / I)

    # 장동운동은 세차와 겹쳐서, theta(t)가 시간에 따라 작은 진동(위아래)이 추가됨
    theta = theta0 + nutation_amp * np.cos(omega_n * t)
    phi = Omega * t + phi0
    psi = omega_disk * t + psi0   # 내부 회전 (플롯에는 영향 없음)

    # 각운동량 방향벡터의 궤적 (단위벡터)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)

    # 크기*벡터(L로 스케일링)
    x = L * x
    y = L * y
    z = L * z

    return x, y, z, t, theta, phi

# ===== 사용 예시 =====
# 사용자가 원하는 값으로 입력해서 실험하세요!
I = 0.01           # 관성모멘트 (kg*m^2)
omega_disk = 40.0   # 각속도 (rad/s)
M = 0.25           # 무게추 (kg)
r = 0.12           # 거리 (m)
theta0_deg = 28    # 초기 회전축 각도
phi0_deg = 0       # 세차각 시작값
psi0_deg = 0       # 고유회전 초기값
nutation_amp_deg = 7 # 장동 진폭(최대)
T = 10             # 시뮬레이션 시간(초)
n_steps = 1500     # 플롯 해상도

# 궤적 계산
x, y, z, t, theta, phi = gyro_motion_3d(
    I, omega_disk, M, r,
    theta0_deg=theta0_deg, phi0_deg=phi0_deg, psi0_deg=psi0_deg,
    nutation_amp_deg=nutation_amp_deg,
    T=T, n_steps=n_steps
)

# 3D 그래프 플롯
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

# 세차(φ), 장동(θ) 시간에 따른 변화도 확인용 2D 그래프
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
