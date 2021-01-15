
#Librerias para las funciones de retroalimentacion
import numpy as np
import math
#Librearías para los motores

import threading
import RPi.GPIO as GPIO
import time

# ---- Quitar datos
# Se hace un corte de datos, basandonos en el alto del sujeto
# lo que se hara es quitar datos en un gango menor y mayo en eje Z

def QuitarDatos(Cl,AS,AL):
    """
    Con esta función se quitaran datos que pueden ser innecesarios
    @inputs  AS - Altura del sujeto
             AL - Altura del lidar
    
    @Outputs Cl - la misma nube sin algnos datos
    """
    
    AL = 110
    AS = 170
    
    HZ = (AS-AL)+40
    DH = []
    
    for nn in range(0,len(Cl)):
        if (Cl[nn,2] >= HZ):
            DH.append(nn)
        
    Cl = np.delete(Cl,DH,axis=0)
    
    SZ = (AL/5) - AL # AProx 1/5 del tamaño del lidar
    
    SH = []
    for nnn in range(0,len(Cl)):
        if (Cl[nnn,2] <= SZ):
            SH.append(nnn)
    Cl = np.delete(Cl,SH,axis=0)
    
    return(Cl)



# ES DE AQUI PARA ABAJO, SOLO QUE NO ESTA PUESTO EN FUNCIONES;
# las funciones estan escondidas para que veas el codigo asi 
# sin ser funcion claro.
# -----Checar objetos...

# Primero - Buscar centro de cada objeto y limites.

def losdatos(TN,chch):
    """
    Obtención de datos de cada cluster, siendo centro y limites
    
    @inputs  TN - matriz de clsuter
             chch - vector de cantidad de datos de cada cluster
             
    @output cc - centros de cada cluster
            lmts - limites de cada clsuter
    """
    m,f,c = np.shape(TN)
    cc = np.zeros((m,c))
    lmts = np.zeros((m,6))
    for nm in range(0,m):
        Cl = TN[nm,0:int(chch[nm]),:]
        
        cx = np.mean(Cl[:,0])
        cy = np.mean(Cl[:,1])
        cz = np.mean(Cl[:,2])
        
        cc[nm,:] = [cx,cy,cz]
        
        xmin = min(Cl[:,0])
        xmax = max(Cl[:,0])
        ymin = min(Cl[:,1])
        ymax = max(Cl[:,1])
        zmin = min(Cl[:,2])
        zmax = max(Cl[:,2])
        
        lmts[nm,:] = [xmin,xmax,ymin,ymax,zmin,zmax]
    return(cc,lmts)

    
# Segundo - Formas de detección o como se diga

# primer forma - centro de humano
# Se trata de obtener los datos en cada cluster que esten dentro del intervalo
# del centro del humano-prototipo (0 en eje z) 
# no se cree sea bueno ya que objetos reconcidos de menor o mayor tamaño no seran catalogados
def forma1(TN,chch):
    """
    Función para crear la forma de obtención de datos cercanos al sujeto
    
    @inputs TN - MAtriz de cluster
            chch - vector de cuantos datos hay en cada cluster
            
    @Output deint - matriz con datos dentro de lo establecido

    """
    m,f,c = np.shape(TN)
    deint = np.array([[0,0,0]]) # indica que datos si andan en el intervalo
    cdob = []
    
    for nm in range(0,m):
        Cl = TN[nm,0:int(chch[nm]),:]
        cou = 0 # cuenta cuantos datos hay en cada objeto dentro del intervalo
        
        for ini in range(0,len(Cl)):
            dz = Cl[ini,2]
            
            if (dz >= -5)and(dz <= 5):
                dix = Cl[ini,0]
                diy = Cl[ini,1]
                diz = Cl[ini,2]
                
                deint = np.append(deint,[[dix,diy,diz]],axis=0)
                cou += 1
        if (cou > 0):
            cdob.append(nm+1)
    deint = np.delete(deint,0,axis=0)
    return(deint)
# segunda forma - datos del centro del objeto. 
# Para cada objeto se le encotro previamente el centro, y los limites 
# en x,y,z así que se buscan los datos que esten en el centro de cada objeto
# dependiendo los limites del objeto
def forma2(TN,chch,cc,lmts):
    """
    Función para crear la forma de obtención de datos cercanos al sujeto
    
    @inputs TN - MAtriz de cluster
            chch - vector de cuantos datos hay en cada cluster
            cc - centro de cada cluster
            lmts - limites de cada clsuter
            
    @Output dint - matriz con datos dentro de lo establecido

    """    
    m,f,c = np.shape(TN)
    dint = np.array([[0,0,0]])
    ncs = 0
    NC = []
    for nm in range(0,m):
        Cl = TN[nm,0:int(chch[nm]),:]
        centro = cc[nm]
        lcluster = lmts[nm,:]
        ncs += 1
        d1 = centro[0] # es x
        d2 = centro[1] # es y
        d3 = centro[2] # es z
        
        p1 = int(lcluster[0])
        p2 = int(lcluster[1])
        for dd in range(p1,p2):
            # Para obtener datos en x            
            dint = np.append(dint,[[dd,d2,d3]],axis=0)
            NC.append(ncs)
            
        p3 = int(lcluster[2])
        p4 = int(lcluster[3])
        for ddd in range(p3,p4):
            # Para obtener datos en y
            dint = np.append(dint,[[d1,ddd,d3]],axis=0)
            NC.append(ncs)
        
    dint = np.delete(dint,0,axis=0)
    return(dint,NC)

# Tercer forma - La verdad olvide el tercero real
# en este se busca el uso de datos en los limites x,y 
def forma3(TN,chch,cc,lmts):
    """
    Función para crear la forma de obtención de datos cercanos al sujeto
    
    @inputs TN - MAtriz de cluster
            chch - vector de cuantos datos hay en cada cluster
            cc - centro de cada cluster
            lmts - limites de cada clsuter
            
    @Output dints - matriz con datos dentro de lo establecido

    """
    m,f,c = np.shape(TN)
    dints = np.array([[0,0,0]])
    
    for nm in range(0,m):
        Cl = TN[nm,0:int(chch[nm]),:]
        centro = cc[nm,:]
        lcluster = lmts[nm]
        dints = np.append(dints,[centro],axis=0)
        d1 = centro[0] # es x
        d2 = centro[1] # es y
        d3 = centro[2] # es z
        
        # los de x
        p1 = int(lcluster[0])
        p2 = int(lcluster[1])      
        # los de y
        p3 = int(lcluster[2])
        p4 = int(lcluster[3])
        
        dints = np.append(dints,[[p1,d2,d3]],axis=0)
        dints = np.append(dints,[[p2,d2,d3]],axis=0)
        dints = np.append(dints,[[d1,p3,d3]],axis=0)
        dints = np.append(dints,[[d1,p4,d3]],axis=0)
    
    dints = np.delete(dints,0,axis=0)
    return(dints)

# Tercero - Expresion de datos dentro del rango
# PAra conocer si existe algun objeto que obstruya el caminar del 
# sujeto de pruebas, se realiza el uso de dos circulos
# un circulo externo y un circulo interno para alertar al sujeto
# del mismo

# Como se tendran tres vibradores, se cree lo siguiente dependiendo
# del rango de observación.

def DangerDanger(dmd,rci,rce):
    """
    La función sirve alerta al sujeto de si existe un objeto qu ele obstruya
    
    @inputs md - es matriz de los datos a usar para conocer la cercania de algun objeto
            rci - radio del circulo interno
            rce - radio del circulo externo
    
    @outputs I - intensidad de vibración
             NV - numéro de motor    
    """
    
    # lmd = len(md)
    I = 0
    NM = 0    
    # for nnn in range(0,lmd):
    dx = dmd[0]
    dy = dmd[1]
    dz = dmd[2]
    dd = np.sqrt(((dx)**2)+((dy)**2)+((dz)**2))
    # angulo = -1
    
    die = rce-rci
    
    if (dd <= rce):
        # Decisiones dentro del Radio externo
        angulo = math.atan2(dy,dx)
        angulo = math.degrees(angulo)
        # Angls.append(angulo)
        
        if ((dd > (die+rci))and(dd <= rce)):
            I = 70
        elif ((dd > rci)and(dd <= (rci+die))):
            I = 50
                    
        if ((angulo >= 150)and(angulo <= 180)):
            NM = 5          
        if ((angulo <= 30)and(angulo >= 0)):
            NM = 1
        if ((angulo > 30)and(angulo < 80)):
            NM = 2
        if ((angulo > 100)and(angulo < 150)):
            NM = 4
        if ((angulo >= 80)and(angulo <= 100)):
            NM = 3
            
    if (dd <= rci):
        # Decisiones dentro del radio intero
        angulo = math.atan2(dy,dx)
        angulo = math.degrees(angulo)
        # Angls.append(angulo)
        if (dd <= rci/2):
            I = 100
        elif ((dd > rci/2)and(dd <= rci)):
            I = 80
        
        # if (angulo >= 120):
        #     print("obstaculo a la izquierda")
            
        # if (angulo <= 60):
        #     print("obstaculo a la derecha")
        # if ((angulo > 60)and(angulo < 120)):
        #     print("Obstaculo enfrente")
        
        if ((angulo >= 150)and(angulo <= 180)):
            NM = 5              
        if ((angulo <= 30)and(angulo >= 0)):
            NM = 1
        if ((angulo > 30)and(angulo < 80)):
            NM = 2
        if ((angulo > 100)and(angulo < 150)):
            NM = 4
        if ((angulo >= 80)and(angulo <= 100)):
            NM = 3

            
    return(I,NM)



def vec_retro(TN,chch,metodo=0,rci=30,rce=80):
    # Como usarlos o alo así
    cc,lmts = losdatos(TN,chch)
    if   metodo==0: md = forma1(TN,chch) #Primer metodo
    elif metodo==1: md,NC = forma2(TN,chch,cc,lmts)
    elif metodo==2: md = forma3(TN,chch,cc,lmts) 

    #rci = 50; rce = 80
    lmd = len(md)
    vec_retro = [0,0,0,0,0]
    for nnn in range(0,lmd):
        dmd = md[nnn,:]
        I,NM = DangerDanger(dmd,rci,rce)
        #print(I,NM)
        if I>vec_retro[4-NM]:
            vec_retro[4-NM]=I

    print(vec_retro)
    return vec_retro
        # En esta parte pondrias la parte de vibración


#MOVIMIENTO DE LOS MOTORES VIBRADORES --------------------------------------------------------------------------
import threading
import RPi.GPIO as GPIO
import time

class PWM1(threading.Thread):
    """
    Clase para el control de los motores vibradores
    necesita como entrada una lista con el porcentaje
    del ciclo al que trabajará cada vibrador,
    de izquierda a derecha.
    Ej: CICLE = [1,10,50,100,20]
    ENTRADA -> clices
    SALIDA -> none
    """
    def __init__(self,cicles):
        super().__init__()
        self.CICLE=cicles
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.pwm=[]
        """
        NOTAS: PINES 11,13,15,16,18 EN USO
        """
        self.PIN=[11,13,15,16,18]
        for i in range(5):
            GPIO.setup(self.PIN[i], GPIO.OUT, initial=GPIO.LOW)
            self.pwm.append(GPIO.PWM(self.PIN[i],100))
    """
    Secuencia con la que vibrarán los motores por cada
    corrida
    """
    def run(self):
        for j in range(5):
            for i in range(5):
                GPIO.output(self.PIN[i], True)
                self.pwm[i].start(self.CICLE[i])
            time.sleep(0.2)
            for i in range(5):
                self.pwm[i].stop()
                GPIO.output(self.PIN[i], False)
            time.sleep(0.05)
        #Limpieza de pines
        #GPIO.cleanup()

"""
#CODIGO EJEMPLO
PIN=[11,12,13,15,16]
CICLE = [100,10,50,100,100]
thread1 = PWM1(CICLE)
thread1.start()
thread1.join() #Espeara a que termine su ejecución
print ("Exiting Main Thread")

GPIO.cleanup()
"""
#Codigo para limpiar pines
#import RPi.GPIO as GPIO
#GPIO.cleanup()
