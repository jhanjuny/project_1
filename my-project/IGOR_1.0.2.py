import erlab
import erlab.analysis as era
import erlab.interactive as eri
import erlab.plotting as eplt
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import os

xr.set_options(keep_attrs=True)
xr.set_options(display_expand_data=False)

#name= input('file name [ibw]=')
data = xr.open_dataarray(r"D:/URP/3D modeling/0046.ibw")

eri.itool(data)
data.qshow()