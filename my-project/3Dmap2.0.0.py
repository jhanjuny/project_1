import xarray as xr
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#===�뚯씪 �몄텧�섍린===
name=input('file_name [ibw]=')
data_ibw=xr.open_dataarray(r'D:\URP\CPAG,CPAS\analsis data/%s' %(name))
new_data_ibw=data_ibw.rename({'Energy [eV]':'energy'})
name = input('file_name [txt]=')
data = np.loadtxt(r'D:\URP\CPAG,CPAS\analsis data/%s' %(name), delimiter='\t')


energy_vals=new_data_ibw.coords['energy'].values
X_coords=new_data_ibw.coords['X'].values
Y_coords=new_data_ibw.coords['Y'].values


energy_startpoint=energy_vals[0]
X_startpoint=X_coords[0]
Y_startpoint=Y_coords[0]

energy_delta=energy_vals[1]-energy_vals[0]
X_delta=X_coords[1]-X_coords[0]
Y_delta=Y_coords[1]-Y_coords[0]

#===湲곕낯 �곗씠�곕줈 蹂��섑븯湲�===
col=len(X_coords)
row=len(energy_vals)
layer=len(Y_coords)
split_data = np.vsplit(data, layer)

volume_data = np.zeros((row, col, layer))
for k in range(layer):
    volume_data[:, :, k] = split_data[k]
volume_data=np.sqrt(volume_data)
volume_data=np.transpose(volume_data,(1,2,0))
print('volume_data', volume_data.shape)


#===3D modling process===
print('===3D modling info insert section===')
col_sliced_1=float(input('what value you want to set kx-1 slice value [횇^-1]='))
col_sliced_2=float(input('what value you want to set kx-2 slice value [횇^-1]='))
layer_sliced_1=float(input('what vlaue you want to set ky-1 slice value [횇^-1]='))
layer_sliced_2=float(input('what vlaue you want to set ky-2 slice value [횇^-1]='))
row_sliced_1=float(input('what value you want to set energy-1 slice value [ev]='))
row_sliced_2=float(input('what value you want to set energy-2 slice value [ev]='))

col_sliced_refind_1=int((col_sliced_1-X_startpoint)//X_delta)
col_sliced_refind_2=int((col_sliced_2-X_startpoint)//X_delta)
layer_sliced_refind_1=int((layer_sliced_1-Y_startpoint)//Y_delta)
layer_sliced_refind_2=int((layer_sliced_2-Y_startpoint)//Y_delta)
row_sliced_refind_1=int((row_sliced_1-energy_startpoint)//energy_delta)
row_sliced_refind_2=int((row_sliced_2-energy_startpoint)//energy_delta)

X_coords_3D=X_coords[(col_sliced_refind_1):(col_sliced_refind_2)]
Y_coords_3D=Y_coords[(layer_sliced_refind_1):(layer_sliced_refind_2)]
Z_coords_3D=energy_vals[row_sliced_refind_1:row_sliced_refind_2]

volume_data_3D=volume_data[(col_sliced_refind_1):(col_sliced_refind_2),
                        (layer_sliced_refind_1):(layer_sliced_refind_2),
                        row_sliced_refind_1:row_sliced_refind_2]

# print('x,y,z:',len(X_coords_3D),len(Y_coords_3D),len(energy_vals))
print('volume_3d shape',volume_data_3D.shape)

reduced_value=int(input('what value do you want to set as the reduced resolution?='))
volume_data_reduced = volume_data_3D[::reduced_value, ::reduced_value, ::reduced_value]  
z_reduced_3D = Z_coords_3D[::reduced_value]
x_reduced_3D = X_coords_3D[::reduced_value]
y_reduced_3D = Y_coords_3D[::reduced_value]

print('volume data reduced shape:',volume_data_reduced.shape)

X, Y, Z= np.meshgrid(x_reduced_3D, y_reduced_3D, z_reduced_3D,  indexing='ij')

X_flat = X.flatten()
Y_flat = Y.flatten()
Z_flat = Z.flatten()

for i in range(volume_data_reduced.shape[0]):
    for j in range(volume_data_reduced.shape[1]):
        for k in range(volume_data_reduced.shape[2]):
            if np.isnan(volume_data_reduced[i, j, k]):
                volume_data_reduced[i, j, k]=0

intensity_flat = volume_data_reduced.flatten()
print(X_flat.shape,Y_flat.shape,Z_flat.shape)

# optional=input('do you want to set gamma[y/n]=')
# if optional=='y':
#     max=float(input('set intensity max='))
#     min=float(input('set intensity min='))
# else:
max=np.max(intensity_flat)
min=np.min(intensity_flat)

# opacity_val=float(input('set opacity value[0~1]='))
opacity_val=0.4
opacity_ratio=volume_data_reduced/np.max(volume_data_reduced)
# for i in range(volume_data_reduced.shape[0]):
#     for j in range(volume_data_reduced.shape[1]):
#         for k in range(volume_data_reduced.shape[2]):
#             if opacity_ratio[i,j,k]<=0.3:
#                 opacity_ratio[i,j,k]=0

#===End===


print('===some cutting info inserting section===')

#===kx-ky cuting====
energy_select=float(input('what value you want to see energy value='))
selected_energy_vals=int((energy_select-energy_startpoint)//energy_delta)
intensity_energy=volume_data[:,:,selected_energy_vals]
intensity_energy=np.transpose(intensity_energy)

#===kx-Eng cuting===
Y_select=float(input('what value you want to see kx value='))
selected_Y_vals=int((Y_select-Y_startpoint)//Y_delta)
volume_data_Y=np.transpose(volume_data,(2,1,0))
intensity_Y=volume_data_Y[:,selected_Y_vals,:]


#===ky-Eng cuting===
X_select=float(input('what value you want to see ky value='))
selected_X_vlas=int((X_select-X_startpoint)//X_delta)
intensity_X=volume_data[selected_X_vlas,:,:]

#===Eng-Intensity curve===
intensity_ev=volume_data[selected_X_vlas,selected_Y_vals,:]

#=== plotly subplot===
fig=make_subplots(
    rows=2, cols=3,
    column_widths=[0.5, 0.25, 0.25],
    row_heights=[0.25,0.25],
    specs=[[{'type':'Volume','rowspan':2}, {'type':'Heatmap'},{'type':'Scatter'}],
           [None, {'type':'Heatmap'}, {'type':'Heatmap'}]],
    # subplot_titles=('', f'ky={Y_select:.2f} [횇<sup>-1</sup>]', 'intensity-Eng'
    #                 , f'Eng={energy_select:.2f} [eV]', f'kx={X_select:.2f} [횇<sup>-1</sup>]')
)

fig.add_trace(
    go.Volume(
    x=X_flat,
    y=Y_flat,
    z=Z_flat,
    value=intensity_flat,
    opacity=opacity_val,
    opacityscale=opacity_ratio,
    surface_count=15,
    colorscale='matter',
    cmin=min,
    cmax=max,
    colorbar=dict(
        title='intensity',
        ticks='outside',
        x=0.427
    )),
    row=1,col=1
)

fig.add_trace(
    go.Heatmap(z=intensity_Y,
               y=energy_vals,
               x=X_coords,
               colorscale='Viridis',
               colorbar=dict(
                   title='intensity',
                   x=0.715,
                   len=0.45,
                   y=0.565,
                   yanchor='bottom'
               ),
               showscale=True),
    row=1, col=2
)

fig.add_trace(
    go.Scatter(
        x=energy_vals,
        y=intensity_ev),
    row=1, col=3
)
 
fig.add_trace(
    go.Heatmap(x=X_coords,
                y=Y_coords,
                z=intensity_energy,
                colorscale='Viridis',
                colorbar=dict(
                    title='intensity',
                    x=0.715,
                    len=0.45,
                    y=-0.01,
                    yanchor='bottom'
                ),
                showscale=True),
    row=2, col=2
)

fig.add_trace(
    go.Heatmap(z=intensity_X,
               y=Y_coords,
               x=energy_vals,
               colorscale='Viridis',
               colorbar=dict(
                   title='intensity',
                   x=1,
                   len=0.45,
                   y=-0.01,
                   yanchor='bottom'
               ),
               showscale=True),
    row=2, col=3
)

#====axis labling====
fig.update_layout(
    title=f'[{name}]<br> 3D modle-cut By JeonJongIn <br> Subplot info: k<sub>x</sub>={X_select:.2f}[횇<sup>-1</sup>]   k<sub>y</sub>={Y_select:.2f}[횇<sup>-1</sup>]   Eng={energy_select:.2f}[eV]',
    scene=dict(
        xaxis_title=r'kx [횇<sup>-1</sup>]',
        yaxis_title=r'ky [횇<sup>-1</sup>]',
        zaxis_title='E [eV]'
    ),       
    margin=dict(l=0, r=0, b=0, t=120),
    xaxis_title='kx [횇<sup>-1</sup>]',
    yaxis_title='Energy [eV]',
    xaxis2_title='Eng [eV]',
    yaxis2_title='Intensity',
    xaxis3_title='kx [횇<sup>-1</sup>]',
    yaxis3_title='ky [횇<sup>-1</sup>]',
    xaxis4_title='Energy [eV]',
    yaxis4_title='ky [횇<sup>-1</sup>]',
)

#===adding buttons===
fig.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=['colorscale', 'Viridis'],
                    label='Viridis',
                    method='restyle'
                ),
                dict(
                    args=['colorscale', 'Blues'],
                    label='Blues',
                    method='restyle'
                ),
                dict(
                    args=['colorscale', 'Reds'],
                    label='Reds',
                    method='restyle'
                ),
                dict(
                    args=['colorscale', 'Rainbow'],
                    label='Rainbow',
                    method='restyle'
                ),
                dict(
                    args=['colorscale', 'Cividis'],
                    label='Cividis',
                    method='restyle'
                ),
                dict(
                    args=['colorscale', 'Blackbody'],
                    label='Blackbody',
                    method='restyle'
                ),                
                dict(
                    args=['colorscale', 'Bluered'],
                    label='Bluered',
                    method='restyle'
                ),
                dict(
                    args=['colorscale', 'Electric'],
                    label='Electric',
                    method='restyle'
                ),
                dict(
                    args=['colorscale', 'Hot'],
                    label='Hot',
                    method='restyle'
                ),
                dict(
                    args=['colorscale', 'Jet'],
                    label='Jet',
                    method='restyle'
                ),
                dict(
                    args=['colorscale', 'Greens'],
                    label='Greens',
                    method='restyle'
                ),
                dict(
                    args=['colorscale', 'Greys'],
                    label='Greys',
                    method='restyle'
                ),
                dict(
                    args=['colorscale', 'YlGnBu'],
                    label='YlGnBu',
                    method='restyle'
                ),
                dict(
                    args=['colorscale', 'YlOrRd'],
                    label='YlOrRd',
                    method='restyle'
                ),
                dict(
                    args=['colorscale', 'Earth'],
                    label='Earth',
                    method='restyle'
                ),
                dict(
                    args=['colorscale', 'Picnic'],
                    label='Picnic',
                    method='restyle'
                ),
                dict(
                    args=['colorscale', 'Portland'],
                    label='Portland',
                    method='restyle'
                ),
                dict(
                    args=['colorscale', 'RdBu'],
                    label='RdBu',
                    method='restyle'
                ),
            ]),
            direction='up',
            pad={'r':10, 't':10},
            showactive=True,
            x=0.57,
            xanchor='left',
            y=-0.05,
            yanchor='top'
        ),
        dict(
            buttons=list([
                dict(
                    args=['reversescale', False],
                    label='False',
                    method='restyle'
                ),
                dict(
                    args=['reversescale', True],
                    label='True',
                    method='restyle'
                )
            ]),
            direction='up',
            pad={'r':10, 't':10},
            showactive=True,
            x=0.80,
            xanchor='left',
            y=-0.05,
            yanchor='top'
        )
    ]
)

#===buttons position===
fig.update_layout(
    annotations=[
        dict(text='colorscale', x=0.54, xref='paper', y=-0.1,yref='paper',
             align='left',showarrow=False),
        dict(text='Reverse<br>Colorscale',x=0.77, xref='paper', y=-0.1, yref='paper',
             showarrow=False)
    ]
)

#===set slider===
cmax_steps=[]
for i in range(0,int(np.max(intensity_flat)),5):
    cmax_steps.append(dict(
        method='restyle',
        args=[{'cmax':[i]},[0]],
        label=f'{i}'
    ))

opacity_steps=[]
for j in np.linspace(0.1,1.0,10):
    opacity_steps.append(dict(
        method='restyle',
        args=[{'opacity':[j]},[0]],
        label=f'{j:.1f}'
    ))


slider_cmax=dict(
    active=int(np.max(intensity_flat)),
    currentvalue={'prefix':'cmax:'},
    pad={'t':5},
    steps=cmax_steps,
    len=0.5,
    x=0,
    xanchor='left'
)

slider_opa=dict(
    active=int(opacity_val*10),
    currentvalue={'prefix':'opacity:'},
    pad={'t':55},
    steps=opacity_steps,
    len=0.5,
    x=0,
    xanchor='left'
)

fig.update_layout(
    sliders=[slider_cmax,slider_opa]
)

fig.show()