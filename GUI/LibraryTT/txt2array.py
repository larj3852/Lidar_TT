#%%
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

def GuardarSet_txt(data):
    """  
    Generacion de un archivo de texto *.txt de la nube de puntos
    lidar en coordenadas cartesianas a partir de un array, 
    que se guardará en la carpeta "./Sets"
    @input          LidarPoints_array dimensions: nx3
    @output         N/A
    """
    #Comprobar si existe la carpeta de CSV
    if not os.path.isdir("./Sets"):
        os.mkdir(os.getcwd()+"/Sets")
        file_num=0
        
    dir_Sets = os.getcwd()+"/Sets/"
    file = open(dir_Sets+"prueba_{0}.txt".format(strftime("%y%m%d%H%M%S")),"w")
    
    #Acomodar matrix a la forma 3xn
    if np.shape(data)[0]==3:
        data=data.T
    for vec in data:
        txt=f"{vec[0]}\t{vec[1]}\t{vec[2]}\n"
        file.write(txt)
    file.close()


#%%
def array2txt(data,a):
    """  
    Generacion de un archivo de texto *.txt de la nube de puntos
    lidar en coordenadas cartesianas a partir de un array, 
    que se guardará en la carpeta "./Sets"
    @input          LidarPoints_array dimensions: nx3
    @output         N/A
    """
    #Comprobar si existe la carpeta de CSV
    if not os.path.isdir("./Sets"):
        os.mkdir(os.getcwd()+"/Sets")
        file_num=0
        
    dir_Sets = os.getcwd()+"/Sets/"
    # file = open(dir_Sets+"prueba_{0}.txt".format(strftime("%y%m%d%H%M%S")),"w")
    file = open(dir_Sets+"objeto"+str(a)+".txt","w") #.format(strftime("%y%m%d%H%M%S")),"w")
    #Acomodar matrix a la forma 3xn
    if np.shape(data)[0]==3:
        data=data.T
    for vec in data:
        txt=f"{vec[0]}\t{vec[1]}\t{vec[2]}\n"
        file.write(txt)
    file.close()

def array2csv(data):
    """
    Generacion de un archivo csv de la nube de puntos
    lidar en coordenadas cartesianas a partir de un array, 
    que se guardará en la carpeta "./Sets_CSV"
    @input          LidarPoints_array dimensions: nx3
    @output         N/A
    """
    #Comprobar si existe la carpeta de CSV
    if not os.path.isdir("./Sets_CSV"):
        os.mkdir(os.getcwd()+"/Sets_CSV")

    #Generar nuevo archivo
    dir_Sets = os.getcwd()+"/Sets_CSV/"
    file = open(dir_Sets+"prueba_{0}.csv".format(strftime("%y%m%d%H%M%S")),"w")

    with file:
        #Acomodar matrix a la forma 3xn
        if np.shape(data)[0]==3: 
            data=data.T
        writer = csv.writer(file)
        for vec in data:
            writer.writerow(list(vec))
    


def txt2array(file_path=None):
    """ 
    Lectura de nube de puntos [x,y,z] desde archivo de texto *.txt
    a un array de la de dimensiones nx3 donde n=numero de puntos
    @input          file_path  *.txt
    @output         array dimenions: nx3
    """
    if not file_path:
        #Buscar solo Text files
        file_path=__FileDialog([("Text files", "*.txt")])
    lista =[]
    with open(file_path,"r") as file:
        a=file.read()
        for linea in a.split("\n"):
            line = linea.split("\t")
            try:
                lista.append([float(line[0]),float(line[1]),float(line[2])])
            except ValueError:
                continue

    return np.array(lista)

def csv2array(file_path=None):
    """ 
    Lectura de nube de puntos [x,y,z] desde archivo CSV
    a un array de la de dimensiones nX3 donde n=numero de puntos
    @input          file_path *.csv
    @output         array dimensions: nx3
    """
    if not file_path:
        #Buscar solo archivos csv
        file_path=__FileDialog(valid_types = [("csv files", "*.csv")])
    with open(file_path, 'r') as csvfile:
        spamreader = csv.reader(csvfile)
        lista = []
        for row in spamreader:
            try:
                lista.append([float(row[0]),float(row[1]),float(row[2])])
            except ValueError:
                continue
            
    return np.array(lista)

def __FileDialog(valid_types=[("All Files","*.*")]):
    """
    Metodo Privado
    Abre ventana de busqueda de archivo, en caso que no
    se haya introducido ninguna ruta de archivo
    """
    from tkinter import filedialog, Tk
    default_path = os.getcwd()
    Tk().withdraw()#Evita que se abra pantalla tkinter
    file_path = filedialog.askopenfilename(initialdir=default_path,filetypes=valid_types)
    # Other options: message="Choose one or more files",
    # multiple=True,title="File Selector", filetypes=valid_types
    return file_path

def imprimir3D(array):
    """
    Ploteo en 3D de un array con nube de puntos
    Parametros
    ----------------
    array dimensiones: 3xn
    """
    import matplotlib.pyplot as plt
    #Lista etiquetas con angulos
    b=['Orig']                      
    
    #Configuracion Inicial
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #   Punto de  origen, activacion de la maya y edicion de labels
    ax.scatter(0, 0, 0, marker='o');   #Origen
    ax.legend(b)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_ylim(-1,300)
    ax.grid(True)
    
    if np.shape(array)[0]==3:
        array=array.T
    #   Scaneo de los datos
    ax.scatter(array[:,0], array[:,1], array[:,2], marker='.')
    plt.show()

def RObjetos(DD,Epsilon,MinPts):
    
    """
    Reconocimiento de objetos o separación de objetos por BDSCAN

    """
    
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
    
    result = DBSCAN(DD,Epsilon,MinPts)
    
    mv = int(np.amax(result))
    cou = 0
    mv += 1
    chch = np.ones(mv) # Marca cuantos datos tiene cada cluster
    # Desde cero hasta el maximo cluster
    
    # ccln = 0
    # cccc = np.array([])
    
    # Se crean los txt de los clusters objetos. 
    for ix in range(0,int(mv)):
        Dondehay = np.where(result == ix)[0]
        lhay = len(Dondehay)
        chch[ix] =lhay
        
        cl = np.ones((lhay,3))
        cl = obtenerdato(cl,Dondehay,lhay,DD)
        cou += 1 # Cuantos clusters hubo al fin contando cero
    
        # conversion.array2txt(cl,ix)
        array2txt(cl,ix)
        file = os.listdir("./Sets")
        file.sort()
        print("Archivo creado:" +file[ix]) #Imprime el ultimo elemento de la lista
    
    return chch

def usar(chch):
    """
    Para poder usar los datos guardados en txt para pasar de txt a array datos guerdados
    """
    mv = len(chch)
    
    for ob in range(0,mv):
        # program = 'cll'+str(ob)+' = conversion.txt2array("./Sets/prueba"+str(ob)+".txt")'
        program = 'cll'+str(ob)+' = txt2array("./Sets/objeto"+str(ob)+".txt")'
        exec(program)
        
    mt = int(np.amax(chch))
    TN = np.zeros((mv,mt,3)) # Todas las nubes de puntos

    # for ii in range(1,mv):
    #     prog2 = 'TN[ii-1,0:int(chch[ii-1])] = cll' + str(ii-1) 
    #     exec(prog2)
    for ii in range(0,mv):
        prog2 = 'TN[ii,0:int(chch[ii])] = cll' + str(ii) 
        exec(prog2)
    return TN

def usar2(chch,nobj):
    """
    Para poder usar los datos guardados en txt de los planos de cada cumulo
    chch - indica cuantos planos hay y cuantos puntos tiene cada plano
    nobj - indica que cumulo o que objeto es (los obtenidos despues de DBSCAN)
    """    

    mv = len(chch)    
    for ob in range(1,mv+1):
        # program = 'cll'+str(ob)+' = conversion.txt2array("./Sets/prueba"+str(ob)+".txt")'
        program = 'cll'+str(nobj)+str(ob)+' = txt2array("./Sets/Plano"+str(nobj)+str(ob)+".txt")'
        exec(program)
        
    mt = int(np.amax(chch))
    TN = np.zeros((mv,mt,3)) # Todas las nubes de puntos

    # for ii in range(1,mv):
    #     prog2 = 'TN[ii-1,0:int(chch[ii-1])] = cll' + str(ii-1) 
    #     exec(prog2)
    for ii in range(0,mv):
        prog2 = 'TN[ii,0:int(chch[ii])] = cll'+str(nobj) + str(ii+1) 
        exec(prog2)
    return TN


def imprimirObjetos(DD,TN,chch,nnn,cho):
        
    plt.ion()
    figura = plt.figure()
    
    grafica = figura.add_subplot(111,projection = '3d')
    plt.xlim(min(DD[:,0])-25,max(DD[:,0])+25)
    plt.ylim(min(DD[:,1])-25,max(DD[:,1])+25)
    grafica.set_zlim(min(DD[:,2])-25,max(DD[:,2])+25)
    
    # at = TN.shape
    vcolores = ['b','g','r','c','m','y','k','b','g','r','c','m','y','k','b','g','r','c','m','y','k','b','g','r','c','m']
    vformas = ['o','o','o','o','o','o','o','x','x','x','x','x','x','x','+','+','+','+','+','+','+','d','d','d','d','d']
    
    if (nnn == 0):
        # Sin datos ruido
        for ak in range(1,len(chch)):
            di1 = vcolores[ak]
            di2 = vformas[ak]
            # vl = TN[ak,:]
            vl = TN[ak,0:int(chch[ak]),:]
                                    
            [xi,yi,zi] = np.transpose(vl)
            grafica.scatter(xi,yi,zi,
                            color = di1,
                            marker = di2)
        grafica.set_xlabel('eje x')
        grafica.set_ylabel('eje y')
        grafica.set_zlabel('eje z')
        #grafica.legend()
        plt.show()
    
    elif (nnn == 1):
        # Con datos ruido
        
        for ak in range(0,len(chch)):
            di1 = vcolores[ak]
            di2 = vformas[ak]
            vl = TN[ak,0:int(chch[ak]),:]
            
            [xi,yi,zi] = np.transpose(vl)
            grafica.scatter(xi,yi,zi,
                            color = di1,
                            marker = di2)
        grafica.set_xlabel('eje x')
        grafica.set_ylabel('eje y')
        grafica.set_zlabel('eje z')
        #grafica.legend()
        plt.show()
        
    elif (nnn == 2):
        # Solo un cluster

        # for ak in range(0,at[0]):
        di1 = vcolores[cho]
        di2 = vformas[cho]
        vl = TN[cho,0:int(chch[cho]),:]        
        
        [xi,yi,zi] = np.transpose(vl)
        grafica.scatter(xi,yi,zi,
                color = di1,
                marker = di2)

        grafica.set_xlabel('eje x')
        grafica.set_ylabel('eje y')
        grafica.set_zlabel('eje z')
        #grafica.legend()
        plt.show()
        
def fragmentos(data,nobj,nplano):
    """  
    Generacion de un archivo de texto *.txt de la nube de puntos
    lidar en coordenadas cartesianas a partir de un array, 
    que se guardará en la carpeta "./Sets"
    @input          LidarPoints_array dimensions: nx3
    @output         N/A
    
    Partida de un Objeto en varias partes planas
    
    """
    #Comprobar si existe la carpeta de CSV
    if not os.path.isdir("./Sets"):
        os.mkdir(os.getcwd()+"/Sets")
        file_num=0
        
    dir_Sets = os.getcwd()+"/Sets/"
    # file = open(dir_Sets+"prueba_{0}.txt".format(strftime("%y%m%d%H%M%S")),"w")
    file = open(dir_Sets+"Plano"+str(nobj)+str(nplano)+".txt","w") #.format(strftime("%y%m%d%H%M%S")),"w")
    #Acomodar matrix a la forma 3xn
    if np.shape(data)[0]==3:
        data=data.T
    for vec in data:
        txt=f"{vec[0]}\t{vec[1]}\t{vec[2]}\n"
        file.write(txt)
    file.close()
    
def rnsc(TN,chch,abcd,ldps,gplns):
    for objts in range(1,len(TN)):
        
    # Cl = np.copy(TN[1,0:int(chch[1]),:]) # Creamos copia de datos para no afectar a los originales
        Cl = np.copy(TN[objts,0:int(chch[objts]),:])
    
    # inliers_result = [] #set() # desbloquear al poner todo el while con maxiterations
    # dist_threshold = 1 # El umbra de distancia de dato al plano
    # Plns = 0
    # while Plns<=1:
        mit = 50 #120 # es indiferente 50 o 120 iteraciones
        ldplano = np.array([])
        Planos = 0
        PlPasado = 0
        PlFuturo = 1
        cou = 0
        boecl = 1
        cplc = 0
        while boecl:
            if (len(Cl)<15):
                break
        
            cou += 1
            ppp = 0 # Indicador de plano
            inliers_result = [] #set() # Donde guardo cada Plano ganador por asi decirlo
            dist_threshold = 5 # El umbra de distancia de dato al plano
            
            for l in range(1,mit+1):
                
                inliers = []
                while (len(inliers) < 3):
                    
                    random_index = random.randint(0, len(Cl)-1)                
                # inliers = np.append(inliers,random_index)
                    if (len(inliers) == 0):
                        inliers.append(random_index)
                    if ((len(inliers) > 0)and(random_index in inliers)):
                            tr = 0
                            while tr != 0:
                                random_index = random.randint(0, len(Cl)-1) 
                                if (random_index != inliers):
                                    inliers.append(random_index)
                                    tr = 1
                    elif ((len(inliers) > 0)and(random_index != inliers)):
                        inliers.append(random_index)
                # obetener dato
                # x1,y1,z1 = Cl[int(inliers[0]),:]
                # x2,y2,z2 = Cl[int(inliers[1]),:]
                # x3,y3,z3 = Cl[int(inliers[2]),:]
            
                x1,y1,z1 = Cl[inliers[0],:]
                x2,y2,z2 = Cl[inliers[1],:]
                x3,y3,z3 = Cl[inliers[2],:]
                
                # Se buscan los datos necesarios A,B,C y D
                a = (y2 - y1)*(z3 - z1) - (z2 - z1)*(y3 - y1)
                b = (z2 - z1)*(x3 - x1) - (x2 - x1)*(z3 - z1)
                c = (x2 - x1)*(y3 - y1) - (y2 - y1)*(x3 - x1)
                d = -(a*x1 + b*y1 + c*z1)
                dplano = max(0.1, sqrt(a*a + b*b + c*c)) # se pone un max por si dplano es 0 o algo así.
                
                for datito in range(0,len(Cl)):
                    pdato = datito
                    if pdato in inliers:
                        continue
                # Se consigue el dato a probar
                    x,y,z = Cl[pdato,:]
                
                # Se prueba la distancia del puntito al plano creado
                    dispp = math.fabs(a*x + b*y + c*z + d)/dplano
                    
                    if dispp <= dist_threshold:
                        inliers.append(pdato)
                
                if len(inliers) > len(inliers_result):
                    inliers_result.clear()
                    inliers_result = inliers
                    
                    # if (l == 50):
                        # CuentaPlanos += 1
                    ppp = 1
                    # if (ppp == 1)and(len(inliers) > len(inliers_result)):
                    arr = np.array([a,b,c,d])
                    # abcd = np.append(abcd,[[a,b,c,d]],axis=0)
                    # print(len(inliers_result))
                    # print([a,b,c,d])
    
            if (ppp == 1):
                
                abcd = np.append(abcd,[arr],axis=0)
                Planos += 1 
                Plano = np.array([[0,0,0]])
                for dentro in range(0,len(inliers_result)):
                    
                    eldato = Cl[inliers_result[dentro],:] #TN[1,inliers_result[dentro],:]
                    Plano = np.append(Plano,[eldato],axis=0)
                
                Plano = np.delete(Plano,0,axis=0)
                # print(Plano[0:3,:])
                ldplano = np.append(ldplano,len(Plano))
                # conversion.fragmentos(Plano,objts,Planos)
                fragmentos(Plano,objts,Planos)
                # En lo de arriba recordar 1 cambiar por cualquier TN
                Cl = np.delete(Cl,inliers_result,axis=0)
                ldps = np.append(ldps,len(Plano))
                # print(ldplano)
                # print(len(Cl))
            
            if (cou == 1)and(ppp == 1)and(cou<=20):
            # cuenta que si hay primer plano y no pasa los 20 dados
                cplc = 1 
            elif (cou > 1)and(cplc == 1):
                # Crear pasado y futuro sabiendo que si hubo primer plano
                PlPasado += 1
                PlFuturo += 2
            elif (cou>20)and(cplc == 0):
                # Por si despues de 20 cou de 50 it no hubo primer plano
                # indica Objeto no tiene planos -- chale
                break
        
            if (PlPasado>=Planos)and((PlFuturo-Planos)>1):
                break
            
            # Plns = Planos
            
        gplns = np.append(gplns,Planos)
    
        # Ps = conversion.usar2(ldplano,objts)
        Ps = usar2(ldplano,objts)
        # conversion.imprimirObjetos(Ps,ldplano,1,0)
        imprimirObjetos(Ps,ldplano,1,0)
        
        print("Termina cumulo")    
            
    abcd = np.delete(abcd,0,axis=0)
    return(abcd,ldps,gplns)

def centros(cplanos,Dists,TN,ldps,gplns):
    datosx = np.array([[0,0]]) # aqui va xmin y xmax de cada plano
    datosy = np.array([[0,0]]) # aqui va ymin y ymax de cada plano
    datosz = np.array([[0,0]]) # aqui va zmin y zmax de cada plano
    sa,sb,sc = np.shape(TN)
    ccc = 0
    for lll in range(1,sa):
        if (lll == 1):
            p1 = 0
            sc = 0
            p2 = gplns[sc]
        elif (lll > 1):
            sc += 1
            p1 = p2
            # p2 = int(p1)+ int(gplns[sc])
            p2 = int(p1)+ int(gplns[sc])
        # Cada abcd debe ser un array que guarde el de todos los planos en el cumulo
        # Verificar = conversion.usar2(ldps[int(p1):int(p2)],lll)
        # Verificar = conversion.usar2(ldps[int(p1):int(p2)],lll)
        Verificar = usar2(ldps[int(p1):int(p2)],lll)        
        fff = len(Verificar)        

        for plaxpla in range(0,fff):
            xmin = np.min(Verificar[plaxpla,:,0])
            xmax = np.max(Verificar[plaxpla,:,0])
            
            ymin = np.min(Verificar[plaxpla,:,1])
            ymax = np.max(Verificar[plaxpla,:,1])
            
            zmin = np.min(Verificar[plaxpla,:,2])
            zmax = np.max(Verificar[plaxpla,:,2])
            
            datosx = np.append(datosx,[[xmin,xmax]],axis=0)
            datosy = np.append(datosy,[[ymin,ymax]],axis=0)
            datosz = np.append(datosz,[[zmin,zmax]],axis=0)
            
            
            Dts = Verificar[plaxpla,0:int(ldps[ccc]),:]
            print(len(Dts))
            
            cx = np.mean(Dts[:,0])
            cy = np.mean(Dts[:,1])
            cz = np.mean(Dts[:,2])
            
            # cx = np.mean(Verificar[plaxpla,:,0])
            # cy = np.mean(Verificar[plaxpla,:,1])
            # cz = np.mean(Verificar[plaxpla,:,2])
        
            cplanos = np.append(cplanos,[[cx,cy,cz]],axis=0)
            ccc += 1
    cplanos = np.delete(cplanos,0,axis=0)
    
    for opp in range(0,len(cplanos)):
        dimm = sqrt((cplanos[opp,0]**2)+(cplanos[opp,1]**2)+(cplanos[opp,2]**2))
        Dists = np.append(Dists,dimm)

    return(cplanos,Dists)

def bytxt():
    for a in range(0,100):
            
        if not os.path.isdir("./Sets"):
            os.mkdir(os.getcwd()+"/Sets")
            file_num=0
        
        dir_Sets = os.getcwd()+"/Sets/"

        if os.path.exists(dir_Sets+"objeto"+str(a)+".txt"):
            os.remove(dir_Sets+"objeto"+str(a)+".txt")
        
        for aa in range(1,101):
            # if not os.path.isdir("./Sets"):
            #     os.mkdir(os.getcwd()+"/Sets")
            #     file_num=0
        
            # EL dir_Sets ya esta
        
            if os.path.exists(dir_Sets+"Plano"+str(a)+str(aa)+".txt"):
                os.remove(dir_Sets+"Plano"+str(a)+str(aa)+".txt")
                # dir_Sets+"Plano"+str(nobj)+str(nplano)+".txt"

def rnsc2(Cl,abcd,ldps,gplns):    
    # for objts in range(1,len(TN)):
        
    # Cl = np.copy(TN[1,0:int(chch[1]),:]) # Creamos copia de datos para no afectar a los originales
        # Cl = np.copy(TN[objts,0:int(chch[objts]),:])
    
    # inliers_result = [] #set() # desbloquear al poner todo el while con maxiterations
    # dist_threshold = 1 # El umbra de distancia de dato al plano
    # Plns = 0
    # while Plns<=1:
    mit = 50 #120 # es indiferente 50 o 120 iteraciones
    ldplano = np.array([])
    Planos = 0
    PlPasado = 0
    PlFuturo = 1
    cou = 0
    boecl = 1
    cplc = 0
    while boecl:
        if (len(Cl)<15):
            break
        
        cou += 1
        ppp = 0 # Indicador de plano
        inliers_result = [] #set() # Donde guardo cada Plano ganador por asi decirlo
        dist_threshold = 5 # El umbra de distancia de dato al plano
        
        for l in range(1,mit+1):
            
            inliers = []
            while (len(inliers) < 3):
                
                random_index = random.randint(0, len(Cl)-1)                
            # inliers = np.append(inliers,random_index)
                if (len(inliers) == 0):
                    inliers.append(random_index)
                if ((len(inliers) > 0)and(random_index in inliers)):
                        tr = 0
                        while tr != 0:
                            random_index = random.randint(0, len(Cl)-1) 
                            if (random_index != inliers):
                                inliers.append(random_index)
                                tr = 1
                elif ((len(inliers) > 0)and(random_index != inliers)):
                    inliers.append(random_index)
            # obetener dato
            # x1,y1,z1 = Cl[int(inliers[0]),:]
            # x2,y2,z2 = Cl[int(inliers[1]),:]
            # x3,y3,z3 = Cl[int(inliers[2]),:]
        
            x1,y1,z1 = Cl[inliers[0],:]
            x2,y2,z2 = Cl[inliers[1],:]
            x3,y3,z3 = Cl[inliers[2],:]
            
            # Se buscan los datos necesarios A,B,C y D
            a = (y2 - y1)*(z3 - z1) - (z2 - z1)*(y3 - y1)
            b = (z2 - z1)*(x3 - x1) - (x2 - x1)*(z3 - z1)
            c = (x2 - x1)*(y3 - y1) - (y2 - y1)*(x3 - x1)
            d = -(a*x1 + b*y1 + c*z1)
            dplano = max(0.1, sqrt(a*a + b*b + c*c)) # se pone un max por si dplano es 0 o algo así.
            
            for datito in range(0,len(Cl)):
                pdato = datito
                if pdato in inliers:
                    continue
            # Se consigue el dato a probar
                x,y,z = Cl[pdato,:]
            
            # Se prueba la distancia del puntito al plano creado
                dispp = math.fabs(a*x + b*y + c*z + d)/dplano
                
                if dispp <= dist_threshold:
                    inliers.append(pdato)
            
            if len(inliers) > len(inliers_result):
                inliers_result.clear()
                inliers_result = inliers
                
                # if (l == 50):
                    # CuentaPlanos += 1
                ppp = 1
                # if (ppp == 1)and(len(inliers) > len(inliers_result)):
                arr = np.array([a,b,c,d])
                # abcd = np.append(abcd,[[a,b,c,d]],axis=0)
                # print(len(inliers_result))
                # print([a,b,c,d])

        if (ppp == 1):
            
            abcd = np.append(abcd,[arr],axis=0)
            Planos += 1 
            Plano = np.array([[0,0,0]])
            for dentro in range(0,len(inliers_result)):
                
                eldato = Cl[inliers_result[dentro],:] #TN[1,inliers_result[dentro],:]
                Plano = np.append(Plano,[eldato],axis=0)
            
            Plano = np.delete(Plano,0,axis=0)
            # print(Plano[0:3,:])
            ldplano = np.append(ldplano,len(Plano))
            # conversion.fragmentos(Plano,objts,Planos)
            objts=1
            fragmentos(Plano,objts,Planos)
            # En lo de arriba recordar 1 cambiar por cualquier TN
            Cl = np.delete(Cl,inliers_result,axis=0)
            ldps = np.append(ldps,len(Plano))
            # print(ldplano)
            # print(len(Cl))
        
        if (cou == 1)and(ppp == 1)and(cou<=20):
        # cuenta que si hay primer plano y no pasa los 20 dados
            cplc = 1 
        elif (cou > 1)and(cplc == 1):
            # Crear pasado y futuro sabiendo que si hubo primer plano
            PlPasado += 1
            PlFuturo += 2
        elif (cou>20)and(cplc == 0):
            # Por si despues de 20 cou de 50 it no hubo primer plano
            # indica Objeto no tiene planos -- chale
            break
    
        if (PlPasado>=Planos)and((PlFuturo-Planos)>1):
            break
        
        # Plns = Planos
        
    gplns = np.append(gplns,Planos)

    # Ps = conversion.usar2(ldplano,objts)
        # objts=1
        # Ps = usar2(ldplano,objts)
    # conversion.imprimirObjetos(Ps,ldplano,1,0)
        # imprimirObjetos(Ps,ldplano,1,0)
    
    print("Termina cumulo")    
            
    abcd = np.delete(abcd,0,axis=0)
    return(abcd,ldps,gplns)


def kk(Cl,k):
    centros = []
    
    etiquetador = []
    for po in range(1,k+1):
        etiquetador.append(po)
    
    Pertenencia = np.zeros(len(Cl))
    
    
    while (len(centros)<k):
        random_centro = random.randint(0, len(Cl)-1)
        # inliers = np.append(inliers,random_index)
        if (len(centros) == 0):
            centros.append(random_centro)
        if ((len(centros) > 0)and(random_centro in centros)):
            tr = 0
            while tr != 0:
                random_centro = random.randint(0, len(Cl)-1) 
                if (random_centro != centros):
                    centros.append(random_centro)
                    tr = 1
        elif ((len(centros) > 0)and(random_centro != centros)):
            centros.append(random_centro)
        
    kk = 0
    ck = np.array([[0,0,0]]) # serian los centros de cada cluster, ahorita necesito los k numeros de DD o Cl
    for i in centros:
        Pertenencia[i] = etiquetador[kk]
        ck = np.append(ck,[Cl[i]],axis=0)
        kk += 1
    
    ck = np.delete(ck,0,axis=0)
    it = 50 # las iteraciones por lo mientras
    # print(ck)
    for itera in range(0,it):
        for ddd in range(0,len(Cl)):
            if (itera == 0):
                if (Pertenencia[ddd] > 0):
                    continue
            dpx = Cl[ddd,0]
            dpy = Cl[ddd,1]
            dpz = Cl[ddd,2]
            datoprueba = [dpx,dpy,dpz]
            # La parte usada para conocer a que cluster pertenece cada dato
            ddptock = [] # distancai euclideana de cada centro al punto prueba
            for vv in range(0,len(ck)):
                dck = sqrt(((datoprueba[0]-ck[vv,0])**2)+((datoprueba[1]-ck[vv,1])**2)+((datoprueba[2]-ck[vv,2])**2))
                ddptock.append(dck)
            posmin = ddptock.index(min(ddptock))
            
            marca = etiquetador[posmin]
            Pertenencia[ddd] = marca
        # if itera == 0:
            # print(Pertenencia)
            
        # la actualizacion de centros conforme los datos pertenecientes
        for vvv in range(0,len(etiquetador)):
            pk = np.where(Pertenencia == etiquetador[vvv])[0]
            
            tdpk = len(pk)
            
            sx = 0
            sy = 0
            sz = 0
            for iv in range(0,tdpk):
                # sx += Cl[int(pk[iv]),0]
                # sy += Cl[int(pk[iv]),1]
                # sz += Cl[int(pk[iv]),2]
                sx += Cl[pk[iv],0]
                sy += Cl[pk[iv],1]
                sz += Cl[pk[iv],2]
            
            sx = sx/tdpk
            sy = sy/tdpk
            sz = sz/tdpk
            
            ck[vvv,0] = sx
            ck[vvv,1] = sy
            ck[vvv,2] = sz
    chch = []        
    for ix in range(0,len(etiquetador)):
        ppk = np.where(Pertenencia == etiquetador[ix])[0] 
        chch.append(len(ppk))
    mchch = max(chch)
    mv = len(chch)
    TN = np.zeros((mv,mchch,3))
    for xi in range(0,len(etiquetador)):
        ccl = np.zeros([chch[xi],3])
        pppk = np.where(Pertenencia == etiquetador[xi])[0]    
        ccc = 0
        for xii in pppk:
            ax = Cl[xii,0]
            ay = Cl[xii,1]
            az = Cl[xii,2]
            TN[xi,ccc,:] = [ax,ay,az]
            ccl[ccc,:] = [ax,ay,az]
            ccc += 1
        array2txt(ccl,etiquetador[xi])
        file = os.listdir("./Sets")
        file.sort()
        print("Archivo creado:" +file[xi]) #Imprime el ultimo elemento de la lista
    return(TN,chch)
