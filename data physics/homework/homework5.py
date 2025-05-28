import numpy as np
import matplotlib.pyplot as plt

# --- 파라미터 설정 ---
N = 20                  # 격자 크기 N x N
J = 1.0                 # 상호작용 상수 (에너지 단위)
n_eq = 1000             # 평형화 스텝 수
n_mc = 1000             # 측정 스텝 수
T_list = np.linspace(1.0, 4.0, 30)  # 온도 구간

# --- 주기적 경계조건 이웃합 함수 ---
def neighbor_sum(S, i, j):
    return (S[(i+1)%N, j] + S[(i-1)%N, j] + S[i, (j+1)%N] + S[i, (j-1)%N])

# --- 메트로폴리스 알고리즘 (단일 온도, 단일 시뮬레이션) ---
def ising_mc(T):
    S = np.random.choice([1, -1], size=(N,N))
    for _ in range(n_eq):
        for _ in range(N*N):
            i, j = np.random.randint(0, N, 2)
            dE = 2 * J * S[i,j] * neighbor_sum(S, i, j)
            if dE < 0 or np.random.rand() < np.exp(-dE/T):
                S[i,j] *= -1
    # 샘플링
    m_list = []
    for _ in range(n_mc):
        for _ in range(N*N):
            i, j = np.random.randint(0, N, 2)
            dE = 2 * J * S[i,j] * neighbor_sum(S, i, j)
            if dE < 0 or np.random.rand() < np.exp(-dE/T):
                S[i,j] *= -1
        m = np.abs(np.sum(S)) / (N*N)
        m_list.append(m)
    return np.mean(m_list)

# --- 온도별 자화 측정 ---
m_vs_T = []
for T in T_list:
    m = ising_mc(T)
    m_vs_T.append(m)
    print(f"T={T:.2f}, <|m|>={m:.3f}")

# --- 그래프 출력 ---
plt.plot(T_list, m_vs_T, 'o-')
plt.axvline(2.27, color='gray', linestyle='--', label=r'$T_c \approx 2.27$')
plt.xlabel("온도 T")
plt.ylabel("평균 자화 |m|")
plt.title("2D 이징 모델 자화 곡선 (주기적 경계조건)")
plt.legend()
plt.show()
