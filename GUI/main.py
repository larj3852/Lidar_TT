from PyQt5.QtWidgets import (QApplication, QMessageBox, QMainWindow, QVBoxLayout, QAction, QFileDialog, QDialog, QLabel, QSpinBox)
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
        self.Lista_Algoritmos.activated.connect(self.KMEANS_NUM_OBJETOS)
        #Incializacion Pantallas
        self.Inicializacion()
        #Declaracion variables globales
        self.dataSet = None
        #Añade el plot a los frames
        self.sc = myCanvas()
        self.sc2 = myCanvas()
        self.l = QVBoxLayout(self.reconstrucion)
        self.l.addWidget(self.sc)
        self.ll = QVBoxLayout(self.deteccion)
        self.ll.addWidget(self.sc2)

        #Conexion Botones
        self.corrida_1.clicked.connect(self.Prueba_Unitaria)
        self.reconstruir.clicked.connect(self.Reconstruir)
        self.Boton_Detectar.clicked.connect(self.Detectar)
        self.Boton_Comenzar.clicked.connect(self.Comenzar)
        self.Boton_Configuraciones.clicked.connect(self.Configuracion)
        self.Boton_Regresar.clicked.connect(self.Pantalla_Principal)
        #Sepa
        self.Qe = 0
        self.quit = 0
        self.p = 0
    
    def Inicializacion(self):
        #Vista/Ocultamiento de Pantallas
        self.Pantalla_Central.setVisible(False)
        self.Pantalla_Configuraciones.setVisible(False)
        self.Pantalla_Presentacion.setVisible(True)
        #Insertar LOGO UPIITA
        image = 'icons/Logo_UPIITA_2.png'
        self.UPIITA_LOGO.setStyleSheet("*{background-color:transparent;}")
        pixmap = QPixmap(image)
        self.UPIITA_LOGO.setPixmap(pixmap)
        self.UPIITA_LOGO.setScaledContents(True)
        #Insertar selector de Nubm. de objetos a detectar con K-MEANS
        self.k = QSpinBox(parent=self.Pantalla_Central)
        self.k.setValue(2)
        self.k.setMinimum(2)
        self.k.setMaximum(10)
        self.k.setGeometry(330,490,40,21)
        self.k.setVisible(True)
        #Inicializar/Desplegar Retroalimentacion
        #Personita
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
        #self.Motor_color = [Qt.yellow,Qt.red,Qt.green,Qt.red,Qt.yellow]
        self.Motor_color = [QColor(0X5E,0XF0,0X0A),QColor(0xAD,0xF7,0x0C),QColor(0xE0,0xDF,0x00),QColor(0XFA,0XE3,0X00),QColor(0XF0,0XC4,0X00),
                            QColor(0XF0,0X93,0X0C),QColor(0XFA,0X72,0X00),QColor(0XE0,0X46,0X01),QColor(0XFA,0X2C,0X00),QColor(0XF0,0X08,0X00)]
        Motor_Pos  = [[60,65],[120,20],[205,3],[290,20],[345,65]]
<<<<<<< HEAD
        Motor_Size = [[1,1,45,45],[1,1,45,45],[1,1,50,50],[1,1,45,45],[1,1,45,45]] #X,Y,ANCHO,ALTO
        #Motor1
=======
        Motor_Size = [[1,1,45,45],[1,1,45,45],[1,1,45,45],[1,1,45,45],[1,1,45,45]] #X,Y,ANCHO,ALTO
        #Dibujar Motores
>>>>>>> 5406a1ef646bfe8d0bca1cde824c76aeeed313dc
        for i in range(5):
            self.circuito.append(QLabel(parent=self.retroalimentacion))
            self.circuito[i].move(Motor_Pos[i][0],Motor_Pos[i][1])
            self.circuito[i].setStyleSheet("*{background-color:transparent;}")
            canvas = QPixmap(54,54)
            canvas.fill(Qt.transparent)
            self.circuito[i].setPixmap(canvas)
            self.dibujar.append(QPainter(self.circuito[i].pixmap()))
            self.dibujar[i].setPen(QPen(self.Motor_color[i],2,Qt.SolidLine))   
            self.dibujar[i].setBrush(QBrush(self.Motor_color[i],Qt.SolidPattern)) 
            self.dibujar[i].drawEllipse(Motor_Size[i][0],Motor_Size[i][1],Motor_Size[i][2],Motor_Size[i][3])
            #self.dibujar[i].end()
<<<<<<< HEAD
        
        self.dibujar[2].setPen(QPen(Qt.black,2,Qt.SolidLine))   
        self.dibujar[2].setBrush(QBrush(Qt.black,Qt.SolidPattern))
        self.dibujar[2].drawEllipse(10,10,10,20)
        self.dibujar[2].setCompositionMode(QPainter.CompositionMode_Source)
        self.dibujar[2].fillRect(0, 0, 500, 500, Qt.transparent)
=======
        self.Desplegar_Retroalimentacion(10)
>>>>>>> 5406a1ef646bfe8d0bca1cde824c76aeeed313dc

    def KMEANS_NUM_OBJETOS(self):
        if self.Lista_Algoritmos.currentText()=="K-Means":
            self.k.setVisible(True)
        else:   
            self.k.setVisible(False)

    def Comenzar(self):
        self.Pantalla_Presentacion.setVisible(False)
        self.Pantalla_Central.setVisible(True)

    def Desplegar_Retroalimentacion(self,diametro):
        for i in range(5):
            #Borrar Circulo
            self.dibujar[i].setCompositionMode(QPainter.CompositionMode_Clear)
            self.dibujar[i].eraseRect(0,0,55,55)
            self.dibujar[i].setCompositionMode(QPainter.CompositionMode_SourceOver)
            #Dibujar Circulo
            d= diametro//10-1
            self.dibujar[i].setPen(QPen(self.Motor_color[d],2,Qt.SolidLine))   
            self.dibujar[i].setBrush(QBrush(self.Motor_color[d],Qt.SolidPattern)) 
            d = int(diametro/2); offset= 26-int(d/2)
            self.dibujar[i].drawEllipse(offset,offset,d,d)
            self.circuito[i].repaint()

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
        #Metodo K-MEANS
        if self.Lista_Algoritmos.currentText()=="K-Means":
            
            #Inicio de la deteccion
            self.Label_Deteccion.setStyleSheet("*{color:red;}")
            self.Label_Deteccion.setText("Detectando "+str(self.k.value())+" Objetos...")
            self.Label_Deteccion.repaint()

            k = int(self.k.value())
            TN,chch = conversion.kk(self.dataSet,k)
            #Fin de la deteccion
            self.Label_Deteccion.setText("Deteccion")
            self.Label_Deteccion.setStyleSheet("*{color:#555;}")
            try:
                self.sc2.ImprimirOBjetos(self.dataSet,TN,chch,1,0)
            except:
                QMessageBox.critical(self, 'Erorre', "   Erore Plot")
            
            self.Desplegar_Retroalimentacion(k*10)
            return
        #Metodo DBSCAN
        if self.Lista_Algoritmos.currentText()=="DBSCAN":
            #Inicio de la deteccion
            self.Label_Deteccion.setStyleSheet("*{color:red;}")
            self.Label_Deteccion.setText("Detectando...")
            self.Label_Deteccion.repaint()

            Epsilon = 40 #35 #30
            MinPts =  20 #40 #75 #78
            chch = conversion.RObjetos(self.dataSet,Epsilon,MinPts)
            TN = conversion.usar(chch)
            #Fin de la deteccion
            self.Label_Deteccion.setText("Deteccion")
            self.Label_Deteccion.setStyleSheet("*{color:#555;}")
            try:
                self.sc2.ImprimirOBjetos(self.dataSet,TN,chch,1,0)
            except:
                QMessageBox.critical(self, 'Erorre', "   Erore Plot")
            return

    def Configuracion(self):
        self.Pantalla_Central.setVisible(False)
        self.Pantalla_Presentacion.setVisible(False)
        self.Pantalla_Configuraciones.setVisible(True)
    
    def Pantalla_Principal(self):
        self.Pantalla_Configuraciones.setVisible(False)
        self.Pantalla_Presentacion.setVisible(False)
        self.Pantalla_Central.setVisible(True)
    
    def closeEvent(self, event):
        #http://pythondiario.com/2014/12/dialogos-en-pyqt-con-qmessagebox-python.html
        reply = QMessageBox.question(self, 'Cerrar Aplicacion', '¿Estas seguro de cerrar la aplicación?',
				QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for i in range(5):
                self.dibujar[i].end()
            event.accept()
            #print('Window closed')
        else:
            event.ignore()


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