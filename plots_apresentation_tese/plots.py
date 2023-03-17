# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 11:58:09 2023
Figuras para Apresentação da tese 
@author: Anderson Bilibio
"""

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
import cartopy.feature as cfeature
from src.base import load_files, plot_traj, plot_alt

import os
from utils import circle_with_legend
class MapaRT:
    
    
    def __init__(self, fig):
    
        self.fig = fig
        self.G = gridspec.GridSpec(4, 4, hspace=0.5, wspace=0.5)
    
   
    def mapa(self):
        ax1 = self.fig.add_subplot(
            self.G[0:4, 0:3],
            projection= ccrs.PlateCarree()
            )
        
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
        
        circle_with_legend(ax1, [300, 700, 1100, 1500], scale = 110)
        
        infile = "database/vento/"

        files = os.listdir(infile)
        phase = "ascendente"
        for filename in files:
        
            plot_traj(ax1, infile, filename, phase = "ascendente")
        
        return ax1
    
    
    
    def latitude(self):
        ax3 = self.fig.add_subplot(self.G[1:3, 3:4])
        ax3.set(ylim=self.mapa().get_ylim())
        ax3.set_xlabel('Altitude (km)')
        ax3.set_ylabel('Latitude (°)')
        infile = "database/vento/"

        files = os.listdir(infile)
        phase = "ascendente"
        for filename in files:
            plot_alt(ax3, 
                      infile, filename, 
                      phase = "ascendente", 
                      rt_type = "fordward", 
                      alt_lon = False)
        return ax3
    
    def longitude(self):
        ax4 = self.fig.add_subplot(self.G[3:4, 0:3])
        ax4.set(xlim=self.mapa().get_xlim())
        ax4.set_xlabel('Longitude (°)')
        ax4.set_ylabel('Altitude (km)')
        infile = "database/vento/"

        files = os.listdir(infile)
        phase = "ascendente"
        for filename in files:
            plot_alt(ax4, 
                      infile, filename, 
                      phase = "ascendente", 
                      rt_type = "fordward", 
                      alt_lon = True)
        return ax4
    

    def tempo(self):
        ax5 = self.fig.add_subplot(self.G[3:4, 3:4])
        #ax5.set(ylim=self.longitude().get_ylim())
        #ax5.set_ylabel('Altitude (km)')
        ax5.set_xlabel('Horas (LT)')
        import pandas as pd
        df = pd.read_csv("ascendente_final_positions.txt", index_col = 0
                         )
        #df = df.mean()
        ax5.grid()
        ax5.scatter(df.time, df.alt, color = "b")
        return ax5
    
    

fig = plt.figure(figsize=(12, 12))

mp = MapaRT(fig)

mapa = mp.mapa()



lon = mp.longitude()

lat = mp.latitude()
tim = mp.tempo()