# -*- coding: utf-8 -*-
"""

Otro solo RANSAC

"""

conversion.bytxt()
D = conversion.txt2array()
D = np.delete(D,0,axis=0)
DD = np.copy(D) # Creamos copia de datos para no afectar a los originales
abcd = np.array([[0,0,0,0]])
ldps = np.array([])
gplns = np.array([])

abcd,ldps,gplns = conversion.rnsc2(DD,abcd,ldps,gplns)
# abcd = np.delete(abcd,0,axis=0)
      
# Me falta ver eso de quitar piso y superficies más alla del tamaño del tipo
Ps = conversion.usar2(ldps,1)
# conversion.imprimirObjetos(Ps,ldplano,1,0)
conversion.imprimir3D(DD)
conversion.imprimirObjetos(Ps,ldps,1,0)

conversion.imprimirObjetos(Ps,ldps,2,0)
