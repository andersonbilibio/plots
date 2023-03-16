# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 11:04:06 2023
FONTE:https://scitools.org.uk/cartopy/docs/latest/gallery/scalar_data/geostationary.html#sphx-glr-gallery-scalar-data-geostationary-py
@author: Anderson - figuras Apresentacao tese 
"""
from io import BytesIO
from urllib.request import urlopen

import cartopy.crs as ccrs
import matplotlib.pyplot as plt


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
    img_extent = [-9500000, 6500000, -6500000, 6500000]
    return img, img_proj, img_extent, 'upper'


def main():
    fig = plt.figure()
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
