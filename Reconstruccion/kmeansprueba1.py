#%%
# -*- coding: utf-8 -*-
"""
Para el Kmeans

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


# PArte de los datos
conversion.bytxt()
D = conversion.txt2array()
# D = np.delete(D,0,axis=0)
DD = np.copy(D) # Creamos copia de datos para no afectar a los originales
# EL Kmeans inicio
k = 5 # Creo es bueno, igual pondre 9

TN,chch = conversion.kk(DD,k)

# Parte graficacion
conversion.imprimir3D(DD)
#%%
conversion.imprimirObjetos(DD,TN,chch,1,0)

# conversion.imprimirObjetos(DD,Ps,chch,2,0)


# ----
# centros = []

# etiquetador = []
# for po in range(1,k+1):
#     etiquetador.append(po)

# Pertenencia = np.zeros(len(Cl))


# while (len(centros)<k):
#     random_centro = random.randint(0, len(Cl)-1)
#     # inliers = np.append(inliers,random_index)
#     if (len(centros) == 0):
#         centros.append(random_centro)
#     if ((len(centros) > 0)and(random_centro in centros)):
#         tr = 0
#         while tr != 0:
#             random_centro = random.randint(0, len(Cl)-1) 
#             if (random_centro != centros):
#                 centros.append(random_centro)
#                 tr = 1
#     elif ((len(centros) > 0)and(random_centro != centros)):
#         centros.append(random_centro)
    
# kk = 0
# ck = np.array([[0,0,0]]) # serian los centros de cada cluster, ahorita necesito los k numeros de DD o Cl
# for i in centros:
#     Pertenencia[i] = etiquetador[kk]
#     ck = np.append(ck,[Cl[i]],axis=0)
#     kk += 1

# ck = np.delete(ck,0,axis=0)
# it = 50 # las iteraciones por lo mientras
# # print(ck)
# for itera in range(0,it):
#     for ddd in range(0,len(Cl)):
#         if (itera == 0):
#             if (Pertenencia[ddd] > 0):
#                 continue
#         dpx = Cl[ddd,0]
#         dpy = Cl[ddd,1]
#         dpz = Cl[ddd,2]
#         datoprueba = [dpx,dpy,dpz]
#         # La parte usada para conocer a que cluster pertenece cada dato
#         ddptock = [] # distancai euclideana de cada centro al punto prueba
#         for vv in range(0,len(ck)):
#             dck = sqrt(((datoprueba[0]-ck[vv,0])**2)+((datoprueba[1]-ck[vv,1])**2)+((datoprueba[2]-ck[vv,2])**2))
#             ddptock.append(dck)
#         posmin = ddptock.index(min(ddptock))
        
#         marca = etiquetador[posmin]
#         Pertenencia[ddd] = marca
#     if itera == 0:
#         print(Pertenencia)
        
#     # la actualizacion de centros conforme los datos pertenecientes
#     for vvv in range(0,len(etiquetador)):
#         pk = np.where(Pertenencia == etiquetador[vvv])[0]
        
#         tdpk = len(pk)
        
#         sx = 0
#         sy = 0
#         sz = 0
#         for iv in range(0,tdpk):
#             # sx += Cl[int(pk[iv]),0]
#             # sy += Cl[int(pk[iv]),1]
#             # sz += Cl[int(pk[iv]),2]
#             sx += Cl[pk[iv],0]
#             sy += Cl[pk[iv],1]
#             sz += Cl[pk[iv],2]
        
#         sx = sx/tdpk
#         sy = sy/tdpk
#         sz = sz/tdpk
        
#         ck[vvv,0] = sx
#         ck[vvv,1] = sy
#         ck[vvv,2] = sz
# chch = []        
# for ix in range(0,len(etiquetador)):
#     ppk = np.where(Pertenencia == etiquetador[ix])[0] 
#     chch.append(len(ppk))
# mchch = max(chch)
# mv = len(chch)
# TN = np.zeros((mv,mchch,3))
# for xi in range(0,len(etiquetador)):
#     pppk = np.where(Pertenencia == etiquetador[xi])[0]    
#     ccc = 0
#     for xii in pppk:
#         ax = Cl[xii,0]
#         ay = Cl[xii,1]
#         az = Cl[xii,2]
#         TN[xi,ccc,:] = [ax,ay,az]
#         ccc += 1



# for kc in range(0,k):
#     # program = 'cll'+str(ob)+' = conversion.txt2array("./Sets/prueba"+str(ob)+".txt")'
#     program = 'kcentro'+str(kc+1) =     
#     exec(program)
# %%
