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
import csv 
export_data = 0

class MainWindow(QMainWindow):
       
    def __init__(self):
      super(QMainWindow,self).__init__()
      self.settings = QSettings("Imolation","Belle_Demoiselle")
      self.pathui=r.resource_path("main.ui")
      loadUi(self.pathui,self)
      #self.createdata()
      
      self.connections()
      print("val de self settings" + str(self.settings))
      if self.settings.value("Finder") != None :
          print("loading du Finder")
          self.getdata()
      else:
            print("passage import")
            self.importer()
            
      if export_data==1:
            self.export()
            #self.importer()
            pass
      
    def export(self):
          filename = r.resource_path("save.csv")
           
          with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile) 
            print(self.finder.path)
            print(self.finder.dico)
            csvwriter.writerow([self.finder.path,"Reponses"])
            recuptuples =list(self.finder.dico.items())
            for i in range(len(recuptuples)) : 
                recuptuples[i] = (recuptuples[i][0],recuptuples[i][1],self.finder.reponses[i])
              
              
            for tuple in recuptuples :
                csvwriter.writerow([tuple[0],tuple[1],tuple[2]]) 
            

            print(self.finder.reponses)
          print(self.results)
    
    def importer(self):
        filename = r.resource_path("save.csv")
        filename2 = r.resource_path("reponses.csv")
        place = r.resource_path("data/")
        self.finder = r.LetsGoo(place)
        self.results=[]
        with open(filename, 'r') as csvfile:
          csvFile = csv.reader(csvfile)
          #self.finder.path = csvFile[0]
          # displaying the contents of the CSV file
          self.finder.reponses = []

          for lines in csvFile:
            
            self.finder.dico[lines[0]]=lines[1]
            ##A est bien la reponse, où était elle stock avant
            

          with open(filename2, 'r') as csvfile:
            csvFile = csv.reader(csvfile)
          #self.finder.path = csvFile[0]
          # displaying the contents of the CSV file
            self.finder.reponses = []
            self.finder.addrep("ladataaaa")
            
            for lines in csvfile:
              ##A est bien la reponse, où était elle stock avant
                a= lines
                self.finder.addrep(a)


          listkey=list(self.finder.dico.keys())
          for key in listkey :
                if key.__contains__("data"):
                      self.finder.path=key

          print(self.finder.reponses)
          self.settings.setValue("Finder",self.finder)
          self.settings.setValue("Results",self.results)

          print(self.finder.reponses)
          self.rangImg=0
         
        
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