# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 20:36:13 2020

@author: Matias
"""

import LibraryTT.txt2array as conversion
import numpy as np
from numpy import sqrt
import pandas as pd
import matplotlib.pyplot as plt
import random
import math
from mpl_toolkits.mplot3d import Axes3D
import open3d as o3d

from mat4py import loadmat
from sklearn.datasets import make_blobs

# Gráficos
# ==============================================================================

from matplotlib import style
import seaborn as sns
#style.use('ggplot') or plt.style.use('ggplot')

# Preprocesado y modelado
# ==============================================================================
from sklearn.mixture import GaussianMixture
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# Configuración warnings
# ==============================================================================
import warnings
warnings.filterwarnings('ignore')

D = conversion.txt2array()
D = np.delete(D,0,axis=0)
DD = np.copy(D) # Creamos copia de datos para no afectar a los originales


fig,ax = plt.subplots(figsize=(6,3.84))
n_components = range(1,10)
covariance_types=['spherical','tied','diag','full']

for covariance_type in covariance_types:
    valores_bic = []
    
    for i in n_components:
        modelo = GaussianMixture(n_components=i,covariance_type=covariance_type)
        modelo = modelo.fit(DD)
        valores_bic.append(modelo.bic(DD))
    
    ax.plot(n_components,valores_bic,label=covariance_type)
ax.set_title('Valores BIC')
ax.set_xlabel("Numero componentes")
ax.legend()
    