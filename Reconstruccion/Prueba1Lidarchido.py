# -*- coding: utf-8 -*-
"""
... 

"""

import LibraryTT.txt2array as conversion
import numpy as np
from numpy import sqrt
import pandas as pd
import matplotlib.pyplot as plt
import random
import math
from mpl_toolkits.mplot3d import Axes3D
# import open3d as o3d

# %matplotlib inline
D = conversion.txt2array()

DD = np.copy(D) # Creamos copia de datos para no afectar a los originales

Epsilon = 30
MinPts = 75 #78
# result = DBSCAN(DD,Epsilon,MinPts)

chch = conversion.RObjetos(DD,Epsilon,MinPts)

TN = conversion.usar(chch)

# Graficar un dato
conversion.imprimir3D(D)
# conversion.imprimir3D(DD)

# Imprimir sin ruido--- graficar
conversion.imprimirObjetos(TN,chch,0,0) 
# Graficar con ruido
conversion.imprimirObjetos(TN,chch,1,0)

# conversion.imprimirObjetos(TN,chch,2,1)
# (Objetos,tamañoobjetos,2,cualObjeto)

# el ransac
# vectores para guardar datos.
abcd = np.array([[0,0,0,0]])
ldps = np.array([])
gplns = np.array([])

abcd,ldps,gplns = conversion.rnsc(TN,chch,abcd,ldps,gplns)
abcd = np.delete(abcd,0,axis=0)

# BUSCAR centros de planos aunque debiera buscar algo más con planos pequeños.
cplns = 0 # va pasando por cada valor abcd para hacer la prueba
# p1 = 0
# sc = 0
# p2 = gplns[sc]
cplanos = np.array([[0,0,0]])
Dists = np.array([])
cplanos,Dists = conversion.centros(cplanos,Dists,TN,ldps,gplns)

