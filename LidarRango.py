import rplidar
from time import sleep,time
import numpy as np
import matplotlib.pyplot as plt


PuertoUSB = '/dev/ttyUSB0'
#Inicializacion
lidar = rplidar.RPLidar(PuertoUSB)
sleep(1)
info =lidar.get_info()
print(info)
process_scan = lambda scan: None

lidar.get_health()
lidar.connect()
lidar._serial_port.flushInput()
i=0
scan2 = []
for scan in lidar.iter_scans():
    process_scan(scan)
    scan2 =  scan2+scan
    i+=1

    if i>= 3:
        break
    
print(f"Muestras = {len(scan2)}")
scan=np.array(scan2)
lidar.stop()
lidar.stop_motor()
lidar.disconnect()

#PLOTEO
plt.figure(1)
plt.plot(scan[:,1],scan[:,2])
plt.show()

del(lidar)

# %%
