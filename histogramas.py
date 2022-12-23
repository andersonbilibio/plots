# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 14:52:08 2022

@author: Ander
"""
import pandas as pd
from Ler_dados_raytracing_plots import maximum_flux, ler_dados_rt, forward_backward, raytrancing_parametros


phase = "ascendente"
parame, dado = raytrancing_parametros(phase, start = None, end = None)  

out = []

for i in range(len(dado)):
    df = dado[i][0]
    
    hora_inicial, _, _ = tuple(parame[i])
    
    max_flux_time, max_flux_alt, flux_max, _, _, _ = maximum_flux(df, phase)
    hora = max_flux_time/3600 + hora_inicial
    out.append([hora, max_flux_alt, flux_max])
    

res = pd.DataFrame(out, columns = ["time", "alt", "fm"])

import matplotlib.pyplot as plt


for x in res.columns:
    for y in res.columns:
        if x == y:
            break
        else:
            fig, ax = plt.subplots(figsize =(5, 5))
            ax.plot(res[x], res[y], "o")
            ax.set(ylabel = y, xlabel = x)