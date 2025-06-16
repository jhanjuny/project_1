def gyro_motion_3d(I, omega_disk, M, r,
                   theta0_deg, phi0_deg, psi0_deg,
                   nutation_amp_deg, g, T, n_steps):
    # 라디안 변환
    phi0   = np.deg2rad(phi0_deg)
    theta0 = np.deg2rad(theta0_deg)
    psi0   = np.deg2rad(psi0_deg)
    nut_amp= np.deg2rad(nutation_amp_deg)

    t = np.linspace(0, T, n_steps)
    L = I * omega_disk
    tau = M * g * r
    Omega = tau / L                     # 이론 세차 각속도

    omega_n = np.sqrt(M * g * r / I)    # 장동 주파수
    theta = theta0 + nut_amp * np.cos(omega_n * t)
    phi   = Omega * t + phi0

    x = L * np.sin(theta) * np.cos(phi)
    y = L * np.sin(theta) * np.sin(phi)
    z = L * np.cos(theta)

    return x, y, z, t, theta, phi


def get_user_params():
    print("자이로스코프 시뮬레이션 파라미터를 입력하세요:")
    I               = float(input("관성모멘트 I (kg·m^2): "))
    omega_disk      = float(input("디스크 각속도 ω (rad/s): "))
    M               = float(input("무게추 질량 M (kg): "))
    r               = float(input("무게추 거리 r (m): "))
    theta0_deg      = float(input("초기 틸트 각 θ0 (deg): "))
    phi0_deg        = float(input("초기 세차 각 φ0 (deg): "))
    psi0_deg        = float(input("초기 스핀 각 ψ0 (deg): "))
    nutation_amp_deg= float(input("장동 진폭 (deg): "))
    g               = float(input("중력가속도 g (m/s^2): "))
    T               = float(input("시뮬레이션 시간 T (s): "))
    n_steps         = int(input("스텝 수 n_steps: "))
    return I, omega_disk, M, r, theta0_deg, phi0_deg, psi0_deg, nutation_amp_deg, g, T, n_steps



if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    import plotly.graph_objects as go

    # 1) 사용자로부터 파라미터 입력
    params = get_user_params()
    I, omega_disk, M, r, theta0_deg, phi0_deg, psi0_deg, nut_amp, g, T, n_steps = params

    # 2) 시뮬레이션 수행
    x, y, z, t, theta, phi = gyro_motion_3d(*params)

    # 3) 그래프 출력 (Matplotlib 3D)
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z, lw=2, label='Trajectory')
    ax.scatter(0,0,0, color='red', s=50, label='Origin')
    ax.set(title="3D Precession+Nutation", xlabel="X", ylabel="Y", zlabel="Z")
    ax.legend()
    plt.show()

    # 4) Plotly 3D
    fig_p = go.Figure()
    fig_p.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', name='Trajectory'))
    fig_p.update_layout(title="Gyro 3D Sim (Plotly)", scene=dict(
        xaxis_title="X", yaxis_title="Y", zaxis_title="Z"))
    fig_p.show()

    # 5) 2D 장동/세차 각도 변화
    fig2, axs = plt.subplots(2,1,sharex=True)
    axs[0].plot(t, np.rad2deg(theta), label='θ (deg)')
    axs[1].plot(t, np.rad2deg(phi), label='φ (deg)', color='g')
    axs[0].set_ylabel('θ (deg)'); axs[1].set_ylabel('φ (deg)')
    axs[1].set_xlabel('Time (s)')
    axs[0].legend(); axs[1].legend()
    plt.suptitle("Nutation & Precession Angle vs Time")
    plt.show()
