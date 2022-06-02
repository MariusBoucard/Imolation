import re
import shutil
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow,QLineEdit
from PyQt5.uic import loadUi
import subprocess
import platform
from PyQt5.QtCore import Qt, QSettings
import Reco as r
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow, QGraphicsScene,QGraphicsPixmapItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QSettings
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from importlib.resources import path
from PyQt5 import QtCore, QtGui,QtWidgets
from PyQt5.QtCore import QUrl,QRect
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow, QGraphicsScene,QGraphicsPixmapItem, QMessageBox,QListWidget, QSpinBox, QColumnView, QComboBox
import sys, os
from PyQt5.QtGui import QPainterPath
from datetime import datetime
from PyQt5.QtMultimedia import QMultimedia, QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QSettings

class MainWindow(QMainWindow):
       
    def __init__(self):
      super(QMainWindow,self).__init__()
      self.settings = QSettings("Imolation","Belle_Demoiselle")
      self.pathui=r.resource_path("main.ui")
      loadUi(self.pathui,self)
      #self.createdata()
      self.getdata()
      self.connections()
      

    def createdata(self):
        place = r.resource_path("data/")
        self.finder = r.LetsGoo(place)
        self.finder.recupladata(place)
        self.finder.getreponses("./reponses.csv")
        self.results=[]
        self.rangImg=0
        self.settings.setValue("Finder",self.finder)
        self.settings.setValue("Results",self.results)
        

    def getdata(self):  
      self.finder = self.settings.value("Finder")
      self.results = self.settings.value("Results")
      self.rangImg=0

    def connections(self):
        self.Validation.clicked.connect(self.search)
        self.Gauche.clicked.connect(self.gauche)
        self.Droite.clicked.connect(self.droite)
  
    def gauche(self):
            if self.rangImg >0 :
              self.updateUI(self.rangImg-1)
    def droite(self):
        if self.rangImg+1 <len(self.results) :
              self.updateUI(self.rangImg+1)

      
    def search(self):  
       recherche = self.Requete.text() 
       res = self.finder.request(recherche)
       print(res)
       self.results = res
       #self.results = self.finder.reponses
       #self.Arrayimg = list(self.finder.dico.keys())
       self.updateUI(0)

    def updateUI(self,indice):
          self.rangImg=indice 
          
          print("On a ca comme path : "+self.results[indice][0])
          path = r.resource_path("./data/"+str(self.results[indice][0]))
          self.image_qt = QImage(path)
          self.pixmap = QPixmap.fromImage(self.image_qt)
          w = self.Image.width()
          h=self.Image.height()
          self.Image.setPixmap(self.pixmap.scaled(w,h,Qt.KeepAspectRatio))
          self.Resultat.setText(str(self.results[indice][1]))

      
    
if __name__ == '__main__':
      app=QApplication(sys.argv)
      mainWindow=MainWindow()
      widget=QtWidgets.QStackedWidget()
      widget.addWidget(mainWindow)
      widget.setFixedWidth(900)
      widget.setFixedHeight(585)
      widget.show()
      sys.exit(app.exec_())