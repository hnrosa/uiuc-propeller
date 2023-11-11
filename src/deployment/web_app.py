# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 00:19:26 2023

@author: Heitor Nunes Rosa
@gmail: heitornunes12@gmail.com
@github: @hnrosa
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import streamlit as st
from SurrogateProp import SurrogateProp

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
}

lst_families = list(family_names.keys())

st.title('Propeller Surrogate Model')
st.text('Propeller Performance Prediction using XGBoost Algorithm')
st.image('./propeller_photo.png')

family = None
solidity = None

with st.sidebar:
    V = st.slider(
        'Define speed [m/s]',
        0.0, 50.0, (0.0, 30.0))
    D = st.number_input(
        'Define Diameter [in.]', 5, 18, 12,
        )
    P = st.number_input(
        'Define Pitch [in.]', 5, 18, 12, 
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

D *= converter
P *= converter

V = np.linspace(V[0], V[1], 100)

fam = family_names[family]

prop = SurrogateProp(D, P, V, N, rho, solidity, fam)

T = prop.T

fig, ax = plt.subplots(1, 1, figsize = (12, 6))

ax.plot(V, T[:, 0], ls = '--', color = 'b')
ax.plot(V, T[:, 1], color = 'b')
ax.plot(V, T[:, 2], ls = '--', color = 'b')

st.pyplot(fig)




    
    
    