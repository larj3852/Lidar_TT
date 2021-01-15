# -*- coding: utf-8 -*-
"""
Checar de nuevo el DBSCAN

"""
import LibraryTT.txt2array as conversion
from numpy import sqrt
import pandas as pd


import numpy as np
import matplotlib.pyplot as plt
import os
import csv
from time import strftime
import random


# Para el DBSCAN
from numpy import shape
import scipy as scipy
from sklearn import cluster
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from math import sqrt
import math

# def RObjetos(DD,Epsilon,MinPts):

def set2List(npArray):
    list = []
    for item in npArray:
        list.append(item.tolist())
    return list

def DBSCAN(Data, Epsilon,MinumumPoints,DistanceMethod = 'euclidean'):
    #    Dataset is a mxn matrix, m is number of item and n is the dimension of data
    m,n=Data.shape
    Visited=np.zeros(m,'int')
    Type=np.zeros(m)
    #    print(m)
    #    print(n)
    #   -1 noise, outlier
    #    0 border
    #    1 core
    ClustersList=[]
    Cluster=[]
    PointClusterNumber=np.zeros(m)
    PointClusterNumberIndex=1
    PointNeighbors=[]
    DistanceMatrix = scipy.spatial.distance.squareform(scipy.spatial.distance.pdist(Data, DistanceMethod))
    for i in range(m):
        if Visited[i]==0:
            Visited[i]=1
            PointNeighbors=np.where(DistanceMatrix[i]<Epsilon)[0]
            if len(PointNeighbors)<MinumumPoints:
                Type[i]=-1
            else:
                for k in range(len(Cluster)):
                    Cluster.pop()
                Cluster.append(i)
                PointClusterNumber[i]=PointClusterNumberIndex        
                PointNeighbors=set2List(PointNeighbors)    
                ExpandCluster(Data[i], PointNeighbors,Cluster,MinumumPoints,Epsilon,Visited,DistanceMatrix,PointClusterNumber,PointClusterNumberIndex  )
                Cluster.append(PointNeighbors[:])
                ClustersList.append(Cluster[:])
                PointClusterNumberIndex=PointClusterNumberIndex+1
    return PointClusterNumber

def ExpandCluster(PointToExapnd, PointNeighbors,Cluster,MinumumPoints,Epsilon,Visited,DistanceMatrix,PointClusterNumber,PointClusterNumberIndex  ):
    Neighbors=[]
 
    for i in PointNeighbors:
        if Visited[i]==0:
            Visited[i]=1
            Neighbors=np.where(DistanceMatrix[i]<Epsilon)[0]
            # print(len(Neighbors))
            if len(Neighbors)>=MinumumPoints:
            #      Neighbors merge with PointNeighbors
                for j in Neighbors:
                    if j in PointNeighbors:
                        continue
                    else:
                        PointNeighbors.append(j)
                    # try:
                    #     PointNeighbors.index(j)
                    # except ValueError:
                    #     PointNeighbors.append(j)                
        if PointClusterNumber[i]==0:
            Cluster.append(i)
            PointClusterNumber[i]=PointClusterNumberIndex
    return

def obtenerdato(acumulador,dondehay,lhay,Datos):
    for i in range(0,lhay):
        F = Datos[dondehay[i],:]
        acumulador[i,:] = F
    return acumulador


# DD = np.zeros([len(D),3])

# for nix in range(0,len(D)):
#     xa = int(D[nix,0])
#     ya = int(D[nix,1])
#     za = int(D[nix,2])

# DD[nix,:] = [xa,ya,za]

# Epsilon = 30
# MinPts = 75 #78

# def ExpandCluster(PointToExapnd, PointNeighbors,Cluster,MinumumPoints,Epsilon,Visited,DistanceMatrix,PointClusterNumber,PointClusterNumberIndex  ):

Neighbors=[]

for pp in PointNeighbors:
    if Visited[pp] == 0:
        Visited[pp] = 1
        Neighbors=np.where(DistanceMatrix[pp]<Epsilon)[0]
        # print(len(Neighbors))
        if len(Neighbors)>=MinumumPoints:
        #      Neighbors merge with PointNeighbors
            for ppp in Neighbors:
                if ppp in PointNeighbors:
                    # print("yaestadentro")
                    
                    continue
                    
                else:
                    PointNeighbors.append(ppp)
                    # print("nuevo")
                # try:
                #     PointNeighbors.index(ppp)
                # except ValueError:
                #     PointNeighbors.append(ppp)
    if PointClusterNumber[pp]==0:
        Cluster.append(pp)
        PointClusterNumber[pp]=PointClusterNumberIndex


D = conversion.txt2array()
conversion.imprimir3D(D)
DD = np.copy(D) # Creamos copia de datos para no afectar a los originales


# MinPts =  50 #78
# result = DBSCAN(DD,Epsilon,MinPts)
Epsilon = 40
MinumumPoints = 50

DistanceMethod = 'euclidean'

#----------------------
m,n = DD.shape
Visited=np.zeros(m,'int') # Datos visitados enteros32
Type=np.zeros(m) # el normal float64
    #    print(m)
    #    print(n)
    #   -1 noise, outlier
    #    0 border
    #    1 core
ClustersList=[] # Lista de clusters
Cluster=np.array([]) # cuantos clusters hay
PointClusterNumber=np.zeros(m) # guardara que cluster le corresponde a cada punto de DD
PointClusterNumberIndex=1 # indice de numero puntos cluster, inicia 1 porque se busca el primer cluster
PointNeighbors=[] # acumula puntos vecinos
# el metodo de distancia euclideana pero mas resumida
DistanceMatrix = scipy.spatial.distance.squareform(scipy.spatial.distance.pdist(DD, DistanceMethod))
# busqueda por cada punto
for i in range(m):
    if Visited[i]==0: # Si dato visited es 0
        Visited[i]=1 # se pasa a 1
        PointNeighbors=np.where(DistanceMatrix[i]<Epsilon)[0]
        if len(PointNeighbors)<MinumumPoints:
            Type[i]=-1
        else:
            for k in range(len(Cluster)):
                Cluster.pop()
            Cluster.append(i)
            PointClusterNumber[i]=PointClusterNumberIndex
            PointNeighbors=set2List(PointNeighbors)
            ExpandCluster(DD[i], PointNeighbors,Cluster,MinumumPoints,Epsilon,Visited,DistanceMatrix,PointClusterNumber,PointClusterNumberIndex  )
            Cluster.append(PointNeighbors[:])
            ClustersList.append(Cluster[:])
            PointClusterNumberIndex=PointClusterNumberIndex+1


ok = 0
i = 0
while ok != 0:
    
    if Visited[i] == 0:
        Visited[i]=1
        PointNeighbors = np.where(DistanceMatrix[i]<Epsilon)[0]
        
        if (len(PointNeighbors) < MinumumPoints):
            Type[i] = -1
        else:
            for k in range(len(Cluster)):
                Cluster.pop()                        
            PointNeighbors=set2List(PointNeighbors)
            for mm in PointNeighbors:
                Cluster.append(mm)
                Visited[mm] = 1
                PointClusterNumber[mm]=PointClusterNumberIndex
                #ExpandCluster
            ClustersList.append(Cluster[:])
            PointClusterNumberIndex += 1
                
                
                
            
            
Neighbors=[]

for pp in PointNeighbors:
    if Visited[pp] == 0:
        Visited[pp] = 1
        Neighbors=np.where(DistanceMatrix[pp]<Epsilon)[0]
        # print(len(Neighbors))
        if len(Neighbors)>=MinumumPoints:
        #      Neighbors merge with PointNeighbors
            for ppp in Neighbors:
                if ppp in PointNeighbors:
                    # print("yaestadentro")
                    
                    continue
                    
                else:
                    PointNeighbors.append(ppp)
                    # print("nuevo")
                # try:
                #     PointNeighbors.index(ppp)
                # except ValueError:
                #     PointNeighbors.append(ppp)
    if PointClusterNumber[pp]==0:
        Cluster.append(pp)
        PointClusterNumber[pp]=PointClusterNumberIndex
         
            
            
    
    
        
        




