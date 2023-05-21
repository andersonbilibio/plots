# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 16:19:12 2023

@author: Ander
"""

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
from base import load_files, sep_for_and_back
import csv
import pandas as pd
import os
from utils import circle_with_legend, save




import matplotlib.pyplot as plt 



def plot_traj( 
              infile,
              filename, 
              phase, 
              rt_type):
    
    df, obs, _ = load_files(infile, filename, phase = phase)
    forward, backward = sep_for_and_back(df, phase = phase)
    
    if rt_type == "fordward":
        ba = forward
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
            
        
    
    lats = ba["lat"].values
    lons = ba["lon"].values
    alts = ba["z"].values
    
    # plt.plot(lons, 
    #          lats,  
    #          color='blue', 
    #          linestyle='-')
    
    lat = lats[end]
    lon = lons[end]
    alt = alts[end] /1000
    
        
    return lons, lats, alts, lat, lon, alt
    
        
def mapa(fig, G):
    ax1 = fig.add_subplot(
        G[0:4, 0:3],
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
    
    
    
    
    return ax1
    
    
def latitude(fig, ax1, G):
    ax3 = fig.add_subplot(G[1:3, 3:4])
    ax3.set(ylim= ax1.get_ylim())
    ax3.set_xlabel('Altitude (km)')
    ax3.set_ylabel('Latitude (°)')
    ax3.grid()
    return ax3

def longitude(fig, ax1, G):
    ax4 = fig.add_subplot(G[3:4, 0:3])
    ax4.set(xlim=ax1.get_xlim())
    ax4.set_xlabel('Longitude (°)')
    ax4.set_ylabel('Altitude (km)')
    ax4.grid()
    return ax4



def tempo(fig, ax3, G):
    ax5 = fig.add_subplot(G[3:4, 3:4])
 #   ax5.set(ylim = ax3.get_ylim())
    ax5.set_ylabel('Altitude (km)')
    ax5.set_xlabel('Horas (LT)')
    ax5.grid()
   
    return ax5
    



from utils import config_labels
config_labels()

for phase in ["ascendente", "descendente"]:
    for rt_type in ["backward", "fordward"]:
            
        infile = f"C:\\Users\\Ander\\OneDrive\\Documentos\\ANDERSON\\a_Programas_raytracing\\{phase}\\rt\\vento\\"
         
        fig = plt.figure(figsize=(12, 12))
        G = gridspec.GridSpec(4, 4, hspace=0.5, wspace=0.5)
        
        ax1 = mapa(fig, G)
        ax2 = latitude(fig, ax1, G)
        ax3 = longitude(fig, ax1, G)
        #ax4 = tempo(fig, ax3, G)
        
        
        
        files = os.listdir(infile)
        
        circle_with_legend(ax1, [300, 700, 1100, 1500], scale = 110)
        
        for filename in files:
        
            lons, lats, alts, lat, lon, alt = plot_traj( 
                      infile, 
                      filename, 
                      phase = phase, 
                      rt_type = rt_type)
            
            
                
            ax1.plot(lons, lats,  color = "b",  markersize = 4)
            ax1.scatter(lon, lat, color = "b", alpha = 0.5)
            ax3.scatter(lon, alt, color = "b")
            ax2.scatter(alt, lat, color = "b")
            
        
        
        # fig.suptitle(f'Fase {phase} - Posição final das OGME', y = 0.7)
        
        fig.suptitle(f'Posição final das OGME', y = 0.7)
        
        FigureName = f'{phase}_final_positions.pdf'
    
        
        if phase == "ascendente":
            phase = "descendente"
        else:
            phase = "ascendente"
            
        df = pd.read_csv(f"{phase}_final_positions.txt", index_col = 0)
        
        #rt_type = "fordward"
        df = df[rt_type]
        
    
        
        time = df.loc[df.index == "time"].values
        alt = df.loc[df.index == "alt"].values
        
        ax1.legend(["São João do Cariri", "Cachoeira Paulista",
                    "Trajetoria com vento",  "Posição final"], 
                   bbox_to_anchor=(1.4, -0.2))
        
      #  ax4.scatter(time, alt, color = "b")
        
        path = 'C:\\Users\\Ander\\OneDrive\\Documentos\\ANDERSON\\a_Programas_raytracing\\'
        save(fig, path, FigureName)
        # save

