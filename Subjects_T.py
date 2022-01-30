from PyQt5 import QtCore, QtGui, QtWidgets
import Login
from subprocess import call
import subprocess
import string,os,pathlib

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(631, 492)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 460, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(190, 20, 241, 51))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 150, 91, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(260, 150, 91, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(460, 150, 91, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setGeometry(QtCore.QRect(50, 250, 91, 41))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(Dialog)
        self.pushButton_6.setGeometry(QtCore.QRect(260, 250, 91, 41))
        self.pushButton_6.setText("")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(Dialog)
        self.pushButton_7.setGeometry(QtCore.QRect(460, 250, 91, 41))
        self.pushButton_7.setText("")
        self.pushButton_7.setObjectName("pushButton_7")
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Logout"))
        self.textEdit.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; font-weight:600; font-style:italic; text-decoration: underline;\">Subjects</span></p></body></html>"))
        self.pushButton_2.setText(_translate("Dialog", "Science"))
        self.pushButton_3.setText(_translate("Dialog", "Computer"))
        self.pushButton_4.setText(_translate("Dialog", "Alphabets"))
        self.pushButton_5.setText(_translate("Dialog", "Assign Tests"))
        self.pushButton_6.setText(_translate("Dialog", "Student Details"))

        self.pushButton.clicked.connect(self.back)
        self.pushButton_2.clicked.connect(self.science)
        self.pushButton_3.clicked.connect(self.computer)
        self.pushButton_4.clicked.connect(self.alphabets)
        self.pushButton_5.clicked.connect(self.test)
        self.pushButton_6.clicked.connect(self.progress)

    def back(self):
        Dialog.close()
        call(["python","Login.py"])

    def science(self):
        Dialog.close()
        data_path=pathlib.Path.cwd().joinpath('videos_2\Science')
        subprocess.check_output(["python", 'Explorer_T.py', str(data_path)])

    def computer(self):
        Dialog.close()
        data_path=pathlib.Path.cwd().joinpath('videos_2\Computer')
        subprocess.check_output(["python", 'Explorer_T.py', str(data_path)])
    
    def alphabets(self):
        Dialog.close()
        data_path=pathlib.Path.cwd().joinpath('videos_2\Alphabets')
        subprocess.check_output(["python", 'Explorer_T.py', str(data_path)])
    
    def test(self):
        Dialog.close()
        data_path=pathlib.Path.cwd().joinpath('videos_2')
        subprocess.check_output(["python", 'TestAssign.py', str(data_path)])

    def progress(self):
        Dialog.close()
        call(["python","studentDatabase.py"])

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())



