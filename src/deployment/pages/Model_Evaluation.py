# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 00:06:19 2023

@author: Heitor Nunes Rosa
@gmail: heitornunes12@gmail.com
@github: @hnrosa
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import streamlit as st

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

family_names = {v:k for k, v in family_names.items()}

st.title('Model Evaluation')
st.header('Residual Plots')
st.image('./residual_plot.png')
st.header('Test Results per Propeller Family')

tab1, tab2 = st.tabs(['RMSE', 'R²'])

with tab1:
    df = pd.read_csv('test_results_rmse.csv')
    df = df.iloc[1:, :]
    df['Family'] = df['Family'].replace(family_names)
    st.dataframe(df.style.
                 background_gradient(cmap='PuBu',
                                     axis = 0).format(
                                         precision = 3)
                 )

with tab2:
    df = pd.read_csv('test_results_r2.csv')
    df = df.iloc[1:, :]
    df['Family'] = df['Family'].replace(family_names)
    st.dataframe(df.style.
                 background_gradient(cmap='PuBu',
                                     axis = 0).format(
                                         precision = 2)
                )