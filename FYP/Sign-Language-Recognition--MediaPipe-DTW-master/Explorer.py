from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QWidget, QVBoxLayout
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import subprocess
from subprocess import call
import string,os,pathlib



class Ui_Dialog(object):
    def setupUi(self, Dialog,path_video):
        
        l=os.listdir(path_video)
        li=[]
        for i in l:
            if '.mp4' in i:
                li.append(i.split('.')[0])
        
        Dialog.setObjectName("Dialog")
        Dialog.resize(853, 529)
        
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 1000, 481))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(10, 1, 4, 0)




        path = f'{path_video}'
        self.dirModel = QFileSystemModel()
        self.dirModel.setRootPath(f'{path_video}')
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)
        self.fileModel = QFileSystemModel()
        self.fileModel.setFilter(QDir.NoDotAndDotDot |  QDir.Files)
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))

        self.treeview=QtWidgets.QTreeView(self.verticalLayoutWidget)
        self.treeview.setGeometry(QtCore.QRect(0, 0, 835, 921))
        self.verticalLayout.setObjectName("verticalLayout")

        self.treeview.setModel(self.model)
        self.treeview.setRootIndex(self.model.index(path))
        
        self.treeview.hideColumn(1)
        self.treeview.hideColumn(2)
        self.treeview.hideColumn(3)
        self.treeview.doubleClicked.connect(self.on_clicked)
        
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 500, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.close)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Back"))

    def close(self):
        Dialog.close()
        call(["python","Subjects_S.py"])

    def on_clicked(self,index):
        Dialog.close()
        path = self.fileModel.fileName(index)
        path=path.replace('.mp4','')
        print(path)
        print(path_video)
        subprocess.check_output(["python", 'Debug.py', str(path),path_video])

        
if __name__ == "__main__":
    import sys
    path=sys.argv[1:]
    print(path[0])
    path_video=path[0]
    print(path_video)
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog,path_video)
    Dialog.show()
    sys.exit(app.exec_())
    



