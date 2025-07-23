import numpy as np
import glob
import plotly.graph_objs as go

# 1. 레이어로 사용할 RAW 파일 경로 설정 (바이너리 파일)
file_pattern = r'C:\Users\pictu\URP_IGNOR\CPAG\CPAG0001\*.bin'
file_paths = sorted(glob.glob(file_pattern))

# 2. RAW 파일들을 순차적으로 읽어 2D 배열로 변환하여 리스트에 저장
# 반드시 각 파일의 데이터 shape과 dtype을 알아야 함 (예시: float32, 128x128)
ny, nx = 128, 128  # 파일의 실제 행/열 크기로 수정하세요
layers = []
for fp in file_paths:
    data2d = np.fromfile(fp, dtype=np.float32).reshape(ny, nx)
    layers.append(data2d)

# 3. 리스트를 3D 배열로 스택
data3d = np.stack(layers, axis=0)  # shape: (nz, ny, nx)

# 4. 좌표축 생성
nz, ny, nx = data3d.shape
x = np.arange(nx)
y = np.arange(ny)
z = np.arange(nz)

# 5. Plotly Volume 렌더링
fig = go.Figure(data=go.Volume(
    x=np.tile(x, ny * nz),
    y=np.repeat(np.tile(y, nx), nz),
    z=np.repeat(z, nx * ny),
    value=data3d.flatten(),
    isomin=data3d.min(),
    isomax=data3d.max(),
    opacity=0.1,
    surface_count=20,
    colorscale='Viridis'
))

# 6. 레이아웃 설정
fig.update_layout(
    title='3D Stacked Band Structure from RAW Files',
    scene=dict(
        xaxis_title='kx Index',
        yaxis_title='ky Index',
        zaxis_title='Layer (kz Index)'
    )
)

# 7. 시각화 출력
fig.show()