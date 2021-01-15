# -*- coding: utf-8 -*-
"""

Otro solo RANSAC

Para kmeans
from sklearn.cluster import KMeans
from sklearn import metrics

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


# PArte de los datos
conversion.bytxt()
D = conversion.txt2array()
# D = np.delete(D,0,axis=0)
DD = np.copy(D) # Creamos copia de datos para no afectar a los originales

# Quitar datos
pquitar= []
for i in range(0,len(DD)):
    if (DD[i,2] <= -60):
        pquitar.append(i)
DD = np.delete(DD,[pquitar],axis=0)
# PArte del ransac
abcd = np.array([[0,0,0,0]])
ldps = np.array([])
gplns = np.array([])

abcd,ldps,gplns = conversion.rnsc2(DD,abcd,ldps,gplns)
# abcd = np.delete(abcd,0,axis=0)
      
# Me falta ver eso de quitar piso y superficies más alla del tamaño del tipo
Ps = conversion.usar2(ldps,1)
# conversion.imprimirObjetos(Ps,ldplano,1,0)



# PArte graficacion
conversion.imprimir3D(DD)
conversion.imprimirObjetos(DD,Ps,ldps,1,0)

conversion.imprimirObjetos(DD,Ps,ldps,2,0)




