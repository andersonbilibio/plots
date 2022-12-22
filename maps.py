import matplotlib.pyplot as plt
import matplotlib.dates as dates
import cartopy

from Ler_dados_raytracing_plots import convert_time_obs, maximum_flux, ler_dados_rt, forward_backward, raytrancing_parametros

from utils import circle_with_legend

def config_labels(fontsize = 13, lw = 1, major = 8, minor = 4):

    plt.rcParams.update({'font.size': fontsize, 
                     'axes.linewidth' : lw,
                     'grid.linewidth' : lw,
                     'lines.linewidth' : lw,
                     'legend.frameon' : False,
                     'savefig.bbox' : 'tight',
                     'savefig.pad_inches' : 0.05,
                     'mathtext.fontset': 'dejavuserif', 
                     'font.family': 'serif', 
                     'ytick.direction': 'in',
                     'ytick.minor.visible' : True,
                     'ytick.right' : True,
                     'ytick.major.size' : lw + major,
                     'ytick.major.width' : lw,
                     'ytick.minor.size' : lw + minor,
                     'ytick.minor.width' : lw,
                     'xtick.direction' : 'in',
                     'xtick.major.size' : lw + major,
                     'xtick.major.width': lw,
                     'xtick.minor.size' : lw + minor,
                     'xtick.minor.width' :lw,
                     'xtick.minor.visible' : True,
                     'xtick.top' : True,
                     'axes.prop_cycle' : 
                    plt.cycler('color', ['#0C5DA5', '#00B945', '#FF9500', 
                                                              '#FF2C00', '#845B97', '#474747', '#9e9e9e'])
                         }) 



    
    
def plot(ax, 
         fo, ba, 
         hora_inicial,
         xcol = "altitude_(metros)",
         ycol = "latitude", 
         formato = False, 
         alt_emission = 97, color = "blue"):
    
    
    time_col = "tempo_em_seg_desde_a_hora_inicial"
    
    
    try:
        tf = hora_inicial + max(fo.index)
        ti = hora_inicial + min(ba.index)
    except:
        tf = hora_inicial + max(fo[time_col])
        ti = hora_inicial + min(ba[time_col])
        

    zero = convert_time_obs(hora_inicial, date_sel)
    start = convert_time_obs(ti, date_sel)
    end = convert_time_obs(tf, date_sel)

    fo.index = pd.date_range(zero, end, periods = len(fo))
    ba.index = pd.date_range(start, zero, periods = len(ba))
    
    args = dict(color = color, lw = 2)
    
    if xcol == "time":
    
        ax.plot(fo[ycol], **args)
        ax.plot(ba[ycol], **args)
        ax.plot(zero, alt_emission, "^", 
                markersize = 15, 
                color = "purple")
        
        ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
        ax.xaxis.set_major_locator(dates.MinuteLocator(interval = 20))
        ax.axhline(alt_emission, color = "k", lw = 1)
        
        flux_time, flux_alt, time10, alt10 = maximum_flux(fo, phase = phase)
        
        flux_time = convert_time_obs(hora_inicial + flux_time, date_sel)
        time10 = convert_time_obs(hora_inicial + time10, date_sel)
        
        args_sq = dict(marker = "s", color = color, markersize =10)
        
        ax.plot(flux_time, flux_alt, **args_sq)
        ax.plot(time10, alt10, fillstyle = "none", **args_sq)
        
    else:
        ax.plot(fo[xcol], fo[ycol], **args)
        ax.plot(ba[xcol], ba[ycol], **args)
        

    return ax




config_labels(fontsize = 13, lw = 1, major = 8, minor = 4)

def plot_tri(fo, ba, hora_inicial):

    fig, axs = plt.subplots(figsize = (12, 8), 
                            nrows = 3)
    
    plt.subplots_adjust(hspace = 0.4)
    
    combinations = [("altitude_(metros)", "time"), 
                    ("altitude_(metros)", "longitude"), 
                    ("latitude", "altitude_(metros)")]
    
    letters = ["(a)", "(b)", "(c)"]
    
    for num, ax in enumerate(axs.flat):
        
        ycol, xcol = combinations[num]
        
        
        xlabel = xcol.replace("_(metros)", "") 
        ylabel = ycol.replace("_(metros)", "") 
        
        
        
        ax.set(ylabel = ylabel, xlabel = xlabel, title = letters[num])
        
        args = dict(color = 'gray', 
                    linestyle = '--', 
                    linewidth = 0.5)
        
        if xlabel == "longitude" and ylabel == "altitude":
            ax.grid(axis='x', **args) 
            formato = False
            
        elif xlabel == "altitude" and ylabel == "latitude":
            ax.grid(axis='y', **args)
            formato = False
        else:
            ax.grid(axis='both', **args) 
            formato = True
            
            
            
            
        ax = plot(ax, fo, ba, 
                  hora_inicial, 
                  xcol = xcol , 
                  ycol = ycol, 
                  formato = formato)
        



import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
import cartopy.feature as cfeature
import numpy as np
import matplotlib.ticker as mticker




def mapping():
    
    fig = plt.figure(figsize = (20, 20))

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
    
    
    ax1.set(title = '(a) Posição Final das OGME')
    return fig, ax1


def save(fig, path, FigureName):
    fig.savefig(f"{path}\\{FigureName}", dpi = 300)


    
def plot_trajetorias(phase, rt_type = False):

    fig, ax1 = mapping()
    
    out, dados = raytrancing_parametros(phase, start = 0)
    
    
    for i, vals in enumerate(dados):
        
        color = ["blue", "red"]
        
        df = dados[i][0]
    
        fordward, backward = forward_backward(df, phase = phase)
        
        if rt_type == "fordward":
            ba = fordward
            if phase == "descendente":
                end = -1
            else:
                end = 0
        else:
            ba = backward
            if phase == "descendente":
                end = 0
            else:
                end = -1
            
    
        ax1.plot(ba.iloc[:,16], 
                 ba.iloc[:,15],  
                 color='blue', 
                 linestyle='-', 
                 label='Ray Tracing com vento HWM14',
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
    phase ="ascendente" 
    
    #for phase in ["descendente", "ascendente"]:
    
    caminho_vento = f"C:\\Users\\Ander\\OneDrive\\Documentos\\ANDERSON\\a_Programas_raytracing\\{phase}\\rt\\vento\\"
     
    for rt_type in ["fordward", "backward"]:
        
                
        FigureName = f"{phase}_todosCasos_{rt_type}.png"
        path_to_save = "\\".join(caminho_vento.split("\\")[:8])
        
        fig = plot_trajetorias(phase, rt_type = rt_type)
        
        save(fig, path_to_save, FigureName)
