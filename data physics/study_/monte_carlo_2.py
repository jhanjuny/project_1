import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

N = 1000000  # 샘플 개수
x = np.random.rand(N) * 5      # x in [0, 5]
y = np.random.rand(N) * 1      # y in [0, 1]

# 적분할 함수: y < e^{-x^2} 인 점의 비율을 센다
count = np.sum(y < np.exp(-x**2))
area = 5 * 1  # x구간 길이 * y구간 길이

integral = area * count / N
print("Monte Carlo 적분값:", integral)

# scipy를 이용한 정확한 적분값
def f(x):
    return np.exp(-x**2)

integral_scipy, error = quad(f, 0, 5)
print("scipy.integrate.quad 적분값:", integral_scipy)
print("오차 추정:", error)

# 두 방법의 차이 출력
print("두 방법의 차이:", abs(integral - integral_scipy))
area = 5 * 1  # x구간 길이 * y구간 길이

for N in 10**np.array([1, 2, 3, 4, 5, 6, 7]):
    x = np.random.rand(N) * 5      # x in [0, 5]
    y = np.exp(-x**2) 
    integral_mean = np.sum(y)*5.0/N
    print(N, integral_mean)



print("방법1(면적비)-방법2(scipy):", abs(integral - integral_scipy))
print("방법1(면적비)-방법3(평균값):", abs(integral - integral_mean))
print("방법2(scipy)-방법3(평균값):", abs(integral_scipy - integral_mean))

# (참고) N 변화에 따른 평균값 몬테카를로 적분값 출력
for N in 10**np.array([1, 2, 3, 4, 5, 6, 7]):
    x = np.random.rand(N) * 5      # x in [0, 5]
    y = np.exp(-x**2)
    print(f"N={N}, 평균값 몬테카를로 적분값: {np.sum(y)*5.0/N}")