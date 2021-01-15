#%%
# -*- coding: utf-8 -*-
"""

El DBSCAN solito sin nada más... °-°

"""

import LibraryTT.txt2array as conversion
import numpy as np
from numpy import sqrt
import pandas as pd
import matplotlib.pyplot as plt
import random
import math
from mpl_toolkits.mplot3d import Axes3D
#import open3d as o3d

#%%
conversion.bytxt()
# %matplotlib inline
D = conversion.txt2array()
D = np.delete(D,0,axis=0)
DD = np.copy(D) # Creamos copia de datos para no afectar a los originales

Epsilon = 40 #35 #30
MinPts =  20 #40 #75 #78
# result = DBSCAN(DD,Epsilon,MinPts)

chch = conversion.RObjetos(DD,Epsilon,MinPts)

TN = conversion.usar(chch)
# print(chch)
# Graficar un dato
#%%
#conversion.imprimir3D(D)
#%%
conversion.imprimirObjetos(DD,TN,chch,0,0)
#%%
conversion.imprimirObjetos(DD,TN,chch,2,0)
#%% Graficar con ruido
conversion.imprimirObjetos(DD,TN,chch,1,0)


# %%
