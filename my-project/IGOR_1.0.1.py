import erlab
import erlab.analysis as era
import erlab.plotting as eplt
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

data1 = xr.open_dataarray(r"D:/URP/3D modeling/chunkCube_3DEk1.ibw")
#data2 = xr.open_dataarray(r"D:/URP/3D modeling/chunkCube_3DEk2.ibw")
#data3 = xr.open_dataarray(r"D:/URP/3D modeling/chunkCube_3DEk3.ibw")
#data4 = xr.open_dataarray(r"D:/URP/3D modeling/chunkCube_3DEk4.ibw")

print(data1)

xr.set_options(display_expand_data=False)

data1.sel(Energy =0.0, method="nearest").plot()





plt.show()