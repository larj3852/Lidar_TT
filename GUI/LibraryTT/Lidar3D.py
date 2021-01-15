import rplidar
from time import sleep,time
import numpy as np
import matplotlib.pyplot as plt
from   LibraryTT.Servo import  Servo
import LibraryTT.txt2array as txt2array
import logging
from os.path import exists

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
        
        #Inicializacion Servo en  inicial
        self.servo = Servo(90)
        
        #Inicializacion Lidar (en puerto ttyUSB0 o ttyUSB1)
        if exists("/dev/ttyUSB0"):
            self.lidar = rplidar.RPLidar("/dev/ttyUSB0")
        else:
            self.lidar = rplidar.RPLidar("/dev/ttyUSB1")
            
        sleep(1)
        self.lidar.get_info()        #Informacion del Lidar
        self.lidar.get_health()      #Informacion del estado del Lidar
        self.process_scan = lambda scan: None   #Lectura de generadores


    def Scanear(self, Angulo_Init=80,Angulo_Fin=120,paso=1, revxplano=1, plotear=False):
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
        self.paso = np.abs(paso)
        self.a=np.arange(self.Angulo_Init,self.Angulo_Fin,self.paso)
        self.phi=self.a*np.pi/180 #90 a 60        #Array de angulos
        
        #Inicializacion vector de datos
        self.data = np.array([[],[],[]])        
        
        #Extraccion de puntos
        for j in range(len(self.phi)):
            #print(len(lidar._serial_port.read_all()))
            self.servo.setAngle(self.a[j])
            self.lidar.connect()
            self.lidar._serial_port.flushInput()
            i=0
            scan=[]
            for scan2 in self.lidar.iter_scans():
                self.process_scan(scan2)
                i+=1
                scan= scan2 + scan
                if i>= revxplano:
                    break
            

            #   Muestras por escaneo
            informacion.info(f"Ang={self.a[j]} |Muestras = {len(scan)}")

            #   Pre-procesamiento de los datos
            scan = self.recorte(scan)  #Selecciona solo los puntos frontales
            scan=np.array(scan)
            #Resolucion cm
            self.x = -np.round(np.cos(np.pi - scan[:,1] *(np.pi/180))*scan[:,2]/10) #np.round(vec,decimals=0) 
            self.y = -np.round(np.sin(np.pi-scan[:,1]*(np.pi/180))*np.sin(self.phi[j])*scan[:,2]/10)
            #Nota, como el lidar está en 90° se le inverte la función sin(phi)
            cte = 10/180*np.pi #compenza el desface producido por los engranes
            self.z = -np.round(np.sin(np.pi- scan[:,1]*(np.pi/180))*np.cos(self.phi[j]-cte)*scan[:,2]/10)

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
        self.data=self.data.astype(int)       
        #Guardar datos
        txt2array.GuardarSet_txt(self.data)
        #txt2array.array2csv(self.data)
        
        #¿Plotear?
        if plotear:
            self.ploteo3D()
            
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
        #ax.set_xlim(-200,200)
        #ax.set_ylim(-200,10)
        ax.set_zlim(-100,150)
        #ax.set_xlim(np.min(self.data[0,:]),np.max(self.data[0,:]))
        #ax.set_ylim(np.min(self.data[1,:]),np.max(self.data[1,:]))
        #ax.set_zlim(np.min(self.data[2,:]),np.max(self.data[2,:]))
        ax.grid(True)

        #   Scaneo de los datos
        ax.scatter(self.data[0,:], self.data[1,:], self.data[2,:], marker='.', c=self.data[0,:], cmap="jet")
        plt.show()
       
    @staticmethod
    def recorte(scan):
        """
        Filtra los puntos de la parte frontal del LiDAR
        """
        lista = []
        for a in scan:
            if (a[1]>150):
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
