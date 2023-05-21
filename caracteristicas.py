import matplotlib.pyplot as plt
import pandas as pd
from Ler_dados_raytracing_plots import maximum_flux, ler_dados_rt, forward_backward, raytrancing_parametros, read_parameters, pegue_os_parametros

from utils import config_labels, save


def trocando_eixo(ax):
    def rate(xx):
        if  xx >= 24:
            return str(int(xx - 24)) + ":00"
        else:
            return str(int(xx)) + ":00"
        
    
    ax.set(xticks = ax.get_xticks(), 
           xlabel = "Horas (UT)", 
           xlim = ax.get_xlim())
    
    ax.xaxis.set_major_formatter(lambda x, pos: rate(x))
    
    
def plot(ax, 
         df, 
         hora_inicial,
         date_sel,
         phase = "descendente",
         xcol = "altitude_(metros)",
         ycol = "latitude", 
         alt_emission = 97, color = "blue", 
         linestyle = "-", 
         name = "Vento HWM14"):    
    
    fo, ba = forward_backward(df,
                            hora_inicial, 
                            phase = phase)   
    
    
    args = dict(color = color, lw = 2, linestyle = linestyle)
    
    if xcol == "time":
    
        ax.plot(fo[ycol], **args, label = name)
        ax.plot(ba[ycol], **args)
        ax.plot(hora_inicial, alt_emission, "^", 
                markersize = 15, 
                color = "purple")
        
    
        max_flux_time, max_flux_alt, flux_max, flux10_alt, flux10_time, flux10Menor = maximum_flux(df, phase)
      
        args_sq = dict(marker = "s", color = color, markersize =10)
    
    
        ax.plot(hora_inicial + max_flux_time, max_flux_alt, **args_sq)
        ax.plot(hora_inicial + flux10_time, flux10_alt, fillstyle = "none", **args_sq)
        trocando_eixo(ax)
        ax.legend()
    else:
        ax.plot(fo[xcol], fo[ycol], **args, label = name)
        ax.plot(ba[xcol], ba[ycol], **args)
        
        ax.legend()
        
    
    return ax


def plot_caracteristicas(axs, 
                         df, 
                         hora_inicial, 
                         date_sel, 
                         altitude, 
                         phase = "descendente", 
                         color = "blue", 
                         linestyle = "-", 
                         name = "Vento HWM14"):

    
   
    combinations = [("altitude_(metros)", "time"), 
                    ("altitude_(metros)", "longitude"), 
                    ("latitude", "altitude_(metros)")]
    
    labels = [("Altitude (km)", "Horas (UT)", "both"), 
             ("Altitude (km)", "Longitude (°)", "x"), 
             ("Latitude (°)", "Altitude (km)", "y")]
    
    letters = ["(a)", "(b)", "(c)"]
    
    for num, ax in enumerate(axs.flat):
        
        ycol, xcol = combinations[num]
        
        
        ylabel, xlabel, grid = labels[num]
        
        ax.text(0., 1.1, 
                letters[num], 
                transform = ax.transAxes)
        
        ax.set(ylabel = ylabel, 
               xlabel = xlabel)
        
        args = dict(color = 'gray', 
                    linestyle = '--', 
                    linewidth = 0.5)
        ax.grid(axis=grid, **args) 
        
        ax = plot(ax, 
                 df, 
                 hora_inicial,
                 date_sel,
                 xcol = xcol,
                 ycol = ycol, 
                 phase = phase,
                 alt_emission = altitude, 
                 color = color, 
                 linestyle = linestyle, 
                 name = name)
            
                
def plot_lat_lon_tempo(parameters, dados, num, phase):
    
     hora_inicial, altitude, date_sel = tuple(parameters[num])    
     colors = ["blue", "red"]
     styles = ["-", "--"]
     names = ["Vento HWM14", "sem vento"]
     
     parametros = read_parameters(phase, date_sel)
     emission, lambdaH, lambdaV, periodo, vel_fase, propagacao =  pegue_os_parametros(parametros)
     
     infos = f"$\lambda_H = ${lambdaH} km, $\\tau = $ {periodo} min, $c_H = $ {vel_fase} m/s, $\phi = $ {propagacao}°"
     com_vento, sem_vento = dados[num]
     
                
     fig, axs = plt.subplots(figsize = (12, 10), 
                             nrows = 3)
     
     axs[0].text(0.2, 1.1, infos, transform = axs[0].transAxes)
     # altitude = 87
     axs[0].axhline(altitude, color = "k", lw = 1, 
                label = f"Alt. de emissão {altitude} km")
 
     plt.subplots_adjust(hspace = 0.4)
 
         
     for i, df in enumerate(dados[num]):
         plot_caracteristicas(axs, 
                              df, 
                              hora_inicial, 
                              date_sel, 
                              altitude, 
                              phase = phase, 
                              color = colors[i], 
                              linestyle = styles[i], 
                              name = names[i])
         
     path_to_save = f"C:\\Users\\Ander\\OneDrive\\Documentos\\ANDERSON\\a_Programas_raytracing\\{phase}"
     path = "C:\\Users\\Ander\\OneDrive\\Documentos\\ANDERSON\\a_Programas_raytracing\\figures\\"
     FigureName = f"{phase}_{date_sel.strftime('%Y_%m_%d')}.pdf"
     print(FigureName)
     #save(fig, path_to_save, FigureName)
     
     fig.savefig(path + FigureName, dpi = 500)
     
     
def all_plots(phase = "descendente"):
        
    parameters, dados = raytrancing_parametros(phase, start = None, end = None)
    
    for num in range(len(dados)):
        try:
            plot_lat_lon_tempo(parameters, dados, num, phase)
        except:
            continue
       
def run():
    for na in ["descendente", "ascendente"]:
        all_plots(phase = na)
phase = "descendente"
parameters, dados = raytrancing_parametros(phase, start = None, end = None)

num = 0

plot_lat_lon_tempo(parameters, dados, num, phase)
all_plots(phase = "ascendente")