import matplotlib.pyplot as plt
from Ler_dados_raytracing_plots import  ler_dados_rt, forward_backward, raytrancing_parametros
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
import cartopy.feature as cfeature
import numpy as np
import matplotlib.ticker as mticker

from utils import circle_with_legend, config_labels, save



    
    




config_labels(fontsize = 13, lw = 1, major = 8, minor = 4)


        


def mapping():
    
    fig = plt.figure(figsize = (25, 25))

    background = cimgt.GoogleTiles(style='satellite')
    
    ax1 = plt.subplot(1,2,1, projection=ccrs.PlateCarree())
    ax1.set_extent([-80, 0, -40, 10], ccrs.PlateCarree())
    
    
    ax1.add_feature(cfeature.COASTLINE)
    ax1.add_feature(cfeature.BORDERS)
    
    states = cfeature.NaturalEarthFeature(category='cultural', 
                                          name='admin_1_states_provinces_lines', 
                                          scale='50m',                  
                                          facecolor='none')
    
    
    ax1.add_feature(states,
                    edgecolor='black',
                    linestyle=':', 
                    linewidth=1)
    ax1.stock_img()
    
    
    g1 = ax1.gridlines(crs=ccrs.PlateCarree(), 
                       draw_labels=True, 
                       linestyle='--',
                       linewidth=1,
                       color='white')
  
    
    g1.top_labels = False
    g1.right_labels = False
    
    g1.ylocator = mticker.FixedLocator(np.arange(-40, 20, 10))
    g1.yformatter = LATITUDE_FORMATTER
    g1.xformatter = LONGITUDE_FORMATTER
    
    
    #ax1.set(title = '(a) Posição Final das OGME')
    return fig, ax1





    
def plot_trajetorias(phase, rt_type = False):

    fig, ax1 = mapping()
    
    out, dados = raytrancing_parametros(phase, start = 0)
    
    hora_inicial, altitude, date_sel = tuple(out[0])    
    
    for i, vals in enumerate(dados):
        
        color = ["blue", "red"]
        
        df = dados[i][0]
    
        fordward, backward = forward_backward(df, 
                                              hora_inicial, 
                                              phase = phase)
        
        if rt_type == "fordward":
            ba = fordward
            if phase == "descendente":
                end = 0
            else:
                end = -1
        else:
            ba = backward
            if phase == "descendente":
                end = -1
            else:
                end = 0
            
    
        ax1.plot(ba.iloc[:,16], 
                 ba.iloc[:,15],  
                 color='blue', 
                 linestyle='-', 
                 transform=ccrs.PlateCarree())      
        
        lat = ba.iloc[:,15].values[end]
        lon = ba.iloc[:,16].values[end]
        
            
        ax1.plot(lon, 
                 lat, 
                 color = color[0],
                 marker = "o",
                 markersize = 4,
                 transform = ccrs.PlateCarree())
           
    radius_list = [300, 700, 1100, 1500]
    
    circle_with_legend(ax1, radius_list, scale = 110)
    
    return fig

def main():
    phase ="descendente" #"ascendente" 
    
    #for phase in ["descendente", "ascendente"]:
    
    caminho_vento = f"C:\\Users\\Ander\\OneDrive\\Documentos\\ANDERSON\\a_Programas_raytracing\\{phase}\\rt\\vento\\"
     
    for rt_type in ["fordward", "backward"]:
        
                
        FigureName = f"{phase}_todosCasos_{rt_type}.png"
        path_to_save = "\\".join(caminho_vento.split("\\")[:8])
        
        fig = plot_trajetorias(phase, rt_type = rt_type)
        
        save(fig, path_to_save, FigureName)

