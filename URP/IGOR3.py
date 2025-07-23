import numpy as np
import glob
import os
import plotly.graph_objs as go

# 1. 여러 폴더 경로 패턴 설정 (예: 'data/set*')
folder_pattern = r'C:\Users\pictu\URP_IGNOR\CPAG\CPAG0001'
folders = sorted(glob.glob(folder_pattern))

all_data_sets = []
for folder in folders:
    # 각 폴더 내의 .bin 및 .ini 파일 경로 지정
    ini_file = os.path.join(folder, 'Spectrum_Fmap_fixed.ini')
    bin_file = os.path.join(folder, 'Spectrum_Fmap_fixed.bin')
    
    # ini 파일에서 메타 데이터 읽기
    import configparser
    config = configparser.ConfigParser()
    config.read(ini_file)
    width = config.getint('spectrum', 'width')
    height = config.getint('spectrum', 'height')
    depth = config.getint('spectrum', 'depth')
    byteperpoint = config.getint('spectrum', 'byteperpoint')
    
    # 바이너리 데이터 읽기
    data = np.fromfile(bin_file, dtype=np.float32)
    data = data.reshape((depth, height, width))  # (kz, ky, kx)
    all_data_sets.append(data)

# 3D 스택 -> 4D 배열로 변환
data_4d = np.stack(all_data_sets, axis=0)  # (nSets, kz, ky, kx)

# 축 인덱스 생성
nsets, nz, ny, nx = data_4d.shape

# 4D 시각화를 위해 각 세트별 슬라이스를 3D plot으로 만들고 애니메이션 프레임으로 지정
frames = []
for i in range(nsets):
    vol = go.Volume(
        x=np.tile(np.arange(nx), ny * nz),
        y=np.repeat(np.tile(np.arange(ny), nx), nz),
        z=np.repeat(np.arange(nz), nx * ny),
        value=data_4d[i].flatten(),
        isomin=data_4d.min(), isomax=data_4d.max(),
        opacity=0.1, surface_count=20,
        colorscale='Viridis'
    )
    frames.append(go.Frame(data=[vol], name=f'Set{i}'))

# 초기 프레임
fig = go.Figure(
    data=[frames[0].data[0]],
    layout=go.Layout(
        title='4D Stacked Band Structure Animation',
        updatemenus=[dict(
            type='buttons',
            buttons=[dict(label='Play',
                          method='animate',
                          args=[None, {'frame': {'duration': 500, 'redraw': True}}])]
        )]
    ),
    frames=frames
)

# 축 레이블 설정
fig.update_layout(
    scene=dict(
        xaxis_title='kx Index',
        yaxis_title='ky Index',
        zaxis_title='kz Index'
    )
)

fig.show()
