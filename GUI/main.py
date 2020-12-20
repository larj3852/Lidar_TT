from PyQt5.QtWidgets import (QApplication, QMessageBox, QMainWindow, QVBoxLayout, QAction, QFileDialog, QDialog, QLabel)
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap
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
                pixmap = QPixmap(image)
                self.persona.setPixmap(pixmap)
                self.persona.setScaledContents(True)
                #self.persona.move(180,100)
                self.persona.setGeometry(170,50,120,70)
        except FileNotFoundError:
            print("Image Not Found")


    def Plot3D(self):
        global filename
        
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Open", "", "Text Files (*.txt);;All Files (*)")
        #if filename:
        #    self.listWidget.clear()
        #   self.listWidget.addItem(filename)        
        
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