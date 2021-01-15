# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN

X, v = make_blobs(n_samples=60, centers=4, cluster_std=.60, random_state=0)

plt.figure(figsize=(15,10))
plt.scatter(X[:,0], X[:,1])

N = len(X)
ind = np.arange(N)
print(ind)
for label, x, y in zip(ind,X[:,0], X[:,1]):
    plt.annotate(label,xy=(x,y))
    

clustering = DBSCAN(eps=.8, min_samples=5) # cambiar para que se vea diferente.
etiqueta = clustering.fit_predict(X)

plt.figure(figsize=(15,10))
plt.xlim(-5,5)
plt.ylim(0,10)
plt.scatter(X[:,0], X[:,1], c=etiqueta)

N = len(X)
ind = np.arange(N)
for label, x, y in zip(ind, X[:,0], X[:,1]):
    plt.annotate(label,xy=(x,y))


def buscarVecinos(P,X,epsilon):
    N = len(X)
    vecinos = []
    for i in range(N):
        if(np.linalg.norm(P-X[i]) <= epsilon):
            vecinos.append(i)
    return(vecinos)

v = buscarVecinos(X[28], X, .5)

# Para cada punto P en el cluster C, miramos si es un nodo, y en caso afirmativo
# agregamos todos los vecinos de P al cluster C

def agregarAlcanzablesDirectos(C, X, etiqueta, epsilon, minPuntos):
    N = len(X) # cantidad de datos
    nuevoPunto = 0 # Indica si encontramos u nuevo punto alcanzable direco del cluster
    etiquetaCopia = np.copy(etiqueta) # copiamos las etiquetas para no modificar 
                                        #  de entrada 
                                        
    for i in range(N):
        if(etiqueta[i] == C):
            vecinos = buscarVecinos(X[i],X,epsilon)
            if(len(vecinos) >= minPuntos): # entocntramos un nucleo!
                for j in vecinos:
                    if(etiquetaCopia[j] <= 0):
                        etiquetaCopia[j] = C
                        nuevoPunto = 1 # Permite agrwegar puntos nuevos

    return(etiquetaCopia, nuevoPunto)

etiqueta = np.zeros(N)
etiqueta[28] = 1
print(etiqueta)

etiqueta2, nuevoPunto = agregarAlcanzablesDirectos(1,X,etiqueta,.8,5)
print(etiqueta2)

plt.figure(figsize=(15,10))
plt.xlim(-5,5)
plt.ylim(0,10)
plt.scatter(X[:,0], X[:,1], c=etiqueta2)


N = len(X)
ind = np.arange(N)
for label,x,y in zip(ind, X[:,0],X[:,1]):
    plt.annotate(label,xy=(x,y))


# Para calcular todos los puntos alcanzables a los puntos de un cluster,
# vamos agregando los alcanzables directos hasta que no haya mas nada para agregar

def agregarAlcanzablesTodos(C,X,etiqueta,epsilon,minPuntos):
    nuevoPunto = 1
    etiquetaCopia = np.copy(etiqueta)
    
    while(nuevoPunto == 1):
        etiquetaCopia2, nuevoPunto = agregarAlcanzablesDirectos(C,X,etiquetaCopia, epsilon, minPuntos)
        
        etiquetaCopia = np.copy(etiquetaCopia2)
    return(etiquetaCopia)

etiqueta2 = agregarAlcanzablesTodos(1,X,etiqueta,1,5)
print(etiqueta2)

plt.figure(figsize=(15,10))
plt.xlim(-5,5)
plt.ylim(0,10)
plt.scatter(X[:,0], X[:,1], c=etiqueta2)


N = len(X)
ind = np.arange(N)
for label,x,y in zip(ind, X[:,0],X[:,1]):
    plt.annotate(label,xy=(x,y))

# Ahora podemos definir la función que calcula todos los clusters

def DBSCANClusters(X, epsilon, minPuntos):
    N = len(X) # Cantidad de datos
    etiqueta = np.zeros(N) # vamos a guardar a que cluster pertenece cada punto
    C = 0     # Indica el numero de cluster que estamos construyendo
    for i in range(N):
        if(etiqueta[i] == 0):
            vecinos = buscarVecinos(X[i],X,epsilon)
            if(len(vecinos) >= minPuntos):  # Encontramos un nodo
            # Construimos el cluster corresponidente a ese nucleo
                C = C+1 # un nodo mas
                etiqueta[i] = C
                etiqueta = agregarAlcanzablesTodos(C,X,etiqueta,epsilon,minPuntos)
            else:
                # Si no es un nodo, lo marcamos como ruido
                etiqueta[i] = -1
    return(etiqueta)

etiqueta = DBSCANClusters(X,.7,5)
print(etiqueta)




