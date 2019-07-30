import sys
import threading
from multiprocessing import*
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from desain_GUI import Ui_mainWindow
import nltk, random, csv
from nltk.corpus import names
from nltk.tokenize import word_tokenize
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob


class Main (QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.Load_DataSet)
        self.ui.pushButton.clicked.connect(self.Print_Akurasi)
        self.ui.pushButton_2.clicked.connect(self.Proses_Klasifikasi)
        self.ui.progressBar

    def Load_DataSet(self):
        global clasifi
        global akurasi
        filename = QFileDialog.getOpenFileName(self, 'Open File', '/')
        self.ui.lineEdit.setText(filename)
        trainTweets = []
        testTweets = []
        with open(filename, 'rb') as csvfile: 
            reader = csv.reader(csvfile, delimiter=';', quotechar='|')  #pembatas ;      
            counter = 0
            for row in reader:
                kalimat = []
                kata = row[0].split() #memecah data 
                for i in kata:
                    i = i.lower()
                    i = i.strip('@#\'"?,.!')
                    kalimat.append(i)
                row[0] = kalimat
                if counter < 830:
                    trainTweets.append(row) #menambahakan trainTweets ke dalam row 
                else:
                    testTweets.append(row)
                counter += 1   
            clasifi = NaiveBayesClassifier(trainTweets)
            akurasi = format(clasifi.accuracy(testTweets)*100)
            
    def Proses_Klasifikasi(self):
        global clasifi     
        tweetWords = []
        tweet =  str(self.ui.lineEdit_3.text())
        words = tweet.split()
        for i in words:
            i = i.lower()
            i = i.strip('@#\'"?,.!')
            tweetWords.append(i)
        tweet = ' '.join(tweetWords)
        hasil = clasifi.classify(tweet)
        self.ui.lineEdit_4.setText(hasil)
        
    def Print_Akurasi(self):
        global akurasi
        selesai = 0
        while selesai < 100:
            selesai += 0.000005
            self.ui.progressBar.setValue(selesai)
        self.ui.lineEdit_2.setText(akurasi)
       

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    coba = Main()
    coba.show()
    sys.exit(app.exec_())

