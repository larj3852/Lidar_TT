# -*- coding: utf-8 -*-


import LibraryTT.txt2array as conversion
import numpy as np
from numpy import sqrt
import pandas as pd
import matplotlib.pyplot as plt
import random
import math
from mpl_toolkits.mplot3d import Axes3D
import open3d as o3d


conversion.bytxt()
# %matplotlib inline
D = conversion.txt2array()
D = np.delete(D,0,axis=0)
DD = np.copy(D) # Creamos copia de datos para no afectar a los originales

Epsilon = 30
MinPts =  75 #78
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
# abcd = np.delete(abcd,0,axis=0)


# BUSCAR centros de planos aunque debiera buscar algo más con planos pequeños.
# cplns = 0 # va pasando por cada valor abcd para hacer la prueba
# # p1 = 0
# # sc = 0
# # p2 = gplns[sc]
# cplanos = np.array([[0,0,0]])
# Dists = np.array([])
# # cplanos,Dists = conversion.centros(cplanos,Dists,TN,ldps,gplns)

# dext = 100
# dint = 50 

# tvdext = np.array([])
# tvdint = np.array([])
# # Para checar que objetos andan dentro del rango int y ext
# #  np.append(datosx,[[xmin,xmax]],axis=0)
# # Se guardan las posiciones
# for ima in range(0,len(Dists)):
#     if (Dists[ima] <= dext):
#         tvdext = np.append(tvdext,ima)     
#         # print("hay un obstaculo en zona alejada")
#     if (Dists[ima] <= dint):
#         tvdint = np.append(tvdint,ima)
#         # print("Hay obstaculo cercano, detener y cambiar posicion")

# # Para conocer mejor cuales son int mas que ext porque son mas importantes
# if (len(tvdext) > 0) and (len(tvdint) > 0):
#     for ixt in range(0,len(tvdint)):
#         for ixtt in range(0,len(tvdext)):
#             if (tvdint[ixt] == tvdext[ixtt]):
#                 tvdext = np.delete(tvdext[ixtt])
#         if (len(tvdext) <= 0):
#             break
    
# prac = 0
# if (len(tvdext) > 0) or (len(tvdint) > 0):
#     if (len(tvdint)>0):
        
#         for din in range(0,len(tvdint)):
#             xd = cplanos[int(tvdint[din]),0]
#             yd = cplanos[int(tvdint[din]),1]
        
#             angulo = math.atan2(xd,yd)
#             angulo = math.degrees(angulo)
        
#             # En cada uno encender vibrador
#             if (angulo >= 120):
#                 print("rapido dar un paso a la derecha")
#                 prac += 1
#             if (angulo <= 60):
#                 print("rapido dar un paso a la izquierda")
#                 prac += 1
#             if ((angulo > 60)and(angulo < 120)):
#                 print("Deten tu carruaje")
#                 prac += 1
                
#             # Aqui apagara los vibradores
#     if (prac == 0) and (len(tvdext)>0):        
#         for din in range(0,len(tvdext)):
#             xd = cplanos[int(tvdext[din]),0]
#             yd = cplanos[int(tvdext[din]),1]
            
#             angulo = math.atan2(xd,yd)
#             angulo = math.degrees(angulo)
            
#             # En cada uno encender vibrador
#             if (angulo >= 120):
#                 print("dar un paso a la derecha")
#             if (angulo <= 60):
#                 print("dar un paso a la izquierda")
#             if ((angulo > 60)and(angulo < 120)):
#                 print("Abra algo")
                
                
# ----------

# --- 
# --- graficar

# Corro = conversion.usar2(ldps[10:12],4)

# plt.ion()
# figura = plt.figure()

# grafica = figura.add_subplot(111,projection = '3d')
# plt.xlim(-210,150)
# plt.ylim(25,250)
# grafica.set_zlim(-115,180)

# # at = TN.shape
# vcolores = ['b','g','r','c','m','y','k']
# vformas = ['o','x','o','o','o','o','o']

# # if (nnn == 0):
#     # Sin datos ruido
# # for ak in range(1,len(chch)):
# ak = 0
# di1 = vcolores[ak]
# di2 = vformas[ak]
# # vl = TN[ak,:]
# # vl = TN[ak,0:int(chch[ak]),:]
# # vl = Verificar[0,0:389,:]
# vl = Corro[1,0:int(ldps[11]),:]

# [xi,yi,zi] = np.transpose(vl)
# grafica.scatter(xi,yi,zi,
#                 color = di1,
#                 marker = di2)
# xx,yy,zz = cplanos[11,:]
# grafica.scatter(xx,yy,zz,
#                 color=vcolores[2],
#                 marker=vformas[1])

# grafica.set_xlabel('eje x')
# grafica.set_ylabel('eje y')
# grafica.set_zlabel('eje z')
# #grafica.legend()
# plt.show()



# plt.ion()
# figura = plt.figure()

# grafica = figura.add_subplot(111,projection = '3d')
# plt.xlim(-210,150)
# plt.ylim(25,250)
# grafica.set_zlim(-115,180)

# # at = TN.shape
# vcolores = ['b','g','r','c','m','y','k']
# vformas = ['o','x','o','o','o','o','o']

# # if (nnn == 0):
#     # Sin datos ruido
# # for ak in range(1,len(chch)):
# ak = 0
# di1 = vcolores[ak]
# di2 = vformas[ak]
# # vl = TN[ak,:]
# # vl = TN[ak,0:int(chch[ak]),:]
# # vl = Verificar[0,0:389,:]
# vl = Corro[1,0:int(ldps[11]),:]

# [xi,yi,zi] = np.transpose(vl)
# grafica.scatter(xi,yi,zi,
#                 color = di1,
#                 marker = di2)
# # xx,yy,zz = centrosplanos[0,:]
# # grafica.scatter(xx,yy,zz,
# #                 color=vcolores[2],
# #                 marker=vformas[1])

# grafica.set_xlabel('eje x')
# grafica.set_ylabel('eje y')
# grafica.set_zlabel('eje z')
# #grafica.legend()
# plt.show()


# plt.ion()
# figura = plt.figure()
# grafica = figura.add_subplot(111,projection = '3d')
# plt.xlim(-210,150)
# plt.ylim(25,250)
# grafica.set_zlim(-115,180)
# # at = TN.shape
# vcolores = ['b','g','r','c','m','y','k']
# vformas = ['o','x','o','o','o','o','o']

# # if (nnn == 0):
#     # Sin datos ruido
# # for ak in range(1,len(chch)):
# ak = 0
# di1 = vcolores[ak]
# di2 = vformas[ak]
# # vl = TN[ak,:]
# # vl = TN[ak,0:int(chch[ak]),:]
# # vl = Verificar[0,0:389,:]
# # vl = Corro[0,0:int(ldps[0]),:]

# # [xi,yi,zi] = np.transpose(vl)
# # grafica.scatter(xi,yi,zi,
# #                 color = di1,
# #                 marker = di2)
# xx,yy,zz = cplanos[11,:]
# grafica.scatter(xx,yy,zz,
#                 color=vcolores[2],
#                 marker=vformas[1])

# grafica.set_xlabel('eje x')
# grafica.set_ylabel('eje y')
# grafica.set_zlabel('eje z')
# #grafica.legend()
# plt.show()




# buscar centro real o no sé como decirlo, porque no ma, salen raros los centros
# Ya solo falta buscar distancia hasta 1m y .5m o cambiar eso claro. 




# # ------------------------------------------
# # Checar de nuevo la obtención de partes planas o planos por Cluster
# # Pero esta vez desde un punto aleatorio inicial o más cercanos al centro

# # # centro del cluster
# cl = TN[1,0:int(chch[1]),:] #cl3 # Seria como el pasado. ir poco a poco checando que datos si que datos no.
# nx = np.mean(cl[:,0])
# ny = np.mean(cl[:,1])
# nz = np.mean(cl[:,2])

# ## mmm = np.array([nx,ny,nz])

# ## Por razones buscar el más cercanos al centro aunque no será bueno esto

# d = 0 # Distancia 
# pd = 0 # Posicion de distancia
# pdm = 0 # Posición distancia menor
# dm = 0 # Distancia minima

# for i in range(0,len(cl)):
#     d = sqrt(((nx-cl[i,0])**2)+((ny-cl[i,1])**2)+((nz-cl[i,2])**2))
#     pd = i
#     if (i == 0):
#         pdm = pd
#         dm = d
#     if (i >= 1):
#         if (d < dm):
#             dm = d
#             pdm = pd

# ## Iniciamos o ponemos inicial el que este en pdm
# mmm = np.array([cl[pdm,0],cl[pdm,1],cl[pdm,2]])

# cl = np.delete(cl,pdm,axis=0)
# dd = np.array([])
# for ix in range(0,len(cl)):
#     va = sqrt(((mmm[0]-cl[ix,0])**2)+((mmm[1]-cl[ix,1])**2)+((mmm[2]-cl[ix,2])**2))
#     dd = np.append(dd,va)

# cll = np.array([[0,0,0]])
# pdele = np.array([])
# for ix in range(0,len(cl)):
#     if (dd[ix] <= 15):
#         cll = np.append(cll,[[cl[ix,0],cl[ix,1],cl[ix,2]]],axis=0)
#         pdele = np.append(pdele,ix)
# cll = np.delete(cll,0,axis=0)

# # Nube = np.delete(Nube,aquitarr,axis=0) # RECONSTRUCCIÓN DE LA NUBE
# # Areno = np.append(Areno,[[ia1,ia2,ia3]],axis=0)
# # Areno = np.array([[0,0,0]])

# # HACEINDO MATRIZ COVARIANZA
# MC = np.zeros((3,3))
# a = 3
# b = 3
# x = len(cll) # cambiar a lo que se hara despues

# # METODO PARA MARIZ DE COVARIANZA
# for i in range(0,a):
#     for j in range(0,b):
#         for k in range(0,x):
#             MC[i,j] = MC[i,j] + (cll[k,j]-mmm[j])*(cll[k,i]-mmm[i]) #*np.sqrt((W[k]))
    
#         MC[i,j] = MC[i,j]/(x)
# #            MC = MC/x
# # valores y vectores propios

# auval,auvec = np.linalg.eigh(MC)
# # Recordar que son horizontales cada vector propio
# v1 = auvec[0,:]
# v2 = auvec[1,:]
# v3 = auvec[2,:]

# vecnormal = v1
# curvas = auval[0] / (auval[0]+auval[1]+auval[2]) # formula para saber curvatura de una superficie

# RANSAC ---------------------
# Se crea esta parte para poder obtener partes planas del objeto, dividiendo 
# el objeto en posibles objetos para luego no sé

# for objts in range(1,len(TN)):
# # for objts in range(1,2):

#     # Cl = np.copy(TN[1,0:int(chch[1]),:]) # Creamos copia de datos para no afectar a los originales
#     Cl = np.copy(TN[objts,0:int(chch[objts]),:])
    
#     # inliers_result = [] #set() # desbloquear al poner todo el while con maxiterations
#     # dist_threshold = 1 # El umbra de distancia de dato al plano
#     # Plns = 0
#     # while Plns<=1:
    
#     mit = 50 #120 # es indiferente 50 o 120 iteraciones
#     ldplano = np.array([])
#     Planos = 0
#     PlPasado = 0
#     PlFuturo = 1
#     cou = 0
#     boecl = 1
#     cplc = 0
    
#     while boecl:
        
#         if (len(Cl)<15):
#             break
        
#         cou += 1
#         ppp = 0 # Indicador de plano
#         inliers_result = [] #set() # Donde guardo cada Plano ganador por asi decirlo
#         dist_threshold = 5 # El umbra de distancia de dato al plano
        
#         # while mit:
#         #     mit -= 1
        
#         # iteraciones para pobtener inliers
#         for l in range(1,mit+1):
            
#             # if (len(Cl) >= 1):
            
#             #random.seed()
#             inliers = []
#             while (len(inliers) < 3):
#                 random_index = random.randint(0, len(Cl)-1)                
#                 # inliers = np.append(inliers,random_index)
#                 if (len(inliers) == 0):
#                     inliers.append(random_index)
#                 if ((len(inliers) > 0)and(random_index in inliers)):
#                     tr = 0
#                     while tr != 0:
#                         random_index = random.randint(0, len(Cl)-1) 
#                         if (random_index != inliers):
#                             inliers.append(random_index)
#                             tr = 1
#                 elif ((len(inliers) > 0)and(random_index != inliers)):
#                     inliers.append(random_index)
                            
#                 # Areno = np.append(Areno,[[ia1,ia2,ia3]],axis=0)
#             # obetener dato
#             # x1,y1,z1 = Cl[int(inliers[0]),:]
#             # x2,y2,z2 = Cl[int(inliers[1]),:]
#             # x3,y3,z3 = Cl[int(inliers[2]),:]
            
#             x1,y1,z1 = Cl[inliers[0],:]
#             x2,y2,z2 = Cl[inliers[1],:]
#             x3,y3,z3 = Cl[inliers[2],:]
            
#             # Se buscan los datos necesarios A,B,C y D
#             a = (y2 - y1)*(z3 - z1) - (z2 - z1)*(y3 - y1)
#             b = (z2 - z1)*(x3 - x1) - (x2 - x1)*(z3 - z1)
#             c = (x2 - x1)*(y3 - y1) - (y2 - y1)*(x3 - x1)
#             d = -(a*x1 + b*y1 + c*z1)
#             dplano = max(0.1, math.sqrt(a*a + b*b + c*c)) # se pone un max por si dplano es 0 o algo así.
            
#             # Hacer un for para mandar todos los datos
#             for datito in range(0,len(Cl)):
#                 pdato = datito
#                 if pdato in inliers:
#                     continue
#                 # Se consigue el dato a probar
#                 x,y,z = Cl[pdato,:]
                
#                 # Se prueba la distancia del puntito al plano creado
#                 dispp = math.fabs(a*x + b*y + c*z + d)/dplano
                
#                 # Se introduce un nuevo inlier o no
#                 if dispp <= dist_threshold:
#                     inliers.append(pdato)
            
#             # Por cada iteración se guardan los mejores inliers
#             if len(inliers) > len(inliers_result):
#                 inliers_result.clear()
#                 inliers_result = inliers
                
#                 # if (l == 50):
#                 # CuentaPlanos += 1
#                 ppp = 1
#                 # if (ppp == 1)and(len(inliers) > len(inliers_result)):
#                 arr = np.array([a,b,c,d])
#                     # abcd = np.append(abcd,[[a,b,c,d]],axis=0)
#                 # print(len(inliers_result))
#                     # print([a,b,c,d])
                    
                    
            
#         if (ppp == 1):
#             # print(inliers_result[0:3])
#             # print(Cl[inliers_result[0],:])
#             # print(Cl[inliers_result[1],:])
#             # print(Cl[inliers_result[2],:])
#             # print([a,b,c,d])
#             abcd = np.append(abcd,[arr],axis=0)
#             Planos += 1 
#             Plano = np.array([[0,0,0]])
#             for dentro in range(0,len(inliers_result)):
#                 eldato = Cl[inliers_result[dentro],:] #TN[1,inliers_result[dentro],:]
#                 Plano = np.append(Plano,[eldato],axis=0)
        
#             Plano = np.delete(Plano,0,axis=0)
#             # print(Plano[0:3,:])
#             ldplano = np.append(ldplano,len(Plano))
#             conversion.fragmentos(Plano,objts,Planos)
#             # En lo de arriba recordar 1 cambiar por cualquier TN
#             Cl = np.delete(Cl,inliers_result,axis=0)
#             ldps = np.append(ldps,len(Plano))
#             # print(ldplano)
#             # print(len(Cl))
        
#         if (cou == 1)and(ppp == 1)and(cou<=20):
#             # cuenta que si hay primer plano y no pasa los 20 dados
#             cplc = 1 
#         elif (cou > 1)and(cplc == 1):
#             # Crear pasado y futuro sabiendo que si hubo primer plano
#             PlPasado += 1
#             PlFuturo += 2
#         elif (cou>20)and(cplc == 0):
#             # Por si despues de 20 cou de 50 it no hubo primer plano
#             # indica Objeto no tiene planos -- chale
#             break
        
#         if (PlPasado>=Planos)and((PlFuturo-Planos)>1):
#            break
           
#         # Plns = Planos
        
#     gplns = np.append(gplns,Planos)
    
#     Ps = conversion.usar2(ldplano,objts)
    
#     conversion.imprimirObjetos(Ps,ldplano,1,0)
    
#     print("Termina cumulo")

# abcd = np.delete(abcd,0,axis=0)

# Falta gguardar datos de cada objeto (DBSCAN) 
# o sea para cada objts su ldplnao. junto con tipo de objetos 1,2 etc.
# igual guardar valores a,b,c,d para hacer de nuevo proceso y checar que si son planos.
# y los tres puntos principales de cada plano.
# los ldplanos guardar o no
