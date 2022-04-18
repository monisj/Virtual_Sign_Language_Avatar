from fileinput import filename
from telnetlib import LOGOUT
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sqlite3
import pathlib,os,mediapipe,cv2
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from utils.dataset_utils import load_dataset, load_reference_signs,new_videos_load_dataset,new_load_reference_signs,newer_load_reference_signs,load_embeds
from utils.mediapipe_utils import mediapipe_detection
from utils.landmark_utils import save_landmarks_from_new_video
from sign_recorder import SignRecorder
from webcam_manager import WebcamManager
from pynput import keyboard
import time
import shutil
import trim
import sys
import pandas as pd
from cmath import inf
import subprocess

from UI import Ui_MainWindow

class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.user_remove=''
        self.test_roll_no=0
        self.sentences=[]
        self.std_roll_number=0
        self.test_sign=''
        self.test_path=''
        self.test_attempt=4
        self.test_accuracy=0
        self.acc2=0
        self.onlyInt = QtGui.QIntValidator()
        self.sentences_pass=0
        self.sentences_record=0
    ################## New widgets ######################
        self.dirModel = QFileSystemModel()
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)
        self.fileModel = QFileSystemModel()
        self.fileModel.setFilter(QDir.NoDotAndDotDot |  QDir.Files)
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.ui.treeview.setModel(self.model)
        self.ui.treeview.hideColumn(1)
        self.ui.treeview.hideColumn(2)
        self.ui.treeview.hideColumn(3)
        self.ui.treeview.doubleClicked.connect(self.select_video)

        self.ui.treeview_3.setModel(self.model)
        self.ui.treeview_3.hideColumn(1)
        self.ui.treeview_3.hideColumn(2)
        self.ui.treeview_3.hideColumn(3)
        self.ui.treeview_3.doubleClicked.connect(self.select_video_test)
        
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.ui.verticalLayout_30.addWidget(self.videoWidget)
        self.videoWidget.setMinimumSize(QtCore.QSize(352, 240))

        self.playlist = QMediaPlaylist()
        #self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile('videos/alphabet/a.mp4')))
        self.playlist.setPlaybackMode(self.playlist.Loop)
        self.mediaPlayer.setPlaylist(self.playlist)

    ################## Connections ######################
        self.ui.pushButton.clicked.connect(self.login)
        self.ui.pushButton_14.clicked.connect(self.New_User)
        self.ui.pushButton_9.clicked.connect(self.aphabets_folder)
        self.ui.pushButton_11.clicked.connect(self.science_folder)
        self.ui.pushButton_12.clicked.connect(self.computer_folder)
        self.ui.pushButton_16.clicked.connect(self.back_videos)
        self.ui.pushButton_21.clicked.connect(self.back_video)
        self.ui.pushButton_19.clicked.connect(self.play)
        self.ui.pushButton_19.setIcon(QtGui.QIcon('play-button.png'))
        self.ui.pushButton_17.clicked.connect(self.delete_video)
        self.ui.pushButton_18.clicked.connect(self.add_video)
        self.ui.horizontalSlider_4.sliderMoved.connect(self.setPosition)
        self.ui.passwordLineEdit.returnPressed.connect(self.login)
        self.ui.pushButton_20.clicked.connect(self.logout)
        self.ui.pushButton_222.clicked.connect(self.sentence_screen)
        self.ui.pushButton_22.clicked.connect(self.clear_sentences)
        self.ui.lineEdit_2.textChanged.connect(self.teachers_search)
        self.ui.lineEdit_3.textChanged.connect(self.students_search)
        self.ui.lineEdit_5.textChanged.connect(self.search_manage_tests)
        self.ui.pushButton_2.clicked.connect(self.manage_teachers)
        self.ui.pushButton_3.clicked.connect(self.manage_students)
        self.ui.pushButton_4.clicked.connect(self.manage_tests)
        self.ui.pushButton_5.clicked.connect(self.manage_courses)
        self.ui.tableWidget_5.cellDoubleClicked.connect(self.std_data)
        self.ui.pushButton_7.clicked.connect(self.Create_New_User)
        self.ui.pushButton_8.clicked.connect(self.logout)
        self.ui.pushButton_23.clicked.connect(self.Back_sentences)
        self.ui.pushButton_24.clicked.connect(self.add_space)
        self.ui.pushButton_25.clicked.connect(self.sentence_back)
        self.ui.pushButton_27.clicked.connect(self.logout)
        self.ui.pushButton_26.clicked.connect(self.teachers_back)
        self.ui.pushButton_6.clicked.connect(self.Remove_Student)


        #self.ui.pushButton_7.clicked.connect(self.students_info_back)
       
       
        self.ui.pushButton_29.clicked.connect(self.test_back)
        self.ui.pushButton_35.clicked.connect(self.test_back_screen)
        self.ui.pushButton_13.clicked.connect(self.test_screen)
        self.ui.pushButton_33.clicked.connect(self.submit_test)
        self.ui.pushButton_334.clicked.connect(self.back_progress)
        self.ui.pushButton_15.clicked.connect(self.progress)
        self.ui.pushButton_38.clicked.connect(self.back_manage_test)
        self.ui.pushButton_40.clicked.connect(self.back_assign_test)
        self.ui.pushButton_28.clicked.connect(self.students_info_back)
        self.ui.pushButton_31.clicked.connect(self.std_teach_back)
        self.ui.pushButton_39.clicked.connect(self.Add_Teacher)
        self.ui.pushButton_36.clicked.connect(self.Update_Teacher)
        self.ui.pushButton_37.clicked.connect(self.Remove_Teacher)
        self.ui.pushButton_41.clicked.connect(self.Add_Student)
        self.ui.pushButton_42.clicked.connect(self.Update_Student)
        self.ui.pushButton_43.clicked.connect(self.Add_Teacher_Back)
        self.ui.pushButton_44.clicked.connect(self.Add_Teacher_Credentials)
        self.ui.pushButton_45.clicked.connect(self.Update_Teacher_Credentials_Back)
        self.ui.pushButton_46.clicked.connect(self.Update_Teacher_Credentials_Submit)
        self.ui.pushButton_47.clicked.connect(self.Back_Add_Student)
        self.ui.pushButton_48.clicked.connect(self.Add_Student_Credentials)
        self.ui.pushButton_51.clicked.connect(self.Back_Update_Student)
        self.ui.pushButton_52.clicked.connect(self.Update_Student_Credentials_Submit)

        self.ui.tableWidget.cellDoubleClicked.connect(self.std_data_progress)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)

        #############Validators###################
        self.ui.lineEdit_2.setValidator(self.onlyInt)
        self.ui.lineEdit_3.setValidator(self.onlyInt)
        self.ui.usernameLineEdit.setValidator(self.onlyInt)
        self.ui.phoneNumberLineEdit.setValidator(self.onlyInt)
        self.ui.rollNumberLineEdit.setValidator(self.onlyInt)
        self.ui.fatherSPhoneNumberLineEdit.setValidator(self.onlyInt)
        self.ui.IDNumberLineEdit_4.setValidator(self.onlyInt)
        self.ui.phoneNumberLineEdit_4.setValidator(self.onlyInt)
        self.ui.rollNumberLineEdit_5.setValidator(self.onlyInt)
        self.ui.phoneNumberLineEdit_7.setValidator(self.onlyInt)
        self.ui.phoneNumberLineEdit_9.setValidator(self.onlyInt)
        self.ui.fatherSPhoneNumberLineEdit_5.setValidator(self.onlyInt)
        self.ui.fatherSPhoneNumberLineEdit_7.setValidator(self.onlyInt)
        self.ui.phoneNumberLineEdit_5.setValidator(self.onlyInt)

    

    def test_screen(self):
        self.ui.stackedWidget_2.setCurrentIndex(5)
        self.ui.treeWidget_2.clear()
        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
        conn = sqlite3.connect(f"{data_path}/Student_info.db")
        cur = conn.cursor()
        cur.execute(f'SELECT Sign_Name,Marks_Obtained,Test_Completed,Path FROM Student_Tests where ID == {self.std_roll_number};')
        passw=cur.fetchall()
        
        if passw==None:
            parent=QtWidgets.QTreeWidgetItem(1)
            parent.setText(0,"No Tests Are Assigned #Winning")
            self.ui.treeWidget_2.addTopLevelItem(parent)
        else:
            for i in passw:
                if i[2]=="No":
                    parent=QtWidgets.QTreeWidgetItem(1)
                    parent.setText(0,f"{i[0]}")
                    self.ui.treeWidget_2.addTopLevelItem(parent)

            
            
                    conn.close()
            self.ui.treeWidget_2.itemClicked.connect(self.perform_test)

    def test_back_screen(self):
        self.ui.stackedWidget_2.setCurrentIndex(0)

    def progress(self):
        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
        conn = sqlite3.connect(f"{data_path}/Student_info.db")
        cur = conn.cursor()
        cur.execute(f'SELECT ID,Sign_Name,Marks_Obtained,Test_Completed FROM Student_Tests where ID == {self.std_roll_number};')
        passw=cur.fetchall()
        conn.close()
        for details in passw:
            row_number = self.ui.tableWidget_4.rowCount()
            if row_number == len(passw):
                pass
            else:
                self.ui.tableWidget_4.insertRow(row_number)
            for column_number, data in enumerate(details):
                self.ui.tableWidget_4.setItem(
                row_number, column_number, QTableWidgetItem(str(data)))
        self.ui.stackedWidget_2.setCurrentIndex(6)
    
    def std_data(self):
        current_row = self.ui.tableWidget_5.currentRow()
        current_column = self.ui.tableWidget_5.currentColumn()
        if current_column!=0:
            pass
        else:
            self.test_roll_no = self.ui.tableWidget_5.item(current_row, current_column).text()
            path=pathlib.Path(__file__).parent.absolute().joinpath('videos')
            path=str(path)
            self.dirModel.setRootPath(path)
            self.ui.treeview_3.setRootIndex(self.model.index(path))
            self.ui.stackedWidget.setCurrentIndex(5)
    def std_teach_back(self):
        self.ui.tableWidget_6.setRowCount(0)
        self.ui.stackedWidget.setCurrentIndex(3)

    def std_data_progress(self):
        current_row = self.ui.tableWidget.currentRow()
        current_column = self.ui.tableWidget.currentColumn()
        
        if current_column!=0:
            pass
        else:
            self.test_roll_no = self.ui.tableWidget.item(current_row, current_column).text()
            self.ui.stackedWidget.setCurrentIndex(3)
            data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
            conn = sqlite3.connect(f"{data_path}/Student_info.db")
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM Student_Tests Where ID = {self.test_roll_no};')
            passw=cur.fetchall()
            conn.close()
            for details in passw:
                row_number = self.ui.tableWidget_6.rowCount()
                if row_number == len(passw):
                    pass
                else:
                    self.ui.tableWidget_6.insertRow(row_number)
                for column_number, data in enumerate(details):
                    self.ui.tableWidget_6.setItem(
                    row_number, column_number, QTableWidgetItem(str(data)))
            self.ui.stackedWidget.setCurrentIndex(8)

    def Add_Teacher(self):
        #b=self.retrieveTeacherinfoValue()
        self.ui.stackedWidget.setCurrentIndex(9)
        
    def Add_Teacher_Credentials(self):
        popup=QMessageBox()
        if self.ui.TeachersNameLineEdit_4.text()=="" or self.ui.AssignedSubjectsComboBox_4.currentText()=="Please Select Subjects" or self.ui.IDNumberLineEdit_4.text()=="" or self.ui.phoneNumberLineEdit_4.text()=="" or self.ui.AssignedClassComboBox_4.currentText()=="Please Select Class":
            popup.setWindowTitle("Create Teacher User")
            popup.setText("Please Enter All Fields")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
        else:
            teach_name=self.ui.TeachersNameLineEdit_4.text()
            teach_assign_subj=self.ui.AssignedSubjectsComboBox_4.currentText()
            teach_id=self.ui.IDNumberLineEdit_4.text()
            teach_ph_no=self.ui.phoneNumberLineEdit_4.text()
            teach_assign_class=self.ui.AssignedClassComboBox_4.currentText()
            if int(teach_id) <=10000:
                popup.setWindowTitle("Create Teacher User")
                popup.setText("Teacher ID Cannot Be Less than 1000x")
                popup.setStandardButtons(QMessageBox.Ok)
                popup.setIcon(QMessageBox.Critical)
                popup.exec_()
            else:
                data=(teach_id,teach_name,teach_assign_subj,teach_ph_no,teach_assign_class)
                data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
                conn = sqlite3.connect(f"{data_path}/Login.db")
                cur = conn.cursor()
                cur.execute(f'SELECT Roll_No From LOGIN_S WHERE Roll_no = {teach_id};')
                passw=cur.fetchall()

                if passw==None:
                    data=(teach_id,teach_name,teach_assign_subj,teach_ph_no,teach_assign_class)
                    data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
                    conn = sqlite3.connect(f"{data_path}/Teachers_info.db")
                    cur = conn.cursor()
                    sql=''' INSERT INTO Teacher_info (ID,Name,Assigned_Subjects,Phone_No,
                            Assigned_Class) VALUES (?,?,?,?,?) ''' 
                    cur.execute(sql,data)
                    conn.commit()
                    conn.close()
                    passw=subprocess.check_output([sys.executable, "Password.py"])
                    passw=str(passw.decode("utf-8"))
                    passw=passw[:-2]
                    data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
                    conn = sqlite3.connect(f"{data_path}/Login.db")
                    cur = conn.cursor()
                    sql2=''' INSERT INTO LOGIN_S (Roll_No,Password,Type) VALUES (?,?,?) '''
                    task2=(teach_id,passw,"T")
                    cur.execute(sql2,task2)
                    conn.commit()
                    conn.close()
                            
                    self.ui.tableWidget_2.setRowCount(0)  
                    self.manage_teachers()
                    popup.setWindowTitle("Create Teacher User")
                    popup.setText(f'Teacher with ID ={teach_id} Has Been Added')
                    popup.setStandardButtons(QMessageBox.Ok)
                    popup.setIcon(QMessageBox.Information)
                    popup.exec_()
                elif passw==[]:
                    data=(teach_id,teach_name,teach_assign_subj,teach_ph_no,teach_assign_class)
                    data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
                    conn = sqlite3.connect(f"{data_path}/Teachers_info.db")
                    cur = conn.cursor()
                    sql=''' INSERT INTO Teacher_info (ID,Name,Assigned_Subjects,Phone_No,
                            Assigned_Class) VALUES (?,?,?,?,?) ''' 
                    cur.execute(sql,data)
                    conn.commit()
                    conn.close()
                    passw=subprocess.check_output([sys.executable, "Password.py"])
                    passw=str(passw.decode("utf-8"))
                    passw=passw[:-2]
                    data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
                    conn = sqlite3.connect(f"{data_path}/Login.db")
                    cur = conn.cursor()
                    sql2=''' INSERT INTO LOGIN_S (Roll_No,Password,Type) VALUES (?,?,?) '''
                    task2=(teach_id,passw,"T")
                    cur.execute(sql2,task2)
                    conn.commit()
                    conn.close()
                            
                    self.ui.tableWidget_2.setRowCount(0)  
                    self.manage_teachers()
                    popup.setWindowTitle("Create Teacher User")
                    popup.setText(f'Teacher with ID ={teach_id} Has Been Added')
                    popup.setStandardButtons(QMessageBox.Ok)
                    popup.setIcon(QMessageBox.Information)
                    popup.exec_()
                    
                    self.ui.stackedWidget.setCurrentIndex(2)
                else:
                    popup.setWindowTitle("Create Teacher User")
                    popup.setText(f'The Roll Number Already Exsists')
                    popup.setStandardButtons(QMessageBox.Ok)
                    popup.setIcon(QMessageBox.Critical)
                    popup.exec_()

    def Add_Teacher_Back(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def Teacher_Update_button(self,i):
        if i.text() == '&Yes' :
            data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
            conn = sqlite3.connect(f"{data_path}/Teachers_info.db")
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM Teacher_Info where ID == {self.user_remover};')
            passw=cur.fetchall()
            conn.close()
            temp=passw[0]
            self.ui.TeachersNameLineEdit_5.setText(temp[1])
            self.ui.AssignedSubjectsComboBox_5.setItemText(0,temp[2])
            self.ui.IDNumberLineEdit_5.setText(str(temp[0]))
            self.ui.phoneNumberLineEdit_5.setText(str(temp[3]))
            self.ui.AssignedClassComboBox_5.setItemText(0,str(temp[4]))
            self.ui.stackedWidget.setCurrentIndex(10)
            self.user_remover=''
        else:
            pass

    def Teacher_Update(self):           
        popup=QMessageBox()
        if self.ui.TeachersNameLineEdit_5.text()=="" or self.ui.AssignedSubjectsComboBox_5.currentText()=="Please Select Subjects" or self.ui.IDNumberLineEdit_5.text()=="" or self.ui.phoneNumberLineEdit_5.text()=="" or self.ui.AssignedClassComboBox_5.currentText()=="Please Select Class":
            popup.setWindowTitle("Update Teacher User")
            popup.setText("Please Enter All Fields")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
        else:
            teach_name=self.ui.TeachersNameLineEdit_5.text()
            teach_assign_subj=self.ui.AssignedSubjectsComboBox_5.currentText()
            teach_id=self.ui.IDNumberLineEdit_5.text()
            teach_ph_no=self.ui.phoneNumberLineEdit_5.text()
            teach_assign_class=self.ui.AssignedClassComboBox_5.currentText()
            data=(teach_name,teach_assign_subj,teach_ph_no,teach_assign_class,teach_id)
            data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
            conn = sqlite3.connect(f"{data_path}/Teachers_info.db")
            cur = conn.cursor()
            sql=''' UPDATE Teacher_info
                    SET Name = ?, Assigned_Subjects= ? ,Phone_No = ?, Assigned_Class=?
                    WHERE ID = ?''' 
            cur.execute(sql,data)
            conn.commit()
            conn.close()   
            self.ui.tableWidget_2.setRowCount(0)  
            self.manage_teachers()
            popup.setWindowTitle("Update Teacher User")
            popup.setText(f'Teacher Information Has Been Updated')
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Information)
            popup.exec_()
            self.ui.stackedWidget.setCurrentIndex(2)


        
        

    def Update_Teacher_Credentials_Back(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def Teach_Update(self,i):
        if i.text() == '&Yes' :
            self.Teacher_Update()
        else:
            pass

    def Update_Teacher_Credentials_Submit(self):
        popup=QMessageBox()
        popup.setWindowTitle("Update Teacher")
        popup.setText(f"Are you sure you want to Update Teacher Information")
        popup.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        popup.setIcon(QMessageBox.Information)
        popup.buttonClicked.connect(self.Teach_Update)
        popup.exec_()

    def Update_Teacher(self):
        b=self.retrieveTeacherinfoValue()
        
        if b==[]:
            popup=QMessageBox()
            popup.setWindowTitle("Update Teacher")
            popup.setText(f"First Select Teachers To Update Their Information")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Information)
            popup.exec_()
        elif len(b)>1:
            popup=QMessageBox()
            popup.setWindowTitle("Update Teacher")
            popup.setText(f"You can only update Information of One Teacher At a Time")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Information)
            popup.exec_()
        else:
            temp=b[0]
            self.user_remover=temp[0]
            popup=QMessageBox()
            popup.setWindowTitle("Update Teacher")
            popup.setText(f"Are you sure you want to Update Teacher Information")
            popup.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            popup.setIcon(QMessageBox.Information)
            popup.buttonClicked.connect(self.Teacher_Update_button)
            popup.exec_()

   

    def Teacher_Remove_button(self,i):
        if i.text() == '&Yes' :
            b=self.retrieveTeacherinfoValue()
            if len(b)==1:
                temp=b[0]
                self.user_remove=temp[0]
                data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
                conn = sqlite3.connect(f"{data_path}/Teachers_info.db")
                cur = conn.cursor()
                cur.execute(f'DELETE FROM Teacher_Info WHERE ID = {self.user_remove};')
                conn.commit()
                conn.close()

                conn = sqlite3.connect(f"{data_path}/Login.db")
                cur = conn.cursor()
                cur.execute(f'DELETE FROM Login_S WHERE Roll_No = {self.user_remove};')
                conn.commit()
                conn.close()

                self.ui.tableWidget_2.setRowCount(0)  
                self.manage_teachers()
                popup=QMessageBox()
                popup.setWindowTitle("Remove Teacher")
                popup.setText(f"The Teacher with ID = {self.user_remove} Has Been Removed")
                popup.setStandardButtons(QMessageBox.Ok)
                popup.setIcon(QMessageBox.Information)
                popup.exec_()
                
                self.user_remove=''
            else:
                b=self.retrieveTeacherinfoValue()
                
                for i in range(len(b)):
                    temp=b[i]
                    self.user_remove=temp[0]
                    data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
                    conn = sqlite3.connect(f"{data_path}/Teachers_info.db")
                    cur = conn.cursor()
                    cur.execute(f'DELETE FROM Teacher_Info WHERE ID = {self.user_remove};')
                    conn.commit()
                    conn.close()

                    conn = sqlite3.connect(f"{data_path}/Login.db")
                    cur = conn.cursor()
                    cur.execute(f'DELETE FROM Login_S WHERE Roll_No = {self.user_remove};')
                    conn.commit()
                    conn.close()
                    self.user_remove=''
                self.ui.tableWidget_2.setRowCount(0)  
                self.manage_teachers()
                popup=QMessageBox()
                popup.setWindowTitle("Remove Teacher")
                popup.setText(f"The Selected Teachers Have Been Removed")
                popup.setStandardButtons(QMessageBox.Ok)
                popup.setIcon(QMessageBox.Information)
                popup.exec_()

    def Remove_Teacher(self):
        b=self.retrieveTeacherinfoValue()
        if b==[]:
            popup=QMessageBox()
            popup.setWindowTitle("Remove Teacher")
            popup.setText(f"First Select Teachers To Remove ")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Information)
            popup.exec_()
        else:
            popup=QMessageBox()
            popup.setWindowTitle("Remove Teacher")
            popup.setText(f"Are you Sure to Remove The Teacher ")
            popup.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            popup.setIcon(QMessageBox.Information)
            popup.buttonClicked.connect(self.Teacher_Remove_button)
            popup.exec_()

    

    def Add_Student(self):
        self.ui.stackedWidget.setCurrentIndex(11)

    def Add_Student_Credentials(self):
        popup=QMessageBox()
        if self.ui.studentNameLineEdit_5.text()=="" or self.ui.fatherSNameLineEdit_5.text()=="" or self.ui.rollNumberLineEdit_5.text()=="" or self.ui.phoneNumberLineEdit_7.text()=="" or self.ui.fatherSPhoneNumberLineEdit_5.text()=="" or self.ui.gradeComboBox_5.currentText()=="":
            popup.setWindowTitle("Add Student User")
            popup.setText("Please Enter All Fields")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
        else:
            std_name=self.ui.studentNameLineEdit_5.text()
            std_father_name=self.ui.fatherSNameLineEdit_5.text()
            std_roll_no=self.ui.rollNumberLineEdit_5.text()
            std_ph_no=self.ui.phoneNumberLineEdit_7.text()
            std_fathers_ph_no=self.ui.fatherSPhoneNumberLineEdit_5.text()
            std_class=self.ui.gradeComboBox_5.currentText()

            if self.ui.radioButton_9.isChecked():
                gender="Male"
            elif self.ui.radioButton_10.isChecked():
                gender="Female"

           
            data=(std_name,std_father_name,std_ph_no,std_fathers_ph_no,gender,std_class,std_roll_no)
            if int(std_roll_no) >=5000:
                popup.setWindowTitle("Add Student User")
                popup.setText("Teacher ID Cannot Be More Than than 5000x")
                popup.setStandardButtons(QMessageBox.Ok)
                popup.setIcon(QMessageBox.Critical)
                popup.exec_()
            else:
                data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
                conn = sqlite3.connect(f"{data_path}/Login.db")
                cur = conn.cursor()
                cur.execute(f'SELECT Roll_No From LOGIN_S WHERE Roll_no = {std_roll_no};')
                passw=cur.fetchall()

                if passw==None:
                    data=(std_roll_no,std_name,std_father_name,std_ph_no,std_fathers_ph_no,gender,std_class)
                    data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
                    conn = sqlite3.connect(f"{data_path}/Student_info.db")
                    cur = conn.cursor()
                    sql=''' INSERT INTO Teacher_info (Roll_No,Student_Name,Father_Name,Phone,Fathers_Phone,Gender,
                            Class_Enroll) VALUES (?,?,?,?,?,?,?) ''' 
                    cur.execute(sql,data)
                    conn.commit()
                    conn.close()
                    passw=subprocess.check_output([sys.executable, "Password.py"])
                    passw=str(passw.decode("utf-8"))
                    passw=passw[:-2]
                    data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
                    conn = sqlite3.connect(f"{data_path}/Login.db")
                    cur = conn.cursor()
                    sql2=''' INSERT INTO LOGIN_S (Roll_No,Password,Type) VALUES (?,?,?) '''
                    task2=(std_roll_no,passw,"S")
                    cur.execute(sql2,task2)
                    conn.commit()
                    conn.close()
                            
                    self.ui.tableWidget.setRowCount(0)  
                    self.manage_students()
                    popup.setWindowTitle("Add Student User")
                    popup.setText(f'Student with ID ={std_roll_no} Has Been Added')
                    popup.setStandardButtons(QMessageBox.Ok)
                    popup.setIcon(QMessageBox.Information)
                    popup.exec_()
                    self.ui.stackedWidget.setCurrentIndex(3)
                elif passw==[]:
                    data=(std_roll_no,std_name,std_father_name,std_ph_no,std_fathers_ph_no,gender,std_class)
                    data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
                    conn = sqlite3.connect(f"{data_path}/Student_info.db")
                    cur = conn.cursor()
                    sql=''' INSERT INTO Std_In (Roll_No,Student_Name,Father_Name,Phone,Fathers_Phone,Gender,
                            Class_Enroll) VALUES (?,?,?,?,?,?,?) ''' 
                    cur.execute(sql,data)
                    conn.commit()
                    conn.close()
                    passw=subprocess.check_output([sys.executable, "Password.py"])
                    passw=str(passw.decode("utf-8"))
                    passw=passw[:-2]
                    data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
                    conn = sqlite3.connect(f"{data_path}/Login.db")
                    cur = conn.cursor()
                    sql2=''' INSERT INTO LOGIN_S (Roll_No,Password,Type) VALUES (?,?,?) '''
                    task2=(std_roll_no,passw,"S")
                    cur.execute(sql2,task2)
                    conn.commit()
                    conn.close()
                            
                    self.ui.tableWidget.setRowCount(0)  
                    self.manage_students()
                    popup.setWindowTitle("Add Student User")
                    popup.setText(f'Student with ID ={std_roll_no} Has Been Added')
                    popup.setStandardButtons(QMessageBox.Ok)
                    popup.setIcon(QMessageBox.Information)
                    popup.exec_()
                    
                    self.ui.stackedWidget.setCurrentIndex(3)
                else:
                    popup.setWindowTitle("Add Student User")
                    popup.setText(f'The Roll Number Already Exsists')
                    popup.setStandardButtons(QMessageBox.Ok)
                    popup.setIcon(QMessageBox.Critical)
                    popup.exec_()

    def Back_Add_Student(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def Student_Update_button(self,i):
        if i.text()=='&Yes':
            data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
            conn = sqlite3.connect(f"{data_path}/Student_info.db")
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM Std_In where Roll_No == {self.user_remover};')
            passw=cur.fetchall()
            conn.close()
            temp=passw[0]
            self.ui.studentNameLineEdit_7.setText(temp[1])
            self.ui.fatherSNameLineEdit_7.setText(temp[2])
            self.ui.rollNumberLineEdit_7.setText(str(temp[0]))
            self.ui.phoneNumberLineEdit_9.setText(str(temp[3]))
            self.ui.fatherSPhoneNumberLineEdit_7.setText(str(temp[4]))
            self.ui.gradeComboBox_7.setItemText(0,str(temp[6]))
            if temp[5]=="Male":
                self.ui.radioButton_13.setChecked(True)
            elif temp[5]=="Female":
                self.ui.radioButton_14.setChecked(True)
            self.user_remover=''
            self.ui.stackedWidget.setCurrentIndex(12)
        else:
            pass

    def Update_Student(self):
        b=self.retrieveStudentinfoValue()
        if b==[]:
            popup=QMessageBox()
            popup.setWindowTitle("Update Student")
            popup.setText(f"First Select Student To Update Their Information")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Information)
            popup.exec_()
        elif len(b)>1:
            popup=QMessageBox()
            popup.setWindowTitle("Update Student")
            popup.setText(f"You can only update Information of One Student At a Time")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Information)
            popup.exec_()
        else:
            temp=b[0]
            self.user_remover=temp[0]
            popup=QMessageBox()
            popup.setWindowTitle("Update Student")
            popup.setText(f"Are you sure you want to Update Student Information")
            popup.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            popup.setIcon(QMessageBox.Information)
            popup.buttonClicked.connect(self.Student_Update_button)
            popup.exec_()

    def Student_Update(self):
        popup=QMessageBox()
        if self.ui.studentNameLineEdit_7.text()=="" or self.ui.fatherSNameLineEdit_7.text()=="" or self.ui.rollNumberLineEdit_7.text()=="" or self.ui.phoneNumberLineEdit_9.text()=="" or self.ui.fatherSPhoneNumberLineEdit_7.text()=="" or self.ui.gradeComboBox_7.currentText()=="":
            popup.setWindowTitle("Update Student User")
            popup.setText("Please Enter All Fields")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
        else:
            std_name=self.ui.studentNameLineEdit_7.text()
            std_father_name=self.ui.fatherSNameLineEdit_7.text()
            std_roll_no=self.ui.rollNumberLineEdit_7.text()
            std_ph_no=self.ui.phoneNumberLineEdit_9.text()
            std_fathers_ph_no=self.ui.fatherSPhoneNumberLineEdit_7.text()
            std_class=self.ui.gradeComboBox_7.currentText()

            if self.ui.radioButton_13.isChecked():
                gender="Male"
            elif self.ui.radioButton_14.isChecked():
                gender="Female"

           
            data=(std_name,std_father_name,std_ph_no,std_fathers_ph_no,gender,std_class,std_roll_no)
            data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
            conn = sqlite3.connect(f"{data_path}/Student_info.db")
            cur = conn.cursor()
            sql=''' UPDATE Std_In
                    SET Student_Name = ?, Father_Name= ? ,Phone = ?, Fathers_Phone = ? , Gender = ?, Class_Enroll=?
                    WHERE Roll_No = ?''' 
            cur.execute(sql,data)
            conn.commit()
            conn.close()   
            self.ui.tableWidget.setRowCount(0)  
            self.manage_students()
            popup.setWindowTitle("Update Student User")
            popup.setText(f'Student Information Has Been Updated')
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Information)
            popup.exec_()
            self.ui.stackedWidget.setCurrentIndex(3)
    def Std_Update(self,i):
        if i.text() == '&Yes' :
            self.Student_Update()
        else:
            pass

    def Update_Student_Credentials_Submit(self):
        popup=QMessageBox()
        popup.setWindowTitle("Update Teacher")
        popup.setText(f"Are you sure you want to Update Teacher Information")
        popup.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        popup.setIcon(QMessageBox.Information)
        popup.buttonClicked.connect(self.Std_Update)
        popup.exec_()
        

    def Back_Update_Student(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def Remove_Student(self):
        b=self.retrieveStudentinfoValue()
        if b==[]:
            popup=QMessageBox()
            popup.setWindowTitle("Remove Student")
            popup.setText(f"First Select Students To Remove ")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Information)
            popup.exec_()
        else:
            popup=QMessageBox()
            popup.setWindowTitle("Remove Student")
            popup.setText(f"Are you Sure to Remove The Student ")
            popup.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            popup.setIcon(QMessageBox.Information)
            popup.buttonClicked.connect(self.Student_Remove_button)
            popup.exec_()

    def Student_Remove_button(self,i):         
        if i.text() == '&Yes' :
            b=self.retrieveStudentinfoValue()
            if len(b)==1:
                temp=b[0]
                self.user_remove=temp[0]
                data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
                conn = sqlite3.connect(f"{data_path}/Student_info.db")
                cur = conn.cursor()
                cur.execute(f'DELETE FROM Std_In WHERE Roll_No = {self.user_remove};')
                conn.commit()
                cur.execute(f'DELETE FROM Student_Tests WHERE ID = {self.user_remove};')
                conn.commit()
                conn.close()
                conn = sqlite3.connect(f"{data_path}/Login.db")
                cur = conn.cursor()
                cur.execute(f'DELETE FROM Login_S WHERE Roll_No = {self.user_remove};')
                conn.commit()
                conn.close()
                self.ui.tableWidget.setRowCount(0)  
                self.manage_students()
                popup=QMessageBox()
                popup.setWindowTitle("Remove Student")
                popup.setText(f"The Student with ID = {self.user_remove} Has Been Removed")
                popup.setStandardButtons(QMessageBox.Ok)
                popup.setIcon(QMessageBox.Information)
                popup.exec_()
                self.user_remove=''
            else:
                b=self.retrieveStudentinfoValue()
                for i in range(len(b)):
                    temp=b[i]
                    self.user_remove=temp[0]
                    data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
                    conn = sqlite3.connect(f"{data_path}/Student_info.db")
                    cur = conn.cursor()
                    cur.execute(f'DELETE FROM Std_In WHERE Roll_No = {self.user_remove};')
                    conn.commit()
                    cur.execute(f'DELETE FROM Student_Tests WHERE ID = {self.user_remove};')
                    conn.commit()
                    conn.close()
                    conn = sqlite3.connect(f"{data_path}/Login.db")
                    cur = conn.cursor()
                    cur.execute(f'DELETE FROM Login_S WHERE Roll_No = {self.user_remove};')
                    conn.commit()
                    conn.close()
                    self.user_remove=''
                self.ui.tableWidget.setRowCount(0)  
                self.manage_students()
                popup=QMessageBox()
                popup.setWindowTitle("Remove Student")
                popup.setText(f"The Selected Students Have Been Removed")
                popup.setStandardButtons(QMessageBox.Ok)
                popup.setIcon(QMessageBox.Information)
                popup.exec_()

    def perform_test(self):
        popup=QMessageBox()
        popup.setWindowTitle("Perform Test")
        popup.setText(f"Please Put your hands down before the Camera is Turned On Press Ok When Ready")
        popup.setStandardButtons(QMessageBox.Ok)
        popup.setIcon(QMessageBox.Information)
        popup.exec_()
        sign=''
        for ix in self.ui.treeWidget_2.selectedIndexes():
            sign = ix.data(Qt.DisplayRole) # or ix.data()
        self.test_sign=sign
        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
        conn = sqlite3.connect(f"{data_path}/Student_info.db")
        cur = conn.cursor()
        cur.execute(f"SELECT path FROM Student_Tests where ID == {self.std_roll_number} AND Sign_Name == '{sign}' AND Test_Completed == 'No';")
        passw=cur.fetchall()
        conn.close()
        reference_sign=''
        for i in passw:
            reference_sign=i[0]

        reference_sign=globals()[reference_sign]
        self.ui.stackedWidget_2.setCurrentIndex(4)
        self.sentences=[]
        self.camerathread = cameraThread()
        self.camerathread.attempt_no=0
        self.test_accuracy=0
        self.test_attempt=0
        self.camerathread.reference_signs=reference_sign
        self.camerathread.acc_sign=sign
        self.video=sign

        self.camerathread.record=False
        self.camerathread.start()
        self.camerathread.ImageUpdate.connect(self.ImageUpdateSlot_sentences)
        self.camerathread.accuracyUpdate.connect(self.accuracyUpdateSlot)
        self.camerathread.accuracy_reset.connect(self.accuracy_reset)

        
    def test_back_button(self,i):
        if i.text() == 'OK' :
            self.acc2=0
            self.camerathread.stop()
            self.sentences_pass=0
            self.sentences=[]
            self.camerathread.sentences_pass_on=False
            self.ui.stackedWidget_2.setCurrentIndex(5)
            self.test_accuracy=0
            self.test_attempt=0
        else:
            pass

        
    def test_back(self):
        if self.test_attempt<3:
            popup=QMessageBox()
            popup.setWindowTitle("Test Incompleted")
            popup.setText(f"You Have not the completed the test Pressing Ok will not record the test marks")
            popup.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            popup.setIcon(QMessageBox.Information)
            popup.buttonClicked.connect(self.test_back_button)
            popup.exec_()
        elif self.test_attempt==3:
            popup=QMessageBox()
            popup.setWindowTitle("Test Completed")
            popup.setText(f"Press the Submit Button to record the marks the test is completed")
            popup.setStandardButtons(QMessageBox.Ok )
            popup.setIcon(QMessageBox.Information)
            popup.exec_()

    def teachers_back(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.tableWidget_2.setRowCount(0)

    def students_info_back(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.tableWidget.setRowCount(0)

    def manage_teachers(self):
        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
        conn = sqlite3.connect(f"{data_path}/Teachers_info.db")
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM Teacher_Info;')
        passw=cur.fetchall()
        conn.close()
        for details in passw:
            row_number = self.ui.tableWidget_2.rowCount()
            if row_number == len(passw):
                pass
            else:
                self.ui.tableWidget_2.insertRow(row_number)
            for column_number, data in enumerate(details):
                if column_number==0:
                    chkBoxItem =QTableWidgetItem(str(data))
                    chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    chkBoxItem.setCheckState(QtCore.Qt.Unchecked)       
                    self.ui.tableWidget_2.setItem(row_number,column_number,chkBoxItem)
                else:
                    self.ui.tableWidget_2.setItem(
                    row_number, column_number, QTableWidgetItem(str(data)))

        self.ui.stackedWidget.setCurrentIndex(2)

    def retrieveTeacherinfoValue(self):
        list1=[]
        for row in range(self.ui.tableWidget_2.rowCount()):
            if self.ui.tableWidget_2.item(row,0).checkState()==Qt.CheckState.Checked:
                list1.append([self.ui.tableWidget_2.item(row,col).text() for col in range(self.ui.tableWidget_2.columnCount())])
        return list1

    def retrieveStudentinfoValue(self):
        list1=[]
        for row in range(self.ui.tableWidget.rowCount()):
            if self.ui.tableWidget.item(row,0).checkState()==Qt.CheckState.Checked:
                list1.append([self.ui.tableWidget.item(row,col).text() for col in range(self.ui.tableWidget.columnCount())])
        return list1

        
    def teachers_search(self):
        self.ui.tableWidget_2.setRowCount(0)
        data=self.ui.lineEdit_2.text()
        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
        conn = sqlite3.connect(f"{data_path}/Teachers_info.db")
        cur = conn.cursor()
        if data:
            cur.execute("SELECT * FROM Teacher_Info WHERE ID LIKE ?",(data+'%',))
            passw=cur.fetchall()
            conn.close()
            for details in passw:
                row_number = self.ui.tableWidget_2.rowCount()
                if row_number == len(passw):
                    pass
                else:
                    self.ui.tableWidget_2.insertRow(row_number)
                for column_number, data in enumerate(details):
                    if column_number==0:
                        chkBoxItem =QTableWidgetItem(str(data))
                        chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                        chkBoxItem.setCheckState(QtCore.Qt.Unchecked)       
                        self.ui.tableWidget_2.setItem(row_number,column_number,chkBoxItem)
                    else:
                        self.ui.tableWidget_2.setItem(
                        row_number, column_number, QTableWidgetItem(str(data)))
        else:
            conn.close()
            self.manage_teachers()
    
    def manage_students(self):
        data=self.ui.lineEdit_3.text()
        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
        conn = sqlite3.connect(f"{data_path}/Student_info.db")
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM Std_In ;')
        passw=cur.fetchall()
        conn.close()
        for details in passw:
            row_number = self.ui.tableWidget.rowCount()
            if row_number == len(passw):
                pass
            else:
                self.ui.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(details):
                if column_number==0:
                    chkBoxItem =QTableWidgetItem(str(data))
                    chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    chkBoxItem.setCheckState(QtCore.Qt.Unchecked)       
                    self.ui.tableWidget.setItem(row_number,column_number,chkBoxItem)
                else:
                    self.ui.tableWidget.setItem(
                    row_number, column_number, QTableWidgetItem(str(data)))

        self.ui.stackedWidget.setCurrentIndex(3)

    def students_search(self):
        self.ui.tableWidget.setRowCount(0)
        data=self.ui.lineEdit_3.text()
        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
        conn = sqlite3.connect(f"{data_path}/Student_info.db")
        cur = conn.cursor()
        if data:
            cur.execute("SELECT * FROM Std_In WHERE Roll_No LIKE ?",(data+'%',))
            passw=cur.fetchall()
            conn.close()
            for details in passw:
                row_number = self.ui.tableWidget.rowCount()
                if row_number == len(passw):
                    pass
                else:
                    self.ui.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(details):
                    if column_number==0:
                        chkBoxItem =QTableWidgetItem(str(data))
                        chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                        chkBoxItem.setCheckState(QtCore.Qt.Unchecked)       
                        self.ui.tableWidget.setItem(row_number,column_number,chkBoxItem)
                    else:
                        self.ui.tableWidget.setItem(
                        row_number, column_number, QTableWidgetItem(str(data)))

        else:
            conn.close()
            self.manage_students()

    def back_progress(self):
        self.ui.stackedWidget_2.setCurrentIndex(0)
        self.ui.tableWidget_4.setRowCount(0)
    
    def submit_test(self):
        if self.test_attempt==3:
            popup=QMessageBox()
            popup.setWindowTitle("Test Submission")
            popup.setText(f"Test has been Submitted")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Information)
            popup.exec_()
            self.camerathread.stop()
            self.camerathread.sentences_pass_on=False

            data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
            conn = sqlite3.connect(f"{data_path}/Student_info.db")
            cur = conn.cursor()
            sql='''UPDATE Student_Tests
                SET Marks_Obtained = (?), Test_Completed = (?)
                WHERE ID = (?) AND Sign_Name = (?);'''
            data=(self.test_accuracy,"Yes",self.std_roll_number,self.test_sign)
            cur.execute(sql,data)
            conn.commit()
            conn.close()
            self.sentences_pass=0
            self.sentences=[]
            self.acc2=0
            self.test_attempt=0
            self.test_accuracy=0
            


            self.ui.stackedWidget_2.setCurrentIndex(0)
        else:
            popup=QMessageBox()
            popup.setWindowTitle("Test Submission")
            popup.setText(f"First Attempt the Test")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Information)
            popup.exec_()

    def manage_tests(self):
        data=self.ui.lineEdit_5.text()
        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
        conn = sqlite3.connect(f"{data_path}/Student_info.db")
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM Std_In ;')
        passw=cur.fetchall()
        conn.close()
        for details in passw:
            row_number = self.ui.tableWidget_5.rowCount()
            if row_number == len(passw):
                pass
            else:
                self.ui.tableWidget_5.insertRow(row_number)
            for column_number, data in enumerate(details):
                 self.ui.tableWidget_5.setItem(
                row_number, column_number, QTableWidgetItem(str(data)))
        self.ui.stackedWidget.setCurrentIndex(4)

    def search_manage_tests(self):
        self.ui.tableWidget_5.setRowCount(0)
        data=self.ui.lineEdit_5.text()
        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
        conn = sqlite3.connect(f"{data_path}/Student_info.db")
        cur = conn.cursor()
        if data:
            cur.execute(f'SELECT * FROM Std_In WHERE Roll_No LIKE {data};')
            passw=cur.fetchall()
            conn.close()
            for details in passw:
                row_number = self.ui.tableWidget_5.rowCount()
                if row_number == len(passw):
                    pass
                else:
                    self.ui.tableWidget_5.insertRow(row_number)
                for column_number, data in enumerate(details):
                    self.ui.tableWidget_5.setItem(
                    row_number, column_number, QTableWidgetItem(str(data)))

        else:
            conn.close()
            self.manage_tests()


    def back_manage_test(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def back_assign_test(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def manage_courses(self):
        self.ui.stackedWidget.setCurrentIndex(7)
        
    
    def login(self):
        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
        conn = sqlite3.connect(f"{data_path}/Login.db")
        cur = conn.cursor()
        
        a=self.ui.usernameLineEdit.text()
        b=self.ui.passwordLineEdit.text()
        popup=QMessageBox()
        if a=="" or b=="":
            popup.setWindowTitle("Login Credientials")
            popup.setText("Username or Password not entered!")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
        else:
            cur.execute(f'SELECT Roll_no ,Password, Type FROM Login_S where Roll_no == {a} AND Password == "{b}";')
            passw=cur.fetchall()
            conn.close()
            if passw==None:
                popup.setWindowTitle("Login Credientials")
                popup.setText("Incorrect Username or Password!")
                popup.setStandardButtons(QMessageBox.Ok)
                popup.setIcon(QMessageBox.Critical)
                popup.exec_()
            elif passw==[]:
                popup.setWindowTitle("Login Credientials")
                popup.setText(f"Username with ID ={a} Does not exsist")
                popup.setStandardButtons(QMessageBox.Ok)
                popup.setIcon(QMessageBox.Critical)
                popup.exec_()
            else:
                for i in passw:
                    if int(a)==900:
                        self.user='Teacher'
                        self.ui.tableWidget_3.show()
                        self.ui.pushButton_18.show()
                        self.ui.pushButton_17.show()
                        self.ui.pushButton_10.hide()
                        self.ui.pushButton_13.hide()
                        self.ui.pushButton_15.hide()

                        self.ui.pushButton_42.show()
                        self.ui.pushButton_41.show()
                        self.ui.pushButton_6.show()
                        self.ui.pushButton_39.show()
                        self.ui.pushButton_36.show()
                        self.ui.pushButton_37.show()

                        self.ui.label_20.setText('Teacher')
                        self.ui.stackedWidget.setCurrentIndex(1)
                    elif i[2]=="S":
                        self.user='Student'
                        self.std_roll_number=a
                        self.ui.tableWidget_3.hide()
                        self.ui.pushButton_10.hide()
                        self.ui.pushButton_18.hide()
                        self.ui.pushButton_13.show()
                        self.ui.pushButton_15.show()
                        self.ui.pushButton_17.hide()
                        self.ui.label_20.setText('Student')
                        self.ui.stackedWidget.setCurrentIndex(7)
                        self.ui.stackedWidget_2.setCurrentIndex(0)
                    else:
                        self.user='Teacher'
                        self.ui.tableWidget_3.show()
                        self.ui.pushButton_18.show()
                        self.ui.pushButton_17.show()
                        self.ui.pushButton_10.hide()
                        self.ui.pushButton_13.hide()
                        self.ui.pushButton_15.hide()
                        self.ui.pushButton_42.hide()
                        self.ui.pushButton_41.hide()
                        self.ui.pushButton_6.hide()
                        self.ui.pushButton_39.hide()
                        self.ui.pushButton_36.hide()
                        self.ui.pushButton_37.hide()

                        self.ui.label_20.setText('Teacher')
                        self.ui.stackedWidget.setCurrentIndex(1)
    def logout(self):
        self.std_roll_number=0
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.stackedWidget_2.setCurrentIndex(0)
        
    def New_User(self):
        self.ui.stackedWidget.setCurrentIndex(6)

    def Create_New_User(self):
        popup=QMessageBox()
        if self.ui.studentNameLineEdit.text()=="" or self.ui.fatherSNameLineEdit.text()=="" or self.ui.rollNumberLineEdit.text()=="" or self.ui.phoneNumberLineEdit.text()=="" or self.ui.fatherSPhoneNumberLineEdit.text()=="" or self.ui.gradeComboBox.currentText()=="":
            popup.setWindowTitle("Create User")
            popup.setText("Please Enter All Fields")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
        else:
            std_name=self.ui.studentNameLineEdit.text()
            fath_name=self.ui.fatherSNameLineEdit.text()
            roll_no=int(self.ui.rollNumberLineEdit.text())
            phone=int(self.ui.phoneNumberLineEdit.text())
            fath_phone=int(self.ui.fatherSPhoneNumberLineEdit.text())
            class_enroll=int(self.ui.gradeComboBox.currentText())
            
            if self.ui.radioButton.isChecked():
                gender="Male"
            elif self.ui.radioButton_2.isChecked():
                gender='Female'
            else:
                popup.setText("Please Enter All Fields")
                popup.setStandardButtons(QMessageBox.Ok)
                popup.setIcon(QMessageBox.Critical)
                popup.exec_()



            data=(roll_no,std_name,fath_name,phone,fath_phone,gender,class_enroll)

            if std_name == '' or fath_name == '' or roll_no =='' or phone == '':
                popup.setWindowTitle("Create User")
                popup.setText("Please Enter All Fields")
                popup.setStandardButtons(QMessageBox.Ok)
                popup.setIcon(QMessageBox.Critical)
                popup.exec_()
            else:
                data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
                conn = sqlite3.connect(f"{data_path}/Student_info.db")
                cur = conn.cursor()
                sql=''' INSERT INTO STD_IN (Roll_no,Student_Name,Father_Name,Phone,
                    Fathers_Phone,Gender,Class_Enroll) VALUES (?,?,?,?,?,?,?) '''
                cur.execute(f'SELECT Roll_no  FROM STD_IN where Roll_no == {roll_no} ;')
                passw=cur.fetchone()
                
                print(passw)
                import subprocess
                if passw==None:
                    cur.execute(sql,data)
                    conn.commit()
                    conn.close()
                    passw=subprocess.check_output([sys.executable, "Password.py"])
                    passw=str(passw.decode("utf-8"))
                    passw=passw[:-2]
                    conn1 = sqlite3.connect(f"{data_path}/Login.db")
                    cur2 = conn1.cursor()
                    sql2=''' INSERT INTO LOGIN_S (Roll_No,Password,Type) VALUES (?,?,?) '''
                    task2=(roll_no,passw,"S")
                    cur2.execute(sql2,task2)
                    conn1.commit()
                    conn1.close()
                    popup.setWindowTitle("Create User")
                    popup.setText(f"Information of Person {std_name} has been Added")
                    popup.setStandardButtons(QMessageBox.Ok)
                    popup.setIcon(QMessageBox.Information)
                    popup.exec_()
                    self.ui.stackedWidget_2.setCurrentIndex(0)
                    self.ui.stackedWidget.setCurrentIndex(0)
                    #print("Data has been Entered")
                    
                    # MainWindow.close()
                    # call(["python","Login.py"])
                else:
                    popup.setWindowTitle("Create User")
                    popup.setText("Roll Number Already Exists!")
                    popup.setStandardButtons(QMessageBox.Ok)
                    popup.setIcon(QMessageBox.Critical)
                    popup.exec_()
                    
    def aphabets_folder(self):
        path=pathlib.Path(__file__).parent.absolute().joinpath('videos','Alphabets')
        path=str(path)
        self.dirModel.setRootPath(path)
        self.ui.treeview.setRootIndex(self.model.index(path))
        self.ui.stackedWidget_2.setCurrentIndex(1)
        self.ui.frame_13.hide()
        self.current_folder='Alphabets'
    def science_folder(self):
        path=pathlib.Path(__file__).parent.absolute().joinpath('videos','Science')
        path=str(path)
        self.dirModel.setRootPath(path)
        self.ui.treeview.setRootIndex(self.model.index(path))
        self.ui.stackedWidget_2.setCurrentIndex(1)
        self.ui.frame_13.hide()
        self.current_folder='Science'
    def computer_folder(self):
        path=pathlib.Path(__file__).parent.absolute().joinpath('videos','Computer')
        path=str(path)
        self.dirModel.setRootPath(path)
        self.ui.treeview.setRootIndex(self.model.index(path))
        self.ui.stackedWidget_2.setCurrentIndex(1)
        self.ui.frame_13.hide()
        self.current_folder='Computer'


    def sentence_screen(self):
        self.sentences=[]
        self.camerathread = cameraThread()
        self.camerathread.reference_signs=all_data_sentences
        self.camerathread.acc_sign='A'
        self.video='A'
        self.camerathread.record=False
        self.test_attempt=4
        self.camerathread.attempt_no=4
        self.camerathread.start()
        self.camerathread.ImageUpdate.connect(self.ImageUpdateSlot_sentences)
        self.camerathread.accuracyUpdate.connect(self.accuracyUpdateSlot)
        self.camerathread.accuracy_reset.connect(self.accuracy_reset)
        self.ui.stackedWidget_2.setCurrentIndex(3)
    
    def select_video_test(self,index): #For Student Video Assignment
        path=pathlib.Path.cwd().joinpath('videos')
        video = self.fileModel.fileName(index)
        folder=''
        folders=os.listdir(path)
        if ".mp4" in video:
            for i in folders:
                folders_2=os.listdir(str(path)+'\\'+i)
                if video in folders_2:
                    folder=i
                    break
        folder=folder+'_signs'
        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
        conn = sqlite3.connect(f"{data_path}/Student_info.db")
        cur = conn.cursor()
        path2=video.replace(".mp4","")
        sql= '''INSERT INTO Student_Tests (ID,Sign_Name,Marks_Obtained,
                Test_Completed,Path) VALUES (?,?,?,?,?)'''
        data=(self.test_roll_no,path2,0,'No',folder)


        cur.execute(f"SELECT Test_Completed from Student_Tests WHERE ID=={self.test_roll_no} AND Sign_Name=='{path2}' ;")
        passw=cur.fetchone()
        if passw==None:
            cur.execute(sql,data)
            conn.commit()
            conn.close()
            popup=QMessageBox()
            popup.setWindowTitle("Assign Test")
            popup.setText(f"Test of Sign={path2} has been Assigned to Roll_No {self.test_roll_no}")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Information)
            popup.exec_()
            self.ui.stackedWidget.setCurrentIndex(1)
        elif passw[0]=="No":
            popup=QMessageBox()
            popup.setWindowTitle("Assign Test")
            popup.setText(f"Test of Sign={path2} has Already been Assigned to Roll_No {self.test_roll_no}")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
        else:
            cur.execute(sql,data)
            conn.commit()
            conn.close()
            popup=QMessageBox()
            popup.setWindowTitle("Assign Test")
            popup.setText(f"Test of Sign={path2} has been Assigned to Roll_No {self.test_roll_no}")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Information)
            popup.exec_()
            self.ui.stackedWidget.setCurrentIndex(1)

    def select_video(self,index):
        video = self.fileModel.fileName(index)
        path=''
        folders=['alphabets','computer','science']
        folder=''
        
        for i in folders:
            path=pathlib.Path(__file__).parent.absolute().joinpath('videos',i,video)
            if path.is_file():
                folder=i
                break

        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(str(path))))
        self.mediaPlayer.play()
        #self.mediaPlayer.pause()
        time.sleep(0.15)
        
        
        if folder == "alphabets":
            self.camerathread = cameraThread()
            self.camerathread.reference_signs=Alphabets_signs
            self.camerathread.acc_sign=video[:-4]
            self.video=video[:-4]
            self.camerathread.record=False
            try:
                self.camerathread.reference_signs=self.camerathread.reference_signs.append(self.new_ref_alph)
            except:
                pass
        elif folder == 'computer':
            self.camerathread = cameraThread()
            self.camerathread.reference_signs=Computer_signs
            self.camerathread.acc_sign=video[:-4]
            self.video=video[:-4]
            self.camerathread.record=False
            try:
                self.camerathread.reference_signs=self.camerathread.reference_signs.append(self.new_ref_comp)
            except:
                pass
            
        elif folder == 'science':
            self.camerathread = cameraThread()
            self.camerathread.reference_signs=Science_signs
            self.camerathread.acc_sign=video[:-4]
            self.video=video[:-4]
            self.camerathread.record=False
            try:
                self.camerathread.reference_signs=self.camerathread.reference_signs.append(self.new_ref_sci)
            except:
                pass
            
        self.camerathread.start()
        self.camerathread.ImageUpdate.connect(self.ImageUpdateSlot)
        self.camerathread.accuracyUpdate.connect(self.accuracyUpdateSlot)
        self.camerathread.accuracy_reset.connect(self.accuracy_reset)
        self.ui.stackedWidget_2.setCurrentIndex(2)
        self.camerathread.sentences_pass_on=False
    
    def back_video(self):
        self.playlist.clear()
        self.camerathread.stop()
        self.ui.label_16.setText('Closest Sign:')
        self.ui.label_17.setText('None')
        __sortingEnabled = self.ui.tableWidget_3.isSortingEnabled()
        self.ui.tableWidget_3.setSortingEnabled(False)
        item = self.ui.tableWidget_3.item(1, 1)
        item = self.ui.tableWidget_3.item(0, 0)
        item.setText("0")
        item = self.ui.tableWidget_3.item(0, 1)
        item.setText("0")
        item = self.ui.tableWidget_3.item(1, 0)
        item.setText("0")
        item = self.ui.tableWidget_3.item(1, 1)
        item.setText("0")
        self.ui.tableWidget_3.setSortingEnabled(__sortingEnabled)
        self.ui.stackedWidget_2.setCurrentIndex(1)
    def back_videos(self):
        self.ui.stackedWidget_2.setCurrentIndex(0)
        self.ui.frame_13.show()
        self.sentences_pass=0
        self.sentences=[]
        #self.camerathread.sentences_pass_on=False

    def sentence_back(self):
        self.camerathread.stop()
        self.ui.stackedWidget_2.setCurrentIndex(0)
        self.sentences_pass=0
        self.test_attempt=4
        self.sentences=[]
        self.camerathread.sentences_pass_on=False
        
    def new_account_cancel(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def add_video(self):
        folder=self.current_folder
        folder_path=pathlib.Path(__file__).parent.absolute().joinpath('videos',folder)
        if folder == "Alphabets":
            datapath=pathlib.Path(__file__).parent.absolute().joinpath('data','Alphabets_dataset')
        else:
            datapath=pathlib.Path(__file__).parent.absolute().joinpath('data',f'{folder}_dataset')
        fileName, _ = QFileDialog.getOpenFileName(None,"Delete Video",str(folder_path),filter="*.mp4")
        
        progress=QProgressDialog()
        progress.setLabelText("Video being Processed Please wait......")
       
        if fileName:
            progress.show()
            file=QFileInfo(fileName).fileName()
            video_path=fileName
            video_data_path=pathlib.Path(datapath).joinpath(file[:-4])
            progress.setValue(0)
            video_dest_path=pathlib.Path(folder_path).joinpath(file) ## Do changes to this because the patlib change to CWD was made in landmark_utils just send the file name not the entire path
            temp_vid_path=pathlib.Path(__file__).parent.absolute().joinpath('temp_videos')
            progress.setValue(10)
            progress.setValue(20)
            progress.setValue(30)
            shutil.copyfile(video_path,video_dest_path)
            trim.trim(file[:-4],video_path,temp_vid_path)
            vid1=f'{file[:-4]}_1'
            vid2=f'{file[:-4]}_2'
            save_landmarks_from_new_video(vid1,temp_vid_path,video_data_path)
            save_landmarks_from_new_video(vid2,temp_vid_path,video_data_path)
            if folder == "Alphabets":
                self.new_ref_alph=new_load_reference_signs([vid1,vid2],"Alphabets")
                Alphabets_signs.append(new_ref)
            elif folder == 'Science':
                self.new_ref_sci=new_load_reference_signs([vid1,vid2],'Science')
                Science_signs.append(new_ref)
            elif folder == 'Computer':
                self.new_ref_comp=new_load_reference_signs([vid1,vid2],'Computer')
                Computer_signs.append(new_ref)
            progress.setValue(100)
            
            #self.dirModel.modelReset()
            self.model.setRootPath((QtCore.QDir.rootPath()))
            self.ui.treeview.setRootIndex(self.model.index(str(folder_path)))
    def delete_video(self):
        folder=self.current_folder
        folder_path=pathlib.Path(__file__).parent.absolute().joinpath('videos',folder)
        if folder == "Alphabets":
            datapath=pathlib.Path(__file__).parent.absolute().joinpath('data','Alphabets_dataset')
        else:
            datapath=pathlib.Path(__file__).parent.absolute().joinpath('data',f'{folder}_dataset')
        
        fileName, _ = QFileDialog.getOpenFileName(None,"Delete Video",str(folder_path),filter="*.mp4")
        if folder == 'Alphabets':
            signs=Alphabets_signs
        elif folder == 'Computer':
            signs=Computer_signs
        elif folder == 'Science':
            signs=Science_signs
        if fileName:
            #print(fileName)
            #print(self.path_video)
            #url = QUrl.fromLocalFile(fileName)
            file=QFileInfo(fileName).fileName()
            print(file,fileName)
            video_path=pathlib.Path(folder_path).joinpath(file)
            video_data_path=pathlib.Path(datapath).joinpath(file[:-4])
            
            try:
                os.remove(video_path)
                shutil.rmtree(video_data_path)
                
                signs.drop(signs.index[signs['name'] == file[:-4]], inplace=True)
            except:
                pass
    ############# Video and Camera Feed ##################

    def ImageUpdateSlot(self, Image):
        self.ui.label_18.setPixmap(QPixmap.fromImage(Image))
        self.camerathread.sentences_pass_on=False

    def ImageUpdateSlot_sentences(self, Image):
        self.camerathread.sentences_pass_on=True
        self.ui.label_4.setPixmap(QPixmap.fromImage(Image))
        self.ui.label_7.setPixmap(QPixmap.fromImage(Image))
    
    def accuracyUpdateSlot(self,predicted,sign,dist,acc):
        acc=float(acc)
        if self.test_attempt<3:
            if self.test_accuracy==0:
                if acc!=0:
                    self.test_accuracy=acc
                    self.test_attempt=0
            else:
                if dist[0]!=self.acc2 and acc!=0:
                    if self.acc2==0:
                        self.test_attempt=0
                        self.camerathread.attempt_no=self.test_attempt
                        self.acc2=dist[0]
                        self.test_accuracy=acc
                    
                    else:
                        self.acc2=dist[0]
                        self.test_accuracy=acc
                        self.test_attempt+=1
                        self.camerathread.attempt_no=self.test_attempt
        else:
            if len(sign)<2:
                pass
            else:
                if self.sentences_pass==1:
                    if len(predicted) <2:
                        self.sentences.append(predicted)
                        self.ui.textEdit.insertPlainText(str(predicted))
                    else:
                        self.sentences.append(" ")
                        self.sentences.append(predicted)
                        self.ui.textEdit.insertPlainText(str(" "))
                        self.ui.textEdit.insertPlainText(str(predicted))
                    self.sentences_pass=0
                    
                
                sign=sign[:4]
                dist=dist[:4]
                pre_val=0
                list1=[]
                for i in range(len(sign)):
                    if sign[i]==self.video:
                        pass            
                    else:
                        if dist[0]==float('inf'):
                            self.ui.label_16.setText('No Close Signs Predicted')
                            self.ui.label_17.setText('')
                        else:
                            acc1=((int(dist[i])-60)/60)*100
                            if int(dist[i])<60:
                                acc1=round(acc1,2)
                                self.ui.label_16.setText(str(f"Closest Sign Predicted is {sign[i]} with accuracy ="))
                                self.ui.label_17.setText(str('98.5'))
                                break
                            else:
                                if acc1>100:
                                    acc1=(acc1)//100
                                    acc1=round(acc1,2)
                                    self.ui.label_16.setText(str(f"Closest Sign Predicted is {sign[i]} with accuracy ="))
                                    self.ui.label_17.setText(str(100-acc1))
                                    break
                                else:
                                    acc1=round(acc1,2)
                                    self.ui.label_16.setText(str(f"Closest Sign Predicted is {sign[i]} with accuracy ="))
                                    self.ui.label_17.setText(str(100-acc1))
                                    break

                
                if float(acc)>50 and predicted==self.video:
                    __sortingEnabled = self.ui.tableWidget_3.isSortingEnabled()
                    self.ui.tableWidget_3.setSortingEnabled(False)
                    item = self.ui.tableWidget_3.item(0, 0)
                    item.setText("0")
                    item = self.ui.tableWidget_3.item(0, 1)
                    item.setText("0")
                    item = self.ui.tableWidget_3.item(1, 0)
                    item.setText("0")
                    item = self.ui.tableWidget_3.item(1, 1)
                    item.setText("1")
                    self.ui.tableWidget_3.setSortingEnabled(__sortingEnabled)
                elif float(acc)>50 and predicted!=self.video:
                    __sortingEnabled = self.ui.tableWidget_3.isSortingEnabled()
                    self.ui.tableWidget_3.setSortingEnabled(False)
                    item = self.ui.tableWidget_3.item(0, 0)
                    item.setText("0")
                    item = self.ui.tableWidget_3.item(0, 1)
                    item.setText("0")
                    item = self.ui.tableWidget_3.item(1, 0)
                    item.setText("1")
                    item = self.ui.tableWidget_3.item(1, 1)
                    item.setText("0")
                    self.ui.tableWidget_3.setSortingEnabled(__sortingEnabled)
                elif float(acc)<50 and predicted==self.video:
                    __sortingEnabled = self.ui.tableWidget_3.isSortingEnabled()
                    self.ui.tableWidget_3.setSortingEnabled(False)
                    item = self.ui.tableWidget_3.item(0, 0)
                    item.setText("0")
                    item = self.ui.tableWidget_3.item(0, 1)
                    item.setText("1")
                    item = self.ui.tableWidget_3.item(1, 0)
                    item.setText("0")
                    item = self.ui.tableWidget_3.item(1, 1)
                    item.setText("0")
                    self.ui.tableWidget_3.setSortingEnabled(__sortingEnabled)
                elif float(acc)<50 and predicted!=self.video:
                    __sortingEnabled = self.ui.tableWidget_3.isSortingEnabled()
                    self.ui.tableWidget_3.setSortingEnabled(False)
                    item = self.ui.tableWidget_3.item(0, 0)
                    item.setText("1")
                    item = self.ui.tableWidget_3.item(0, 1)
                    item.setText("0")
                    item = self.ui.tableWidget_3.item(1, 0)
                    item.setText("0")
                    item = self.ui.tableWidget_3.item(1, 1)
                    item.setText("0")
                    self.ui.tableWidget_3.setSortingEnabled(__sortingEnabled)

                else:
                    __sortingEnabled = self.ui.tableWidget_3.isSortingEnabled()
                    self.ui.tableWidget_3.setSortingEnabled(False)
                    item = self.ui.tableWidget_3.item(1, 1)
                    item = self.ui.tableWidget_3.item(0, 0)
                    item.setText("0")
                    item = self.ui.tableWidget_3.item(0, 1)
                    item.setText("0")
                    item = self.ui.tableWidget_3.item(1, 0)
                    item.setText("0")
                    item = self.ui.tableWidget_3.item(1, 1)
                    item.setText("0")
                    self.ui.tableWidget_3.setSortingEnabled(__sortingEnabled)
    def accuracy_reset(self):
        self.ui.label_16.setText('Recording Signs')
        self.ui.label_17.setText('')
        self.sentences_pass=1
        
    
    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
 
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.ui.pushButton_19.setIcon(QtGui.QIcon('pause-button.png'))
        else:
            self.ui.pushButton_19.setIcon(QtGui.QIcon('play-button.png'))

    def positionChanged(self, position):
        self.ui.horizontalSlider_4.setValue(position)

    def durationChanged(self, duration):
        self.ui.horizontalSlider_4.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def clear_sentences(self):
        self.ui.textEdit.clear()
        self.sentences=[]
    def Back_sentences(self):
        if len(self.sentences) <1:
            pass
        else:
            self.sentences.remove(self.sentences[-1])
            print(self.sentences)
            self.ui.textEdit.clear()
            for i in self.sentences:
                self.ui.textEdit.insertPlainText(str(i))
        self.sentences_pass=0
    def add_space(self):
        self.sentences.append(" ")
        self.ui.textEdit.insertPlainText(str(" "))

class cameraThread(QThread):
    reference_signs=''
    acc_sign=''
    attempt_no=4
    sentences_pass_on=False
    record=False
    sentence_key=False
    matrix_sign_predicted=''
    matrix_sign_accuracy_predicted=''
    accuracy_reset=pyqtSignal(str)
    ImageUpdate = pyqtSignal(QImage)
    accuracyUpdate=pyqtSignal(str,list,list,str)
    
    
    def on_release(self,record):
        try:
            if record == False:
                pass
            else:
                self.accuracy_reset.emit('')
            self.sign_recorder.record(record)          
        except:
            pass

    
        

    def run(self):
        self.sign_recorder = SignRecorder(self.reference_signs)
        self.ThreadActive = True
        webcam_manager = WebcamManager()
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


        with mediapipe.solutions.holistic.Holistic(
            min_detection_confidence=0.3, min_tracking_confidence=0.3
        ) as holistic:
            while self.ThreadActive:
                
                # Read feed
                ret, frame = cap.read()

                # Make detections
                image, results = mediapipe_detection(frame, holistic)

                # Process results
                sign_detected, is_recording,sign,dist = self.sign_recorder.process_results(results)

                # Update the frame (draw landmarks & display result)
                FlippedImage,acc=webcam_manager.update(frame, results, sign_detected, is_recording,sign,dist,self.acc_sign,self.sentences_pass_on,self.attempt_no)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_BGR888)
                Pic = ConvertToQtFormat.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
                #self.ImageUpdate.emit(ConvertToQtFormat)
                self.ImageUpdate.emit(Pic)
                self.accuracyUpdate.emit(str(sign_detected),list(sign),list(dist),str(acc))
                
                if results.left_hand_landmarks:
                   self.on_release(True)
                elif results.right_hand_landmarks:
                    self.on_release(True)  
                else:
                    self.on_release(False)
    def stop(self):
        self.ThreadActive = False
        self.quit()


    


def param_capture(n):
    n = [
        file_name.replace(".pickle", "").replace("lh_", "")
        for root, dirs, files in os.walk(os.path.join("data", f'{n}'))
        for file_name in files
        if file_name.endswith(".pickle") and file_name.startswith("lh_")
    ]
    return n

def load_param(np,all_data_sentences):
    np1,all_data_sentences=newer_load_reference_signs(np,all_data_sentences)
    return np1,all_data_sentences

if __name__ == "__main__":
    dataset=pathlib.Path.cwd().joinpath('data')
    data_len=os.listdir(dataset)
    start_time = time.time()
    
    all_data_sentences=pd.DataFrame(columns=["name", "sign_model", "distance"])
    for i in data_len:
        #if i=="Science_dataset" or i=="Alphabets_dataset" or i=="Computer_dataset":
        if i=="Alphabets_dataset":
            temp=[root for root,dirs,files in os.walk(f'data\\{i}') if not dirs]
            temp1,all_data_sentences=load_param(temp,all_data_sentences)
            temp3=i.replace("dataset","signs")
            temp3=temp3.replace(" ","_")
            temp3=temp3.replace("&","and")
            temp3=temp3.replace("(","")
            temp3=temp3.replace(")","")
            temp3=temp3.replace(",","_")
            print(i)
            exec(f'{temp3}=temp1')
        else:
            pass    
    end_time = time.time()

    print(f"The execution time for loading is: {end_time-start_time}")

    app = QtWidgets.QApplication([])
    application = window()
    application.show()
    sys.exit(app.exec())