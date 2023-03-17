import pandas as pd
import os
import datetime as dt

def load(infile):
    
    """
    colunas:
        Raytrancing Type: 0-back, 1-reflexao, 2-for
    
    """
    
    names = ['time', 'dtime', 'x', 'y','z', 
             'kx', 'ky', 'kz', 'nan',
             'cgx', 'cgy', 'cgz', 'fmm', 
             'rho', 'rt_type', 'lat', 'lon',
             'omega_i', 'amp_hor', 'amp_zon',
             'amp_mer','amp_ver', 'RATE_W_U', 
             'amp_temp','amp_den', 'omega_r']
    
    return pd.read_csv(infile, header = None, names = names)

def sep_for_and_back(df, phase = "ascendente"):
    columns = ["time", "fmm", "z", "lat", 
               "lon", "rt_type"]
    index_zero = get_obs_time(df)
    
    if phase == "descendente":
        
        forward  = df.loc[df["time"] < index_zero, columns]
        backward  = df.loc[df["time"] > index_zero, columns]
        
    else:
        
        forward  = df.loc[df["time"] > index_zero, columns]
        backward  = df.loc[df["time"] < index_zero, columns]
    

    return forward, backward

def fname_to_date(filename):
    date = filename.split("_")[-2]
    return dt.datetime.strptime(date, "%Y%m%d")

def float_to_time(time):        
    import math
    frac, whole = math.modf(time)
    minute = int(frac * 60)
    hour = int(whole)
    if hour >=24: hour -= 24
    return hour, minute

def get_obs_time(df):
    """
    Pegue o horario e parametros da observação
    Parameters
    """
    return df.loc[df["time"] == 0].index.item()

def load_parameters(filename, phase = "ascendente"):
    
    infile = f"database/parametros/phase_{phase}.xlsx"
    ts = pd.read_excel(infile)            
    return ts.loc[(ts["Data"] == fname_to_date(filename))]

class get_obs_datetime:
    
    """
    Get datetime from filename (date) after 
    filtered results data
    """

    def __init__(self, ts, filename):
    
        ems = ts["Emiss"].item().strip()
        
        sel_ts = ts[[f"Hi{ems[:2]}", 
                     f"Hi{ems[3:]}"]
                    ].min(axis = 1)
                
        self.date = fname_to_date(filename)
        
        self.obs_time = sel_ts.item()
        
        hour, minute = float_to_time(self.obs_time)
        
        self.obs_datetime = self.date + dt.timedelta(
            hours = hour, 
            minutes = minute
            )
        
    def get_float(self, time):
        return (self.obs_time + time / 3600)
    
    def convert_dt(self, time):
        hour, minute = float_to_time(time)
        return self.date + dt.timedelta(
            hours = hour, minutes = minute
            )
    
    def delta_fmm(self, time):
        tfmm = self.get_float(time)
        if tfmm < self.obs_time:   
            return self.obs_datetime - self.convert_dt(tfmm)
        else:
            return self.convert_dt(tfmm) - self.obs_datetime
        
        

def flux_max(df):
    """Get momentum flux maximum"""
    return df["fmm"].max()

def flux_10max(df):
    """Get 10% of momentum flux maximum"""
    fmax = flux_max(df)
    return fmax - (fmax * 0.1)

def get_fmm(df):
    """Get altitude and time from momentum flux maximum"""
    item = df.loc[(df["fmm"] == flux_max(df)), ["z", "time", "fmm"]]
    return tuple(item.itertuples(
        index = False, name = None))[0]


def get_10fmm(df, phase = "ascendente"):
    """Get altitude, time and 10% of momentum flux maximum"""
    fmm_alt, fmm_time, fmm = get_fmm(df)
    
    columns = ["z", "time", "fmm"]
    
    if phase == "descendente":
    
        fmm10 = df.loc[(df["z"] >  fmm_alt) & 
                       (df["time"] > fmm_time) & 
                       (df["fmm"] < flux_10max(df))]   
    else:
        fmm10 =  df.loc[(df["z"] < fmm_alt) & 
                        (df["time"] > fmm_time) & 
                        (df["fmm"] < flux_10max(df))]  
     
    last = fmm10[-1:][columns]
    
    return  tuple(last.itertuples(
        index = False, name = None))[0]   

def get_final_position(df, phase = "ascendente"):

    forward, backward = sep_for_and_back(df, phase = phase)
    
    if phase == "ascendente":
        
        first = forward[:1][["time", "z"]]
        
        time, alt = tuple(first.itertuples(
                index = False, name = None))[0]   
        
        t = obs.get_float(time)
        
        return alt /1000, obs.convert_dt(t) - obs.obs_datetime
        
        
    else:
        first = backward[-1:][["time", "z"]]
        
        time, alt = tuple(first.itertuples(
                index = False, name = None))[0]   
        
        t = obs.get_float(time)
        
        return alt / 1000, obs.obs_datetime - obs.convert_dt(t) 
    


infile = "database/vento/"

files = os.listdir(infile)

filename = files[0]

phase = "ascendente"


df = load(infile + filename)
ts = load_parameters(filename, phase = phase)

obs = get_obs_datetime(ts, filename)
alt, time, fmm = get_fmm(df)

delta_fmm = obs.delta_fmm(time)

alt, dtime = get_final_position(df, phase= phase)




