#%% Importar modulo
import sqlite3
#Conexion
conexion = sqlite3.connect('pruebas.db')

#Crear cursor --> Permitirá realizar las consultas
cursor = conexion.cursor()
# %%
#%%
#Crear tabla
cursor.execute("CREATE TABLE IF NOT EXISTS detecciones("+
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"+
                "tamano_set int(10),"+
                "metodo_deteccion VARCHAR(30),"+
                "objetos_detectados int(2),"+
                "tiempo_reconstruccion int(10),"+
                "tiempo_deteccion int(10),"+    
                "data_set LONGTEXT"+
                ")")

#%% Eliminar tabla
cursor.execute("DROP TABLE detecciones")

#%% Insertar Reconstrucciones
cursor.execute("INSERT INTO detecciones VALUES(null,1000,'K-means',5,30,10,'la pata del mameitor');")
conexion.commit()

#%%CONSULTA SELECTIVA EJEMPLO:Productos >= 100
cursor.execute("SELECT * FROM productos WHERE precio>=100;")
productos = cursor.fetchall()
for producto in productos:
    print("\n",producto)
    
# %% CERRAR CONEXION
conexion.close()