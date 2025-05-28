import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# RLC 회로 파라미터 입력(임의 값)
R = 100   # 저항 (Ohm)
L = 10e-3 # 인덕턴스 (H)
C = 47e-6  # 커패시턴스 (F)

# 신호 생성 파라미터
f1 = 100  # 채널1 신호 주파수 (Hz)
f2 = 100  # 채널2 신호 주파수 (Hz)
phi = np.pi/4  # 위상차 (rad)
A1 = 1      # 채널1 진폭 (V)
A2 = 1      # 채널2 진폭 (V)

t = np.linspace(0, 2e-3, 1000)

# 회로의 위상차 계산 (이론식)
omega = 2*np.pi*f1
ZL = omega*L
ZC = 1/(omega*C)
Z = np.sqrt(R**2 + (ZL - ZC)**2)
phi_theory = np.arctan2((ZL-ZC), R)  # 전류와 전압의 위상차

# CH1: 입력 신호, CH2: 회로를 지난 신호(위상차 부여)
ch1 = A1 * np.sin(2*np.pi*f1*t)
ch2 = A2 * np.sin(2*np.pi*f2*t + phi_theory)

# 리사주 도형 그리기
plt.figure(figsize=(6,6))
plt.plot(ch1, ch2)
plt.title(f'Lissajous Figure\nR={R}Ω, L={L*1e3}mH, C={C*1e6}uF\n주파수={f1}Hz, 위상차={phi_theory*180/np.pi:.1f}도')
plt.xlabel('CH1 입력 (V)')
plt.ylabel('CH2 출력 (V)')
plt.grid(True)
plt.axis('equal')
plt.show()

# 여러 값에 따라 변화 확인용 함수

def plot_lissajous(R=100, L=10e-3, C=1e-6, f1=1000, f2=1000, A1=1, A2=1):
    t = np.linspace(0, 2e-3, 1000)
    omega = 2*np.pi*f1
    ZL = omega*L
    ZC = 1/(omega*C)
    phi_theory = np.arctan2((ZL-ZC), R)
    ch1 = A1 * np.sin(2*np.pi*f1*t)
    ch2 = A2 * np.sin(2*np.pi*f2*t + phi_theory)
    plt.figure(figsize=(5,5))
    plt.plot(ch1, ch2)
    plt.title(f'Lissajous Figure\nR={R}Ω, L={L*1e3:.1f}mH, C={C*1e6:.1f}uF\n주파수={f1}Hz, 위상차={phi_theory*180/np.pi:.1f}도')
    plt.xlabel('CH1 입력 (V)')
    plt.ylabel('CH2 출력 (V)')
    plt.grid(True)
    plt.axis('equal')
    plt.show()

# 사용 예시
# plot_lissajous(R=100, L=10e-3, C=1e-6, f1=1000, f2=1000)
# plot_lissajous(R=100, L=20e-3, C=1e-6, f1=1000, f2=1000)
# plot_lissajous(R=100, L=10e-3, C=2e-6, f1=1000, f2=1000)
