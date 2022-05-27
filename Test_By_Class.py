from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(370, 138)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 81, 21))
        self.label.setObjectName("label")
        # self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        # self.lineEdit.setGeometry(QtCore.QRect(120, 20, 201, 31))
        # self.lineEdit.setObjectName("lineEdit")

        self.AssignedClassComboBox_4 = QtWidgets.QComboBox(self.centralwidget)
        self.AssignedClassComboBox_4.setObjectName("AssignedClassComboBox_4")
        self.AssignedClassComboBox_4.setGeometry(QtCore.QRect(120, 20, 201, 31))
        self.AssignedClassComboBox_4.addItem("")
        self.AssignedClassComboBox_4.setItemText(0, "Please Select Class")
        self.AssignedClassComboBox_4.addItem("")
        self.AssignedClassComboBox_4.addItem("")
        self.AssignedClassComboBox_4.addItem("")
        self.AssignedClassComboBox_4.addItem("")
        self.AssignedClassComboBox_4.addItem("")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(150, 60, 75, 23))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 370, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Virtual Sign Teacher"))
        self.label.setText(_translate("MainWindow", "Select Class"))
        self.AssignedClassComboBox_4.setItemText(1, _translate("MainWindow", "1"))
        self.AssignedClassComboBox_4.setItemText(2, _translate("MainWindow", "2"))
        self.AssignedClassComboBox_4.setItemText(3, _translate("MainWindow", "3"))
        self.AssignedClassComboBox_4.setItemText(4, _translate("MainWindow", "4"))
        self.AssignedClassComboBox_4.setItemText(5, _translate("MainWindow", "5"))
        self.pushButton.setText(_translate("MainWindow", "Submit"))
        self.pushButton.clicked.connect(self.classw)
    def classw(self):
        if self.AssignedClassComboBox_4.currentText()=="Please Select Class":
            popup=QMessageBox()
            popup.setWindowTitle("Select Class")
            popup.setText("Please Select Class Before Submitting")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
        else:
            MainWindow.close()  
            print(str(self.AssignedClassComboBox_4.currentText()))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("logo.png"))
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())