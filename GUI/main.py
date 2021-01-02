from PyQt5.QtWidgets import (QApplication, QMessageBox, QMainWindow, QVBoxLayout, QAction, QFileDialog, QDialog, QLabel)
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap, QPainter,  QBrush, QPen, QColor
from PyQt5.uic import loadUiType
from os.path import dirname, realpath, join
from sys import argv
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import axis3d ,axes3d
import matplotlib.pyplot as plt
from time import sleep
import LibraryTT.txt2array as conversion
import numpy as np

scriptDir = dirname(realpath(__file__))
FROM_MAIN, _ = loadUiType(join(dirname(__file__), "Prueba_1.ui"))

class Main(QMainWindow, FROM_MAIN):
    def __init__(self, parent = FROM_MAIN):
        super(Main, self).__init__()
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QIcon('icons/Logo_UPIITA.png'))
        #Definir algoritmos Aparicion
        self.Lista_Algoritmos.addItem("K-Means")
        self.Lista_Algoritmos.addItem("DBSCAN")
        self.Lista_Algoritmos.addItem("C")
        #Declaracion variables globales
        self.dataSet = None
        #Añade el plot a los frames
        self.sc = myCanvas()
        self.sc2 = myCanvas()
        self.l = QVBoxLayout(self.reconstrucion)
        self.l.addWidget(self.sc)
        self.ll = QVBoxLayout(self.deteccion)
        self.ll.addWidget(self.sc2)
        #PA CAMBIAR EL TEXTO PUES
        #
        
        self.Desplegar_Retroalimentacion()

        #Conexion Botones
        self.corrida_1.clicked.connect(self.Prueba_Unitaria)
        self.reconstruir.clicked.connect(self.Reconstruir)
        self.Boton_Detectar.clicked.connect(self.Detectar)
        #Sepa
        self.Qe = 0
        self.quit = 0
        self.p = 0
    
    def Desplegar_Retroalimentacion(self):
        image = 'icons/persona.png'
        try:
            with open(image):
                self.persona = QLabel(parent=self.retroalimentacion)
                self.persona.setStyleSheet("*{background-color:transparent;}")
                pixmap = QPixmap(image)
                self.persona.setPixmap(pixmap)
                self.persona.setScaledContents(True)
                #self.persona.move(180,100)
                self.persona.setGeometry(170,60,120,70)
        except FileNotFoundError:
            print("Image Not Found")

        #Retroalimentacion
        self.circuito = []
        self.dibujar = []
        self.Motor_color = [Qt.yellow,Qt.red,Qt.green,Qt.red,Qt.yellow]
        Motor_Pos  = [[60,65],[120,20],[205,3],[290,20],[345,65]]
        Motor_Size = [[1,1,45,45],[1,1,45,45],[1,1,45,45],[1,1,45,45],[1,1,45,45]] #X,Y,ANCHO,ALTO
        #Dibujar Motores
        for i in range(5):
            self.circuito.append(QLabel(parent=self.retroalimentacion))
            self.circuito[i].move(Motor_Pos[i][0],Motor_Pos[i][1])
            self.circuito[i].setStyleSheet("*{background-color:transparent;}")
            canvas = QPixmap(50,50)
            canvas.fill(Qt.transparent)
            self.circuito[i].setPixmap(canvas)
            self.dibujar.append(QPainter(self.circuito[i].pixmap()))
            self.dibujar[i].setPen(QPen(self.Motor_color[i],2,Qt.SolidLine))   
            self.dibujar[i].setBrush(QBrush(self.Motor_color[i],Qt.SolidPattern)) 
            self.dibujar[i].drawEllipse(Motor_Size[i][0],Motor_Size[i][1],Motor_Size[i][2],Motor_Size[i][3])
            self.dibujar[i].end()

    def Reconstruir(self):      
        conversion.bytxt()
        self.dataSet = conversion.txt2array()
        self.dataSet = np.delete(self.dataSet,0,axis=0)
        #DD = np.copy(D)
        try:
            self.sc.plot1(self.dataSet[:,0], self.dataSet[:,1], self.dataSet[:,2])
        except:
            QMessageBox.critical(self, 'Erorre', "   Erore Plot")
        
    def Prueba_Unitaria(self):
        if self.dataSet is None:
            return
        try:
            self.Reconstruir()
            self.Detectar()
        except:
            QMessageBox.critical(self, 'Erorre', "   Erore Plot")

    def Prueba_Continua(self):
        pass

    def Detectar(self):
        if self.dataSet is None:
            return
        
        if self.Lista_Algoritmos.currentText()=="K-Means":
            k = 5
            
            self.Label_Deteccion.setStyleSheet("*{color:red;}")
            self.Label_Deteccion.setText("Detectando...")
            self.Label_Deteccion.repaint()
            
            TN,chch = conversion.kk(self.dataSet,k)

            self.Label_Deteccion.setText("Deteccion")
            self.Label_Deteccion.setStyleSheet("*{color:#555;}")
            try:
                self.sc2.ImprimirOBjetos(self.dataSet,TN,chch,1,0)
            except:
                QMessageBox.critical(self, 'Erorre', "   Erore Plot")
        



    def Configuracion(self):
        pass
    def Quit(self):
        self.quit = 1
        self.MessageSave()


class myCanvas(FigureCanvas):

    def __init__(self):
        self.fig = Figure()
        FigureCanvas.__init__(self, self.fig)

    def plot1(self, xarray, yarray, zarray):
        self.fig.clear()
        self.ax = self.fig.add_subplot(111, projection = '3d')
        self.ax.mouse_init(rotate_btn = 1, zoom_btn = 3)
        self.ax.scatter(0,0,0,'ok')
        self.ax.plot(xarray, yarray, zarray, '.',color='orange')
        self.ax.set_xlabel('X ')
        self.ax.set_ylabel('Y ')
        self.ax.set_zlabel('Z ')
        self.ax.legend(['Set','Origen'])
        self.draw()
    
    def ImprimirOBjetos(self,DD,TN,chch,nnn,cho):
        
        self.fig.clear()
        #plt.ion()
        #figura = plt.figure()
        self.ax = self.fig.add_subplot(111,projection = '3d')
        self.ax.mouse_init(rotate_btn = 1, zoom_btn = 3)
        self.ax.set_xlim(min(DD[:,0])-25,max(DD[:,0])+25)
        self.ax.set_ylim(min(DD[:,1])-25,max(DD[:,1])+25)
        self.ax.set_zlim(min(DD[:,2])-25,max(DD[:,2])+25)
        
        # at = TN.shape
        vcolores = ['b','g','r','c','m','y','k','b','g','r','c','m','y','k','b','g','r','c','m','y','k','b','g','r','c','m']
        vformas = ['o','o','o','o','o','o','o','x','x','x','x','x','x','x','+','+','+','+','+','+','+','d','d','d','d','d']
        
        if (nnn == 0):
            # Sin datos ruido
            for ak in range(1,len(chch)):
                di1 = vcolores[ak]
                di2 = vformas[ak]
                # vl = TN[ak,:]
                vl = TN[ak,0:int(chch[ak]),:]
                                        
                [xi,yi,zi] = np.transpose(vl)
                self.ax.scatter(xi,yi,zi,
                                color = di1,
                                marker = di2)
            self.ax.set_xlabel('eje x')
            self.ax.set_ylabel('eje y')
            self.ax.set_zlabel('eje z')
            #grafica.legend()
            self.draw()
        
        elif (nnn == 1):
            # Con datos ruido
            
            for ak in range(0,len(chch)):
                di1 = vcolores[ak]
                di2 = vformas[ak]
                vl = TN[ak,0:int(chch[ak]),:]
                
                [xi,yi,zi] = np.transpose(vl)
                self.ax.scatter(xi,yi,zi,
                                color = di1,
                                marker = di2)
            self.ax.set_xlabel('eje x')
            self.ax.set_ylabel('eje y')
            self.ax.set_zlabel('eje z')
            #grafica.legend()
            self.draw()
            
        elif (nnn == 2):
            # Solo un cluster

            # for ak in range(0,at[0]):
            di1 = vcolores[cho]
            di2 = vformas[cho]
            vl = TN[cho,0:int(chch[cho]),:]        
            
            [xi,yi,zi] = np.transpose(vl)
            self.ax.scatter(xi,yi,zi,
                    color = di1,
                    marker = di2)

            self.ax.set_xlabel('eje x')
            self.ax.set_ylabel('eje y')
            self.ax.set_zlabel('eje z')
            #grafica.legend()
            self.draw()
        


def main():
    app = QApplication(argv)
    window = Main()
    window.show()  # Start position max screen
    app.exec_()


if __name__ == '__main__':
    main()