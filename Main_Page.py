# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 00:19:26 2023

@author: Heitor Nunes Rosa
@gmail: heitornunes12@gmail.com
@github: @hnrosa
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import pandas as pd
import numpy as np
import streamlit as st
from SurrogateProp import SurrogateProp

mpl.rcParams.update(mpl.rcParamsDefault)

custom_params = {
    'lines.linestyle': '-',
    'lines.markersize': 0,
    'font.family': 'sans-serif',
    'xtick.labelsize': 15,
    'ytick.labelsize': 15,
    'grid.linestyle': '--',
    'grid.color': '#CCCCCC',
    'figure.titlesize': 21,
    'legend.fontsize': 13,
    'axes.labelsize': 15,
    'axes.titlesize':20
}

mpl.rcParams.update(custom_params)

def convert_df(df):
    return df.to_csv(index = False).encode('utf-8')

family_names = {
'Aeronautic Carbon Eletric' : 'ancf',
'APC Carbon Fiber' : 'apccf',
'APC Slow Flyer': 'apcsf',
'APC Sport' : 'apcsp',
'APC Thin Electric' : 'apce',
'APC 29 Free Flight' : 'apc29ff',
'APC Free Flight' : 'apcff',
'DA4002' : 'da4002',
'DA4022' : 'da4022',
'DA4052' : 'da4052',
'E-Flite' : 'ef',
'Graupner CAM Prop' : 'grcp',
'Graupner CAM Slim' : 'grcsp',
'Graupner Super Nylon' : 'grsn',
'GWS Direct-Drive' : 'gwsdd',
'GWS Slow Flyer' : 'gwssf',
'Kavon FK' : 'kavfk',
'KP Folding' : 'kpf',
'Kyosho' : 'kyosho',
'Master Airscrew' : 'ma',
'Master Airscrew Eletric' : 'mae',
'Master Airscrew G-F' : 'magf',
'Master Airscrew Scimitar' : 'mas',
'Micro Invent': 'mi',
'NR640' : 'nr640',
'Plantraco' : 'pl',
'Rev Up' : 'rusp',
'Union' : 'union',
'Vapor' : 'vp',
'Zingali' : 'zin',
 None: None,
}

lst_families = list(family_names.keys())

st.set_page_config(
    page_title="Main"
)

st.title('Two Blade Propeller Surrogate Model')
st.text('Propeller Performance Prediction using XGBoost Algorithm')
st.image('src/models/propeller_photo.png')

stacks = ['performance curves', 'disadvantages', 
          'surrogate models', 'optimal parameters',
          'making decisions']

intro = r'''
When designing a UAV, something that must be taken into consideration is its
propulsive system. Good predictions of its **performance curves** guarantee a robust
and reliable project. To achieve this, numerical and experimental methods can be
used. However, both have their **disadvantages**. Numerical methods require time,
are computationally expensive and need a defined geometry of the propeller to be
applied, in addition to a advanced knowledge of the designer. Experimental tests
require wind tunnels and calibrated equipment for the correct measurement of the
propellers. A third alternative is use **surrogate models**, which consist of compact
models to estimate complex results, based on experimental or/and simulation data.
Thus, the designer can quickly predict the performance of a propeller, choosing
**optimal parameters** for preliminary propeller design, or **making decisions** such as
purchase of commercial propellers based on parameters provided by the 
manufacturer.
        '''
        
st.markdown(intro, unsafe_allow_html=True)

st.header('Propeller Performance Charts')
    
family = None
solidity = None

with st.sidebar:
    V = st.slider(
        'Define Freestream Velocity [m/s]',
        0.0, 50.0, (0.0, 30.0))
    D = st.number_input(
        'Define Diameter [in.]', 3., 20., 12.,
        )
    P = st.number_input(
        'Define Pitch [in.]', 3., 20., 8., 
        )
    N = st.number_input(
        'Define Rotation [RPM]', 1000, 15000, 8000
        )
    rho = st.number_input(
        'Define Air Density [kg/m³]', 0.1, 10., 1.25
        )
    
    approach = st.selectbox('Select Approach: ', ['General', 'Family', 'Solidity'])
    
    if approach == 'Family':
        family = st.selectbox('Propeller Family', lst_families)
    
    elif approach == 'Solidity':
        solidity = st.number_input(
            'Define Solidity [adim.]',
            )
        
converter = 25.6 * 0.001 # inch to meters

title  = f'Propeller {D}x{P} Performance Charts, Family: {family}; Solidity: {solidity}'

D *= converter
P *= converter

V = np.linspace(V[0], V[1], 100)

fam = family_names[family]

prop = SurrogateProp(D, P, V, N, rho, solidity, fam)

adim_df, df = prop.to_dataframe()

Tr = prop.Tr
Pw = prop.Pw
eta = prop.eta

CT = prop.CT
CP = prop.CP
J = prop.J

tab1, tab2 = st.tabs(['Dimensional Values', 'Adimensional Values'])

with tab1:

    fig, ax = plt.subplots(3, 1, figsize = (11, 14), dpi = 300)
    #fig.suptitle(title)
    
    ax[0].set_title('Thrust Performance Curve')
    ax[0].plot(V, Tr[:, 0], ls = '--', color = 'b', lw = 2, label = 'Thrust Quantiles [0.05-0.95]')
    ax[0].plot(V, Tr[:, 1], color = 'b', lw = 3, label = 'Thrust Median')
    ax[0].plot(V, Tr[:, 2], ls = '--', color = 'b', lw = 2)
    ax[0].axhline(ls = '-', color = 'k')
    ax[0].fill_between(V, Tr[:, 2], Tr[:, 0],
                       color = 'r', alpha = 0.3,
                       label = '90% Coverage')
    ax[0].legend()
    ax[0].set_xlim(V[0], V[-1])
    ax[0].set_ylabel('Thrust [N]')
    ax[0].set_xlabel('Freestream Velocity [m/s]')
    ax[0].spines['top'].set_visible(False)
    ax[0].spines['right'].set_visible(False)

    ax[1].set_title('Power Performance Curve')
    ax[1].plot(V, Pw[:, 0] * 0.001, ls = '--', color = 'b', lw = 2, label = 'Power Quantiles [0.05-0.95]')
    ax[1].plot(V, Pw[:, 1] * 0.001, color = 'b', lw = 3, label = 'Power Median')
    ax[1].plot(V, Pw[:, 2] * 0.001, ls = '--', color = 'b', lw = 2)
    ax[1].axhline(ls = '-', color = 'k')
    ax[1].fill_between(V, Pw[:, 2] * 0.001, Pw[:, 0] * 0.001,
                       color = 'r', alpha = 0.3,
                       label = '90% Coverage')
    ax[1].legend()
    ax[1].set_xlim(V[0], V[-1])
    ax[1].set_ylabel('Power [kW]')
    ax[1].set_xlabel('Freestream Velocity [m/s]')
    ax[1].spines['top'].set_visible(False)
    ax[1].spines['right'].set_visible(False)

    ax[2].set_title('Efficiency Performance Curve')
    ax[2].plot(V, eta[:, 0], ls = '--', color = 'b', lw = 2, label = r'$\eta$ Quantiles [0.05-0.95] ')
    ax[2].plot(V, eta[:, 1], color = 'b', lw = 3, label = r'$\eta$ median')
    ax[2].plot(V, eta[:, 2], ls = '--', color = 'b', lw = 2)
    ax[2].axhline(ls = '-', color = 'k')
    ax[2].fill_between(V, eta[:, 2], eta[:, 0],
                       color = 'r', alpha = 0.3,
                       label = '90% Coverage')
    ax[2].legend()
    ax[2].set_xlim(V[0], V[-1])
    ax[2].set_ylabel('Efficiency')
    ax[2].set_xlabel('Freestream Velocity [m/s]')
    ax[2].spines['top'].set_visible(False)
    ax[2].spines['right'].set_visible(False)
    fig.tight_layout()
    
    st.pyplot(fig)
    
    csv = convert_df(df)

    st.download_button(
        label="Download Dimensional Data as CSV",
        data=csv,
        file_name='df_dimensional.csv',
        mime='text/csv')
    
with tab2:

    fig, ax = plt.subplots(3, 1, figsize = (11, 14), dpi = 300)

    #fig.suptitle(title)

    ax[0].set_title('Thrust Coefficient Performance Curve')
    ax[0].plot(J, CT[:, 0], ls = '--', color = 'b', lw = 2, label = 'CT Quantiles [0.05-0.95]')
    ax[0].plot(J, CT[:, 1], color = 'b', lw = 3, label = 'CT Median')
    ax[0].plot(J, CT[:, 2], ls = '--', color = 'b', lw = 2)
    ax[0].axhline(ls = '-', color = 'k')
    ax[0].fill_between(J, CT[:, 2], CT[:, 0],
                       color = 'r', alpha = 0.3,
                       label = '90% Coverage')
    ax[0].legend()
    ax[0].set_xlim(J[0], J[-1])
    ax[0].set_ylabel('Thrust Coefficient')
    ax[0].set_xlabel('Advanced Ratio')
    ax[0].spines['top'].set_visible(False)
    ax[0].spines['right'].set_visible(False)

    ax[1].set_title('Power Coefficient Performance Curve')
    ax[1].plot(J, CP[:, 0], ls = '--', color = 'b', lw = 2, label = 'CP Quantiles [0.05-0.95]')
    ax[1].plot(J, CP[:, 1], color = 'b', lw = 3, label = 'CP Median')
    ax[1].plot(J, CP[:, 2], ls = '--', color = 'b', lw = 2)
    ax[1].axhline(ls = '-', color = 'k')
    ax[1].fill_between(J, CP[:, 2], CP[:, 0],
                       color = 'r', alpha = 0.3,
                       label = '90% Coverage')
    ax[1].legend()
    ax[1].set_xlim(J[0], J[-1])
    ax[1].set_ylabel('Power Coefficient')
    ax[1].set_xlabel('Advanced Ratio')
    ax[1].spines['top'].set_visible(False)
    ax[1].spines['right'].set_visible(False)

    ax[2].set_title('Efficiency Performance Curve')
    ax[2].plot(J, eta[:, 0], ls = '--', color = 'b', lw = 2, label = r'$\eta$ Quantiles [0.05-0.95] ')
    ax[2].plot(J, eta[:, 1], color = 'b', lw = 3, label = r'$\eta$ median')
    ax[2].plot(J, eta[:, 2], ls = '--', color = 'b', lw = 2)
    ax[2].axhline(ls = '-', color = 'k')
    ax[2].fill_between(J, eta[:, 2], eta[:, 0],
                       color = 'r', alpha = 0.3,
                       label = '90% Coverage')
    ax[2].legend()
    ax[2].set_xlim(J[0], J[-1])
    ax[2].set_ylabel('Efficiency')
    ax[2].set_xlabel('Advanced Ratio')
    ax[2].spines['top'].set_visible(False)
    ax[2].spines['right'].set_visible(False)
    
    fig.tight_layout()
    
    st.pyplot(fig)
    
    csv = convert_df(adim_df)

    st.download_button(
        label="Download Adimensional Data as CSV",
        data=csv,
        file_name='df_adimensional.csv',
        mime='text/csv')
    
    




    
    
    