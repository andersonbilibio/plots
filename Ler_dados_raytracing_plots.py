# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 16:00:02 2022

@author: Anderson
Ler dados Ray tracing e variaveis para plots
"""

#*---------------------------------------IMPORTA TODAS AS BIBLIOTECAS

import pandas as pd
import os
import datetime
import numpy as np


def data_do_nome(filename, formato = True):
    
    date = filename.split("_")[-2]
    
    date = datetime.datetime.strptime(date, "%Y%m%d")
    
    if formato:
        return date.strftime("%d/%m/%Y")
    else:
        return date

def ler_dados_rt(caminho_arquivo):
    names=['tempo_em_seg_desde_a_hora_inicial', 'delta_no_tempo', 'x_(metros)', 
           'y_(metros)','altitude_(metros)', 'kx', 'ky', 'kz', 'Not_a_Number',
           'cgx', 'cgy', 'cgz', 'fluxo_momento_medio', 'densidade_(g/m^3)',
           'tipo_do_RT_(0-back,1-reflexao,2-for)', 'latitude', 'longitude',
           'omega_imaginario', 'amplitude_do_vento_horizontal', 
           'amplitude_do_vento_zonal', 'amplitude_do_vento_meridional',
           'amplitude_do_vento_vertical', 'RATE_W_U', 'amplitude_temperatura',
           'amplitude_densidade', 'omega_real']


    df = pd.read_csv(caminho_arquivo, 
                 header = None, 
                 names = names)
    
    return df

def caminho(phase = "ascendente", vento = "vento"):
    """
    Crie o caminho dos resultados do ray tracing

    Parameters
    ----------
    phase : TYPE, optional
        DESCRIPTION. The default is "ascendente".
    vento : TYPE, optional
        DESCRIPTION. The default is "vento".

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    
    root = "C:\\Users\\Ander\\OneDrive\\Documentos\\ANDERSON\\a_Programas_raytracing\\"
    
    return os.path.join(root, phase, "rt")


def pegue_vento_e_zero(phase = "ascendente"):

    root = f"C:\\Users\\Ander\\OneDrive\\Documentos\\ANDERSON\\a_Programas_raytracing\\{phase}\\rt\\"
    
    
    _, folders, vento = next(os.walk(root + "vento\\"))
    
    _, folders, zero = next(os.walk(root + "zero\\"))
    
    out = []
    for u, z in zip(vento, zero):
        
        out.append(tuple((u, z)))
        
    return root, out

def create_nome(data, model, Type):
    return f"_RT_{model}_wind_{data}_{Type}.csv"

def pegue_os_parametros(parametros):
    
    emission = parametros["Emiss"].values[0]
    lambdaH =  parametros['λHm(km)'].values[0]
    lambdaV = parametros['λV(km)'].values[0]
    periodo =  parametros['τm(min)'].values[0]
    vel_fase =  parametros['CHm(m/s)'].values[0]
    direcao =  parametros['φm(°)'].values[0]
    direcaoCAL =  parametros['set(°)'].values[0]
    
    if direcaoCAL != direcaoCAL:
        propagacao = direcao
    else:
        propagacao = direcaoCAL
        
    return emission, lambdaH, lambdaV, periodo, vel_fase, propagacao


def check_camada(phase, 
                 camada):

    
    O5 = 96
    O2 = 94
    OH = 87
    c1, c2 = tuple(camada.strip().split("+"))
    if phase ==  "descendente": 
        
        emission = max([vars()[c2], vars()[c1]])
        
    elif phase == "ascendente":
        emission = min([vars()[c2], vars()[c1]])
    return emission




def read_parameters(phase, date_sel):
    resultados = f"C:\\Users\\Ander\\OneDrive\\Documentos\\ANDERSON\\a_Programas_raytracing\\{phase}\\parametros\\phase_{phase}.xlsx"
    
    df = pd.read_excel(resultados)
    return df.loc[df["Data"] == date_sel, :]

def raytrancing_parametros(phase, start = None, end = None):
    root, res = pegue_vento_e_zero(phase = phase)
    
    out  = []
    dados = []
    for i in range(len(res))[start:end]:
    
        vento, zero = res[i]
    
        caminho_vento = f"{root}vento\\{vento}"
        caminho_zero = f"{root}zero\\{zero}"
        
        
        date_sel = data_do_nome(vento, formato = False)
    
        parametros = read_parameters(phase, date_sel)
        
        emission, lambdaH, lambdaV, periodo, vel_fase, propagacao =  pegue_os_parametros(parametros)
        
    
        first = 'Hi' + emission[:2]
        second = 'Hi' + emission[3:]
        
        sel_minimum = parametros[[first.strip(), 
                                  second.strip()]].values
        
        hora_inicial  = np.nanmin(sel_minimum)
        altura = check_camada(phase, emission)
        
        out.append([hora_inicial, altura, date_sel])
        
        dados.append([ler_dados_rt(caminho_vento),
                      ler_dados_rt(caminho_zero)])
    return out, dados
  

def forward_backward(df, 
                     hora_inicial, 
                     phase = "descendente"):
    
    time_col = 'tempo_em_seg_desde_a_hora_inicial'
    alt_col = "altitude_(metros)"
   
    df[time_col] = df[time_col] / 3600
    
    index_zero = df.loc[df[time_col] == 0].index[0]
    
    if phase == "descendente":
    
        forward  = df[:index_zero]
        backward  = df[index_zero:]
        
    else:
   
        forward  = df[index_zero:]
        backward  = df[:index_zero]
        
        
    def sort_reindex(dat):
        pd.options.mode.chained_assignment = None 
        #dat = dat.sort_values(by = [time_col])
        dat.index = dat[time_col] + hora_inicial
        dat.index.name = "time"
        dat[alt_col] = dat[alt_col] / 1000
        return dat

        
    return sort_reindex(forward), sort_reindex(backward)


def maximum_flux(df, phase):
    
    time_col = 'tempo_em_seg_desde_a_hora_inicial'
    alt_col = "altitude_(metros)"
    flux_col = 'fluxo_momento_medio'
    
    flux_max = df[flux_col].max()
    
    flux_10 = flux_max - (flux_max * 0.1)
    getMaxFlux = df.loc[(df[flux_col] == flux_max), 
                 [alt_col, time_col]].values.ravel()
    
    max_flux_alt, max_flux_time = tuple(getMaxFlux)
    
    
    if phase == "descendente":
    
        getFlux10 =  df.loc[(df[alt_col] > max_flux_alt) &
                            (df[time_col] > max_flux_time) & 
                            (df[flux_col] < flux_10), 
                            [alt_col, time_col, flux_col]].values[-1].ravel()    
    else:
        getFlux10 =  df.loc[(df[alt_col] < max_flux_alt) &
                        (df[time_col] > max_flux_time) & 
                        (df[flux_col] < flux_10), 
                        [alt_col, time_col, flux_col]].values[-1].ravel()    
        
    
    flux10_alt, flux10_time, flux10Menor = tuple(getFlux10)
        
            
    return max_flux_time, max_flux_alt / 1000, flux_max, flux10_alt  / 1000, flux10_time, flux10Menor
    

def main():
    
    time_col = 'tempo_em_seg_desde_a_hora_inicial'
    alt_col = "altitude_(metros)"
    flux_col = 'fluxo_momento_medio'
    
    phase = "descendente"
    
    parameters, dados = raytrancing_parametros(phase, 
                                               start = None, 
                                               end = None)
    
    num = 0
    
    hora_inicial, altitude, date_sel = tuple(parameters[num])
    com_vento, sem_vento = dados[num]
    
    fordward, backward = forward_backward(com_vento,
                                          hora_inicial, 
                                          phase = phase)
    
        
main()