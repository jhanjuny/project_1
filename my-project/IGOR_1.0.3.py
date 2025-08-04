import numpy as np
import matplotlib.pyplot as plt
import plotly.io as pio
pio.renderers.default = 'browser'


alpha = 0.01
Lx, Ly = 1.0, 1.0
Nx, Ny = 50, 50
dx = Lx / (Nx - 1)
dy = Ly / (Ny - 1)
dt = 0.0005
T_total = 1.0
Nt = int(T_total / dt)

s = alpha * dt / dx**2
assert s <= 0.25, f"불안정! s = {s:.3f} > 0.25"

T = np.zeros((Nx, Ny))
T_new = np.zeros_like(T)
T[Nx // 2, Ny // 2] = 100.0

history = []

for n in range(Nt):
    for i in range(1, Nx - 1):
        for j in range(1, Ny - 1):
            T_new[i, j] = T[i, j] + s * (
                T[i+1, j] + T[i-1, j] + T[i, j+1] + T[i, j-1] - 4*T[i, j]
            )
    T[:] = T_new[:]
    history.append(T.copy())


import plotly.graph_objects as go


X, Y = np.meshgrid(np.linspace(0, Lx, Nx), np.linspace(0, Ly, Ny), indexing='ij')

frames = [
    go.Frame(
        data=[go.Surface(z=history[i], x=X, y=Y, colorscale='Hot')],
        name=str(i)
    )
    for i in range(len(history))
]

fig = go.Figure(
    data=[go.Surface(z=history[0], x=X, y=Y, colorscale='Hot')],
    frames=frames
)

fig.update_layout(
    title="2D Heat Diffusion - 3D Surface Animation",
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Temperature'
    ),
    updatemenus=[
        dict(
            type="buttons",
            showactive=False,
            buttons=[
                dict(label="Play", method="animate", args=[None, {"frame": {"duration": 50, "redraw": True}, "fromcurrent": True}]),
                dict(label="Pause", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}])
            ]
        )
    ]
)

fig.show()