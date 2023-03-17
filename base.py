import pandas as pd
import os
import datetime as dt

def load(infile):
    
    names = ['time', 'dtime', 'x', 'y','z', 
             'kx', 'ky', 'kz', 'nan',
             'cgx', 'cgy', 'cgz', 'fmm', 
             'rho', 'rt_type', 'lat', 'lon',
             'omega_i', 'amp_hor', 'amp_zon',
             'amp_mer','amp_ver', 'RATE_W_U', 
             'amp_temp','amp_den', 'omega_r']
    
    return pd.read_csv(infile, header = None, names = names)

def fname_to_datetime(filename):
    date = filename.split("_")[-2]
    return dt.datetime.strptime(date, "%Y%m%d")


infile = "database/vento/"

files = os.listdir(infile)

filename = "_RT_model_wind_20001118_00.csv"

df = load(infile + filename)



print(df)