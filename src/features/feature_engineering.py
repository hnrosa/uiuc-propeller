# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 11:29:27 2023

@author: Heitor Nunes Rosa
@gmail: heitornunes12@gmail.com
@github: @hnrosa
"""

from scipy.integrate import trapezoid
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

data_dir =  '../../data/processed'
interim_dir = '../../data/interim'

def join(file, path = 'int'): 
    
    if path == 'int':
        path = interim_dir
    else:
        path = data_dir
        
    return os.path.join(path, file)

data = pd.read_csv(join('exp_data.csv'))
geom = pd.read_csv(join('full_prop_data.csv'))

def solidity_calc(df_aux):
    d = df_aux['D'].iat[0]
    b = df_aux['Blade'].iat[0]
    
    if df_aux.loc[:, 'c/R'].isnull().sum():
        
        sol = np.nan
        
    else:
        c = df_aux['c/R'].to_numpy() * d * 0.5
        r = df_aux['r/R'].to_numpy() * d * 0.5
        I = trapezoid(c, r)
        sol = 4 * b * I /(d ** 2 * np.pi)
    
    return sol

solidity = geom.groupby('PropName').apply(solidity_calc)

solidity = solidity.reset_index().rename(columns = {0: 'Solidity'})

# %%

data = data.merge(solidity, how = 'left', on = 'PropName')
geom = geom.merge(solidity, how = 'left', on = 'PropName')

plt.figure(dpi = 300)
sns.heatmap(data.isnull());

# %%

data['P_D'] = data['P'] / data['D']
geom['P_D'] = geom['P'] / geom['D']

# %%

def eta_Jmax(df_aux):
    
    idx = df_aux['eta'].idxmax()
    
    return df_aux.at[idx, 'J']

def cp_Jmax(df_aux):
    
    idx = df_aux['CP'].idxmax()
    
    return df_aux.at[idx, 'J']

def ct_Jmax(df_aux):
    
    idx = df_aux['CT'].idxmax()
    
    return df_aux.at[idx, 'J']

    
eta_max = data.groupby('PropName').agg(
    {'eta': 'max'}
   ).reset_index().rename(columns = {'eta': 'eta_max'})

ct_max = data.groupby('PropName').agg(
    {'CT': 'max'}
   ).reset_index().rename(columns = {'CT': 'ct_max'})

cp_max = data.groupby('PropName').agg(
    {'CP': 'max'}
   ).reset_index().rename(columns = {'CP': 'cp_max'})

eta_Jmax = data.groupby('PropName').apply(eta_Jmax
    ).reset_index().rename(columns = {0: 'eta_Jmax'})

ct_Jmax = data.groupby('PropName').apply(ct_Jmax
    ).reset_index().rename(columns = {0: 'ct_Jmax'})

cp_Jmax = data.groupby('PropName').apply(cp_Jmax
    ).reset_index().rename(columns = {0: 'cp_Jmax'})

geom = geom.merge(eta_max, how = 'left', on = 'PropName')
geom = geom.merge(eta_Jmax, how = 'left', on = 'PropName')
geom = geom.merge(ct_max, how = 'left', on = 'PropName')
geom = geom.merge(cp_max, how = 'left', on = 'PropName')
geom = geom.merge(ct_Jmax, how = 'left', on = 'PropName')
geom = geom.merge(cp_Jmax, how = 'left', on = 'PropName')

# %%


data.loc[data['PropName'] == 'gwsdd-2.50x0.80-B2', 'Solidity'] /= 3
geom.loc[geom['PropName'] == 'gwsdd-2.50x0.80-B2', 'Solidity'] /= 3


data.to_csv(join('data.csv', path = 'data'), index = False)
geom.to_csv(join('propeller.csv', path = 'data'), index = False)


#def average_eta(df_aux, cut):
    
#    df_aux = df_aux.sort_values(by = 'J').query(f'J > {cut[0]} and J < {cut[1]}')
    
#    eta = df_aux['eta'].to_numpy()
#    j = df_aux['J'].to_numpy()
    
#    if j.size:
        
#        I = trapezoid(eta, j)/(j[-1] - j[0])
    
#    else:
#        I = np.nan
        
#    return I

