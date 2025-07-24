import numpy as np
np.complex = complex
import igor.packed as pxp
import plotly.graph_objs as go

def find_3d_wave(node, prefix=''):
    """재귀적으로 3D 배열 웨이브를 찾아 반환 (첫 번째 3D 웨이브만)"""
    for key in node:
        obj = node[key]
        if hasattr(obj, 'data'):
            arr = np.array(obj.data)
            print(f"{prefix}{key}: shape={arr.shape}")
            if arr.ndim == 3:
                return arr, f"{prefix}{key}"
        elif isinstance(obj, dict):
            result = find_3d_wave(obj, prefix=f"{prefix}{key}/")
            if result is not None:
                return result
    return None

pxp_path = r'D:\URP\3D modeling\cpag0001.pxp'
with open(pxp_path, 'rb') as f:
    header, waves = pxp.load(f)
    print("[root keys]", waves['root'].keys())
    # 3D 웨이브 자동 탐색
    result = find_3d_wave(waves['root'])
    if result is None:
        raise ValueError("3D 배열 웨이브를 찾을 수 없습니다.")
    data3d, wave_name = result
    print(f"시각화할 웨이브: {wave_name}, shape={data3d.shape}")

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
    title=f'3D Intensity Volume of {wave_name}',
    scene=dict(
        xaxis_title='kx index',
        yaxis_title='ky index',
        zaxis_title='kz index'
    )
)

fig.show()