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
from maps import plot_trajetorias
from utils import circle_with_legend, config_labels, save
from Ler_dados_raytracing_plots import  ler_dados_rt, forward_backward, raytrancing_parametros

# from caracteristicas import plot2
# from vento import plotTrajetorias
# from utilis import circle_with_legend

# import caracteristicas
# import utilis 
# import vento


 
    ###============================================================================
    ###Topo---> para colocar color bar em função da ALTITUDE de parada
    # ax = plt.subplot(G[0, :])
    
    # # The plot itself
    # plt1 = ax.scatter(x, y, c = z, 
    #                     marker = 's', s=20, edgecolor = 'none',alpha =1,
    #                     cmap = 'magma_r', vmin =0 , vmax = 4)
    
    # cb = Colorbar(ax = ax, mappable = plt1, orientation = 'horizontal', ticklocation = 'top')
    # cb.set_label(r'Colorbar !', labelpad=10)
    
    
    ###============================================================================
                    # N de linhas   # N de colunas
    #map 0.1                #0:3
    
###============================================================================
###--->Figura

    ###============================================================================
    ###---> Configurações da FIGUR
    # caracteristicas.plot2()
    # infos = f"$\lambda_H = ${lambdaH} km, $\\tau = $ {periodo} min, $c_H = $ {vel_fase} m/s, $\phi = $ {propagacao}°" 
    #ax1.set_title(f"infos")
    # ax1[0].text(0.2, 1.1, infos, transform = ax1[0].transAxes)

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
        
        phase = "descendente"
        circle_with_legend(mapa, [300, 700, 1100, 1500], scale = 110)
        
        plot_trajetorias(ax1, phase, rt_type = "forward")
        
        return ax1
    
    
    
    def latitude(self):
        ax3 = self.fig.add_subplot(self.G[1:3, 3:4])
        ax3.set(ylim=self.mapa().get_ylim())
        ax3.set_xlabel('Altitude (km)')
        ax3.set_ylabel('Latitude (°)')
        return ax3
    
    def longitude(self):
        ax4 = self.fig.add_subplot(self.G[3:4, 0:3])
        ax4.set(xlim=self.mapa().get_xlim())
        ax4.set_xlabel('Longitude (°)')
        ax4.set_ylabel('Altitude (km)')
        return ax4
    

    def tempo(self):
        ax5 = self.fig.add_subplot(self.G[3:4, 3:4])
        ax5.set(ylim=self.longitude().get_ylim())
        #ax5.set_ylabel('Altitude (km)')
        ax5.set_xlabel('Horas (LT)')
        return ax5
    
    

fig = plt.figure(figsize=(12, 12))

mp = MapaRT(fig)

mapa = mp.mapa()



lon = mp.longitude()

lat = mp.latitude()
tim = mp.tempo()