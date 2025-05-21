import numpy as np

import matplotlib.pyplot as plt

# 데이터 생성
x = np.linspace(0, 10, 100)
y = np.sin(x)

# 그래프 그리기
plt.plot(x, y, label='sin(x)')
plt.title('Sine Wave')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()