import numpy as np
np.complex = complex
import igor.packed as pxp
import plotly.graph_objs as go
import glob

file_paths = sorted(glob.glob(r'C:\Users\pictu\URP_IGNOR\3D modeling\cpag0001.pxp'))
layers = []

for file_path in file_paths:
    with open(file_path, 'rb') as file:
        header, waves = pxp.load(file)
        for key in waves['root']:
            obj = waves['root'][key]
            if hasattr(obj, 'data'):
                print(f"{key}: shape={np.shape(obj.data)}")



data_3d = np.stack(layers, axis=0)
print("data_3d shape:", data_3d.shape)
if data_3d.ndim == 3:
    nz, ny, nx = data_3d.shape
elif data_3d.ndim == 2:
    nz = 1
    ny, nx = data_3d.shape
    data_3d = data_3d.reshape((1, ny, nx))
else:
    raise ValueError("data_3d shape가 예상과 다릅니다:", data_3d.shape)



fig = go.Figure(data=go.Volume(
    x=np.tile(x, ny * nz),
    y=np.repeat(np.tile(y, nx), nz),
    z=np.repeat(z, nx * ny),
    value=data_3d.flatten(),
    isomin=np.min(data_3d),
    isomax=np.max(data_3d),
    opacity=0.1,
    surface_count=20,
    colorscale='Viridis'
))
fig.update_layout(
    title='3D Band Structure from Igor Files',
    scene=dict(
        xaxis_title='kx',
        yaxis_title='ky',
        zaxis_title='Layer (kz)'
    )
)
fig.show()