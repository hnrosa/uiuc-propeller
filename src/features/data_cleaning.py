# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 22:38:37 2023

@author: Heitor Nunes Rosa
@gmail: heitornunes12@gmail.com
@github: @hnrosa
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

interim_dir = '../../data/interim'
    
def join(file): return os.path.join(interim_dir, file)

df1_dym = pd.read_csv(join('dynamic_vol1.csv'))
df2_dym = pd.read_csv(join('dynamic_vol2.csv'))
df3_dym = pd.read_csv(join('dynamic_vol3.csv'))
df4_dym = pd.read_csv(join('dynamic_vol4.csv'))

df1_sta = pd.read_csv(join('static_vol1.csv'))
df2_sta = pd.read_csv(join('static_vol2.csv'))
df3_sta = pd.read_csv(join('static_vol3.csv'))
df4_sta = pd.read_csv(join('static_vol4.csv'))

df1_prop = pd.read_csv(join('propeller_vol1.csv'))
df2_prop = pd.read_csv(join('propeller_vol2.csv'))

df1_sta['eta'] = 0
df1_sta['J'] = 0
df2_sta['eta'] = 0
df2_sta['J'] = 0
df3_sta['eta'] = 0
df3_sta['J'] = 0
df4_sta['eta'] = 0
df4_sta['J'] = 0

df = pd.concat([df1_dym, df2_dym, df3_dym, df4_dym,
           df1_sta, df2_sta, df3_sta, df4_sta], ignore_index= True)

df_prop = pd.concat([df1_prop, df2_prop], ignore_index = True)


# %%
plt.figure(dpi = 300)
sns.histplot(data = df, x = 'D', binwidth = 2) 

print(df.query('D > 25')['PropName'].drop_duplicates())
print(df_prop.query('D > 25')['PropName'].drop_duplicates())

mask1 = df['D'] > 25
mask2 = df['Family'] != 'ancf'
mask3 = df['P'] > 70

mask1_ = df_prop['D'] > 25
mask2_ = df_prop['Family'] != 'ancf'
mask3_ = df_prop['P'] > 70

df.loc[(mask1) & (mask2), 'D'] = df.loc[(mask1) & (mask2), 'D'] / 25.4 
df.loc[(mask1) & (~mask2), 'D'] = df.loc[(mask1) & (~mask2), 'D'] / 10 

df.loc[(mask1) & (mask2), 'P'] = df.loc[(mask1) & (mask2), 'P'] / 25.4 
df.loc[(mask3) & (~mask2), 'P'] = df.loc[(mask3) & (~mask2), 'P'] / 10

df_prop.loc[(mask1_) & (mask2_), 'D'] = df_prop.loc[(mask1_) & (mask2_), 'D'] / 25.4 
df_prop.loc[(mask1_) & (~mask2_), 'D'] = df_prop.loc[(mask1_) & (~mask2_), 'D'] / 10 

df_prop.loc[(mask1_) & (mask2_), 'P'] = df_prop.loc[(mask1_) & (mask2_), 'P'] / 25.4 
df_prop.loc[(mask3_) & (~mask2_), 'P'] = df_prop.loc[(mask3_) & (~mask2_), 'P'] / 10

#df_prop.loc[(mask1) & (mask2) & (mask3), 'D'] = df_prop.loc[(mask1) & (mask2) & (mask3), 'D'] / 10
#df_prop.loc[(mask1) & (mask2) & (mask3), 'D'] = df_prop.loc[(mask1) & (mask2) & (mask3), 'D'] / 10


# %%

plt.figure(dpi = 300)
sns.histplot(data = df, x = 'P', binwidth = 2) 

print(df.query('P > 17')['PropName'].drop_duplicates())
print(df_prop.query('P > 17')['PropName'].drop_duplicates())

# %%
mask1 = df['P'] > 17 

df.loc[mask1, 'P'] = df.loc[mask1, 'P'] / 10 


#%%

plt.figure(dpi = 300)
sns.histplot(data = df, x = 'N')

print(df.query('N > 14900')['PropName'].drop_duplicates())

#%%

df_lst = df['PropName'].unique()
df_prop_lst = df_prop['PropName'].unique()

mask1 = ~df_prop['PropName'].isin(df_lst)
print(df_prop.loc[mask1, 'PropName'].drop_duplicates())

#%%

def diff_propellers(fam):
    
    df_lst = set(df_prop.loc[df_prop['Family'] == fam, 'PropName'].unique())
    df_prop_lst = set(df.loc[df['Family'] == fam, 'PropName'].unique())
    
    #print(df_lst)
    #print(df_prop_lst)
    
    return df_prop_lst.difference(df_lst)

#%%

props = ['da4002-nanxnan-Bnan', 'da4022-nanxnan-Bnan', 'da4052-nanxnan-Bnan'
 'nr640-nanxnan-Bnan', 'pl-nanxnan-Bnan']

fams = ['da4002', 'da4022', 'da4052', 'nr640', 'pl', 'union']

for p, fam in zip(props, fams):
    df_aux = df_prop.loc[df_prop['PropName'] == p, :]
    prop_lst = diff_propellers(fam)
    
    for prop in prop_lst:
        dic_info = df.loc[df['PropName'] == prop,
                          ['PropName', 'P', 'D', 'Blade']].drop_duplicates(
                              )
        
        df_aux.loc[:, 'P'] = dic_info['P'].iat[0]
        df_aux.loc[:,'D'] = dic_info['D'].iat[0]
        df_aux.loc[:,'Blade'] = dic_info['Blade'].iat[0]
        df_aux.loc[:,'PropName'] = dic_info['PropName'].iat[0]
        
        
        df_prop = pd.concat([df_prop, df_aux], ignore_index=True)
        
df_prop.loc[df_prop['Family'] == 'union', 'P'] = 1.96
df_prop.loc[df_prop['Family'] == 'union', 'D'] = 3.15
df_prop.loc[df_prop['Family'] == 'union', 'Blade'] = 2
df_prop.loc[df_prop['Family'] == 'union', 'PropName'] = 'union-3.15x1.96-B2'


#%%

df_prop = df_prop.dropna()

#%%

propnames = df_prop['PropName'].unique()

prop_miss = df.loc[~df['PropName'].isin(propnames), 
             ['P', 'D', 'Blade', 'PropName', 'Family']].drop_duplicates()

df_prop = pd.concat([df_prop, prop_miss])

df.loc[df['PropName'] == 'gwsdd-2.50x0.80-B2', 'Solidity'] /= 3
df_prop.loc[df_prop['PropName'] == 'gwsdd-2.50x0.80-B2', 'Solidity'] /= 3

columns.remove('ct_Jmax')
columns.remove('cp_Jmax')

# %% 

df.to_csv(join('exp_data.csv'), index = False)
df_prop.to_csv(join('full_prop_data.csv'), index = False)





