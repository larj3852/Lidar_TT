import rplidar
import csv
from time import sleep,time
import numpy as np
import matplotlib.pyplot as plt
from   LibraryTT.Servo import  Servo
import LibraryTT.txt2array as txt2array
import logging

class Scaner3D:
    """
    Clase para crea objeto de escaneo 3D para
    la adquisición de la nube de puntos LMS,
    mediante el LiDAR
    """
    def __init__(self):
        """
        Inicialización de la clase para escaneo con
        le LiDAR
        Parametros
        ----------
        Ninguno
        """
        self.PuertoUSB = '/dev/ttyUSB0'
        #Inicializacion Servo en  inicial
        self.servo = Servo(90)
        
        #Inicializacion Lidar
        self.lidar = rplidar.RPLidar(self.PuertoUSB)
        sleep(1)
        self.lidar.get_info()        #Informacion del Lidar
        self.lidar.get_health()      #Informacion del estado del Lidar
        self.process_scan = lambda scan: None   #Lectura de generadores


    def Scanear(self, Angulo_Init=60,Angulo_Fin=50,paso=-1, plotear=False):
        """
        Función para escanear los puntos en el espacio
        Parametros
        ------------
        int  Angulo_Init   Angulo Inicial de escaneo [0,180]°
        int  ANgulo_Fin    Angulo Final de escaneo [0,180]°
        int  paso          paso de los angulos del servo para la reconstruccion
        bool plotear       ¿Desea que se ploté lo escaneado?
        
        Regresa
        ------------
        array nx3          Array con la nube de puntos escaneada en forma cartesina
                           de la forma [x,y,z]xn
        """
        t1 = time()   # Tiempo Inicial
        T_LMS = 0     # Puntos del Set
        
        #logging sesion
        logging.basicConfig(level=logging.INFO,format="[%(name)s: %(levelname)s] %(message)s")
        informacion = logging.getLogger(__name__)
       
        #Generacion de angulos de escaneo en el plano xz (del servo pues)
        self.Angulo_Init = Angulo_Init #90
        self.Angulo_Fin  = Angulo_Fin  #70
        self.paso = -1*np.abs(paso)
        self.a=np.arange(self.Angulo_Init,self.Angulo_Fin,self.paso)
        self.phi=self.a*np.pi/180 #90 a 60        #Array de angulos
        
        #Inicializacion vector de datos
        self.data = np.array([[0],[0],[0]])        
        
        #Extraccion de puntos
        for j in range(len(self.phi)):
            #print(len(lidar._serial_port.read_all()))
            self.servo.setAngle(self.a[j])
            self.lidar.connect()
            self.lidar._serial_port.flushInput()
            i=0
            for scan in self.lidar.iter_scans():
                self.process_scan(scan)
                i+=1
                if i>= 3:
                    break

            #   Muestras por escaneo
            informacion.info(f"Ang={self.a[j]} |Muestras = {len(scan)}")
                             
            #   Pre-procesamiento de los datos
            scan = self.recorte(scan)  #Selecciona solo los puntos frontales
            scan=np.array(scan)
            self.x = np.round(np.cos(np.pi - scan[:,1] *(np.pi/180))*scan[:,2]/10,decimals=3)
            self.y = np.round(np.sin(np.pi-scan[:,1]*(np.pi/180))*np.sin(self.phi[j])*scan[:,2]/10,decimals=3)
            #Nota, como el lidar está en 90° se le inverte la función sin(phi)
            self.z = np.round(np.sin(np.pi- scan[:,1]*(np.pi/180))*np.cos(self.phi[j])*scan[:,2]/10,decimals=3)
            
            T_LMS +=len(scan)
            #   Empaqueta los datos en vector cartesiano [x,y,z]
            self.data = self.__empaquetamiento_cartesinano()
            
            
            #   Parar muestreo lidar
            self.lidar.stop()
            self.lidar.stop_motor()
            self.lidar.disconnect()
        
        #Tiempo total
        t2=time()   #Tiempo final
        print(f"Tiempo Total: {t2-t1}, Muestras totales: {T_LMS}")
        
        #Retornar servo a estado inicial
        self.servo.setAngle(90)
        
        #¿Plotear?
        if plotear:
            self.ploteo3D()
        
        #Guardar datos
        txt2array.array2txt(self.data)
        txt2array.array2csv(self.data)
                
        #Regresa los puntos escaneados
        return self.data.T

    def ploteo3D(self):
        """
        Función para plotear el último set de nube de puntos
        escaneado
        """
        #Lista etiquetas con angulos
        b=['Orig']                      
        
        #Configuracion Inicial
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        #   Punto de  origen, activacion de la maya y edicion de labels
        ax.scatter(0, 0, 0, marker='o');
        ax.legend(b)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        ax.set_ylim(-1,300)
        ax.grid(True)

        #   Scaneo de los datos
        ax.scatter(self.data[0,:], self.data[1,:], self.data[2,:], marker='.')
        plt.show()
       
    @staticmethod
    def recorte(scan):
        """
        Filtra los puntos de la parte frontal del LiDAR
        """
        lista = []
        for a in scan:
            if a[1]<150:
                lista.append(a)
        return lista


    def __empaquetamiento_cartesinano(self):
        """
        Agrega los puntos de la forma x,y,z al la variable
        self.data, que es la que contiene los puntos
        """
        aux  = np.concatenate(([self.x],[self.y],[self.z]),axis=0) #Concatena a = x,y,z en filas
        aux = np.concatenate((self.data,aux),axis=1) #Concatena concatena planos en columnas
        return aux
    