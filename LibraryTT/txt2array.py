#%%
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os
import csv
from time import strftime
#%%
def array2txt(data):
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
                lista.append([int(line[0]),int(line[1]),int(line[2])])
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
    fig .subplots_adjust(left=0, bottom=0, right=1.0, top=1.0)
    ax = fig.add_subplot(111, projection='3d')
    #   Punto de  origen, activacion de la maya y edicion de labels
    ax.scatter(0, 0, 0, marker="D",color=	'k');   #Origen
    ax.legend(b)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_ylim(-1,200)
    ax.set_zlim(-10,100)
    #ax.set_xlim(-100,100)

    ax.grid(True)
    
    if np.shape(array)[0]==3:
        array=array.T
    #   Scaneo de los datos
    print(np.shape(array))
    ax.scatter(array[:,0], array[:,1], array[:,2] , marker='.',c=array[:,1],cmap="spring")
    #ax.scatter(array[:,0], array[:,1], array[:,2] , marker='.',c=array[:,1],cmap="tab20b")
    plt.show()

    
    
    
