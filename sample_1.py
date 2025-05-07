import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# 구껍질 반지름
R = 3  # 구껍질 반지름

# 외부 전하의 위치 r'
r_prime = np.array([5, 0, 0])  # 전하 q의 위치 (r')
q = 1  # 점전하의 크기
epsilon_0 = 8.85e-12  # 진공 유전율

# 내부 포텐셜 계산을 위한 격자 생성
x = np.linspace(-R, R, 50)
y = np.linspace(-R, R, 50)
z = np.linspace(-R, R, 50)
X, Y, Z = np.meshgrid(x, y, z)

# 거리 계산
r_vec = np.stack((X, Y, Z), axis=-1)
r_magnitude = np.linalg.norm(r_vec, axis=-1)

# 내부 포텐셜 계산
V_internal = np.zeros_like(r_magnitude)
for i in range(X.shape[0]):
  for j in range(Y.shape[1]):
    for k in range(Z.shape[2]):
      r = np.array([X[i, j, k], Y[i, j, k], Z[i, j, k]])
      r_magnitude = np.linalg.norm(r)
      if r_magnitude < R:  # 내부에서만 계산
        r_diff = r - r_prime
        r_diff_magnitude = np.linalg.norm(r_diff)
        if r_diff_magnitude != 0:
          V_internal[i, j, k] = q * R / (4 * np.pi * epsilon_0 * r_diff_magnitude * r_magnitude)

# 3D 시각화를 위한 2D 슬라이스 선택 (z=0 평면)
V_slice = V_internal[:, :, V_internal.shape[2] // 2]

# 3D 시각화
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X[:, :, 0], Y[:, :, 0], V_slice, cmap='viridis')

ax.set_title("Electric Potential Inside Grounded Spherical Shell")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Potential (V)")

plt.show()




