# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 21:25:36 2023

@author: Heitor Nunes Rosa
@gmail: heitornunes12@gmail.com
@github: @hnrosa
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from SurrogateProp import SurrogateProp

# D, P, V, N, rho, Sol = None, Family = None

D1 = 12 * 25.6 * 0.001
P1 = 6* 25.6 * 0.001
V = np.linspace(0, 30, 100)
N = 8000
rho = 1.25
Fam = 'ancf'

prop_1 = SurrogateProp(D1, P1, V, N, rho, Family = Fam)

# %%
T1 = prop_1.T

fig, ax = plt.subplots(1, 1, figsize = (12, 6))

ax.plot(V, T1[:, 0], ls = '--', color = 'b')
ax.plot(V, T1[:, 1], color = 'b')
ax.plot(V, T1[:, 2], ls = '--', color = 'b')