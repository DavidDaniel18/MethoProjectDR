import errno
import itertools
import shutil
import os
import threading
import time
from pathlib import Path



from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import (QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt,
                          QTime, QFile)
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QStandardItemModel
import PyQt5.QtGui
import  PyQt5.QtGui
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout, QPushButton,
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView, QVBoxLayout,
                             QWidget, QStyleFactory, QTextEdit)

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot
import ObjectParser
import ctypes, sys

f = None
txts = ""
text = ""
list = []
filename = "DataFrame.txt"




class Directory():
    def copy(src, dest):
        try:
            shutil.copytree(src, dest)
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                shutil.copy(src, dest)
            else:
                print('Directory not copied. Error: %s' % e)


class App(QWidget):


    FROM, SUBJECT, DATE = range(3)
    print("#####################")


    def __init__(self):
        super().__init__()

        global list, filename
        print(filename)
        data = ObjectParser.ObjectParser.Parser(self, filename)


        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!^^^^^^^^^^^^^^^^^^^^^")
        self.title = 'Traitement de CV'
        self.left = 100
        self.top = 100
        self.width = 940
        self.height = 840


        self.initUI(data)



    def initUI(self, data):
        self.setWindowTitle(self.title)
        self.setStyle(QStyleFactory.create("Fusion"))

        self.setGeometry(self.left, self.top, self.width, self.height)
        print(PyQt5.QtWidgets.QStyleFactory.keys())
        self.dataGroupBox = QGroupBox("CVs")
        self.dataView = QTreeView()
        self.dataView.setStyle((QStyleFactory.create("Fusion")))
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)


        advancedLayout = QGridLayout()

        #okButtonq.clicked.connect(self.runFunction())

        self.textDisplay = QTextEdit()
        self.textDisplay.setStyle(QStyleFactory.create("Fusion"))

        #ConsulAppObject.textEdit = QtWidgets.QInputDialog
        font = PyQt5.QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)

        self.textDisplay.setStyleSheet("alternate-background-color: rgb(50, 180,255);\n""background-color: rgb(225, 225, 225);\n""font: 9pt \"Leelawadee UI\";\n""")

        self.textDisplay.setObjectName("textDisplay")
        self.dataView.setStyleSheet("selection-background-color:rgb(50, 180,255); \n""alternate-background-color: rgb(0, 0,0);\n""border: 1px outset rgb(0, 150,255);\n""background-color: rgb(235, 235, 235);\n""font: 10pt \"Leelawadee UI\";\n""")
        self.dataView.setStyle(QStyleFactory.create("Fusion"))

        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.dataView)
        dataLayout.addWidget(self.textDisplay)
        self.dataGroupBox.setLayout(dataLayout)

        model = self.CreateMailModel(self)
        self.dataView.setModel(model)

        self.infoDisplay = QLabel()
        self.infoDisplay.setStyleSheet("selection-background-color:rgb(50, 180,255); \n""alternate-background-color: rgb(0, 0,0);\n""border: 1px outset rgb(0, 150,255);\n""background-color: rgb(235, 235, 235);\n""font: 10pt \"Leelawadee UI\";\n""")
        self.infoDisplay.setText("Likelihood of a match")
        self.infoDisplay.setAlignment(QtCore.Qt.AlignCenter)

        #mainLayout = QVBoxLayout()
        #mainLayout.addWidget(self.dataGroupBox)
        self.setLayout(advancedLayout)

        self.progressBar = PyQt5.QtWidgets.QProgressBar()

        self.progressBar.setStyleSheet("background-color: rgb(200, 200, 200);")
        self.progressBar.setValue(80)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)


        insertButton = QPushButton("Insert", self)
        insertButton.clicked.connect(lambda: self.InsertMethod(model))
        deleteButton = QPushButton("Delete")
       # deleteButton.setStyleSheet("font: 12pt")
        deleteButton.clicked.connect(lambda: self.RemoveEntry(model))

        applyButton = QPushButton("Apply")
        applyButton.setStyle(QStyleFactory.create("Fusion"))
        applyButton.setStyleSheet("alternate-background-color: rgb(0,0,0);\n""background-color: rgb(50, 180,255);\n""font: 10pt \"Leelawadee UI\";\n""")
        applyButton.clicked.connect(lambda: self.ApplyButton(model))

        selectButton = QPushButton("Select Text")
        selectButton.setStyle(QStyleFactory.create("Fusion"))
        selectButton.setStyleSheet("alternate-background-color: rgb(0,0,0);\n""font: 10pt \"Leelawadee UI\";\n""")
        selectButton.clicked.connect(lambda: self.OnChangeCurrentProjectClicked(model))

        cancelButton = QPushButton("Close")
        cancelButton.setStyle(QStyleFactory.create("Fusion"))
        cancelButton.setStyleSheet("alternate-background-color: rgb(0,0,0);\n""background-color: rgb(225,225,225);\n""font: 8pt \"Leelawadee UI\";\n""")
        cancelButton.clicked.connect(exit)
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        global txts
        txts = r"C:\Users\david\OneDrive\Documents\Automatisation Formatage\Template Textes"
        i = 0

        global list
        saveFile = open("bin.txt", 'r')
        index = saveFile.readlines()
        fileNames = []

        if index[1] == "ShowAll":
            for file in os.listdir(os.getcwd() +"\\Template Textes"):
                if file.endswith(".txt"):
                     fileNames.append(file)
        else:
            fileNames = data[int(index[0])].FileNames
        list = fileNames
        for file in range(0, len(list)):
            print(fileNames[file])
            self.addMail(model, fileNames[file], 'insert', 'insert')
            i+=1


        advancedLayout.addWidget(applyButton, 2 , 0,1,1)
        advancedLayout.addWidget(self.dataGroupBox, 0 , 0, 1, 3)
        advancedLayout.addWidget(self.progressBar, 2 , 1, 1, 2)
        advancedLayout.addWidget(self.infoDisplay, 3 , 1, 1, 2)
        advancedLayout.addWidget(selectButton, 3 , 0, 1 , 1)
        advancedLayout.addWidget(insertButton, 4 , 0, 1 , 1)
        advancedLayout.addWidget(deleteButton, 5 , 0, 1, 1)
        advancedLayout.addWidget(cancelButton, 6 , 0, 1, 1)

        #mainLayout.addWidget(applyButton)
        #mainLayout.addWidget(selectButton)
        #mainLayout.addWidget(insertButton)
        #mainLayout.addWidget(deleteButton)
        #mainLayout.addWidget(cancelButton)

        #thread = threading.Thread(target=self.animation, args=(self, "Waiting for input"))
        #thread.start()

        self.show()

    def animation(self, txtToDisplay):
        for c in itertools.cycle(['.', '..', '...', '\\']):
            print(threading.active_count())
            self.textEdit.setPlaceholderText(txtToDisplay + " " + c)
            if threading.active_count() == 3:
                return
            time.sleep(0.5)




    def ReadDat(self, model):
        file = QtCore.QFile("save.dat")
        file.open(QtCore.QIODevice.ReadOnly)
        goIn = QtCore.QDataStream(file)
        array = []
        self.ReadItem(model.invisibleRootItem(), array)
        file.close()
        return array

    def ReadItem(self, item, array = []):
        for i in range(0,item.rowCount()):
            child = item.child(i,0)
            print(child.text())
            array.append(child.text())
# --------------------------------------------------------------------------------------------------------------------
    def OnChangeCurrentProjectClicked(self, model):
        # create text file
        global txts, f, text
        #file.open(QtCore.QIODevice.WriteOnly)
        # open data stream
        #out = QtCore.QDataStream(file)
        print ("1")
        item = model.invisibleRootItem()
        text = self.ChangeCurrentProject(item)
        print ("2")
        print (txts)
        print(txts + "\\" + text)
        print("2.5")
        f = open(txts + "\\" + text, "r+")
        contents = f.read()
        f.close()
        print ("3")
        self.textDisplay.setPlainText(contents)
        print ("4")
        ######
        #i = QtCore.QDataStream(file)
        string=""
        #string = i.readRawData(100)
        print (string)





        print("WW")

    def ChangeCurrentProject(self, item):
        file = open("CurrentProjectInf.bin", "wb")
        if item.rowCount() != None:
            a = self.dataView.selectedIndexes()
            #a = self.dataView.selectedIndexes()
            print("changing project")
            print(a)
            if a != "[]":
                b = a[0].row()
                print("changing project...")
                child = item.child(b, 0)
                print(child.text())

                c =child.text()
                print("XXXXXXXXXX")

                return c

        file.close()
        print("@@@")
            #child.write(out)
# --------------------------------------------------------------------------------------------------------------------


    def RemoveEntry(self, model):

        a = self.dataView.selectedIndexes()
        print (a)
        for x in range(0, len(a)):
            print(a[x])
        #QtCore.QModelIndex
        print("@@@")
        b  = a[x].row()
        print (b)
        print("@@@")
        item = model.invisibleRootItem()
        print("@@@")
        child = item.child(b,0)
        childText = child.text()
        print(child.text())
        #self.GetName(model, child)
        print("@@@")
        model.removeRow(b)
        folders ="C:\\Users\\david\\OneDrive\\Documents\\Automatisation Formatage\\Template Textes\\"
        print("@@@")
        folders = folders + child.text()
        print("@@@")
        print(folders + childText)

        os.remove(folders)
        #os.chmod(folders, stat.S_IWRITE)
        print("SSS")
        #os.remove(folders)


#
 #   def GetName(self, model, qtObject):
  #          file = QtCore.QFile("save.dat")
   #         file.open(QtCore.QIODevice.ReadOnly)
    #        print("still here")
     #       self.FindQtObject(model.invisibleRootItem(), qtObject)
      #      file.close()


#    def FindQtObject(self, item, qtObject):
#
 #       for i in range(0,item.rowCount()):
  #          if item.child == qtObject:
   #             name = item.child(i,0)
    #            print (name.text())
            #print(child.text())

# --------------------------------------------------------------------------------------------------------------------
    def ApplyButton(self,model):
        #self.save_item()
        global f, text, txts
        if text == "":
            return
        currentPr = self.dataView.selectedIndexes()
        #file = QtCore.QFile("save.dat")
        #file.open(QtCore.QIODevice.WriteOnly)
        # open data stream
        a = self.dataView.selectedIndexes()
        item = model.invisibleRootItem()
        #a = self.dataView.selectedIndexes()
        print("changing project")
        print(a)
        if a != "[]":
            b = a[0].row()
            print("changing project...")

            child = item.child(b, 0)
            print(child.text())
        print("this is the text :" +str(text) + ", this is the txts : " + str(txts) + ", and this is f :" + str(f))
        print(text)
        print(child.text())
        print(os.getcwd()+"\\Template Textes\\" + text, os.getcwd()+"\\Template Textes\\" + child.text())
        os.rename(os.getcwd()+"\\Template Textes\\" + text, os.getcwd()+"\\Template Textes\\" + child.text())
        #os.rename(txts + "\\" + text)
        text = child.text()
        f = open(txts + "\\" + text,"r+")
        f.truncate(0)
        f.write(self.textDisplay.toPlainText())

        print (self.textDisplay.toPlainText())
        f.close()
        saveFile = open("bin.txt", 'r')
        index = saveFile.readlines()
        saveFile.close()
        file = open("color.txt", "w+")
        colors = file.read()
        if colors == "":
            file.write(index[0])
        else:
            file.write("\n"+index[0])
        file.close()
        #print(txts + "\\" + text)
        #print(os.getcwd() + "\\ChosenTexts\\" + index[0]+ ".txt")
        print("!!!!")
        print(txts + "\\" + text)
        print("!!!!")
        print(str(index[1]))
        print(os.getcwd() + "\\ChosenTexts\\" + str(index[1]) + ".txt")
        shutil.copy2(txts + "\\" + text, os.getcwd() + "\\ChosenTexts\\" + str(index[1]) + ".txt")
        print("!!!!")


        #out = QtCore.QDataStream(file)
        #self.on_save_button_clicked(model)
        #file.close()


    def on_save_button_clicked(self,model):
        print("@@@@")
        folders = os.getcwd()+"\\Template Textes"


        print(33333)

         #   print(22)
            #file.close()
        print(44444)
        #print(self.dataView.selectedIndexes())


    def save_item(self, item, out):
        print("!!!!##")
        if item.rowCount() != None:
            for i in range(0, item.rowCount()):
                child = item.child(i,0)
                child.write(out)
                print(child.text())
                print ("##")
                if child != None:
                    print("EEE")
                    self.save_item(child, out)
                else: return
        print("zzzzzzzzzz")

    def copy_rename(self, old_file_name, new_file_name):
        src_dir= os.curdir
        dst_dir= os.path.join(os.curdir , "subfolder")
        src_file = os.path.join(src_dir, old_file_name)
        shutil.copy(src_file,dst_dir)

        dst_file = os.path.join(dst_dir, old_file_name)
        new_dst_file_name = os.path.join(dst_dir, new_file_name)
        os.rename(dst_file, new_dst_file_name)

# --------------------------------------------------------------------------------------------------------------------
    def InsertMethod(self, model):
        #folders ="C:\\Users\\david\\OneDrive\\Documents\\ConsulApp\\Projects"
        #iteration = (len([f for f in os.listdir(folders)]))
        fn = os.getcwd()+"\\Template Textes\\empty.txt"
        try:
            file = open(fn, 'r')
        except IOError:
            file = open(fn, 'w')
        #path = "C:\\Users\\david\\OneDrive\\Documents\\ConsulApp\\Projects\\Project_"+str(iteration)
        #Directory.copy("C:\\Users\\david\\OneDrive\\Documents\\ConsulApp\\Source", path)
        self.addMail(model, 'empty.txt', 'insert', 'insert')

    def addMail(self, model, mailFrom, subject, date):
        if mailFrom == "":
            return
        model.insertRow(0)
        model.setData(model.index(0, self.FROM), mailFrom)
        model.setData(model.index(0, self.SUBJECT), subject)
        model.setData(model.index(0, self.DATE), date)

# --------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------
    def CreateMailModel(self, parent):
        model = QStandardItemModel(0, 1, parent)


        model.setHeaderData(self.FROM, Qt.Horizontal, "Potential Texts Names")
        model.setHeaderData(self.SUBJECT, Qt.Horizontal, "Path To Invoices")
        model.setHeaderData(self.DATE, Qt.Horizontal, "Contains DB")
        return model

# --------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
