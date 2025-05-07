import numpy as np
import matplotlib.pyplot as plt

# 초기 질문: 정전기 문제인지 확인
case = input("Is this electrostatic case? (yes/no): ").strip().lower()
if case != "yes":
    print("This script is designed for electrostatic cases only.")
    exit()

# 구 껍질 반지름
R = 10  # 구 껍질 반지름

# 경계 조건 선택
boundary_condition = input("We consider a spherical shell, Which one do you provide for boundary condition? (potential/electric field): ").strip().lower()
if boundary_condition == "potential":
    V_boundary = float(input("Enter the potential V(x) at the boundary: "))
elif boundary_condition == "electric field":
    E_boundary = float(input("Enter the electric field E(x) at the boundary: "))
else:
    print("Invalid boundary condition. Please choose 'potential' or 'electric field'.")
    exit()

# 외부 전하 위치 입력
print("Then the charge q is where?")
q_x = float(input("Enter the x-coordinate of the charge q: "))
q_y = float(input("Enter the y-coordinate of the charge q: "))
q_z = float(input("Enter the z-coordinate of the charge q: "))
q_position = np.array([q_x, q_y, q_z])
q = 1  # 점전하의 크기
epsilon_0 = 8.85e-12  # 진공 유전율

# 격자 생성
x = np.linspace(-R, R, 100)
y = np.linspace(-R, R, 100)
z = np.linspace(-R, R, 100)
X, Y, Z = np.meshgrid(x, y, z)

# 거리 계산
r_vec = np.stack((X, Y, Z), axis=-1)
r_magnitude = np.linalg.norm(r_vec, axis=-1)

# 전기 퍼텐셜 계산
V = np.zeros_like(r_magnitude)
for i in range(X.shape[0]):
    for j in range(Y.shape[1]):
        for k in range(Z.shape[2]):
            r = np.array([X[i, j, k], Y[i, j, k], Z[i, j, k]])
            r_magnitude = np.linalg.norm(r)
            if r_magnitude < R:  # 내부 계산
                if boundary_condition == "potential":
                    V[i, j, k] = V_boundary
                elif boundary_condition == "electric field":
                    V[i, j, k] = -E_boundary * r_magnitude
            else:  # 외부 계산
                r_diff = r - q_position
                r_diff_magnitude = np.linalg.norm(r_diff)
                if r_diff_magnitude != 0:
                    V[i, j, k] = q / (4 * np.pi * epsilon_0 * r_diff_magnitude)

# 특정 위치에서의 퍼텐셜 시각화
V_slice = V[:, :, V.shape[2] // 2]  # z=0 평면

# 2D 시각화
plt.figure(figsize=(8, 6))
plt.contourf(X[:, :, 0], Y[:, :, 0], V_slice, levels=50, cmap='viridis')
plt.colorbar(label="Potential (V)")
plt.title("Electric Potential in the Spherical Shell")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()