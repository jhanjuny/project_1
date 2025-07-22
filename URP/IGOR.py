import numpy as np
np.complex = complex
import igor.packed as pxp
import plotly.graph_objs as go
import glob


# Igor pxp 파일들을 순서대로 불러오기
file_paths = sorted(glob.glob(r'C:\Users\pictu\URP_IGNOR\3D modeling\cpag0001.pxp'))

# 데이터를 저장할 리스트 초기화
layers = []

# 각 파일에서 데이터 추출하여 layers 리스트에 추가
for file_path in file_paths:
    with open(file_path, 'rb') as file:
        record = pxp.load(file)
        # Igor 데이터에서 배열 형태로 데이터 추출 (변수 이름은 실제 데이터 구조에 따라 수정)
        data = np.array(record.wave['chunkCube_3DEk'].data)
        layers.append(data)

# layers를 3차원 배열로 변환
data_3d = np.stack(layers, axis=0)

# 데이터 차원 확인
nz, ny, nx = data_3d.shape

# 3D 시각화 준비
x = np.arange(nx)
y = np.arange(ny)
z = np.arange(nz)

# Plotly를 이용한 3D 볼륨 렌더링
fig = go.Figure(data=go.Volume(
    x=np.tile(x, ny * nz),
    y=np.repeat(np.tile(y, nx), nz),
    z=np.repeat(z, nx * ny),
    value=data_3d.flatten(),
    isomin=np.min(data_3d),
    isomax=np.max(data_3d),
    opacity=0.1, # 투명도 조절
    surface_count=20, # 단면 수 조정
    colorscale='Viridis'
))

# 레이아웃 설정
fig.update_layout(
    title='3D Band Structure from Igor Files',
    scene=dict(
        xaxis_title='kx',
        yaxis_title='ky',
        zaxis_title='Layer (kz)'
    )
)

# 시각화
fig.show()
