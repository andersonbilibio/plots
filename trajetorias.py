import matplotlib.pyplot as plt
from maps import mapping
import cartopy.crs as ccrs

from Ler_dados_raytracing_plots import maximum_flux, ler_dados_rt, forward_backward, raytrancing_parametros
from utils import circle_with_legend, config_labels, save

def float_time(hora, string = True):
    import math
    
    frac, whole = math.modf(hora)
    
    minutes = int(frac * 60)
    
    hour = int(whole)

    if string:
        if hour >=24: 
            hour -= 24
            hour = f"0{hour}"
        
        if minutes < 10:
            minutes = f"0{minutes}"
        
        return  f" {hour}:{minutes} (UT)"
    else:
        if hour >=24: 
            hour -= 24
        return hour, minutes




def plotTrajetorias(parameters, dados, phase):
    fig, ax = mapping()
    
    colors = ["blue", "red"][::-1]
    styles = ["-", "--"][::-1]
    names = ["Vento HWM14", "sem vento"][::-1]
    
    circle_with_legend(ax, [0], scale = 110)
    
    
    hora, _, date = tuple(parameters)
    
    
    ax.text(0., 1.03, "(d)", transform = ax.transAxes)
    time = float_time(hora)
    
    date_str = date.strftime("%d/%m/%Y") + time
    
    FigureName = f"{phase}_{date.strftime('%d_%m_%Y')}_mapa.png"
    
    
    
    flux_col = 'fluxo_momento_medio'
    
    for i, df in enumerate(dados[::-1]):
        
        lat = df["latitude"].values
        
        lon = df["longitude"].values
        
        ax.plot(lon,  
                 lat, 
                 color = colors[i] , 
                 linestyle = styles[i], 
                 label = names[i],
                 transform = ccrs.PlateCarree())     
        
        max_flux_time, max_flux_alt, flux_max, flux10_alt, flux10_time, flux10Menor = maximum_flux(df, phase)
        
        
        
        latMax, lonMax = tuple(df.loc[df[flux_col] == flux_max, 
                                      ["latitude", "longitude"]].values[0])
        lat10, lon10 = tuple(df.loc[df[flux_col] == flux10Menor, 
                                    ["latitude", "longitude"]].values[0])
    
        ax.plot(lonMax, latMax,  
                marker = "s", 
                color = colors[i],
                transform=ccrs.PlateCarree(), 
                label = "FMM")
        
        ax.plot(lon10, lat10,  
                marker = "s", 
                color = colors[i], 
                fillstyle = "none",
                transform=ccrs.PlateCarree(), 
                label = "10% do FM")
        
        print(date_str)
        
        ax.set(title = f"{phase.title()}: {date_str}")
     
        #if phase == "descendente":
        
           # ax.plot(lon[-1], lat[-1], "o", color = colors[i], label = "")
        #else:
           # ax.plot(lon[0], lat[0], "o", color = colors[i])
        
        ax.legend(loc = "lower right")
        
    return FigureName, fig

# for i in range(len(dado)):
    
#     parameters = parame[i]
#     dados = dado[i]
    
#     try:
#      FigureName, fig = plotTrajetorias(parameters, dados, phase)
#      save(fig, path, FigureName)
#     except:
#         continue
    
    
phase = "ascendente"
parame, dado = raytrancing_parametros(phase, start = None, end = None)
path = f"C:\\Users\\Ander\\OneDrive\\Documentos\\ANDERSON\\a_Programas_raytracing\\{phase}"
i = 0
parameters = parame[i]
dados = dado[i]

hora, _, date = tuple(parameters)


import datetime as dt

def date_time(date, hora):
    time = float_time(hora, string = False)

    return date + dt.timedelta(hours = time[0], 
                              minutes = time[1])


# print(date_time(date, hora)) 

    