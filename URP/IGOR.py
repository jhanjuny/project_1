import numpy as np
np.complex = complex
import igor.packed as pxp
import plotly.graph_objs as go

pxp_path = r'D:\URP\3D modeling\cpag0001.pxp'
with open(pxp_path, 'rb') as f:
    header, waves = pxp.load(f)
    print(waves['root'].keys())  # 내부 웨이브 이름 확인

# 예시: 키가 b'chunkCube_3DEK'일 때
wave = waves['root'][b'chunkCube_3DEK']
data3d = np.array(wave.data)



# 이하 기존 코드 동일
nz, ny, nx = data3d.shape
x = np.arange(nx)
y = np.arange(ny)
z = np.arange(nz)

X, Y, Z = np.meshgrid(x, y, z, indexing='xy')

fig = go.Figure(data=go.Volume(
    x=X.flatten(),
    y=Y.flatten(),
    z=Z.flatten(),
    value=data3d.flatten(),
    isomin=data3d.min(),
    isomax=data3d.max(),
    opacity=0.1,
    surface_count=25,
    colorscale='Viridis'
))

fig.update_layout(
    title='3D Intensity Volume of chunkCube_3DEK',
    scene=dict(
        xaxis_title='kx index',
        yaxis_title='ky index',
        zaxis_title='kz index'
    )
)

fig.show()