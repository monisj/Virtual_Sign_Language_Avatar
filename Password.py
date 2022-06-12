from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(370, 142)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 81, 21))
        self.label.setObjectName("label")
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(20, 60, 92, 21))
        self.label2.setObjectName("label2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(120, 20, 201, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit2.setGeometry(QtCore.QRect(120, 60, 201, 20))
        self.lineEdit2.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(150, 100, 75, 23))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 370, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit2.setEchoMode(QtWidgets.QLineEdit.Password)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Set Password"))
        self.label.setText(_translate("MainWindow", "Enter Password"))
        self.label2.setText(_translate("MainWindow", "Re-Enter Password"))
        self.pushButton.setText(_translate("MainWindow", "Submit"))
        self.pushButton.clicked.connect(self.passw)
    def passw(self):
        if str(self.lineEdit.text())=="":
            popup=QMessageBox()
            popup.setWindowTitle("Enter Password")
            popup.setText("Please Enter a Password")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
        elif len(str(self.lineEdit.text()))<2:
            popup=QMessageBox()
            popup.setWindowTitle("Enter Password")
            popup.setText("Password Length Should be More than two characters")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
        else:
            if str(self.lineEdit2.text())=="":
                popup=QMessageBox()
                popup.setWindowTitle("Enter Password")
                popup.setText("Please Enter the Password Again")
                popup.setStandardButtons(QMessageBox.Ok)
                popup.setIcon(QMessageBox.Critical)
                popup.exec_()
            elif len(str(self.lineEdit2.text()))!= len(str(self.lineEdit.text())):
                popup=QMessageBox()
                popup.setWindowTitle("Enter Password")
                popup.setText("Password Length Does not match the previous Password")
                popup.setStandardButtons(QMessageBox.Ok)
                popup.setIcon(QMessageBox.Critical)
                popup.exec_()
            elif (self.lineEdit2.text())!= (self.lineEdit.text()):
                popup=QMessageBox()
                popup.setWindowTitle("Enter Password")
                popup.setText("Passwords do not match please Re-Enter Again")
                popup.setStandardButtons(QMessageBox.Ok)
                popup.setIcon(QMessageBox.Critical)
                popup.exec_()
            else:
                MainWindow.close()  
                print(str(self.lineEdit.text()))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("logo.png"))
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())