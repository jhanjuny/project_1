import os
import glob
import numpy as np
import plotly.graph_objs as go
from igor.binarywave import load

# ─────────────────────────────────────────────────────────────────────────
# 1) 설정
#   root_dir 아래에 각각 3D ibw 파일 하나씩(chunkCube_3DEk.ibw)이 들어있는 폴더들이 있다고 가정
root_dir = r"D:\URP\3D modeling"
#   ibw 파일 이름
ibw_name = "chunkCube_3DEk.ibw"
#   실제 데이터가 들어있는 wave 키
data_key = "wData"
# ─────────────────────────────────────────────────────────────────────────

# 2) 서브폴더 목록
subfolders = sorted([d for d in os.listdir(root_dir)
                     if os.path.isdir(os.path.join(root_dir, d))])

volumes = []
names   = []
for sub in subfolders:
    fn = os.path.join(root_dir, sub, ibw_name)
    if not os.path.exists(fn):
        print(f"[!] {fn!r} 이 존재하지 않습니다, 건너뜁니다")
        continue
    print(f"[+] 로드 중: {fn}")
    ibw = load(fn)
    arr = np.array(ibw["wave"][data_key])
    # 필요하다면 축 순서 맞추기 (예: (nx,ny,nz)->(nz,ny,nx))
    # arr = arr.transpose(2,1,0)
    print(f"    → shape = {arr.shape}")
    volumes.append(arr)
    names.append(sub)

if not volumes:
    raise RuntimeError("한 개도 못 읽었습니다!")

# 3) 4D 배열로 쌓기 (nFolders, Nz, Ny, Nx)
data4d = np.stack(volumes, axis=0)
nsets, nz, ny, nx = data4d.shape

# 4) 좌표 생성
x = np.arange(nx)
y = np.arange(ny)
z = np.arange(nz)

# 5) Plotly Frame 만들기
frames = []
for i, name in enumerate(names):
    X, Y, Z = np.meshgrid(x, y, z, indexing='xy')
    vol = go.Volume(
        x=X.ravel(), y=Y.ravel(), z=Z.ravel(),
        value=data4d[i].ravel(),
        isomin=data4d.min(), isomax=data4d.max(),
        opacity=0.1,         # 0.0 ~ 1.0 사이
        surface_count=20,    # 등치면 개수
        colorscale="Viridis"
    )
    frames.append(go.Frame(data=[vol], name=name))

# 6) Figure + Play 버튼
fig = go.Figure(
    data=[frames[0].data[0]],
    layout=go.Layout(
        title="4D Volume Animation",
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            buttons=[dict(
                label="▶ Play",
                method="animate",
                args=[None, {
                    "frame": {"duration": 500, "redraw": True},
                    "fromcurrent": True
                }]
            )]
        )]
    ),
    frames=frames
)

fig.update_layout(
    scene=dict(
        xaxis_title="kx (pixel)",
        yaxis_title="ky (pixel)",
        zaxis_title="kz (pixel)"
    ),
    margin=dict(t=50, b=0, l=0, r=0)
)

fig.show()
