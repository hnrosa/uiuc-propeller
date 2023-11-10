# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 14:14:34 2023

@author: Heitor Nunes Rosa
@gmail: heitornunes12@gmail.com
@github: @hnrosa
"""

# %% Importando Bibliotecas

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import parse
import os

# %% Definindo Caminhos

raw_dir =  '../../data/raw'
interim_dir = '../../data/interim'

vol_dirs = ['vol1', 'vol2', 'vol3', 'vol4']

# %% Trabalhando com arquivos

# TriTurbo 2.55 x 2.2
# U-80 3.15 x 1.96

def template_maker(file):
    
    if 'static' in file:
        
        
        if '3b' in file or '4b' in file:
            
            if 'deg' in file:
                
                template = '{family}_{diameter:g}_{pitch:g}deg_{blade:d}b_{trash}.txt'
            
            else:
            
                template = '{family}_{diameter:g}x{pitch:g}_{blade:d}b_{trash}.txt'
        
        else:
            
            if 'deg' in file:
                
                template = '{family}_{diameter:g}_{pitch:g}deg_{trash}.txt'
                
            elif 'triturbo' in file:
                
                template = '{family}_triturbo_static_{trash}.txt'
                
            elif 'union' in file:
                
                template = '{family}_u80_static_{trash}.txt'
            
            else:
                
                template = '{family}_{diameter:g}x{pitch:g}_{trash}.txt'
        
    
    elif 'geom' in file:
        
        cond1 = 'da4002' in file 
        cond2 = 'da4022' in file 
        cond3 = 'da4052' in file
        cond4 = 'triturbo' in file
        cond5 = 'union' in file
        cond6 = 'nr640' in file
        cond7 = 'deg' in file
        cond8 = 'x' in file[:-3]
        
        cond = cond1 + cond2 + cond3 + cond4 + cond5 + cond6
        
        if '3b' in file or '4b' in file:
            
            template = '{family}_{diameter:g}x{pitch:g}_{blade:d}b_{trash}.txt'
        
        else:
            template = '{family}_{diameter:g}x{pitch:g}_{trash}.txt'
            
        if cond and (not cond7 and not cond8):
            template = '{family}_{trash}.txt'
        
        elif cond and cond7:
            template = '{family}_{diameter:g}_{pitch:g}deg_{trash}.txt'
        
    
    else:
        
        if '3b' in file or '4b' in file:
            
            if 'deg' in file:
                
                template = '{family}_{diameter:g}_{pitch:g}deg_{blade:d}b_{trash}_{rotation:d}.txt'
            
            else:
            
                template = '{family}_{diameter:g}x{pitch:g}_{blade:d}b_{trash}_{rotation:d}.txt'
            
        
        else:
            
            if 'deg' in file:
                
                template = '{family}_{diameter:g}_{pitch:g}deg_{trash}_{rotation:d}.txt'
            
            elif 'triturbo' in file:
                
                template = '{family}_triturbo_{trash}_{rotation:g}.txt'
                
            elif 'union' in file:
                
                template = '{family}_u80_{trash}_{rotation:g}.txt'
            
            else:
            
                template = '{family}_{diameter:g}x{pitch:g}_{trash}_{rotation:d}.txt'
            
    return template
        
def merger(vol):

    path = os.path.join(raw_dir, vol)

    df_dym = pd.DataFrame()
    df_geo = pd.DataFrame()
    df_sta = pd.DataFrame()
    
    lst = os.listdir(path)

    for i, file in enumerate(lst):
        
        template = template_maker(file)
        
        if 'cfnq' in file or 'thick' in file:
            continue

        if 'static' in file:
            
            path_file = os.path.join(path, file)
            prop_info = parse.parse(template, file)
            
            # if prop_info is None:
            #    print(file, template)
            #   continue
            
            prop_info = prop_info.named
            
            if 'triturbo' in file:
                
                prop_info['diameter'] = 2.55
                prop_info['pitch'] = 2.2
                
            if 'union' in file:
                
                prop_info['diameter'] = 3.15
                prop_info['pitch'] = 1.96
            
            if 'blade' not in prop_info:
                prop_info['blade'] = 2
                
            if 'deg' in file:
                tan = np.tan(np.deg2rad(prop_info['pitch']))
                prop_info['pitch'] = np.pi * 0.75 * prop_info['diameter'] * tan
            
            fam = prop_info['family']
            D = prop_info['diameter']
            P = prop_info['pitch']
            B = prop_info['blade']

            df_aux = pd.read_csv(path_file, delim_whitespace=True)
            df_aux['D'] = D
            df_aux['P'] = P
            df_aux['Family'] = fam
            df_aux['Blade'] = B
            df_aux['PropName'] = f'{fam}-{D:.2f}x{P:.2f}-B{B}'
            
            df_aux = df_aux.rename(columns = {'RPM': 'N'})

            df_sta = pd.concat([df_sta, df_aux], axis=0, ignore_index = True)

        elif 'geom' in file:
            
            
            path_file = os.path.join(path, file)
            prop_info = parse.parse(template, file)
            
         #   if prop_info is None:
         #       print(file)
         #       continue
            
            prop_info = prop_info.named
            
            if 'blade' not in prop_info:
                prop_info['blade'] = 2
                
            if 'deg' in template:
                tan = np.tan(np.deg2rad(prop_info['pitch']))
                prop_info['pitch'] = np.pi * 0.75 * prop_info['diameter'] * tan
                
                
            if 'diameter' not in prop_info:
                prop_info['diameter'] = np.nan 
                prop_info['pitch'] = np.nan
                prop_info['blade'] = np.nan
                
                
            fam = prop_info['family']
            D = prop_info['diameter']
            P = prop_info['pitch']
            B = prop_info['blade']
            
            
            df_aux = pd.read_csv(path_file, delim_whitespace=True)
            df_aux['D'] = D
            df_aux['P'] = P
            df_aux['Family'] = fam
            df_aux['Blade'] = B
            df_aux['PropName'] = f'{fam}-{D:.2f}x{P:.2f}-B{B}'

            df_geo = pd.concat([df_geo, df_aux], axis=0, ignore_index = True)

        else:

            path_file = os.path.join(path, file)
            prop_info = parse.parse(template, file)
            
           # if prop_info is None:
           #     print(file)
           #     continue
            
            prop_info = prop_info.named
            
            if 'triturbo' in file:
                
                prop_info['diameter'] = 2.55
                prop_info['pitch'] = 2.2
                
            if 'union' in file:
                
                prop_info['diameter'] = 3.15
                prop_info['pitch'] = 1.96
            
            if 'blade' not in prop_info:
                prop_info['blade'] = 2
                
            if 'deg' in template:
                tan = np.tan(np.deg2rad(prop_info['pitch']))
                prop_info['pitch'] = np.pi * 0.75 * prop_info['diameter'] * tan
            
            fam = prop_info['family']
            D = prop_info['diameter']
            P = prop_info['pitch']
            N = prop_info['rotation']
            B = prop_info['blade']

            df_aux = pd.read_csv(path_file, delim_whitespace=True)
            df_aux['D'] = D
            df_aux['P'] = P
            df_aux['N'] = N
            df_aux['Family'] = fam
            df_aux['Blade'] = B
            df_aux['PropName'] = f'{fam}-{D:.2f}x{P:.2f}-B{B}'
            
            df_dym = pd.concat([df_dym, df_aux], axis=0, ignore_index=True)
        
        if i%10 == 0: print(f'{vol} Concluido: {i/len(lst) * 100:.2f}%')

    return df_dym, df_geo, df_sta

# %% Salvando arquivos

for vol in vol_dirs:
    df_dym, df_prop, df_static = merger(vol)
    dym_path = os.path.join(interim_dir, f'dynamic_{vol}.csv')
    prop_path = os.path.join(interim_dir, f'propeller_{vol}.csv')
    static_path = os.path.join(interim_dir, f'static_{vol}.csv')
    
    df_dym.to_csv(dym_path, index = False)
    df_prop.to_csv(prop_path, index = False)
    df_static.to_csv(static_path, index = False)
    