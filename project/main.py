
# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import requests, json
import ntplib 
from time import ctime 
import time   
class MatplotlibWidget(QMainWindow):
  
    def __init__(self):
        
        QMainWindow.__init__(self)

        loadUi("test.ui",self)

        #set the title of the window 
        self.setWindowTitle("Projet supervision des réseaux éléctriques")

        #appeler la fonction update() a chaque appuie sur le bouton 
        self.pushButton.clicked.connect(self.update)
        
       
        #appeller la fonction showTime() chaque 10 secondes
        self.showTime()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.setInterval(10000)
        self.timer.start()

        #preparer une barre d'outils ou on peut manipuler la courbe 
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))
       


        #fonction permettant d'envoyer une requete pour obtenir le temps et l'afficher par la suite 
    def showTime(self):
         try:
            ntpClient=ntplib.NTPClient()
            response=ntpClient.request('pool.ntp.org')
            time=ctime(response.tx_time)
            self.date.setText(time[:16]+time[19:])
         except Exception as e:
            pass
       

           
        
    def update(self):
        #ouvrir le fichier excel et acceder aux donnees
        path = QFileDialog.getOpenFileName(self, 'Open Excel File', os.getenv('HOME'), 'xlsx(*.xlsx)')
        file= pd.ExcelFile(path[0])
        df=file.parse(0)
        prod=df['production']
        consom=df['consommation']
        batt=df['batterie']
        local=df['localisation']

        #afficher la localisation
        self.localisation.setText(local[0])

        #Temperature
        # Enter your API key here 
        api_key = "ae56bb2b3e2ff79ba5d5913812925885"
        # base_url variable to store url api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        # Give city name 
        city_name = local[0] 
        # complete url address 
        complete_url = base_url +"q=" + city_name+ "&appid=" + api_key  
        # return response object 
        response = requests.get(complete_url) 
        x = response.json()
        if x["cod"] != "404":
            y = x["main"] 
            current_temperature = round(y["temp"] -273.15,1)
            self.temperature.setText(str(current_temperature)+'°C')


        #afficher le niveau de charge de la batterie
        self.progressBar.setValue(batt[0])
        self.lcdNumber.display(batt[0])

        #dessiner la courbe de production et celle de la consommation 
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(prod)
        self.MplWidget.canvas.axes.plot(consom)
        #regler les axes des courbes 
        self.MplWidget.canvas.axes.set_xlabel('mois')
        self.MplWidget.canvas.axes.set_ylabel('kwh')
        self.MplWidget.canvas.axes.legend(('Production pv', 'Consommation'),loc='upper right')
        self.MplWidget.canvas.axes.set_title('aperçu du système l\'année dernière')
        self.MplWidget.canvas.draw()




        plt.style.use('seaborn')
        fig, ax1 = plt.subplots()
        ax1.plot(consom,label='consommation')
        ax1.plot(prod,label='production')
        ax1.legend()
        ax1.set_title('courbe')
        ax1.set_xlabel('mois')
        ax1.set_ylabel('kwh')
        plt.tight_layout()

        #sauvegarder la courbe sous l'extension png 
        fig.savefig('fig.png')

        #creation d'un fichier excel et insertion de la courbe dans le fichier
        writer = pd.ExcelWriter('plot.xlsx', engine = 'xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        worksheet = writer.sheets['Sheet1']
        worksheet.insert_image('F1','fig.png')
        writer.save()
        
# executer l'application        
app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()


   

   