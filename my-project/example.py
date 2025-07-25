import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 3D 서브플롯 지원

# 1) 예제용 좌표 격자 생성
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)

# 2) Z 값 정의 (예: X^2 + Y^2 의 포물면)
Z = X**2 + Y**2

# 3) Figure 생성 및 3D 서브플롯 추가
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# 4) surface 그리기
surf = ax.plot_surface(
    X, Y, Z,
    cmap='viridis',        # 컬러맵
    edgecolor='none',      # 격자선 없음
    alpha=0.8              # 투명도
)

# 5) 컬러바 추가
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='Intensity')

# 6) 축 라벨링
ax.set_xlabel('X 축')
ax.set_ylabel('Y 축')
ax.set_zlabel('Z 값')

plt.title("3D Surface Plot 예시")
plt.show()
