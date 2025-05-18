import numpy as np
import matplotlib.pyplot as plt

v0 = 1.0
x0 = 0.0
T_real = 1.0
maxt = 1000.0

dt_list = np.arange(0.01, 0.21, 0.01)
T_est_list = []

for dt in dt_list:
    t_arr = []
    x_arr = []
    v_arr = []
    v2_arr = []
    x, v = x0, v0
    a = np.sqrt(6 * T_real / dt)
    for t in np.arange(0, maxt, dt):
        t_arr.append(t)
        x_arr.append(x)
        v_arr.append(v)
        v2_arr.append(v * v)
        eta = a * (2 * np.random.rand() - 1.0)
        x += dt * v
        v += dt * (-v + eta)
    # 운동에너지의 시간평균으로부터 T 추정 (평형 이후 구간 사용)
    v2_avg = np.average(v2_arr[len(v2_arr)//2:-1])
    T_est = v2_avg / 2  # 1차원에서 <v^2> = 2T
    T_est_list.append(T_est)

plt.plot(dt_list, T_est_list, 'o-')
plt.xlabel("Δt")
plt.ylabel("Estimated Temperature T")
plt.title("Estimated Temperature vs Δt")
plt.grid(True)
plt.show()