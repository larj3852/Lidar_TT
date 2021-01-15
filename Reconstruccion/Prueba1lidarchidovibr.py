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

dext = 100
dint = 50 

tvdext = np.array([])
tvdint = np.array([])
# Para checar que objetos andan dentro del rango int y ext
#  np.append(datosx,[[xmin,xmax]],axis=0)
# Se guardan las posiciones
for ima in range(0,len(Dists)):
    if (Dists[ima] <= dext):
        tvdext = np.append(tvdext,ima)     
        # print("hay un obstaculo en zona alejada")
    if (Dists[ima] <= dint):
        tvdint = np.append(tvdint,ima)
        # print("Hay obstaculo cercano, detener y cambiar posicion")

# Para conocer mejor cuales son int mas que ext porque son mas importantes
if (len(tvdext) > 0) and (len(tvdint) > 0):
    for ixt in range(0,len(tvdint)):
        for ixtt in range(0,len(tvdext)):
            if (tvdint[ixt] == tvdext[ixtt]):
                tvdext = np.delete(tvdext[ixtt])
        if (len(tvdext) <= 0):
            break
    
prac = 0
if (len(tvdext) > 0) or (len(tvdint) > 0):
    if (len(tvdint)>0):
        
        for din in range(0,len(tvdint)):
            xd = cplanos[int(tvdint[din]),0]
            yd = cplanos[int(tvdint[din]),1]
        
            angulo = math.atan2(xd,yd)
            angulo = math.degrees(angulo)
        
            # En cada uno encender vibrador
            if (angulo >= 120):
                print("rapido dar un paso a la derecha")
                prac += 1
            if (angulo <= 60):
                print("rapido dar un paso a la izquierda")
                prac += 1
            if ((angulo > 60)and(angulo < 120)):
                print("Deten tu carruaje")
                prac += 1
                
            # Aqui apagara los vibradores
    if (prac == 0) and (len(tvdext)>0):        
        for din in range(0,len(tvdext)):
            xd = cplanos[int(tvdext[din]),0]
            yd = cplanos[int(tvdext[din]),1]
            
            angulo = math.atan2(xd,yd)
            angulo = math.degrees(angulo)
            
            # En cada uno encender vibrador
            if (angulo >= 120):
                print("dar un paso a la derecha")
            if (angulo <= 60):
                print("dar un paso a la izquierda")
            if ((angulo > 60)and(angulo < 120)):
                print("Abra algo")

