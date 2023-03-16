# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 16:12:26 2023
---> Leituras as imagens de Sateélites e impressão sobre o Mapa;
@author: Anderson Bilibio
"""


###++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
###--->ENTRADA DAS BIBLIOTECAS
###++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from io import BytesIO
from pyproj import Transformer, CRS
from urllib.request import urlopen
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import shapely.geometry as sgeom
from cartopy.geodesic import Geodesic
import numpy as np
import matplotlib.pyplot as plt
import os 



###++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
###--->FUNÇÃO PARA CHAMAR A IMAGEM
###++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def geos_image():
    """
    Return a specific SEVIRI image by retrieving it from a github gist URL.

    Returns
    -------
    img : numpy array
        The pixels of the image in a numpy array.
    img_proj : cartopy CRS
        The rectangular coordinate system of the image.
    img_extent : tuple of floats
        The extent of the image ``(x0, y0, x1, y1)`` referenced in
        the ``img_proj`` coordinate system.
    origin : str
        The origin of the image to be passed through to matplotlib's imshow.

    """
    # url = ('https://gist.github.com/pelson/5871263/raw/'
           # 'EIDA50_201211061300_clip2.png')                       ###--->para usar arquivo direto URL
    url = ('C:\\Users\\Ander\\OneDrive\\Documentos\\ANDERSON\\a_Programas_raytracing\\Figuras_apresentation\\2004-09-20-00.png')
    
    # img_handle = BytesIO(urlopen(url).read())                     ###--->para usar arquivo direto URL
    # img = plt.imread(img_handle)                                  ###--->para usar arquivo direto URL
    img = plt.imread(url)
    img_proj = ccrs.Geostationary(satellite_height=35786000)
    img_extent = [-9500000, 1000000, -5500000, 5500000]
    return img, img_proj, img_extent, 'upper'


# ###++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ###--->FUNÇÃO PARA CONVERTER GEODESIA EM LOG,LAT
# ###++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# def convert_coords(obs_x, obs_y, obs_z, to_radians = True):
# # def convert_coords(img_extent, img_proj, to_radians = True):    
#     """
#     Converts cartesian to geodesic coordinates. 
#     Just now, just for the receiver positions.
#     The parameters must be in meters [m]
#     >>> obs_x, obs_y, obs_z = 5043729.726, -3753105.556, -1072967.067
#     >>> print(convert_coords(obs_x, obs_y, obs_z))
#     ...-36.6534, -9.7492, 266.23012
#     """
    
    
    
#     crs_from = CRS(proj = 'geocent', ellps = 'WGS84', datum = 'WGS84')
    
#     crs_to = CRS(proj = 'latlong', ellps = 'WGS84', datum = 'WGS84')
    
#     transformer = Transformer.from_crs(crs_from, crs_to)
    
#     lon, lat, alt = transformer.transform(xx = [-800000,000000],
#                                           yy = [-5500000,5500000],
#                                           zz = 35786000, 
#                                           radians = False) 
    
#     if to_radians:
#         lon = np.radians(lon + 360) 
#         lat = np.radians(lat)
    
#     return lon, lat, alt



###++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
###--->FUNÇÃO PARA CONFIGURAR A LEGENDA DE IMPRESSÃO
###++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
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


###++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
###--->FUNÇÃO PARA IMPRIR A FIGURA 
###++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():
    fig = plt.figure(figsize=(25,25))
    # ax = fig.add_subplot(1, 1, 1, projection=ccrs.Miller())       ###--->outra projeção
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.coastlines()
    ax.set_global()
    print('Retrieving image...')
    img, crs, extent, origin = geos_image()
    print('Projecting and plotting image (this may take a while)...')
    ax.imshow(img, transform=crs, extent=extent, origin=origin, cmap='gray')
    plt.show()


if __name__ == '__main__':
    main()



###++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
###--->FUNÇÃO PARA SALVAR AS IMAGENS EM PDF
###++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def save(fig, path, FigureName):
    # fig.savefig(f"{path}\\{FigureName}.pdf", dpi = 500)  ### imprimi a imagem .png
    local = os.path.join(path, FigureName.replace('png','pdf'))     ### imprimi a imagem .pdf
    fig.savefig(local, dpi = 500)