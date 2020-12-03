import LibraryTT.txt2array as conversion


#  Funcion sin ningun argumento (Se abrirá ventana para buscar el archivo)
from  numpy import shape
get_ipython().run_line_magic("matplotlib", " inline")
a=conversion.txt2array()
print(f"Forma del vector nx3 ={shape(a)}")
conversion.imprimir3D(a)


# Forma 2: Función con algun argumneto
get_ipython().run_line_magic("matplotlib", " inline")
a=conversion.txt2array("./Sets/prueba_200911021124.txt")
conversion.imprimir3D(a)


#Forma 1:   Funcion sin ningun argumento (Se abrirá ventana para buscar el archivo)
from  numpy import shape
get_ipython().run_line_magic("matplotlib", " inline")
a=conversion.csv2array()
print(f"Forma del vector nx3 ={shape(a)}")
conversion.imprimir3D(a)


# Forma 2: Función con algun argumneto
get_ipython().run_line_magic("matplotlib", " inline")
a=conversion.csv2array("./Sets_CSV/prueba_200911015330.csv")
conversion.imprimir3D(a)


import os
a=conversion.txt2array()
conversion.array2txt(a) #Escritura del nuevo vector nx3
file = os.listdir("./Sets")
file.sort()
print("Archivo creado:" +file[-1]) #Imprime el ultimo elemento de la lista


import os
a=conversion.txt2array()
conversion.array2csv(a) #Escritura del nuevo vector nx3
file = os.listdir("./Sets_CSV")
file.sort()
print("Archivo creado:" +file[-1]) #Imprime el ultimo elemento de la lista


get_ipython().run_line_magic("matplotlib", " inline")
a=conversion.txt2array()
conversion.imprimir3D(a) # Hay que meter un array de forma nx3 corespondiente los sets de puntos LiDAR


help(conversion)



