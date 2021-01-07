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

scriptDir = dirname(realpath(__file__))
FROM_MAIN, _ = loadUiType(join(dirname(__file__), "Prueba_1.ui"))

class Main(QMainWindow, FROM_MAIN):
    def __init__(self, parent = FROM_MAIN):
        super(Main, self).__init__()
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QIcon('icons/Logo_UPIITA.png'))
        #Añade el plot al frame
        self.sc = myCanvas()
        self.sc2 = myCanvas()
        self.l = QVBoxLayout(self.reconstrucion)
        self.l.addWidget(self.sc)
        self.ll = QVBoxLayout(self.deteccion)
        self.ll.addWidget(self.sc2)
        #
        self.Desplegar_Retroalimentacion()
        #self.lll = QVBoxLayout(self.retroalimentacion)
        #self.lll.addWidget(self.Desplegar_Retroalimentacion())
        #
        self.corrida_1.clicked.connect(self.Plot3D)
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
        Motor_Size = [[1,1,45,45],[1,1,45,45],[1,1,50,50],[1,1,45,45],[1,1,45,45]] #X,Y,ANCHO,ALTO
        #Motor1
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
            #self.dibujar[i].end()
        
        self.dibujar[2].setPen(QPen(Qt.black,2,Qt.SolidLine))   
        self.dibujar[2].setBrush(QBrush(Qt.black,Qt.SolidPattern))
        self.dibujar[2].drawEllipse(10,10,10,20)
        self.dibujar[2].setCompositionMode(QPainter.CompositionMode_Source)
        self.dibujar[2].fillRect(0, 0, 500, 500, Qt.transparent)

    def Plot3D(self):
        global filename
        
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        
        filename, _ = QFileDialog.getOpenFileName(self, "Open", "", "Text Files (*.txt);;All Files (*)")
        if not(filename):
            return          #Si no se selecciona ningun archivo, nada.

        with open(filename) as f:

            array = []
            for line in f:  # read rest of lines
                array.append([float(x) for x in line.split()])
        n = len(array)

        try:
            if n < 4:
                QMessageBox.warning(self, 'Error!', "Number  of points < 4 !")
                return
        except:
            QMessageBox.critical(self, 'Erorre', "   No data File !")
        
        xarray=[]
        yarray=[] 
        zarray=[]

        with open(filename,"r") as file:
            a=file.read()
            for linea in a.split("\n"):
                line = linea.split("\t")
                try:
                    xarray.append(int(line[0]))
                    yarray.append(int(line[1]))
                    zarray.append(int(line[2]))
                except ValueError:
                    continue

            self.Qe = 1
            try:
                self.sc.plot1(xarray, yarray, zarray)
                self.sc2.plot1(xarray, yarray, zarray)
            except:
                QMessageBox.critical(self, 'Erorre', "   Erore Plot")


    def Quit(self):
        self.quit = 1
        self.MessageSave()


class myCanvas(FigureCanvas):

    def __init__(self):
        self.fig = Figure()
        FigureCanvas.__init__(self, self.fig)

    def plot2(self, xarray, yarray, zarray, za):
        self.fig.clear()
        self.ax = self.fig.add_subplot(111, projection = '3d')

        self.ax.mouse_init(rotate_btn = 1, zoom_btn = 3)

        self.ax.plot_trisurf(xarray, yarray, za, color = 'red', alpha = 0.6, edgecolor = 'red', linewidth = 0.1,
                             antialiased = True, shade = 1)

        self.ax.plot(xarray, yarray, zarray, 'ok')
        self.ax.set_xlabel('X ')
        self.ax.set_ylabel('Y ')
        self.ax.set_zlabel('Z ')
        
        self.draw()

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

    def plot2D(self, xarray, zarray):
        self.fig.clear()
        self.axe = self.fig.add_subplot(111)
        self.axe.plot(xarray, zarray, 'ok')
        self.axe.set_xlabel('X ')
        self.axe.set_ylabel('Y ')
        self.draw()

    def plot2DM(self, xarray, zarray, za):
        self.fig.clear()
        self.axe = self.fig.add_subplot(111)
        self.axe.plot(xarray, zarray, "ok")
        self.axe.plot(xarray, za, 'r-')
        self.axe.set_xlabel('X ')
        self.axe.set_ylabel('Y ')
        self.draw()

def main():
    app = QApplication(argv)
    window = Main()
    # window.showFullScreen() # Start at position full screen
    window.show()  # Start position max screen
    app.exec_()


if __name__ == '__main__':
    main()