#%%
#% cd "/home/pi/Python Scrips"
#% python3 RplidarPrueba_NUEVO.py
#  $ls /dev/*USB*

import rplidar
from time import sleep,time
import numpy as np
import matplotlib.pyplot as plt
from LibraryTT.Servo import Servo
import LibraryTT.txt2array as conversion
#%% SETTINGS
AInit = 80
AFin  = 70
paso = -1
PuertoUSB = '/dev/ttyUSB0'

#%% ------------------------- Prefunciones --------------------------
def recorte():
    lista = []
    for a in range(len(scan)):
        if scan[a,1]<150:
            lista.append(a)
    aux = scan[lista]
    return aux

data = np.array([[0],[0],[0]]) #Vector columna inicio

def empaquetamiento_cartesinano():
    aux  = np.concatenate(([x],[y],[z]),axis=0) #Concatena a = x,y,z
    aux = np.concatenate((data,aux),axis=1) #Concatena concatena planos
    return aux
#%% ------------------- INICIALIZACION LIDAR & SERVO ------------------
lidar = rplidar.RPLidar(PuertoUSB)
servo = Servo(AInit)
sleep(1)
info =lidar.get_info()
print(info)

lidar.get_health()
# plt.figure(1)
# plt.scatter(0,0,cmap="red")
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(0, 0, 0, marker='o');
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
#ax.set_ylim(-1,300)
ax.grid(True)
process_scan = lambda scan: None
#Angulos en Z
a=np.arange(AInit,AFin,paso)
b=['Orig']
for i in a: b.append(str(i))
phi=a*np.pi/180 #90 a 60
print(b)

#%%
t1 = time() #Inicio
T_LMS = 0   
for j in range(len(phi)):
    #print(len(lidar._serial_port.read_all()))
    servo.setAngle(a[j])
    lidar.connect()
    lidar._serial_port.flushInput()
    i=0
    for scan in lidar.iter_scans():
        process_scan(scan)
        i+=1

        if i>= 3:
            break
    print(f"Muestras = {len(scan)} , Ang= {a[j]}")
    T_LMS +=len(scan)
    scan=np.array(scan)
    scan = recorte()
    x = np.round(np.cos(np.pi-scan[:,1]*(np.pi/180))*scan[:,2]/10,decimals=3) #*np.sin(phi[j])*scan[:,2]/10
    y = np.round(np.sin(np.pi-scan[:,1]*(np.pi/180))*np.sin(phi[j])*scan[:,2]/10,decimals=3)
    #Nota, como el lidar está en 90° se le inverte la función sin(phi)
    z = np.round(np.sin(np.pi-scan[:,1]*(np.pi/180))*np.cos(phi[j])*scan[:,2]/10,decimals=3)
    #Empaqueta los datos en vector cartesiano
    data = empaquetamiento_cartesinano()
    print(f"Dimensiones {np.shape(data)}")
    #plt.scatter(x,y)
    ax.scatter(x, y, z, marker='.')
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()

# lidar.stop_motor()
# lidar.disconnect()
#lidar._serial_port._close()
servo.stop()
ax.legend(b)
t2=time()
print(f"Tiempo Total: {t2-t1}, Muestras totales: {T_LMS}")

conversion.array2txt(data)
conversion.array2csv(data)

plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
plt.show()



del(lidar)
del(fig)

# %%
