import xarray as xr
import numpy as np
import pyvista as pv

#=== data input===
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

col=len(X_coords)
row=len(energy_vals)
layer=len(Y_coords)
split_data = np.vsplit(data, layer)

#=== refine data ===
volume_data = np.zeros((row, col, layer))
for k in range(layer):
    volume_data[:, :, k] = split_data[k]
volume_data=np.sqrt(volume_data)
volume_data=np.transpose(volume_data,(1,2,0))
print('volume_data', volume_data.shape)

volume_data[np.isnan(volume_data)] = 0

intensity_flat = volume_data.flatten(order='F')

#=== volume data plot & widget ===
image=pv.ImageData(
    dimensions=(col,layer,row),
    spacing=(X_delta,Y_delta,energy_delta),
    origin=(X_startpoint,Y_startpoint,energy_startpoint)
)
image.point_data['intensity']=intensity_flat
print('intensity:',len(intensity_flat))
print(image)
print(image.point_data)

pl=pv.Plotter()
actor=pl.add_volume(
    image,
    scalars='intensity',
    opacity='sigmoid',
    cmap='matter',
    scalar_bar_args=dict(interactive=True, width=0.02)
)
actor.prop.interpolation_type='linear'

# actor_2=pl.add_volume_clip_plane(image, normal='-x',
#                          interaction_event='always',
#                          opacity='linear',
#                          cmap='viridis')


#=== add color button ===
def update_cmap(cmap_name):
    def callback():
        global actor  
        pl.remove_actor(actor) 
        actor = pl.add_volume(image, scalars='intensity', cmap=cmap_name, opacity='sigmoid',
                              scalar_bar_args=dict(interactive=True, width=0.02))
        pl.render()
    return callback

cmaps = ['YlGnBu','PuRd','spring','Spectral','cool','matter','devon','viridis', 'plasma', 'jet']
positions = [(10,300),(10,270),(10,240),(10,210),(10,180),(10,150), (10,120), (10, 90), (10, 60), (10, 30)] 

for i, cmap in enumerate(cmaps):
    pl.add_radio_button_widget(
        update_cmap(cmap),         # 肄쒕갚 �⑥닔
        radio_button_group='cmap', # 紐⑤몢 媛숈� 洹몃９�� �ы븿
        value=(i==4),              # 泥� 踰덉㎏ 踰꾪듉留� on
        position=positions[i],
        title=cmap,
        size=30,
        border_size=1,
        color_on='green',
        color_off='grey'
    )

#=== add background color button ===
def set_bg(color):
    def wrapped_callback():
        pl.background_color = color
    return wrapped_callback

bgcolor=['raspberry','White','paraview', 'darkslategray','darkcyan']
positions_2=[(200.0, 30.0),(200.0, 60.0),(200.0, 90.0),(200,120),(200,150)]

for i, bg in enumerate(bgcolor):
    pl.add_radio_button_widget(
        set_bg(bg),
        radio_button_group='background',
        value=(i==1),
        position=positions_2[i],
        title=bg,
        size=30,
        border_size=1,
        color_on='green',
        color_off='gray'
    )

#=== add opacity button ===
def update_opacity(opacity_val):
    def callback():
        global actor
        pl.remove_actor(actor)
        actor=pl.add_volume(image, scalars='intensity',cmap='matter', opacity=opacity_val,
                            scalar_bar_args=dict(interactive=True, width=0.02))
        pl.render()
    return callback

opacitys=['None','sigmoid']
positions_3=[(450,30),(450,60)]

for i, opac in enumerate(opacitys):
    pl.add_radio_button_widget(
        update_opacity(opac),
        radio_button_group='opacity',
        value=(i==1),
        position=positions_3[i],
        title=opac,
        size=30,
        border_size=1,
        color_on='green',
        color_off='gray'
    )

#=== add show grid button ===
def toggle_grid(flag):
    def callback():
        if flag:
            pl.show_grid(
                xtitle='kx [횇^-1]',
                ytitle='ky [횇^-1]',
                ztitle='energy [eV]',
                n_xlabels=10,
                n_ylabels=10,
                n_zlabels=10,
                bold=False,
                minor_ticks=True
            )
        else:
            pl.remove_bounds_axes()
    return callback

pl.add_radio_button_widget(
    toggle_grid(True),
    radio_button_group='grid',
    title="on",
    value=True,
    position=(620,60),
    size=30,
    border_size=1,
    color_on='green',
    color_off='grey'
)
pl.add_radio_button_widget(
    toggle_grid(False),
    radio_button_group='grid',
    title='off',
    position=(620,30),
    size=30,
    border_size=1,
    color_on='green',
    color_off='grey'
)
#=== show & hide arrow ===
current_normal = '-x' # 珥덇린 normal 諛⑺뼢 (x異�)
current_origin = image.center 

clip_widget = pl.add_volume_clip_plane(
    image, 
    normal=current_normal,
    origin=current_origin,
    normal_rotation=True,  
    interaction_event='always',
    opacity='linear'  
)

# Plane �곹깭瑜� 異붿쟻�섍린 �꾪븳 肄쒕갚 �⑥닔
def update_plane_state():
    global current_normal, current_origin
    # VTK widget�먯꽌 �꾩옱 �곹깭 媛��몄삤湲�
    if hasattr(clip_widget, 'GetNormal'):
        current_normal = np.array(clip_widget.GetNormal())
    if hasattr(clip_widget, 'GetOrigin'):
        current_origin = np.array(clip_widget.GetOrigin())

def show_arrow():
    global clip_widget, current_normal, current_origin
    update_plane_state()
    pl.clear_plane_widgets()
    
    clip_widget = pl.add_volume_clip_plane(
        actor,
        normal=current_normal,
        origin=current_origin,
        normal_rotation=True,  
        interaction_event='always'
    )
    pl.render()

def hide_arrow():
    global clip_widget, current_normal, current_origin
    
    update_plane_state()
    pl.clear_plane_widgets()
    
    clip_widget = pl.add_volume_clip_plane(
        actor,
        normal=current_normal,
        origin=current_origin,
        normal_rotation=False,  
        interaction_event='always'
    )
    pl.render()


pl.add_radio_button_widget(
    show_arrow,
    'arrow_control',
    position=(720.0, 60.0),
    title='Show Arrow',
    value=True,
    size=30,
    border_size=1,
    color_on='green',
    color_off='grey'  
)

pl.add_radio_button_widget(
    hide_arrow,
    'arrow_control', 
    position=(720.0, 30.0),
    title='Hide Arrow',
    size=30,
    border_size=1,
    color_on='green',
    color_off='grey'
)

#=== set lable & text ===
pl.show_grid(
    xtitle='kx [횇^-1]',
    ytitle='ky [횇^-1]',
    ztitle='energy [eV]',
    n_xlabels=10,
    n_ylabels=10,
    n_zlabels=10,
    bold=False,
    minor_ticks=True
)

pl.add_text(f'[{name}] \n 3D modle-cut By JeonJongIn', font_size=12 )
pl.add_text('colormap', position=(10,330), font_size=10)
pl.add_text('opacity', position=(450,90), font_size=10)
pl.add_text('background color', position=(200,190), font_size=10)
pl.add_text('grid',position=(620,90), font_size=10)
pl.add_text('clip plane', position=(720,90),font_size=10)

pl.show()