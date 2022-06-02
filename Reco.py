from PIL import Image
from cv2 import RETR_CCOMP 
from pytesseract import pytesseract 
import pandas as pd
import sys
import os
import csv
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
#Import un truc pour gérer les resources


class LetsGoo():
    
    def __init__(self,path):
        self.path = path
        self.dico = {}
        self.reponses=[]

    def recupladata(self,path_data=None):
        if path_data==None:
            path_data = self.path
    #Import a frowler here to get the files et appeler le data parser
    #recuperer en crowlant les path
        image_path = self.scanfile(path_data)
        print("Scanfile successfull")
        dico_data={}
        for image in  image_path :
            text_image=self.parseimage(path_data+image)
            dico_data[image]=text_image.replace("\n"," ")
            print("imagescanned")
        self.dico = dico_data
        return dico_data

    def getreponses(self,path):
        reponses = open(path, mode ='r')
        csvFile = csv.reader(reponses)
        array = list(csvFile)
        rep = [90]
        print(array)
        print(len(array))
        for i in range(0,len(array)):
            aa = array[i]
            rep.append(aa)
        self.reponses = rep
        return rep

    def scanfile(self,path):
        paths= []

        
        paths =os.listdir(path=path)
        


        return paths

    def parseimage(self,image_path):
        img = Image.open(image_path) 
        text = pytesseract.image_to_string(img) 
        return text

    def addrep(self,a):
        self.reponses.append(a)

    def request(self,request):
        print("Lancement requete : \n\n\n\n")
        print(self.reponses)
        listchemins = []
        for path in self.dico.keys():
            if self.dico[path].__contains__(request):
                #Recup l id d image
                print(path)
                path2 = str(path)
                path2 =path2.replace(".jpg","")
                path2 =path2.replace(".png","")
                print("path = "+path2)
                num=int(path2)
                try : 
                    print(self.reponses)
                    reponse = self.reponses[num]
                except : 
                    reponse = "ca a chié"
                listchemins.append((path,reponse))
        return listchemins


if __name__ == '__main__':
    place = resource_path("data/")
    finder = LetsGoo(place)
    finder.dico = finder.recupladata(place)
    finder.reponses = finder.getreponses("./reponses.csv")
    res = finder.request("flux disponible")
    print(res)


   
    #print(dicc)