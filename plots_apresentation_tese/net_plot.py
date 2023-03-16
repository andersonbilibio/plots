# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 13:28:10 2023

@author: Ander
"""

import xarray as xr
import proplot as plot

air = xr.tutorial.open_dataset('air_temperature').air[0]

array = [
    [1, 1, 1, 2],
    [1, 1, 1, 2],
    [3, 3, 3, 0]
]

fig, ax = plot.subplots(array, proj={1:'pcarree'}, width=7)

air.plot(ax=ax[0], add_colorbar=False)
air.mean('lon').plot(ax=ax[1], y='lat', xincrease=True)
air.mean('lat').plot(ax=ax[2])

ax.format(abc=True, abcloc='l', abcstyle='(a)')

ax[0].format(lonlim=(air.lon[0], air.lon[-1]), latlim=(air.lat[0], air.lat[-1]),
             coast=True, labels=True, lonlines=20, latlines=10,
             title='temperature')
ax[1].set(title='zonal mean', xlim=[240, 300], ylabel=None,
          yticks=[20, 30, 40, 50, 60, 70],
          yticklabels=['20°N','30°N','40°N','50°N','60°N','70°N'])
ax[2].set(title='meridional mean', ylim=[260, 285],
          ylabel=None, xlabel='longitude',
          xticklabels=['160°W','140°W','120°W','100°W','80°W','60°W','40°W'])