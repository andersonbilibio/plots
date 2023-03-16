import cartopy.crs as ccrs
import shapely.geometry as sgeom
from cartopy.geodesic import Geodesic
import numpy as np
import matplotlib.pyplot as plt
import os 


    
def config_labels(fontsize = 13, lw = 1, major = 8, minor = 4):

    plt.rcParams.update({'font.size': fontsize, 
                     'axes.linewidth' : lw,
                     'grid.linewidth' : lw,
                     'lines.linewidth' : lw,
                     'legend.frameon' : True,
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


def save(fig, path, FigureName):
    # fig.savefig(f"{path}\\{FigureName}.pdf", dpi = 500)  ### imprimi a imagem .png
    local = os.path.join(path, FigureName.replace('png','pdf'))     ### imprimi a imagem .pdf
    fig.savefig(local, dpi = 500)
    

def circle_range(ax, longitude, latitude, 
                 radius = 500, color = "gray"):
             
    gd = Geodesic()

    cp = gd.circle(lon = longitude, 
                   lat = latitude, 
                   radius = radius * 1000.)
    
    geoms = [sgeom.Polygon(cp)]

    ax.add_geometries(geoms, crs=ccrs.PlateCarree(), 
                      edgecolor = 'black', color = color,
                      alpha = 0.2, label = 'radius')
    
    
def circle_with_legend(ax, radius_list, scale = 100):
               
     infos = {"São João do Cariri": [-36.55, -7.38], 
                  "Cachoeira Paulista": [-45.0, -22.81]}
     
     colors = ['darkviolet','deeppink']
     markes = ["^","o"]
         
     for radius in radius_list:
         
         if len(radius_list) > 2:
         
             delta = radius / scale
             ax.text(-36.55, -7.38 + delta, f"{radius} km", 
                 transform=ccrs.PlateCarree())
         
         for i, name in enumerate(infos.keys()):
         
             lon, lat = tuple(infos[name])
        
             circle_range(ax, lon, lat, 
                          radius = radius, 
                          color = "black")
             
             
             ax.plot(lon,lat,
                         marker=markes[i],
                         color= colors[i],
                         markersize=4,
                         label= name,
                         zorder=100,
                         transform=ccrs.PlateCarree())
                 
             
    
def copy(folder_path, dst, files):
    import shutil
    for filename in files:
        if ".csv" in filename:
            
            shutil.copy(folder_path + filename, 
                        dst + filename)
