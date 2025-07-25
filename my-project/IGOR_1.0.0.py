import erlab
import erlab.analysis as era
import erlab.plotting as eplt
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

data = xr.open_dataarray(r"D:/URP/3D modeling/chunkCube_3DEk1.ibw")

print(data)

xr.set_options(display_expand_data=False)

data.sel(Energy =0.0, method="nearest").plot()


a = 6.97

X = [0, 2 * np.pi / (a * np.sqrt(3)), 2 * np.pi / (a * np.sqrt(3)), 0]
Y = [0, 0, 2 * np.pi / (a * 3), 0]


data.qsel(Energy=-0.2).qplot(aspect="equal", cmap="Greys")
plt.plot(X, Y, "o-")

dat_sliced = era.interpolate.slice_along_path(
    data, vertices={"X": X, "Y": Y}, step_size=0.01
)
dat_sliced

dat_sliced.qplot(cmap="Greys")
eplt.fermiline()

# Distance between each pair of consecutive points
distances = np.linalg.norm(np.diff(np.vstack([X, Y]), axis=-1), axis=0)
seg_coords = np.concatenate(([0], np.cumsum(distances)))

plt.xticks(seg_coords, labels=["Γ", "M", "K", "Γ"])
plt.xlim(0, seg_coords[-1])
for seg in seg_coords[1:-1]:
    plt.axvline(seg, ls="--", c="k", lw=1)
plt.show()