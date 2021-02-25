
# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

     
class MatplotlibWidget(QMainWindow):
    
    def __init__(self):
        
        QMainWindow.__init__(self)

        loadUi("test.ui",self)

        self.setWindowTitle("Projet SRE")

        self.pushButton.clicked.connect(self.update_graph)

        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))


    def update_graph(self):
        path = QFileDialog.getOpenFileName(self, 'Open Rxcel File', os.getenv('HOME'), 'xlsx(*.xlsx)')

        plt.style.use('seaborn')
        file= pd.ExcelFile(path[0])
        df=file.parse(0)
        charge=df['charge']

       
        
        

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(charge)
        self.MplWidget.canvas.axes.plot( charge)
        self.MplWidget.canvas.axes.legend(('charge', 'charge'),loc='upper right')
        self.MplWidget.canvas.axes.set_title('Courbes')
        self.MplWidget.canvas.draw()
        plt.savefig('fig.png')

app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()