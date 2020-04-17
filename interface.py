
import itertools
import os
import shutil
import sys
import threading
import time
import docx
import MainOperations
import PyQt5.QtGui
import PyQt5.QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QHBoxLayout, QLabel, QTreeView, QStyleFactory, QTextEdit)
from PyQt5.QtWidgets import QPushButton


f = None
txts = ""
text = ""
list = []
file = ""


class App(QWidget):


    FROM, SUBJECT, DATE = range(3)
    print("#####################")


    def __init__(self):
        super().__init__()

        global list


        self.title = 'Traitement de CV'
        self.left = 100
        self.top = 100
        self.width = 940
        self.height = 840


        self.initUI()



    def initUI(self):
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
        self.dataView.setStyleSheet("selection-background-color:rgb(50, 180,255);\n""border: 1px outset rgb(0, 150,255);\n""background-color: rgb(235, 235, 235);\n""font: 10pt \"Leelawadee UI\";\n""")
        self.dataView.setStyle(QStyleFactory.create("Fusion"))

        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.dataView)
        dataLayout.addWidget(self.textDisplay)
        self.dataGroupBox.setLayout(dataLayout)

        model = self.CreateModel(self)
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
        self.progressBar.setValue(0)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)


        insertButton = QPushButton("Insert", self)
        insertButton.clicked.connect(lambda: self.InsertMethod(model))
        deleteButton = QPushButton("Delete")
        deleteButton.clicked.connect(lambda: self.RemoveEntry(model))

        applyButton = QPushButton("Apply")
        applyButton.setStyle(QStyleFactory.create("Fusion"))
        applyButton.setStyleSheet("alternate-background-color: rgb(0,0,0);\n""background-color: rgb(50, 180,255);\n""font: 10pt \"Leelawadee UI\";\n""")
        applyButton.clicked.connect(lambda: self.ApplyButton())

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

        advancedLayout.addWidget(applyButton, 2 , 0,1,1)
        advancedLayout.addWidget(self.dataGroupBox, 0 , 0, 1, 3)
        advancedLayout.addWidget(self.progressBar, 2 , 1, 1, 2)
        advancedLayout.addWidget(self.infoDisplay, 3 , 1, 1, 2)
        advancedLayout.addWidget(selectButton, 3 , 0, 1 , 1)
        advancedLayout.addWidget(insertButton, 4 , 0, 1 , 1)
        advancedLayout.addWidget(deleteButton, 5 , 0, 1, 1)
        advancedLayout.addWidget(cancelButton, 6 , 0, 1, 1)



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
        global file, f, text
        # open data stream
        item = model.invisibleRootItem()
        text = self.ChangeCurrentProject(item)
        print (txts)
        print(txts + "\\" + text)
        f = docx.Document(file)
        firstDraft = [p.text for p in f.paragraphs]
        self.textDisplay.setPlainText(" ".join(firstDraft))


    def ChangeCurrentProject(self, item):
        file = open("CurrentProjectInf.bin", "wb")
        if item.rowCount() != None:
            a = self.dataView.selectedIndexes()
            if a != "[]":
                b = a[0].row()
                child = item.child(b, 0)
                c =child.text()
                return c

        file.close()
# --------------------------------------------------------------------------------------------------------------------


    def RemoveEntry(self, model):

        a = self.dataView.selectedIndexes()
        print (a)
        for x in range(0, len(a)):
            print(a[x])
        b  = a[x].row()
        item = model.invisibleRootItem()
        model.removeRow(b)

# --------------------------------------------------------------------------------------------------------------------
    def ApplyButton(self):
        #self.save_item()
        global f, file, txts
        if file == "":
            return
        result = MainOperations.Main.Naive(self, file)
        self.progressBar.setValue(result)


    def save_item(self, item, out):
        if item.rowCount() != None:
            for i in range(0, item.rowCount()):
                child = item.child(i,0)
                child.write(out)
                print(child.text())
                if child != None:
                    print("EEE")
                    self.save_item(child, out)
                else: return

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
        global file
        file = self.openFileNameDialog()
        self.addModel(model, file, 'insert', 'insert')
    def openFileNameDialog(self):

        options = PyQt5.QtWidgets.QFileDialog.Options()

        file, _ = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","CV(*.docx);", options=options)
        options = PyQt5.QtWidgets.QFileDialog.Options()
        file, _ = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        return file



    def addModel(self, model, From, subject, date):
        if From == "":
            return
        model.insertRow(0)
        model.setData(model.index(0, self.FROM), From)
        model.setData(model.index(0, self.SUBJECT), subject)
        model.setData(model.index(0, self.DATE), date)

# --------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------
    def CreateModel(self, parent):
        model = QStandardItemModel(0, 1, parent)
        model.setHeaderData(self.FROM, Qt.Horizontal, "Potential Texts Names")
        model.setHeaderData(self.SUBJECT, Qt.Horizontal, "Path")
        model.setHeaderData(self.DATE, Qt.Horizontal, "Contains")
        return model

# --------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
