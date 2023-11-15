# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 13:35:36 2023

@author: Heitor Nunes Rosa
@gmail: heitornunes12@gmail.com
@github: @hnrosa
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib as mpl

mpl.rcParams.update(mpl.rcParamsDefault)

custom_params = {
    'lines.linestyle': '-',
    #'lines.markersize': 0,
    'font.family': 'sans-serif',
    'xtick.labelsize': 15,
    'ytick.labelsize': 12,
    'grid.linestyle': '--',
    'grid.color': '#CCCCCC',
    'figure.titlesize': 21,
    'legend.fontsize': 15,
    'axes.labelsize': 15,
    'axes.titlesize':20
}

mpl.rcParams.update(custom_params)


df1 = pd.read_csv('../../data/processed/data.csv')
df2 = pd.read_csv('../../data/processed/propeller.csv')

df2 = df2.drop(columns = ['r/R', 'c/R', 'beta'], axis = 1).drop_duplicates()

# %%
columns = ['D', 'P', 'P_D', 'Solidity', 
           'eta_max', 'eta_Jmax',
           'ct_max', 'ct_Jmax',
           'cp_max', 'cp_Jmax']

fig, ax = plt.subplots(2, 2, figsize = (12, 6))
for i, c in enumerate(columns[:4]):
    sns.histplot(data = df2, x = c, ax = ax[i//2, i%2])
        
fig.tight_layout()
    
fig, ax = plt.subplots(3, 2, figsize = (12, 6))
for i, c in enumerate(columns[4:]):
    sns.histplot(data = df2, x = c, ax = ax[i//2, i%2])
    
    
fig.suptitle('Performance characteristics distributions', size = 18)
fig.tight_layout()
plt.savefig('images/hist_performance.png', dpi = 300)
plt.show()

columns.remove('ct_Jmax')
columns.remove('cp_Jmax')

# %%

print(df2['Blade'].value_counts().to_markdown())

fams = df2.loc[df2['Blade'] > 2, 'Family'].drop_duplicates()

df_blades = df2.loc[df2['Family'].isin(fams), :]

fig, ax = plt.subplots(2, 2, dpi = 300, figsize = (16, 7))
fig.suptitle('Performance Comparison between Propellers with different Number of Blades', size = 22)
sns.boxplot(data = df_blades, x = 'Family', y = 'eta_max', hue = 'Blade', ax = ax[0, 0]);
sns.boxplot(data = df_blades, x = 'Family', y = 'eta_Jmax', hue = 'Blade', ax = ax[0, 1]);
sns.boxplot(data = df_blades, x = 'Family', y = 'cp_max', hue = 'Blade', ax = ax[1, 0]);
sns.boxplot(data = df_blades, x = 'Family', y = 'ct_max', hue = 'Blade', ax = ax[1, 1]);

fig.tight_layout()
plt.savefig('images/boxplot_performance.png', dpi = 300)
plt.show()


# %%
ind2 = df2.query('Blade > 2').index
ind1 = df1.query('Blade > 2').index

df2 = df2.drop(ind2)
df1 = df1.drop(ind1)


# %% Solidez

fig, ax = plt.subplots(2, 2, figsize = (12, 6))
for i, c in enumerate(columns[4:]):
    sns.scatterplot(data = df2, x = 'Solidity', y = c, ax = ax[i%2, i//2])
    
fig.suptitle('Performance Relationships with Solidity')
fig.tight_layout()
plt.savefig('images/scatter_01.png')
plt.show()


fig, ax = plt.subplots(2, 2, figsize = (12, 6))
for i, c in enumerate(columns[4:]):
    sns.scatterplot(data = df2, x = 'P_D', y = c, ax = ax[i%2, i//2])
    
fig.suptitle('Performance Relationships with Pitch per Diameter')
fig.tight_layout()
plt.savefig('images/scatter_02.png')
plt.show()


# %%

feats = ['cp_max', 'ct_max', 'eta_max', 'eta_Jmax']

values = df2.groupby('Family').mean(
        numeric_only = True).loc[:, feats].reset_index()

fig, axes = plt.subplots(2, 2, figsize = (18, 8), dpi = 300)
for i, f in enumerate(feats):
    order = values.sort_values(by = f, ascending = False)['Family']
    sns.boxplot(data = df2, x = 'Family', y = f,
                ax = axes[i//2, i%2], order = order, palette = 'inferno')
    
    for tick in  axes[i//2, i%2].get_xticklabels():
        tick.set_rotation(60)
        
fig.suptitle('Performance Characteristics per Family')       
fig.tight_layout()
plt.savefig('images/boxplot_performance01.png')
plt.show()

# %%

fig, axes = plt.subplots(2, 2, figsize = (12, 6), dpi = 300)
for i, f in enumerate(feats):
    df_aux = df2.sort_values(by = f, ascending = False).iloc[:15, :]
    order = df_aux['PropName']
    sns.barplot(data = df2, y = 'PropName', x = f, orient = 'h',
                ax = axes[i//2, i%2], order = order, palette = 'inferno')
    
    for tick in  axes[i//2, i%2].get_xticklabels():
        tick.set_rotation(60)
        
fig.tight_layout()
plt.savefig('boxplot_best_props.png')
plt.show()

# %%

families = df1['Family'].unique()


for fam in families:
    df_aux = df1.query(f'Family.str.contains("{fam}")')
    
    fig, ax = plt.subplots(1, 3, figsize = (15, 6))
    
    fig.suptitle(f'{fam} Performance')
    sns.scatterplot(data = df_aux, x = 'J', y = 'CT',
                    hue = 'P_D', ax = ax[0])
    sns.scatterplot(data = df_aux, x = 'J', y = 'CP',
                    hue = 'P_D', ax = ax[1])
    sns.scatterplot(data = df_aux, x = 'J', y = 'eta',
                    hue = 'P_D', ax = ax[2])
    
    fig.tight_layout()
    plt.savefig(f'ct_cp_eta_plots/{fam}_ct_cp_eta.png', dpi = 300)
    print(f'{fam} Concluído.')
    plt.close()



# %%

df_aux = df1.query('J == 0')

for fam in families:
    df_aux_ = df_aux.query(f'Family.str.contains("{fam}")')
    
    fig, ax = plt.subplots(1, 2, figsize = (15, 6))
    
    fig.suptitle(f'{fam} Static Performance')
    sns.scatterplot(data = df_aux_, x = 'N', y = 'CT',
                    hue = 'P_D', ax = ax[0])
    sns.scatterplot(data = df_aux_, x = 'N', y = 'CP',
                    hue = 'P_D', ax = ax[1])
    
    fig.tight_layout()
    plt.savefig(f'j0_ct_cp_plots/{fam}_j0_ct_cp.png', dpi = 300)
    print(f'{fam} Concluído.')
    plt.close()
    
# %%

df_aux = df1.query('J == 0')

fig, ax = plt.subplots(1, 2, figsize = (15, 6))
sns.scatterplot(data = df_aux, x = 'Solidity', y = 'CP', hue = 'P_D', ax = ax[0]);
sns.scatterplot(data = df_aux, x = 'Solidity', y = 'CT', hue = 'P_D', ax = ax[1]);






 
