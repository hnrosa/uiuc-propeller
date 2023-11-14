# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 23:21:30 2023

@author: Heitor Nunes Rosa
@gmail: heitornunes12@gmail.com
@github: @hnrosa
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(
    page_title= 'Notations'
)

st.title('Reference Notations')
st.subheader('Propeller Geometry')
st.markdown(r'''Diameter: $D$ [in.]''')
st.markdown(r'''Radius: $r$ [in.]''')
st.markdown(r'''Pitch: $P$ [in.]''')
st.markdown(r'''Chord: $c$ [in.]''')
st.markdown(r'''Number of Blades: $B$''')
st.markdown(r'''Solidity: $\sigma$''')

st.subheader('Adimensional Numbers')
st.markdown(r'''Advanced Ration: $J$''')
st.markdown(r'''Thrust Coefficient: $C_T$''')
st.markdown(r'''Power Coefficient: $C_P$''')
st.markdown(r'''Efficiency: $\eta$''')

st.subheader('Measures')
st.markdown(r'''Thrust: $Tr$ [N]''')
st.markdown(r'''Power: $Pw$ [kW]''')
st.markdown(r'''Freestream Velocity: $V$ [m/s]''')
st.markdown(r'''Rotation: $N$ [RPM]''')
st.markdown(r'''Rotation $n$ [RPS]''')
st.markdown(r'''Air density: $\rho$ [kg/m³]''')

st.title('Equations')

st.markdown('Advanced Ratio:')
st.latex(r'''J = \frac{V}{nD}''')
st.markdown('Thrust Coefficient:')
st.latex(r'''C_T = \frac{Tr}{\rho n^2D^4}''')
st.markdown('Power Coefficient:')
st.latex(r'''C_P = \frac{Pw}{\rho n^3D^5}''')
st.markdown('Efficiency:')
st.latex(r'''\eta = J\frac{C_T}{C_P}''')
st.markdown('Solidity:')
st.latex(r'''\sigma = \frac{4B}{\pi D^2} \large{\int_{0}^{D/2}}c(r)dr''')
