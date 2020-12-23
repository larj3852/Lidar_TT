"""
Este archivo nada mas es para hacer pruebas uniarias joven
"""

import LibraryTT.Lidar3D as Lidar

scan = Lidar.Scaner3D()
a = scan.Scanear(Angulo_Init=130,Angulo_Fin=30,paso=-2,plotear=True)
del(scan.lidar)
del(scan)

#%%
# %%
