from PyQt5.QtWidgets import  QApplication, QMessageBox, QMainWindow, QVBoxLayout, QAction, QFileDialog
from PyQt5.QtGui import  QIcon
from matplotlib.figure import  Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasAgg as FigureCanvas
from PyQt5.uic import  loadUiType
from os.path import  dirname,realpath,join
from sys import argv
from  mpl_toolkits.mplot3d import  axis3d , axes3d

scrpitDir = dirname(realpath(__file__))
FORM_Main,_= loadUiType((join(dirname(__file__),"mainwindow.ui")))

class Main(QMainWindow,FORM_Main):
        def __init__(self,parent=FORM_Main):
            super(Main,self).__init__()
            QMainWindow.__init__(self)
            self.setupUi(self)
            self.Toolbar()  
            self.sc=myCanvas()
            self.l=QVBoxLayout(self.frame)
            self.l.addWidget(self.sc)

        def BrowserFolder(self):
            global filename
            filename,_=QFileDialog.getOpenFileName(self,"Open","","Text Files (*.txt);;Al Files(*)")

        def Toolbar(self):
            addFile = QAction(QIcon("icons/images.png"),'A',self) #Add icon for toolbar button
            addFile.triggered.connect(self.BrowserFolder)
            self.toolBar=self.addToolBar('Add data File')
            self.toolBar.addAction(addFile)
            addPlot = QAction(QIcon('icons/scatter.png'),'',self)
            addPlot.triggered.connect(self.Plot)
            self.toolBar.addAction(addPlot)
        def Get_List(self):
            with(openfilename) as f:
                array=[]

                for line in f:
                    array.append([float(x) for x in line.split()])
                Xarray = []
                Yarray = []
                Zarray = []
                for i in range(len(array)):
                    Xarray.append(array[i][0])
                    Yarray.append(array[i][1])
                    Zarray.append(array[i][2])
            return Xarray,Yarray,Zarray

        def Plot(self):
            x,y,z = Get_List(filename)
            self.sc.plot(x,y,z)


class myCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        FigureCanvas.__init__(self,self.fig)
    
    def plot(self,xarray,yarray,zarray):
        self.fig.clear()
        self.ax= self.fig.add_subplot(111,projection="3d")
        self.ax.scatter(xarray,yarray,zarray,marker='.')
        self.ax.plot(xarray,yarray,zarray,"ok")
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_zlabel('z')

def main():
    app = QApplication(argv)
    window = Main()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()