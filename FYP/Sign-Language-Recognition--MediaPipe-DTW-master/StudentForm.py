from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from sqlite3 import Error
from subprocess import call
import subprocess
import string,os,pathlib
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(794, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(170, 150, 571, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.StudentName = QtWidgets.QLabel(self.centralwidget)
        self.StudentName.setGeometry(QtCore.QRect(50, 150, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.StudentName.setFont(font)
        self.StudentName.setObjectName("StudentName")
        self.FatherName = QtWidgets.QLabel(self.centralwidget)
        self.FatherName.setGeometry(QtCore.QRect(50, 210, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.FatherName.setFont(font)
        self.FatherName.setObjectName("FatherName")
        self.RollNumber = QtWidgets.QLabel(self.centralwidget)
        self.RollNumber.setGeometry(QtCore.QRect(50, 270, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.RollNumber.setFont(font)
        self.RollNumber.setObjectName("RollNumber")
        
        self.phoneNumber = QtWidgets.QLabel(self.centralwidget)
        self.phoneNumber.setGeometry(QtCore.QRect(50, 330, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.phoneNumber.setFont(font)
        self.phoneNumber.setObjectName("phoneNumber")
        self.fatherPhoneNo = QtWidgets.QLabel(self.centralwidget)
        self.fatherPhoneNo.setGeometry(QtCore.QRect(400, 330, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.fatherPhoneNo.setFont(font)
        self.fatherPhoneNo.setObjectName("fatherPhoneNo")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(190, 40, 391, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(170, 210, 571, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(170, 270, 571, 31))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(530, 330, 211, 31))
        self.lineEdit_5.setObjectName("lineEdit_5")

        self.onlyInt = QtGui.QIntValidator()
        
        


        
        self.SubmitButton = QtWidgets.QPushButton(self.centralwidget)
        self.SubmitButton.setGeometry(QtCore.QRect(390, 480, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.SubmitButton.setFont(font)
        self.SubmitButton.setIconSize(QtCore.QSize(30, 30))
        self.SubmitButton.setObjectName("SubmitButton")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(400, 390, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_6.setGeometry(QtCore.QRect(170, 330, 211, 31))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(530, 390, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.spinBox.setFont(font)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(5)
        self.spinBox.setObjectName("spinBox")
        self.Gender = QtWidgets.QLabel(self.centralwidget)
        self.Gender.setGeometry(QtCore.QRect(50, 390, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.Gender.setFont(font)
        self.Gender.setObjectName("Gender")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(170, 390, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.comboBox.setFont(font)
        self.comboBox.setAutoFillBackground(False)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 794, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.lineEdit_6.setValidator(self.onlyInt)
        self.lineEdit_3.setValidator(self.onlyInt)
        self.lineEdit_5.setValidator(self.onlyInt)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "StudentForm"))
        self.StudentName.setText(_translate("MainWindow", "Student Name"))
        self.FatherName.setText(_translate("MainWindow", "Father Name"))
        self.RollNumber.setText(_translate("MainWindow", "Roll Number"))
        self.phoneNumber.setText(_translate("MainWindow", "Phone #"))
        self.fatherPhoneNo.setText(_translate("MainWindow", "Father Phone#"))
        self.label_3.setText(_translate("MainWindow", "STUDENT INFORMATION"))
        self.SubmitButton.setText(_translate("MainWindow", "Submit"))
        self.label_4.setText(_translate("MainWindow", "Class Enroll"))
        self.Gender.setText(_translate("MainWindow", "Gender"))
        
        self.comboBox.setItemText(0, _translate("MainWindow", "Male"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Female"))


        self.SubmitButton.clicked.connect(self.submit)

    def submit(self):
        std_name=self.lineEdit.text()
        fath_name=self.lineEdit_2.text()
        roll_no=int(self.lineEdit_3.text())
        phone=int(self.lineEdit_5.text())
        fath_phone=int(self.lineEdit_6.text())
        gender=self.comboBox.currentText()
        class_enroll=int(self.spinBox.value())

        print(std_name)
        print(fath_name)
        print(roll_no)
        print(phone)
        print(fath_phone)
        print(gender)
        print(class_enroll)

        data=(roll_no,std_name,fath_name,phone,fath_phone,gender,class_enroll)

        if std_name == '' or fath_name == '' or roll_no =='' or phone == '':
            print("Please Enter proper credentials")
        else:
            data_path=pathlib.Path.cwd().joinpath('Databases')
            conn = sqlite3.connect(f"{data_path}/Student_info.db")
            cur = conn.cursor()
            sql=''' INSERT INTO STD_IN (Roll_no,Student_Name,Father_Name,Phone,
                Fathers_Phone,Gender,Class_Enroll) VALUES (?,?,?,?,?,?,?) '''
            cur.execute(f'SELECT Roll_no  FROM STD_IN where Roll_no == {roll_no} ;')
            passw=cur.fetchone()
            
            print(passw)
            if passw==None:
                cur.execute(sql,data)
                conn.commit()
                conn.close()
                passw=subprocess.check_output([sys.executable, "Password.py"])
                passw=str(passw.decode("utf-8"))
                passw=passw[:-2]
                conn1 = sqlite3.connect(f"{data_path}/Login.db")
                cur2 = conn1.cursor()
                sql2=''' INSERT INTO LOGIN_s (Roll_No,Password) VALUES (?,?) '''
                task2=(roll_no,passw)
                cur2.execute(sql2,task2)
                conn1.commit()
                conn1.close()
                print("Data has been Entered")
                
                MainWindow.close()
                call(["python","Login.py"])
            else:
                print("The Data is already There with the entered roll no")
            
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
