"""
Este archivo nada mas es para hacer pruebas uniarias joven
"""
import LibraryTT.Lidar3D as Lidar
from time import sleep

scan = Lidar.Scaner3D()
a = scan.Scanear(Angulo_Init=30,Angulo_Fin=150,paso=5,plotear=True)
sleep(2)
# a = scan.Scanear(Angulo_Init=130,Angulo_Fin=30,paso=-2,plotear=True)
# sleep(2)
# a = scan.Scanear(Angulo_Init=130,Angulo_Fin=30,paso=-1,plotear=True)
# del(scan.lidar)
# del(scan)
