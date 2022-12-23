# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 15:09:38 2022

@author: Ander
"""

import matplotlib.pyplot as plt
from maps import mapping
import cartopy.crs as ccrs
import xarray as xr
import numpy as np
from Ler_dados_raytracing_plots import maximum_flux, ler_dados_rt, forward_backward, raytrancing_parametros
from utils import circle_with_legend, config_labels, save
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

entrada = ('C:\\Users\\Ander\\OneDrive\\Documentos\\ANDERSON\\a_Programas_raytracing\\modelos\\merra\\')

filename = 'MERRA2_300.inst3_3d_asm_Np.20031021.SUB.nc'
def load_models(entrada, filename):
#++++++++++++++++++++++++++++++++++++++++++++++++++


#++++++++++++++++++++++++++++++++++++++++++++++++++

    ds = xr.open_dataset(entrada + filename)
    sel = ds.sel()
    
    ##! --->Extraindo um subset (área)
    ds_subset = ds.sel(lon=slice(-80, 0), lat=slice(-40, 20))
    ds_subset.to_netcdf('C:\\Users\\Ander\\OneDrive\\Documentos\\ANDERSON\\a_Programas_raytracing\\modelos\\merra\\ds_AS.nc')
    
    
    ## -->Extraindo as variáveis separadamente
    t = ds_subset['T'] - 273.15
    u = ds_subset['U']           #podemos utilizar as duas notações ds_subset.u
    v = ds_subset['V']
    
    longitude = ds_subset['lon']
    latitude = ds_subset['lat']
    dia_tempo = ds_subset['time']
    nivel_pressao = ds_subset['lev']
    
    wspd = (u**2 + v**2)**(0.5)     ## elevado no 0.5 para extrair a raiz quadrada = VELOCIDADE DO VENTO
    
    
    temperatura = t.isel(time=0).sel(lev=600).values#.plot(cmap='jet')
    vento_zonal = u.isel(time=0).sel(lev=600).values#.plot(cmap='jet')
    vento_merid = v.isel(time=0).sel(lev=600).values#.plot(cmap='jet')
    velocidade_vento = wspd.isel(time=0).sel(lev=600).values#.plot(cmap='jet')
    
    lon = longitude.values
    lat = latitude.values
    X, Y = np.meshgrid(lon, lat)
    
    return X, Y, vento_zonal, vento_merid
#++++++++++++++++++++++++++++++++++++++++++++++++++

def float_time(hora):
    import math
    
    frac, whole = math.modf(hora)
    
    minutes = int(frac * 60)
    
    hour = int(whole)


    if hour >=24: 
        hour -= 24
        hour = f"0{hour}"
    
    if minutes < 10:
        minutes = f"0{minutes}"
    
    return  f" {hour}:{minutes} (UT)"


def colorbar_setting(img, ax, ticks):
    
    """Color bar settings"""
    axins = inset_axes(
                ax,
                width="3%",  # width: 5% of parent_bbox width
                height="100%",  # height: 50%
                loc="lower left",
                bbox_to_anchor=(1.05, 0., 1, 1),
                bbox_transform=ax.transAxes,
                borderpad=0,
            )
    
    cb = fig.colorbar(img, cax = axins, ticks = ticks)
    
    cb.set_label(r'Vento (m/s)')


def plotTrajetorias(parameters, dados, phase):
    fig, ax = mapping()
    
    colors = ["blue", "red"][::-1]
    styles = ["-", "--"][::-1]
    names = ["Vento HWM14", "sem vento"][::-1]
    
    circle_with_legend(ax, [0], scale = 110)
    
    
    hora, _, date = tuple(parameters)
    
    
    ax.text(0., 1.03, "(d)", transform = ax.transAxes)
    time = float_time(hora)
    
    date_str = date.strftime("%d/%m/%Y") + time
    
    FigureName = f"{phase}_{date.strftime('%d_%m_%Y')}_mapa.png"
    
    x, y, vento_zonal, vento_merid = load_models(entrada, filename)
    magnitude = vento_zonal + vento_merid
    img = ax.streamplot(x, y, vento_zonal, vento_merid, 
                        transform=ccrs.PlateCarree(),
              linewidth=1, density=4, color = magnitude, cmap = 'gnuplot')
    
    colorbar_setting(img, ax, np.arange(-20, 70, 5))
    
    
    flux_col = 'fluxo_momento_medio'
    
    for i, df in enumerate(dados[::-1]):
        
        lat = df["latitude"].values
        
        lon = df["longitude"].values
        
        ax.plot(lon,  
                 lat, 
                 color = colors[i] , 
                 linestyle = styles[i], 
                 label = names[i],
                 transform = ccrs.PlateCarree())     
        
        max_flux_time, max_flux_alt, flux_max, flux10_alt, flux10_time, flux10Menor = maximum_flux(df, phase)
        
        
        
        latMax, lonMax = tuple(df.loc[df[flux_col] == flux_max, 
                                      ["latitude", "longitude"]].values[0])
        lat10, lon10 = tuple(df.loc[df[flux_col] == flux10Menor, 
                                    ["latitude", "longitude"]].values[0])
    
        ax.plot(lonMax, latMax,  
                marker = "s", 
                color = colors[i],
                transform=ccrs.PlateCarree(), 
                label = "FMM")
        
        ax.plot(lon10, lat10,  
                marker = "s", 
                color = colors[i], 
                fillstyle = "none",
                transform=ccrs.PlateCarree(), 
                label = "10% do FM")
        
    
        
        
        ax.set(title = f"{phase.title()}: {date_str}")
     
        #if phase == "descendente":
        
           # ax.plot(lon[-1], lat[-1], "o", color = colors[i], label = "")
        #else:
           # ax.plot(lon[0], lat[0], "o", color = colors[i])
        
        ax.legend(loc = "lower right")
        
    return FigureName, fig, ax 


phase = "ascendente"
parame, dado = raytrancing_parametros(phase, start = None, end = None)
path = f"entrada"


for i in range(3):
    
    parameters = parame[i]
    dados = dado[i]
    
    try:
     FigureName, fig = plotTrajetorias(parameters, dados, phase)
     save(fig, path, FigureName)
    except:
        continue