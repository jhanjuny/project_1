import numpy as np
import matplotlib.pyplot as plt

# 격자 크기 및 몬테카를로 파라미터
L = 20  # 격자 한 변의 길이
N = L * L
J = 1.0  # 상호작용 상수
n_eq = 1000  # 평형화 스텝
n_mc = 2000  # 측정 스텝
T_list = np.linspace(1.5, 3.5, 21)  # 온도 범위

def periodic(i, L):
    return i % L

def delta_E(S, i, j):
    # 최근접 스핀 합 (주기적 경계조건)
    left = S[periodic(i-1, L), j]
    right = S[periodic(i+1, L), j]
    up = S[i, periodic(j-1, L)]
    down = S[i, periodic(j+1, L)]
    return 2 * J * S[i, j] * (left + right + up + down)

m_list = []

for T in T_list:
    S = np.random.choice([-1, 1], size=(L, L))  # 초기 스핀
    # 평형화
    for step in range(n_eq):
        for _ in range(N):
            i = np.random.randint(0, L)
            j = np.random.randint(0, L)
            dE = delta_E(S, i, j)
            if dE < 0 or np.random.rand() < np.exp(-dE / T):
                S[i, j] *= -1
    # 측정
    m_sum = 0
    for step in range(n_mc):
        for _ in range(N):
            i = np.random.randint(0, L)
            j = np.random.randint(0, L)
            dE = delta_E(S, i, j)
            if dE < 0 or np.random.rand() < np.exp(-dE / T):
                S[i, j] *= -1
        m_sum += np.abs(np.sum(S)) / N
    m_avg = m_sum / n_mc
    m_list.append(m_avg)
    print(f"T={T:.2f}, m={m_avg:.3f}")

plt.plot(T_list, m_list, 'o-')
plt.xlabel("Temperature T")
plt.ylabel("Magnetization |m|")
plt.title("2D Ising Model: Magnetization vs Temperature")
plt.grid(True)
plt.show()

# 상전이 온도(Tc)는 m이 급격히 0으로 떨어지는 지점에서 추정할 수 있습니다.