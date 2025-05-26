import numpy as np
import plotly.graph_objects as go

# 그리드 크기
Nx, Ny, Nz = 20, 20, 20
T = np.zeros((Nx, Ny, Nz))
T[Nx//2, Ny//2, Nz//2] = 100  # 중앙만 뜨겁게

# 좌표 생성
x, y, z = np.meshgrid(np.arange(Nx), np.arange(Ny), np.arange(Nz), indexing='ij')

# Plotly 볼륨 시각화
fig = go.Figure(data=go.Volume(
    x=x.flatten(),
    y=y.flatten(),
    z=z.flatten(),
    value=T.flatten(),
    isomin=0,
    isomax=100,
    opacity=0.1,
    surface_count=15,
    colorscale='Hot'
))
fig.update_layout(title="3D Heat Diffusion (Volume Render)")

# 시각화
fig.show()
