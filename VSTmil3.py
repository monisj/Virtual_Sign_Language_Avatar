from ast import excepthandler
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
from utils.dataset_utils import load_dataset, load_reference_signs,new_videos_load_dataset,new_load_reference_signs,newload_reference_signs,newer_load_reference_signs,load_embeds
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

from mil3gui import Ui_MainWindow


class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.test_users=[]
        self.user_remove=''
        self.test_roll_no=0
        self.class_assign=0
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
        self.error=0
        self.left_list=[]
        self.right_list=[]
        self.key1=True
        self.new_ref='a'
        self.subject='a'
        self.folder='a'
        self.test_screen_condition=False
        self.hold_data=0
        self.sentence_accuracy=0
    ################## New widgets ######################
        self.dirModel = QFileSystemModel()
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)
        self.fileModel = QFileSystemModel()
        self.fileModel.setFilter(QDir.NoDotAndDotDot |  QDir.Files)
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        

        self.ui.treeView_3.setModel(self.model)
        self.ui.treeView_3.hideColumn(1)
        self.ui.treeView_3.hideColumn(2)
        self.ui.treeView_3.hideColumn(3)
        self.ui.treeView_3.doubleClicked.connect(self.select_video_test)
        self.ui.treeView_3.clicked.connect(self.pass_variable)
        
        
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(self.ui.videoWidget)

        self.playlist = QMediaPlaylist()
        self.playlist.setPlaybackMode(self.playlist.Loop)
        self.mediaPlayer.setPlaylist(self.playlist)

    ################## Connections ######################
        self.ui.pushButton.clicked.connect(self.login)
        self.ui.pushButton_14.clicked.connect(self.New_User)
        self.ui.pushButton_9.clicked.connect(lambda x : self.select_subject("English"))
        self.ui.pushButton_11.clicked.connect(lambda x : self.select_subject("Science"))
        self.ui.pushButton_12.clicked.connect(lambda x : self.video_browse("Computer","Computer"))
        self.ui.pushButton_33.clicked.connect(lambda x : self.select_subject("Maths"))
        self.ui.pushButton_32.clicked.connect(lambda x : self.select_subject("Geography"))
        self.ui.pushButton_30.clicked.connect(lambda x : self.select_subject("General_Knowlege"))
        self.ui.pushButton_16.clicked.connect(self.back_videos)
        self.ui.pushButton_21.clicked.connect(self.back_video)
        self.ui.pushButton_19.clicked.connect(self.play)
        self.ui.pushButton_19.setIcon(QtGui.QIcon('play-button.png'))
        self.ui.pushButton_17.clicked.connect(self.delete_video)
        self.ui.pushButton_18.clicked.connect(self.add_video)
        self.ui.horizontalSlider_4.sliderMoved.connect(self.setPosition)
        self.ui.passwordLineEdit.returnPressed.connect(self.login)
        self.ui.forgotpasswordlabel.clicked.connect(self.forgot_password)
        self.ui.pushButton_20.clicked.connect(self.logout)
        self.ui.pushButton_69.clicked.connect(self.sentence_screen)
        self.ui.pushButton_22.clicked.connect(self.clear_sentences)
        self.ui.lineEdit_2.textChanged.connect(self.teachers_search)
        self.ui.lineEdit_3.textChanged.connect(self.students_search)
        self.ui.lineEdit_5.textChanged.connect(self.search_manage_tests)
        self.ui.pushButton_47.clicked.connect(self.manage_teachers)
        self.ui.pushButton_48.clicked.connect(self.manage_students)
        self.ui.pushButton_58.clicked.connect(self.manage_tests)
        # self.ui.tableWidget_5.cellDoubleClicked.connect(self.std_data)
        self.ui.pushButton_7.clicked.connect(self.Create_New_User)
        self.ui.pushButton_8.clicked.connect(self.logout)
        self.ui.pushButton_23.clicked.connect(self.Back_sentences)
        self.ui.pushButton_24.clicked.connect(self.add_space)
        self.ui.pushButton_25.clicked.connect(self.sentence_back)
        # self.ui.pushButton_27.clicked.connect(self.logout)
        self.ui.pushButton_26.clicked.connect(self.teachers_back)
        self.ui.pushButton_6.clicked.connect(self.Remove_Student)
        self.ui.pushButton_10.clicked.connect(self.main)
        self.ui.pushButton_50.clicked.connect(self.main)


        #self.ui.pushButton_7.clicked.connect(self.students_info_back)
       
       
        self.ui.pushButton_29.clicked.connect(self.test_back)
        self.ui.pushButton_35.clicked.connect(self.test_back_screen)
        self.ui.pushButton_13.clicked.connect(self.test_screen)
        self.ui.pushButton_34.clicked.connect(self.submit_test)
        self.ui.pushButton_68.clicked.connect(self.back_progress)
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
        self.ui.pushButton_56.clicked.connect(self.Back_Add_Student)
        self.ui.pushButton_57.clicked.connect(self.Add_Student_Credentials)
        self.ui.pushButton_51.clicked.connect(self.Back_Update_Student)
        self.ui.pushButton_52.clicked.connect(self.Update_Student_Credentials_Submit)
        self.ui.pushButton_53.clicked.connect(self.Assign_Test_By_Class)
        self.ui.pushButton_54.clicked.connect(self.std_data)
        self.ui.pushButton_301.clicked.connect(self.back_to_camera)
        #self.ui.pushButton_321.clicked.connect(self.pause_play) Pause/Play Function Button
        self.ui.pushButton_491.clicked.connect(self.view_previous_recording)
        

        self.ui.tableWidget.cellDoubleClicked.connect(self.std_data_progress)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)

        self.ui.lineEdit_7.textChanged.connect(self.video_search)
        self.ui.lineEdit_8.textChanged.connect(self.subject_search)

        self.ui.CameraFrame_4.resizeEvent = self.camera_resize
        #############Validators###################
        self.ui.lineEdit_2.setValidator(self.onlyInt)
        self.ui.lineEdit_3.setValidator(self.onlyInt)
        self.ui.usernameLineEdit.setValidator(self.onlyInt)
        self.ui.phoneNumberLineEdit.setValidator(self.onlyInt)
        self.ui.rollNumberLineEdit.setValidator(self.onlyInt)
        self.ui.fatherSPhoneNumberLineEdit.setValidator(self.onlyInt)
        self.ui.IDNumberLineEdit_4.setValidator(self.onlyInt)
        self.ui.phoneNumberLineEdit_4.setValidator(self.onlyInt)
        self.ui.rollNumberLineEdit_2.setValidator(self.onlyInt)
        self.ui.phoneNumberLineEdit_2.setValidator(self.onlyInt)
        self.ui.phoneNumberLineEdit_9.setValidator(self.onlyInt)
        self.ui.fatherSPhoneNumberLineEdit_2.setValidator(self.onlyInt)
        self.ui.fatherSPhoneNumberLineEdit_7.setValidator(self.onlyInt)
        self.ui.phoneNumberLineEdit_5.setValidator(self.onlyInt)

    def pass_variable(self):
        pass
    def test_screen(self):
        import datetime
        from datetime import date,datetime
        
        today=date.today()
        c_year,c_month,c_day=str(today).split('-')
        d2 = datetime(int(c_year),int(c_month),int(c_day))
        now = datetime.now().time()
        c_hour,c_min,c_sec=str(now).split(':')

        self.ui.tableWidget_7.setRowCount(0)
        try:
            self.ui.textEdit_2.clear()
            self.playlist.clear()
            self.camerathread.stop()
        except:
            pass

        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')     
        conn = sqlite3.connect(f"{data_path}/Student_info.db")
        cur = conn.cursor()
        cur.execute(f'Select Sign_Name,Test_Completed,Start_Date,End_Date FROM Student_Tests where ID == {self.std_roll_number};')
        passw2=cur.fetchall()
        conn.close()
        
        for details in passw2:
                row_number = self.ui.tableWidget_7.rowCount()
                if row_number == len(passw2):
                    pass
                else:
                    if details[1]=='Yes':
                        pass
                    else:
                        text=details[2]
                        start=text.split(' ')
                        text2=start[0]
                        year,month,day=text2.split('-')
                        c_year,c_month,c_day=str(today).split('-')
                        d1=datetime(int(year),int(month),int(day))
                        if d2<d1:
                            pass
                        elif d2>d1:
                            etext=details[3]
                            end=etext.split(' ')
                            text2=end[0]
                            year,month,day=text2.split('-')
                            d11=datetime(int(year),int(month),int(day))
                            if d2>d11:
                                
                                conn = sqlite3.connect(f"{data_path}/Student_info.db")
                                cur = conn.cursor()
                                sql=''' UPDATE Student_Tests
                                        SET Marks_Obtained = ?, Test_Completed= ? 
                                        WHERE ID = ? AND Sign_Name= ?''' 
                                data2=(0,'Yes',self.std_roll_number,details[0])
                                cur.execute(sql,data2)
                                conn.commit()
                                conn.close()
                            elif d2==d11:
                                text3=end[1]
                                hr,min=text3.split(':')
                                
                                if hr>c_hour:
                                    self.ui.tableWidget_7.insertRow(row_number)
                                elif hr<c_hour:
                                    conn = sqlite3.connect(f"{data_path}/Student_info.db")
                                    cur = conn.cursor()
                                    sql=''' UPDATE Student_Tests
                                            SET Marks_Obtained = ?, Test_Completed= ? 
                                            WHERE ID = ? AND Sign_Name= ?''' 
                                    data2=(0,'Yes',self.std_roll_number,details[0])
                                    cur.execute(sql,data2)
                                    conn.commit()
                                    conn.close()
                                else:   
                                    if min>c_min:
                                        self.ui.tableWidget_7.insertRow(row_number)
                                    else:
                                
                                        conn = sqlite3.connect(f"{data_path}/Student_info.db")
                                        cur = conn.cursor()
                            
                                        sql=''' UPDATE Student_Tests
                                                SET Marks_Obtained = ?, Test_Completed= ? 
                                                WHERE ID = ? AND Sign_Name= ?''' 
                                        data2=(0,'Yes',self.std_roll_number,details[0])
                                        cur.execute(sql,data2)
                                        conn.commit()
                                        conn.close()
                            else:
                                self.ui.tableWidget_7.insertRow(row_number)
                        else:
                            etext=details[3]
                            end=etext.split(' ')
                            text2=end[0]
                            year,month,day=text2.split('-')
                            d11=datetime(int(year),int(month),int(day))
                            if d2>d11:
                                conn = sqlite3.connect(f"{data_path}/Student_info.db")
                                cur = conn.cursor()
                                sql=''' UPDATE Student_Tests
                                        SET Marks_Obtained = ?, Test_Completed= ? 
                                        WHERE ID = ? AND Sign_Name= ?''' 
                                data2=(0,'Yes',self.std_roll_number,details[0])
                                cur.execute(sql,data2)
                                conn.commit()
                                conn.close()
                            elif d2==d11:
                
                                text3=end[1]
                                hr,min=text3.split(':')
                                if hr>c_hour:
                                    self.ui.tableWidget_7.insertRow(row_number)
                                elif hr<c_hour:
                                    conn = sqlite3.connect(f"{data_path}/Student_info.db")
                                    cur = conn.cursor()
                                    sql=''' UPDATE Student_Tests
                                            SET Marks_Obtained = ?, Test_Completed= ? 
                                            WHERE ID = ? AND Sign_Name= ?''' 
                                    data2=(0,'Yes',self.std_roll_number,details[0])
                                    cur.execute(sql,data2)
                                    conn.commit()
                                    conn.close()
                                else:
                                    if min>c_min:
                                        self.ui.tableWidget_7.insertRow(row_number)
                                    else:
                                        conn = sqlite3.connect(f"{data_path}/Student_info.db")
                                        cur = conn.cursor()
                                        sql=''' UPDATE Student_Tests
                                                SET Marks_Obtained = ?, Test_Completed= ? 
                                                WHERE ID = ? AND Sign_Name= ?''' 
                                        data2=(0,'Yes',self.std_roll_number,details[0])
                                        cur.execute(sql,data2)
                                        conn.commit()
                                        conn.close()
                            else:
                                self.ui.tableWidget_7.insertRow(row_number)
                for column_number, data in enumerate(details):
                    self.ui.tableWidget_7.setItem(
                    row_number, column_number, QTableWidgetItem(str(data)))
        self.ui.tableWidget_7.itemDoubleClicked.connect(self.perform_test)
        self.ui.stackedWidget_2.setCurrentIndex(5)

    def test_back_screen(self):
        self.ui.stackedWidget_2.setCurrentIndex(0)
    
    def main(self):
        try:
            self.camerathread.stop()
        except:
            pass
        self.ui.stackedWidget_2.setCurrentIndex(0)

    def progress(self):
        try:
            self.ui.textEdit_2.clear()
            self.playlist.clear()
            self.camerathread.stop()
        except:
            pass
        try:
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
        except:
            pass
    
    def std_data(self):
        try:
            self.ui.textEdit_2.clear()
            self.playlist.clear()
            self.camerathread.stop()
        except:
            pass
        b=self.retrieveTestinfoValue()
        if len(b)==0:
            popup=QMessageBox()
            popup.setWindowTitle("Assign Tests")
            popup.setText("Please Select One or More Students to Assign Tests")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_() 
        else:
            if len(b)==1:
                temp=b[0]
                current_row = self.ui.tableWidget_5.currentRow()
                current_column = self.ui.tableWidget_5.currentColumn()
                if current_column!=0:
                    pass
                else:
                    self.test_roll_no = temp[0]
                    path=pathlib.Path(__file__).parent.absolute().joinpath('Videos')
                    path=str(path)
                    self.dirModel.setRootPath(path)
                    self.ui.treeView_3.setRootIndex(self.model.index(path))
                    self.test_users.append(temp[0])
                    self.ui.stackedWidget_2.setCurrentIndex(15)
            else:
                temp=b[0]
                current_row = self.ui.tableWidget_5.currentRow()
                current_column = self.ui.tableWidget_5.currentColumn()
                if current_column!=0:
                    pass
                else:
                    for i in range(len(b)):
                        temp=b[i]
                        self.test_users.append(temp[0])
                    if self.subject == "Computer":
                        path=pathlib.Path(__file__).parent.absolute().joinpath('Videos',self.subject)
                    else:
                        path=pathlib.Path(__file__).parent.absolute().joinpath('Videos',self.subject,self.folder)
                    path=str(path)
                    self.dirModel.setRootPath(path)
                    self.ui.treeView_3.setRootIndex(self.model.index(path))
                    
                    self.ui.stackedWidget_2.setCurrentIndex(15)
    def Assign_Test_By_Class(self):
        try:
            self.ui.textEdit_2.clear()
            self.playlist.clear()
            self.camerathread.stop()
        except:
            pass
        passw=subprocess.check_output([sys.executable, "Test_By_Class.py"])
        passw=str(passw.decode("utf-8"))
        passw=passw[:-2]
        if passw==None:
            pass
        elif passw=="":
            pass
        else:
            self.class_assign=passw
            path=pathlib.Path(__file__).parent.absolute().joinpath('Videos')
            path=str(path)
            self.dirModel.setRootPath(path)
            self.ui.treeView_3.setRootIndex(self.model.index(path))
            self.ui.stackedWidget_2.setCurrentIndex(15)
        

    def std_teach_back(self):
        try:
            self.ui.textEdit_2.clear()
            self.playlist.clear()
            self.camerathread.stop()
        except:
            pass
        self.ui.tableWidget_6.setRowCount(0)
        self.ui.stackedWidget_2.setCurrentIndex(9)

    def std_data_progress(self):
        try:
            self.ui.textEdit_2.clear()
            self.playlist.clear()
            self.camerathread.stop()
        except:
            pass
        current_row = self.ui.tableWidget.currentRow()
        current_column = self.ui.tableWidget.currentColumn()
        self.ui.tableWidget_7.setRowCount(0)
        if current_column!=0:
            pass
        else:
            self.test_roll_no = self.ui.tableWidget.item(current_row, current_column).text()
            self.ui.stackedWidget_2.setCurrentIndex(9)
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
            self.ui.stackedWidget_2.setCurrentIndex(16)

    def Add_Teacher(self):
        #b=self.retrieveTeacherinfoValue()
        self.ui.stackedWidget_2.setCurrentIndex(11)
        
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
                    
                    self.ui.stackedWidget_2.setCurrentIndex(8)
                else:
                    popup.setWindowTitle("Create Teacher User")
                    popup.setText(f'The Roll Number Already Exsists')
                    popup.setStandardButtons(QMessageBox.Ok)
                    popup.setIcon(QMessageBox.Critical)
                    popup.exec_()

    def Add_Teacher_Back(self):
        self.ui.stackedWidget_2.setCurrentIndex(8)

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
            self.ui.stackedWidget_2.setCurrentIndex(12)
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
            self.ui.stackedWidget_2.setCurrentIndex(8)


        
        

    def Update_Teacher_Credentials_Back(self):
        self.ui.stackedWidget_2.setCurrentIndex(8)

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
        try:
            self.ui.textEdit_2.clear()
            self.playlist.clear()
            self.camerathread.stop()
        except:
            pass
        self.ui.stackedWidget_2.setCurrentIndex(10)

    def Add_Student_Credentials(self):
        popup=QMessageBox()
        if self.ui.studentNameLineEdit_2.text()=="" or self.ui.fatherSNameLineEdit_2.text()=="" or self.ui.rollNumberLineEdit_2.text()=="" or self.ui.phoneNumberLineEdit_2.text()=="" or self.ui.fatherSPhoneNumberLineEdit_2.text()=="" or self.ui.gradeComboBox_2.currentText()=="":
            popup.setWindowTitle("Add Student User")
            popup.setText("Please Enter All Fields")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
        else:
            std_name=self.ui.studentNameLineEdit_2.text()
            std_father_name=self.ui.fatherSNameLineEdit_2.text()
            std_roll_no=self.ui.rollNumberLineEdit_2.text()
            std_ph_no=self.ui.phoneNumberLineEdit_2.text()
            std_fathers_ph_no=self.ui.fatherSPhoneNumberLineEdit_2.text()
            std_class=self.ui.gradeComboBox_2.currentText()

            if self.ui.radioButton_3.isChecked():
                gender="Male"
            elif self.ui.radioButton_4.isChecked():
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
                    self.ui.stackedWidget_2.setCurrentIndex(9)
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
                    
                    self.ui.stackedWidget_2.setCurrentIndex(9)
                else:
                    popup.setWindowTitle("Add Student User")
                    popup.setText(f'The Roll Number Already Exsists')
                    popup.setStandardButtons(QMessageBox.Ok)
                    popup.setIcon(QMessageBox.Critical)
                    popup.exec_()

    def Back_Add_Student(self):
        self.ui.stackedWidget_2.setCurrentIndex(9)

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
            self.ui.stackedWidget_2.setCurrentIndex(13)
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
            self.ui.stackedWidget_2.setCurrentIndex(9)
    def Std_Update(self,i):
        if i.text() == '&Yes' :
            self.Student_Update()
        else:
            pass

    def Update_Student_Credentials_Submit(self):
        popup=QMessageBox()
        popup.setWindowTitle("Update Student")
        popup.setText(f"Are you sure you want to Update Student Information")
        popup.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        popup.setIcon(QMessageBox.Information)
        popup.buttonClicked.connect(self.Std_Update)
        popup.exec_()
        

    def Back_Update_Student(self):
        self.ui.stackedWidget_2.setCurrentIndex(9)

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
        try:
            if self.test_screen_condition==False:
                self.test_screen_condition=True
                popup=QMessageBox()
                popup.setWindowTitle("Perform Test")
                popup.setText(f"Please Put your hands down before the Camera is Turned On Press Ok When Ready")
                popup.setStandardButtons(QMessageBox.Ok)
                popup.setIcon(QMessageBox.Information)
                popup.exec_()
                sign=''
                current_row = self.ui.tableWidget_7.currentRow()
                current_column = self.ui.tableWidget_7.currentColumn()
                sign = self.ui.tableWidget_7.item(current_row, current_column).text()
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
                self.camerathread.previous_record=False
                self.camerathread.attempt_no=0
                self.test_accuracy=0
                self.test_attempt=0
                self.camerathread.reference_signs=reference_sign
                self.camerathread.acc_sign=sign
                self.video=sign
                self.ui.label_13.setText(f'Sign Name:{sign}')
                self.camerathread.record=False
                self.camerathread.start()
                self.camerathread.ImageUpdate.connect(self.ImageUpdateSlot_sentences)
                self.camerathread.accuracyUpdate.connect(self.accuracyUpdateSlot)
                self.camerathread.accuracy_reset.connect(self.accuracy_reset)
        except:
            pass
    

        
    def test_back_button(self,i):
        if i.text() == 'OK' :
            self.ui.tableWidget_7.setRowCount(0)
            data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
            conn = sqlite3.connect(f"{data_path}/Student_info.db")
            cur = conn.cursor()
            sql='''UPDATE Student_Tests
                SET Marks_Obtained = (?), Test_Completed = (?)
                WHERE ID = (?) AND Sign_Name = (?);'''
            data=(0,"Yes",self.std_roll_number,self.test_sign)
            cur.execute(sql,data)
            conn.commit()
            conn.close()

            data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
            conn = sqlite3.connect(f"{data_path}/Student_info.db")
            cur = conn.cursor()
            cur.execute(f'SELECT Sign_Name,Marks_Obtained,Test_Completed,Path FROM Student_Tests where ID == {self.std_roll_number};')
            passw=cur.fetchall()
            self.test_screen_condition=False
            
            self.acc2=0
            self.camerathread.stop()
            self.sentences_pass=0
            self.sentences=[]
            self.camerathread.sentences_pass_on=False
            self.ui.stackedWidget_2.setCurrentIndex(0)
            self.test_accuracy=0
            self.test_attempt=0
        else:
            self.camerathread.stop()

        
    def test_back(self):
        if self.test_attempt<3:
            
            popup=QMessageBox()
            popup.setWindowTitle("Test Incompleted")
            popup.setText(f"You Have not the completed the test Pressing Ok will record the test marks as Zero")
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
        self.ui.stackedWidget_2.setCurrentIndex(0)
        self.ui.tableWidget_2.setRowCount(0)

    def students_info_back(self):
        self.ui.stackedWidget_2.setCurrentIndex(0)
        self.ui.tableWidget.setRowCount(0)

    def manage_teachers(self):
        try:
            self.ui.textEdit_2.clear()
            self.playlist.clear()
            self.camerathread.stop()
        except:
            pass
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

        self.ui.stackedWidget_2.setCurrentIndex(8)

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

    def retrieveTestinfoValue(self):
        list1=[]
        for row in range(self.ui.tableWidget_5.rowCount()):
            if self.ui.tableWidget_5.item(row,0).checkState()==Qt.CheckState.Checked:
                list1.append([self.ui.tableWidget_5.item(row,col).text() for col in range(self.ui.tableWidget_5.columnCount())])
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
        try:
            self.ui.textEdit_2.clear()
            self.playlist.clear()
            self.camerathread.stop()
        except:
            pass
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

        self.ui.stackedWidget_2.setCurrentIndex(9)

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
            self.test_screen_condition=False
            popup=QMessageBox()
            popup.setWindowTitle("Test Submission")
            popup.setText(f"Test has been Submitted")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Information)
            popup.exec_()
            self.camerathread.stop()
            self.camerathread.sentences_pass_on=False
            self.ui.tableWidget_7.setRowCount(0)
            self.ui.tableWidget_4.setRowCount(0)
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
        try:
            self.ui.textEdit_2.clear()
            self.playlist.clear()
            self.camerathread.stop()
        except:
            pass
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
                if column_number==0:
                    chkBoxItem =QTableWidgetItem(str(data))
                    chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    chkBoxItem.setCheckState(QtCore.Qt.Unchecked)       
                    self.ui.tableWidget_5.setItem(row_number,column_number,chkBoxItem)
                else:
                    self.ui.tableWidget_5.setItem(
                    row_number, column_number, QTableWidgetItem(str(data)))
        self.ui.stackedWidget_2.setCurrentIndex(14)

    def search_manage_tests(self):
        self.ui.tableWidget_5.setRowCount(0)
        data=self.ui.lineEdit_5.text()
        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
        conn = sqlite3.connect(f"{data_path}/Student_info.db")
        cur = conn.cursor()
        if data:
            cur.execute("SELECT * FROM Std_In WHERE Roll_No LIKE ?",(data+'%',))
            passw=cur.fetchall()
            conn.close()
            for details in passw:
                row_number = self.ui.tableWidget_5.rowCount()
                if row_number == len(passw):
                    pass
                else:
                    self.ui.tableWidget_5.insertRow(row_number)
                for column_number, data in enumerate(details):
                    if column_number==0:
                        chkBoxItem =QTableWidgetItem(str(data))
                        chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                        chkBoxItem.setCheckState(QtCore.Qt.Unchecked)       
                        self.ui.tableWidget_5.setItem(row_number,column_number,chkBoxItem)
                    else:
                        self.ui.tableWidget_5.setItem(
                        row_number, column_number, QTableWidgetItem(str(data)))

        else:
            conn.close()
            self.manage_tests()


    def back_manage_test(self):
        self.ui.stackedWidget_2.setCurrentIndex(0)

    def back_assign_test(self):
        self.ui.stackedWidget_2.setCurrentIndex(14)

    def manage_courses(self):
        try:
            self.ui.textEdit_2.clear()
            self.playlist.clear()
            self.camerathread.stop()
            
        except:
            pass
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.stackedWidget_2.setCurrentIndex(0)
        
    def forgot_password(self):
        passw=subprocess.check_output([sys.executable, "forgot_password.py"])
        passw=str(passw.decode("utf-8"))
        passw=passw[:-2]
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
                popup.setText("Incorrect Username or Password!")
                popup.setStandardButtons(QMessageBox.Ok)
                popup.setIcon(QMessageBox.Critical)
                popup.exec_()
            else:
                self.ui.tableWidget_7.setRowCount(0)
                for i in passw:
                    if int(a)==900:
                        self.user='Teacher'
                        self.ui.tableWidget_3.show()
                        self.ui.pushButton_18.show()
                        self.ui.pushButton_17.show()
                        #self.ui.pushButton_10.hide()
                        self.ui.pushButton_13.hide()
                        self.ui.pushButton_15.hide()

                        self.ui.pushButton_42.show()
                        self.ui.pushButton_41.show()
                        self.ui.pushButton_6.show()
                        self.ui.pushButton_39.show()
                        self.ui.pushButton_36.show()
                        self.ui.pushButton_37.show()
                        self.ui.pushButton_47.show()
                        self.ui.pushButton_48.show()
                        self.ui.pushButton_58.show()


                        self.ui.label_20.setText('Teacher')
                        self.ui.stackedWidget.setCurrentIndex(2)
                        self.ui.stackedWidget_2.setCurrentIndex(0)
                    elif i[2]=="S":
                        self.user='Student'
                        self.std_roll_number=a
                        self.ui.tableWidget_3.hide()
                        #self.ui.pushButton_10.hide()
                        self.ui.pushButton_18.hide()
                        self.ui.pushButton_13.show()
                        self.ui.pushButton_15.show()
                        self.ui.pushButton_17.hide()
                        self.ui.pushButton_47.hide()
                        self.ui.pushButton_48.hide()
                        self.ui.pushButton_58.hide()
                        self.ui.label_20.setText('Student')
                        self.ui.stackedWidget.setCurrentIndex(2)
                        self.ui.stackedWidget_2.setCurrentIndex(0)
                    else:
                        self.user='Teacher'
                        self.ui.tableWidget_3.show()
                        self.ui.pushButton_18.show()
                        self.ui.pushButton_17.show()
                        #self.ui.pushButton_10.hide()
                        self.ui.pushButton_13.hide()
                        self.ui.pushButton_15.hide()
                        self.ui.pushButton_42.hide()
                        self.ui.pushButton_41.hide()
                        self.ui.pushButton_6.hide()
                        self.ui.pushButton_39.hide()
                        self.ui.pushButton_36.hide()
                        self.ui.pushButton_37.hide()
                        self.ui.pushButton_47.hide()
                        self.ui.pushButton_58.show()
                        self.ui.pushButton_48.show()

                        self.ui.label_20.setText('Teacher')
                        self.ui.stackedWidget.setCurrentIndex(2)
                        self.ui.stackedWidget_2.setCurrentIndex(0)
    def logout(self):
        try:
            self.ui.textEdit_2.clear()
            self.playlist.clear()
            self.camerathread.stop()
        except:
            pass
        self.std_roll_number=0
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.stackedWidget_2.setCurrentIndex(0)
        
    def New_User(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def Create_New_User(self):
        try:
            self.ui.textEdit_2.clear()
            self.playlist.clear()
            self.camerathread.stop()
        except:
            pass
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
                else:
                    popup.setWindowTitle("Create User")
                    popup.setText("Roll Number Already Exists!")
                    popup.setStandardButtons(QMessageBox.Ok)
                    popup.setIcon(QMessageBox.Critical)
                    popup.exec_()
                    
    def sentence_screen(self):
        if self.ui.stackedWidget_2.currentIndex()==3:
            pass
        else:
            try:
                self.ui.textEdit_2.clear()
                self.playlist.clear()
            except:
                pass
            try:
                self.camerathread.stop()
                time.sleep(0.2)
            except:
                pass
            self.ui.tableWidget_7.setRowCount(0)
            self.sentences=[]
            self.ui.textEdit.clear()
            self.camerathread = cameraThread()
            self.camerathread.previous_record=False
            self.camerathread.reference_signs=all_data_sentences
            self.camerathread.acc_sign='A'
            self.video='A'
            self.sentence_accuracy=0
            self.hold_data=0
            self.ui.label_27.setText("Overall Accuracy = None")
            self.camerathread.record=False
            self.test_attempt=4
            self.camerathread.attempt_no=4
            try:
                self.camerathread.start()
            except:
                pass
            self.camerathread.ImageUpdate.connect(self.ImageUpdateSlot_sentences)
            self.camerathread.accuracyUpdate.connect(self.accuracyUpdateSlot)
            self.camerathread.accuracy_reset.connect(self.accuracy_reset)
            self.ui.stackedWidget_2.setCurrentIndex(3)
    
    def click(self,eve,subject,folder,video):
        self.select_video_new(subject,folder,video)

    def video_search(self):
        for i in reversed(range(self.ui.gridLayout_19.count())): 
            self.ui.gridLayout_19.itemAt(i).widget().setVisible(False)
        result = [v for v in list(self.vid_buttons.keys()) if self.ui.lineEdit_7.text().upper() in v]
        for l in result:
            for m in self.vid_buttons[l]:
                m.setVisible(True)
    
    def subject_search(self):
        for i in reversed(range(self.ui.gridLayout_20.count())): 
            self.ui.gridLayout_20.itemAt(i).widget().setVisible(False)
        result = [v for v in list(self.sub_buttons.keys()) if self.ui.lineEdit_8.text().upper() in v]
        for l in result:
                self.sub_buttons[l].setVisible(True)
        


    def video_browse(self,subject,folder):
        self.subject=subject
        self.current_folder=folder
        for i in reversed(range(self.ui.gridLayout_19.count())): 
            self.ui.gridLayout_19.itemAt(i).widget().deleteLater()
        r=0
        c=0
        
        if subject == "Computer":
            path=pathlib.Path(__file__).parent.absolute().joinpath('Videos',subject)
        else:
            path=pathlib.Path(__file__).parent.absolute().joinpath('Videos',subject,folder)
        videos=[]
        for i in path.glob('**/*'):
            if ".mp4" in i.name:
                videos.append(i.stem)
        self.vid_buttons= {}
        for i in range(len(videos)):
            frame = QtWidgets.QFrame(self.ui.frame_39)
            frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            frame.setFrameShadow(QtWidgets.QFrame.Raised)
            frame.setObjectName("frame")
            verticalLayout_15 = QtWidgets.QVBoxLayout(frame)
            verticalLayout_15.setObjectName("verticalLayout_15")
            label=QtWidgets.QLabel(frame)
            label.setMaximumSize(QtCore.QSize(400, 250))
            label.setText("")
            label.setPixmap(QtGui.QPixmap(f"Thumbnails/{folder}/{videos[i]}.jpg"))
            label.setScaledContents(True)
            label.mousePressEvent = lambda eve,subject=subject,folder=folder,video=videos[i],i=i: self.click(eve,subject,folder,video)
            label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            verticalLayout_15.addWidget(label)
            label_2 = QtWidgets.QLabel(frame)
            label_2.setText(f"{videos[i]}")
            font = QtGui.QFont()
            font.setPointSize(12)
            label_2.setFont(font)
            label_2.setObjectName("label_2")
            verticalLayout_15.addWidget(label_2)
            #print(r,c)
            self.vid_buttons[label_2.text().upper()]=[frame,label,label_2]
            self.ui.gridLayout_19.addWidget(frame, c, r, 1, 1)
            if r>1:
                c+=1
                r=0
            else:
                r+=1
        self.ui.stackedWidget_2.setCurrentIndex(7)
        
    def select_subject(self,subject):
        self.subject=subject
        
        path = pathlib.Path(__file__).parent.joinpath("Videos",subject)
        folders = [f.name for f in os.scandir(path) if f.is_dir()]
        for i in reversed(range(self.ui.gridLayout_20.count())): 
            self.ui.gridLayout_20.itemAt(i).widget().deleteLater()
        r=0
        c=0
        icon = QtGui.QIcon()
        self.sub_buttons={}
        for f in folders:
            icon.addPixmap(QtGui.QPixmap(f"./Icons/{f}.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            button = SubjectButton(self.ui.frame_47)
            button.setText("")
            button.setIcon(icon)
            button.setIconSize(QtCore.QSize(200, 100))
            button.setObjectName("button")
            button.setText(f)
            button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            button.clicked.connect(lambda x,subject=subject,folder=f: self.video_browse(subject,folder))
            button.entered.connect(lambda x=None,button=button :self.hover_icon(button))
            button.left.connect(lambda x=None,button=button :self.unhover_icon(button))
            self.sub_buttons[f.upper()]=button
            self.ui.gridLayout_20.addWidget(button, c, r, 1, 1)
            if r>1:
                c+=1
                r=0
            else:
                r+=1
        
        self.ui.stackedWidget_2.setCurrentIndex(1)

    def select_video_new(self,subject,folder,video):
        self.video=video
        self.subject=subject
        self.current_folder=folder
    
        data_signs=eval(f'{folder}_signs')
        if subject == "Computer":
            path=pathlib.Path(__file__).parent.absolute().joinpath('Videos',subject,f"{video}.mp4")
        else:
            path=pathlib.Path(__file__).parent.absolute().joinpath('Videos',subject,folder,f"{video}.mp4")

        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(str(path))))
        self.mediaPlayer.play()
        time.sleep(0.1)
        
        self.camerathread = cameraThread()
        try:
            self.camerathread.display_width=self.display_width
            self.camerathread.display_height=self.display_height
        except:
            pass
        self.camerathread.acc_sign=video
        self.video=video
        self.camerathread.record=False

        self.camerathread.reference_signs=data_signs
        self.current_reference_signs=data_signs
        try:
            self.camerathread.reference_signs=self.camerathread.reference_signs.append(self.new_ref)
        except:
            pass
            
        self.camerathread.start()
        self.camerathread.ImageUpdate.connect(self.ImageUpdateSlot)
        self.camerathread.accuracyUpdate.connect(self.accuracyUpdateSlot)
        self.camerathread.accuracy_reset.connect(self.accuracy_reset)
        self.ui.stackedWidget_2.setCurrentIndex(2)
        self.camerathread.sentences_pass_on=False

    def select_video_test(self,index): #For Student Video Assignment
            import re
            if self.class_assign==0:
                #path=pathlib.Path(__file__).parent.absolute().joinpath('Videos')     
                video = self.fileModel.fileName(index)
                videopath=self.fileModel.filePath(index)
                path=os.path.split(os.path.dirname(videopath))[-1]
                folder=path+'_signs'
                data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
                conn = sqlite3.connect(f"{data_path}/Student_info.db")
                cur = conn.cursor()
                path2=video.replace(".mp4","")
                sql= '''INSERT INTO Student_Tests (ID,Sign_Name,Marks_Obtained,
                        Test_Completed,Path,Start_Date,End_Date) VALUES (?,?,?,?,?,?,?)'''
                for users in self.test_users:
                    repeat_tests=0
                    
                    cur.execute(f"SELECT Test_Completed from Student_Tests WHERE ID=={users} AND Sign_Name=='{path2}' ;")
                    passw=cur.fetchall()
                    for i in range(len(passw)):
                        temp=passw[i]
                        if temp[0]=="No":
                            repeat_tests=1
                    if passw==None:
                        pass1=subprocess.check_output([sys.executable, "test_time.py"])
                        temp=str(pass1)
                        temp=temp.replace('b',"")
                        temp2=temp.split('\\r\\n')
                        if temp2==["''"]:
                            pass
                        else:
                            #YYYY-MM-DD HH:MM
                            temp3=temp2[2]+'-'+temp2[1]+'-'+temp2[0]+' '+temp2[3]+':'+temp2[4]

                            pass2=subprocess.check_output([sys.executable, "test_time_end.py"])
                            temp4=str(pass2)
                            temp4=temp4.replace('b',"")
                            temp5=temp4.split('\\r\\n')
                            if temp5==["''"]:
                                pass
                            else:
                                temp6=temp5[2]+'-'+temp5[1]+'-'+temp5[0]+' '+temp5[3]+':'+temp5[4]
                                data=(users,path2,0,'No',folder,temp3,temp6)  
                                cur.execute(sql,data)
                                conn.commit()
                                popup=QMessageBox()
                                popup.setWindowTitle("Assign Test")
                                popup.setText(f"Test of Sign={path2} has been Assigned to Roll_No {users}")
                                popup.setStandardButtons(QMessageBox.Ok)
                                popup.setIcon(QMessageBox.Information)
                                popup.exec_()
                        
                        
                    else:
                        if repeat_tests==1:
                            popup=QMessageBox()
                            popup.setWindowTitle("Assign Test")
                            popup.setText(f"Test of Sign={path2} has Already been Assigned to Roll_No {users}")
                            popup.setStandardButtons(QMessageBox.Ok)
                            popup.setIcon(QMessageBox.Critical)
                            popup.exec_()
                        else:
                            pass1=subprocess.check_output([sys.executable, "test_time.py"])
                            temp=str(pass1)
                            temp=temp.replace('b',"")
                            temp2=temp.split('\\r\\n')
                            if temp2==["''"]:
                                pass
                            else:
                                #YYYY-MM-DD HH:MM
                                temp3=temp2[2]+'-'+temp2[1]+'-'+temp2[0]+' '+temp2[3]+':'+temp2[4]
                                temp3=temp3.replace("'","")
                                pass2=subprocess.check_output([sys.executable, "test_time_end.py"])
                                temp4=str(pass2)
                                temp4=temp4.replace('b',"")
                                temp5=temp4.split('\\r\\n')
                                if temp5==["''"]:
                                    pass
                                else:
                                    temp6=temp5[2]+'-'+temp5[1]+'-'+temp5[0]+' '+temp5[3]+':'+temp5[4]
                                    temp6=temp6.replace("'","")
                                    data=(users,path2,0,'No',folder,temp3,temp6)
                                    cur.execute(sql,data)
                                    conn.commit()
                                    popup=QMessageBox()
                                    popup.setWindowTitle("Assign Test")
                                    popup.setText(f"Test of Sign={path2} has been Assigned to Roll_No {users}")
                                    popup.setStandardButtons(QMessageBox.Ok)
                                    popup.setIcon(QMessageBox.Information)
                                    popup.exec_()
                conn.close()
                self.test_users=[]
                self.ui.stackedWidget_2.setCurrentIndex(14)
            else:
                pass1=subprocess.check_output([sys.executable, "test_time.py"])
                temp=str(pass1)
                temp=temp.replace('b',"")
                temp2=temp.split('\\r\\n')
                if temp2==["''"]:
                    pass
                else:
                    #YYYY-MM-DD HH:MM
                    temp3=temp2[2]+'-'+temp2[1]+'-'+temp2[0]+' '+temp2[3]+':'+temp2[4]
                    temp3=temp3.replace("'","")
                    pass2=subprocess.check_output([sys.executable, "test_time_end.py"])
                    temp4=str(pass2)
                    temp4=temp4.replace('b',"")
                    temp5=temp4.split('\\r\\n')
                    if temp5==["''"]:
                        pass
                    else:
                        temp6=temp5[2]+'-'+temp5[1]+'-'+temp5[0]+' '+temp5[3]+':'+temp5[4]
                        temp6=temp6.replace("'","")
                        video = self.fileModel.fileName(index)
                        videopath2=self.fileModel.filePath(index)
                        path=os.path.split(os.path.dirname(videopath2))[-1]
                        folder=path+'_signs'
                        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
                        conn = sqlite3.connect(f"{data_path}/Student_info.db")
                        cur = conn.cursor()
                        path2=video.replace(".mp4","")
                        sql= '''INSERT INTO Student_Tests (ID,Sign_Name,Marks_Obtained,
                                Test_Completed,Path,Start_Date,End_Date) VALUES (?,?,?,?,?,?,?)'''
                        cur.execute(f'SELECT Roll_no From Std_In WHERE Class_Enroll = {self.class_assign};')
                        passw=cur.fetchall()
                        for i in range(len(passw)):
                            users=passw[i]
                            repeat_tests=0
                            data=(users[0],path2,0,'No',folder,temp3,temp6)
                            cur.execute(f"SELECT Test_Completed from Student_Tests WHERE ID=={users[0]} AND Sign_Name=='{path2}' ;")
                            passw1=cur.fetchall()
                            for i in range(len(passw1)):
                                temp=passw1[i]
                                if temp[0]=="No":
                                    repeat_tests=1
                            if passw1==None:

                                cur.execute(sql,data)
                                conn.commit()
                                popup=QMessageBox()
                                popup.setWindowTitle("Assign Test")
                                popup.setText(f"Test of Sign={path2} has been Assigned to Roll_No {users[0]}")
                                popup.setStandardButtons(QMessageBox.Ok)
                                popup.setIcon(QMessageBox.Information)
                                popup.exec_()
                                
                            else:
                                if repeat_tests==1:
                                    popup=QMessageBox()
                                    popup.setWindowTitle("Assign Test")
                                    popup.setText(f"Test of Sign={path2} has Already been Assigned to Roll_No {users[0]}")
                                    popup.setStandardButtons(QMessageBox.Ok)
                                    popup.setIcon(QMessageBox.Critical)
                                    popup.exec_()
                                else:
                                    cur.execute(sql,data)
                                    conn.commit()
                                    popup=QMessageBox()
                                    popup.setWindowTitle("Assign Test")
                                    popup.setText(f"Test of Sign={path2} has been Assigned to Roll_No {users[0]}")
                                    popup.setStandardButtons(QMessageBox.Ok)
                                    popup.setIcon(QMessageBox.Information)
                                    popup.exec_()
                conn.close()
                self.test_users=[]
                self.class_assign=0
                self.ui.stackedWidget_2.setCurrentIndex(14)

    def select_video(self,index):
        video = self.fileModel.fileName(index)
        path=''
        folders=['Adjectives', 'Adverbs', 'Airport', 'Alphabets', 'Appliances', 'Around_the_house',
                'Basic_Phrases', 'Bathroom', 'Bedroom', 'Body_Anatomy', 'Buildings_Places', 'Calendar_Time'
                , 'Classroom', 'Clothes_Accessories', 'Colors', 'Computer', 'Countries_Continents', 'Drinks',
                'Farming_Agriculture', 'Food_General', 'Fruits', 'Geography', 'Government', 'Grammar', 'Health_Medical Care',
                'Holidays_Celebrations', 'Insects_Spiders_Reptiles', 'Kitchen', 'Law_Order', 'Living_Room', 'Mammals',
                    'Mathematics', 'Media', 'Military', 'Numbers', 'Pakistan_Places', 'Professions', 'Science', 'Sports_Games',
                    'Suena_Letras', 'Transport', 'Verbs', 'Weather']
        folder=''
        
        for i in folders:
            #path=pathlib.Path(__file__).parent.absolute().joinpath('videos',i,video)
            if self.subject == "Computer":
                path=pathlib.Path(__file__).parent.absolute().joinpath('Videos',self.subject,i,video)
            else:
                path=pathlib.Path(__file__).parent.absolute().joinpath('Videos',self.subject,self.folder,i,video)
            if path.is_file():
                folder=i
                break

        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(str(path))))
        self.mediaPlayer.play()
        time.sleep(0.1)

        monis=eval(f'{folder}_signs')
        self.camerathread = cameraThread()
        self.camerathread.reference_signs=monis
        self.camerathread.acc_sign=video[:-4]
        self.video=video[:-4]
        self.camerathread.record=False
        try:
            self.camerathread.reference_signs=self.camerathread.reference_signs.append(self.new_ref)
        except:
            pass
            
        self.camerathread.start()
        self.camerathread.previous_record=False
        self.camerathread.ImageUpdate.connect(self.ImageUpdateSlot)
        self.camerathread.accuracyUpdate.connect(self.accuracyUpdateSlot)
        self.camerathread.accuracy_reset.connect(self.accuracy_reset)
        self.ui.stackedWidget_2.setCurrentIndex(2)
        self.camerathread.sentences_pass_on=False
    
    def back_video(self):
        self.ui.textEdit_2.clear()
        self.playlist.clear()
        self.camerathread.stop()
        try:
            self.videoThread.key1=False
            self.videoThread.stop()
        except:
            pass
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
        self.ui.stackedWidget_2.setCurrentIndex(7)
    def back_videos(self):
        if self.subject=="Computer":
            self.ui.stackedWidget_2.setCurrentIndex(0)
        else:
            self.ui.stackedWidget_2.setCurrentIndex(1)
        
        self.sentences_pass=0
        self.sentences=[]

    def sentence_back(self):
        self.camerathread.stop()
        try:
            self.videoThread.stop()
            self.videoThread.key1=False
        except:
            pass
        self.ui.textEdit.clear()
        self.ui.stackedWidget_2.setCurrentIndex(0)
        self.sentences_pass=0
        self.test_attempt=4
        self.sentences=[]
        self.camerathread.sentences_pass_on=False
        
    def new_account_cancel(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def add_video(self):
        root=pathlib.Path.cwd()
        import threading
        folder=self.current_folder
        if folder=='Computer':
            datapath=pathlib.Path(__file__).parent.absolute().joinpath('data',f'{folder}_dataset')
            folder_path=pathlib.Path(__file__).parent.absolute().joinpath('Videos',folder)
        else:
            datapath=pathlib.Path(__file__).parent.absolute().joinpath('data',f'{folder}_dataset')
            folder_path=pathlib.Path(__file__).parent.absolute().joinpath('Videos',self.subject,folder)
                
        fileName, _ = QFileDialog.getOpenFileName(None,"add Video",str(folder_path),filter="*.mp4")
        
        
        progress=QProgressDialog()
        progress.setLabelText("Video being Processed Please wait......")
        progress.setCancelButton(None)
        progress.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        if fileName:
            file=QFileInfo(fileName).fileName()
            video_path=fileName
            video_data_path=pathlib.Path(datapath).joinpath(file[:-4])
            if folder=='Computer':
                if os.path.exists(str(root)+'\\'+'Videos'+'\\'+folder+'\\'+file[:-4]+'.mp4'):
                    popup=QMessageBox()
                    popup.setWindowTitle("Video Already Exists")
                    popup.setText("Video Already Exists To Update First Remove the Video")
                    popup.setStandardButtons(QMessageBox.Ok)
                    popup.setIcon(QMessageBox.Critical)
                    popup.exec_()
                    
                else:
                    progress.show()
                    xy=threading.Thread(target=progress.setValue,args=(0,))
                    xy.start()
                    QApplication.processEvents()
                    video_dest_path=pathlib.Path(folder_path).joinpath(file) 
                    temp_vid_path=pathlib.Path(__file__).parent.absolute().joinpath('temp_videos')
                    yx=threading.Thread(target=progress.setValue,args=(10,))
                    yx.start()
                    QApplication.processEvents()
                    
                    datapath=str(datapath)+'\\'+file[:-4]
                    shutil.copyfile(video_path,video_dest_path)
                    trim.trim(file[:-4],video_path,temp_vid_path)
                    vid1=f'{file[:-4]}_1'
                    vid2=f'{file[:-4]}_2'
                    x=threading.Thread(target=progress.setValue,args=(20,))
                    x.start()
                    QApplication.processEvents()
                    temp1=str(video_data_path)+'\\'+vid1
                    temp2=str(video_data_path)+'\\'+vid2
                    save_landmarks_from_new_video(vid1,temp_vid_path,temp1,datapath)
                    
                    y=threading.Thread(target=progress.setValue,args=(40,))
                    y.start()
                    QApplication.processEvents()
                    save_landmarks_from_new_video(vid2,temp_vid_path,temp2,datapath)
                    
                    z=threading.Thread(target=progress.setValue,args=(60,))
                    QApplication.processEvents()
                    z.start()
                    
                    self.new_ref=new_load_reference_signs(file[:-4],[vid1,vid2],folder)
                    exec(f'{folder}_signs.append(self.new_ref)')

                    xyz=threading.Thread(target=progress.setValue,args=(80,))
                    xyz.start()
                    QApplication.processEvents()
                    cp=pathlib.Path.cwd()
                    op=pathlib.Path(cp).joinpath('Thumbnails',folder,f"{file[:-4]}.jpg")
                    pathlib.Path(cp).joinpath('Thumbnails',folder).mkdir(parents=True, exist_ok=True)
                    video_path=str(video_path)
                    video_path=video_path.replace('/','\\')
                    print(video_path)
                    print(op)

                    from ffmpy import FFmpeg
                    ff_path=pathlib.Path.cwd()
                    ff_path2=str(ff_path)+'\\'+'ffmpeg'+'\\'+'bin'+'\\'+'ffmpeg.exe'
                    ff=FFmpeg(executable=ff_path2,inputs={video_path: None}, outputs={op: ['-ss', '00:00:2', '-vframes', '1']})
                    ff.run()
                    
                    progress.setValue(100)
                    QApplication.processEvents()
                    self.video_browse(self.subject,folder)
            else:
                if os.path.exists(str(root)+'\\'+'Videos'+'\\'+self.subject+'\\'+folder+'\\'+file[:-4]+'.mp4'):
                    popup=QMessageBox()
                    popup.setWindowTitle("Video Already Exists")
                    popup.setText("Video Already Exists To Update First Remove the Video")
                    popup.setStandardButtons(QMessageBox.Ok)
                    popup.setIcon(QMessageBox.Critical)
                    popup.exec_()
                    
                else:
                    progress.show()
                    xy=threading.Thread(target=progress.setValue,args=(0,))
                    xy.start()
                    QApplication.processEvents()
                    video_dest_path=pathlib.Path(folder_path).joinpath(file) 
                    temp_vid_path=pathlib.Path(__file__).parent.absolute().joinpath('temp_videos')
                    yx=threading.Thread(target=progress.setValue,args=(10,))
                    yx.start()
                    QApplication.processEvents()
                    
                    datapath=str(datapath)+'\\'+file[:-4]
                    shutil.copyfile(video_path,video_dest_path)
                    trim.trim(file[:-4],video_path,temp_vid_path)
                    vid1=f'{file[:-4]}_1'
                    vid2=f'{file[:-4]}_2'
                    x=threading.Thread(target=progress.setValue,args=(20,))
                    x.start()
                    QApplication.processEvents()
                    temp1=str(video_data_path)+'\\'+vid1
                    temp2=str(video_data_path)+'\\'+vid2
                    save_landmarks_from_new_video(vid1,temp_vid_path,temp1,datapath)
                    
                    y=threading.Thread(target=progress.setValue,args=(40,))
                    y.start()
                    QApplication.processEvents()
                    save_landmarks_from_new_video(vid2,temp_vid_path,temp2,datapath)
                    
                    z=threading.Thread(target=progress.setValue,args=(60,))
                    QApplication.processEvents()
                    z.start()

                    self.new_ref=new_load_reference_signs(file[:-4],[vid1,vid2],folder)
                    exec(f'{folder}_signs.append(self.new_ref)')

                    xyz=threading.Thread(target=progress.setValue,args=(80,))
                    xyz.start()
                    QApplication.processEvents()
                    cp=pathlib.Path.cwd()
                    op=pathlib.Path(cp).joinpath('Thumbnails',folder,f"{file[:-4]}.jpg")
                    pathlib.Path(cp).joinpath('Thumbnails',folder).mkdir(parents=True, exist_ok=True)
                    video_path=str(video_path)
                    video_path=video_path.replace('/','\\')
                    print(video_path)
                    print(op)

                    from ffmpy import FFmpeg
                    ff_path=pathlib.Path.cwd()
                    ff_path2=str(ff_path)+'\\'+'ffmpeg'+'\\'+'bin'+'\\'+'ffmpeg.exe'
                    ff=FFmpeg(executable=ff_path2,inputs={video_path: None}, outputs={op: ['-ss', '00:00:2', '-vframes', '1']})
                    ff.run()
                    
                    progress.setValue(100)
                    QApplication.processEvents()
                    self.video_browse(self.subject,folder)
    def delete_video(self):
        folder=self.current_folder
        if folder == "Computer":
            folder_path=pathlib.Path(__file__).parent.absolute().joinpath('Videos',folder)
            datapath=pathlib.Path(__file__).parent.absolute().joinpath('data','Computer_dataset')
        else:
            datapath=pathlib.Path(__file__).parent.absolute().joinpath('data',f'{folder}_dataset')
            folder_path=pathlib.Path(__file__).parent.absolute().joinpath('Videos',self.subject,folder)
        
        
        fileName, _ = QFileDialog.getOpenFileName(None,"Delete Video",str(folder_path),filter="*.mp4")
        temp_signs=eval(f'{folder}_signs')
        if fileName:
            file=QFileInfo(fileName).fileName()
            video_path=pathlib.Path(folder_path).joinpath(file)
            video_data_path=pathlib.Path(datapath).joinpath(file[:-4])
            thumb_path=pathlib.Path.cwd().joinpath('Thumbnails')
            path=str(thumb_path)+'\\'+folder+'\\'+file[:-4]+'.jpg'
            dataset=pathlib.Path.cwd().joinpath('data')
            data=str(dataset)+'\\'+folder+'_dataset'+'\\'+file[:-4]
            
            try:
                os.remove(video_path)
                os.remove(path)
                shutil.rmtree(video_data_path)
                shutil.rmtree(data)

                
                temp_signs.drop(temp_signs.index[temp_signs['name'] == file[:-4]], inplace=True)
            except:
                pass
        self.video_browse(self.subject,folder)
    ############# Video and Camera Feed ##################

    def camera_resize(self, resizeEvent:QResizeEvent):
        self.ui.label_18.resize(resizeEvent.size())
        self.display_width, self.display_height = self.ui.label_18.width(), self.ui.label_18.height()
        try:
            self.camerathread.display_width=self.display_width
            self.camerathread.display_height=self.display_height
        except:
            pass

    def ImageUpdateSlot(self, Image):
        self.ui.label_18.setPixmap(QPixmap.fromImage(Image))
        self.camerathread.sentences_pass_on=False

    def ImageUpdateSlot_sentences(self, Image):
        self.camerathread.sentences_pass_on=True
        self.ui.label_4.setPixmap(QPixmap.fromImage(Image))
        self.ui.label_7.setPixmap(QPixmap.fromImage(Image))
    def VideoUpdateSlot(self, Image):
        self.ui.label_18.setPixmap(QPixmap.fromImage(Image))
    
    def accuracyUpdateSlot(self,predicted,sign,dist,acc,out_left,out_right,attempt_no):
        acc=float(acc)
        self.test_attempt=attempt_no
        if acc==0:
            pass
        else:
            self.test_accuracy=acc
        # if self.test_attempt<3:
        #     if self.test_accuracy==0:
        #         if acc!=0:
        #             self.test_accuracy=acc
        #             self.test_attempt=0
        #     else:
        #         if dist[0]!=self.acc2 and acc!=0:
        #             if self.acc2==0:
        #                 self.test_attempt=0
        #                 self.camerathread.attempt_no=self.test_attempt
        #                 self.acc2=dist[0]
        #                 self.test_accuracy=acc
                    
        #             else:
        #                 self.acc2=dist[0]
        #                 self.test_accuracy=acc
        #                 self.test_attempt+=1
        #                 self.camerathread.attempt_no=self.test_attempt
        # else:
        if len(sign)<2:
            pass
        else:
            if self.sentences_pass==1:
                if len(predicted) <2:
                    if self.sentence_accuracy==0:
                        self.sentence_accuracy=acc
                        self.hold_data=1
                        self.ui.label_27.setText(f'Overall Accuracy = {self.sentence_accuracy}')
                    else:
                        self.sentence_accuracy+=acc
                        self.hold_data+=1
                        sentence_accuracy=self.sentence_accuracy/self.hold_data
                        self.ui.label_27.setText(f'Overall Accuracy = {sentence_accuracy}')

                    self.sentences.append(predicted)
                    self.ui.textEdit.insertPlainText(str(predicted))
                    
                else:
                    if self.sentence_accuracy==0:
                        self.sentence_accuracy=acc
                        self.hold_data=1
                        self.ui.label_27.setText(f'Overall Accuracy = {self.sentence_accuracy}')
                    else:
                        self.sentence_accuracy+=acc
                        self.hold_data+=1
                        sentence_accuracy=self.sentence_accuracy/self.hold_data
                        self.ui.label_27.setText(f'Overall Accuracy = {sentence_accuracy}')
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
                        if dist[i]==float('inf'):
                            acc1=0
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
        if self.sentences_pass==1:
            pass
        else:
            if acc>90:
                self.ui.textEdit_2.clear()
            if out_right==[] and out_left==[]:
                self.ui.textEdit_2.clear()
            else:
                c=[]
                if self.error==1:
                    if out_right!=[] and out_left==[]:
                        for i in out_right:
                                self.ui.textEdit_2.append(i)
                                self.right_list.append(i)
                                c.append(i)
                        self.error=0
                    elif out_left!=[]  and out_right==[]:
                        for i in out_left:
                                self.ui.textEdit_2.append(i)
                                self.left_list.append(i)
                                c.append(i)
                        self.error=0
                    else:
                        self.ui.textEdit_2.append("For Left Hand")
                        for i in out_left:
                            if i in c:
                                pass
                            else:
                                self.ui.textEdit_2.append(i)
                                self.left_list.append(i)
                                c.append(i)
                        self.ui.textEdit_2.append("For Right Hand")
                        c=[]
                        for i in out_right:
                            for i in c:
                                pass
                            else:
                                self.ui.textEdit_2.append(i)
                                self.right_list.append(i)
                                c.append(i)
                        self.error=0
                else:
                    pass

                
    def accuracy_reset(self):
        self.ui.label_16.setText('Recording Signs')
        self.ui.label_17.setText('')
        self.ui.textEdit_2.clear()
        self.sentences_pass=1
        self.error=1
        
    
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
        self.sentence_accuracy=0
        self.hold_data=0
        self.ui.label_27.setText('Overall Accuracy = None')
    def Back_sentences(self):
        if len(self.sentences) <1:
            pass
        else:
            self.sentences.remove(self.sentences[-1])
            self.ui.textEdit.clear()
            for i in self.sentences:
                self.ui.textEdit.insertPlainText(str(i))
        self.sentences_pass=0
    def add_space(self):
        self.sentences.append(" ")
        self.ui.textEdit.insertPlainText(str(" "))

    def back_to_camera(self):
        try:
            self.videoThread.stop()
            self.videoThread.key1=False
            self.camerathread = cameraThread()
            try:
                self.camerathread.display_width=self.display_width
                self.camerathread.display_height=self.display_height
            except:
                pass
            self.camerathread.acc_sign=self.video
            self.camerathread.reference_signs=self.current_reference_signs
            self.camerathread.record=False
            self.camerathread.start()
            self.camerathread.ImageUpdate.connect(self.ImageUpdateSlot)
            self.camerathread.accuracyUpdate.connect(self.accuracyUpdateSlot)
            self.camerathread.accuracy_reset.connect(self.accuracy_reset)
            self.ui.stackedWidget_2.setCurrentIndex(2)
            self.camerathread.sentences_pass_on=False
            self.left_list=[]
            self.right_list=[]
        except: 
            pass
    def pause_play(self):
        videoThread()
        if self.key1==True:
            self.key1=False
            videoThread.key1=False
        else:
            self.key1=True
            videoThread.key1=True
    def view_previous_recording(self):
        self.camerathread.stop()
        time.sleep(0.2)
        file_size = os.path.getsize('webcamimage.avi')
        convert_to_kb=file_size//1024
        if convert_to_kb<6:
            popup=QMessageBox()
            popup.setWindowTitle("See Previous Recording")
            popup.setText("First Record the Video By Placing your Hand")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
            self.camerathread = cameraThread()
            self.camerathread.acc_sign=self.video
            self.camerathread.reference_signs=self.current_reference_signs
            self.camerathread.record=False
            self.camerathread.start()
            self.camerathread.ImageUpdate.connect(self.ImageUpdateSlot)
            self.camerathread.accuracyUpdate.connect(self.accuracyUpdateSlot)
            self.camerathread.accuracy_reset.connect(self.accuracy_reset)
            self.ui.stackedWidget_2.setCurrentIndex(2)
            self.camerathread.sentences_pass_on=False
        else: 
            self.videoThread=videoThread()
            self.videoThread.leftlist=self.left_list
            self.videoThread.rightlist=self.right_list
            self.videoThread.ImageUpdate.connect(self.VideoUpdateSlot)
            self.videoThread.start()
    ############################Button Icons####################################
    def hover_icon(self,button):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"icons/{button.text()}_result.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        button.setIcon(icon)
    def unhover_icon(self,button):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"icons/{button.text()}.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        button.setIcon(icon)

    def closeEvent(self, event):
            close = QtWidgets.QMessageBox.question(self,
                                         "QUIT",
                                         "Are you sure want to Quit the Application?",
                                         QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if close == QtWidgets.QMessageBox.Yes:
                try:
                    self.videoThread.stop()
                    self.videoThread.key1=False
                except:
                    pass
                try:
                    self.camerathread.stop()
                except:
                    pass
                event.accept()
                
            else:
                event.ignore()

class cameraThread(QThread):
    reference_signs=''
    acc_sign=''
    attempt_no=4
    sentences_pass_on=False
    record=False
    sentence_key=False
    matrix_sign_predicted=''
    matrix_sign_accuracy_predicted=''
    previous_record=False
    accuracy_reset=pyqtSignal(str)
    ImageUpdate = pyqtSignal(QImage)
    accuracyUpdate=pyqtSignal(str,list,list,str,list,list,int)
    display_width=320
    display_height=240
    
    
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
        from cv2 import VideoWriter
        from cv2 import VideoWriter_fourcc
        condition=0
        test_condition=False
        self.sign_recorder = SignRecorder(self.reference_signs,self.acc_sign)
        self.ThreadActive = True
        webcam_manager = WebcamManager()
        if self.previous_record==False:
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

            video = VideoWriter('webcamimage.avi', VideoWriter_fourcc(*'MP42'), 2.0, (640, 480))

            with mediapipe.solutions.holistic.Holistic(
                min_detection_confidence=0.3, min_tracking_confidence=0.3
            ) as holistic:
                while self.ThreadActive:
                    
                    # Read feed
                    ret, frame = cap.read()

                    # Make detections
                    image, results = mediapipe_detection(frame, holistic)

                    # Process results
                    sign_detected, is_recording,sign,dist,out_left,out_right = self.sign_recorder.process_results(results)
                    if self.attempt_no==4:
                        pass
                    else:
                        if self.attempt_no!=3:
                            if is_recording and test_condition==False:
                                self.attempt_no+=1
                                test_condition=True
                    
                    # Update the frame (draw landmarks & display result)
                    FlippedImage,acc,test_no=webcam_manager.update(frame, results, sign_detected, is_recording,sign,dist,self.acc_sign,self.sentences_pass_on,self.attempt_no)
                    ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_BGR888)
                    Pic = ConvertToQtFormat.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
                    self.ImageUpdate.emit(Pic)
                    self.accuracyUpdate.emit(str(sign_detected),list(sign),list(dist),str(acc),list(out_left),list(out_right),int(self.attempt_no))
                    if test_no:
                        test_condition=False
                    if results.left_hand_landmarks:
                        if condition==0:
                            video = VideoWriter('webcamimage.avi', VideoWriter_fourcc(*'MP42'), 2.0, (640, 480))
                            condition=1
                        else:
                            self.on_release(True)
                            video.write(image)
                    elif results.right_hand_landmarks:
                        if condition==0:
                            video = VideoWriter('webcamimage.avi', VideoWriter_fourcc(*'MP42'), 2.0, (640, 480))
                            condition=1
                        else:
                            self.on_release(True)
                            video.write(image)
                    else:
                        if condition==0:
                            self.on_release(False)
                        else:
                            video.release()
                            
                            self.on_release(False)
                            condition=0
        else:
            print(True)
            while True:
                #This is to check whether to break the first loop
                isclosed=0
                cap = cv2.VideoCapture('webcam.avi')
                while (True):

                    ret, frame = cap.read()
                    # It should only show the frame when the ret is true
                    if ret == True:

                        cv2.imshow('frame',frame)
                        if cv2.waitKey(1) == 27:
                            # When esc is pressed isclosed is 1
                            isclosed=1
                            break
                    else:
                        break
                # To break the loop if it is closed manually
                if isclosed:
                    break
    def stop(self):
        self.ThreadActive = False
        self.quit()

class videoThread(QThread):
    ImageUpdate = pyqtSignal(QImage)
    leftlist=[]
    rightlist=[]
    key1=False

    
        

    def run(self):
        self.ThreadActive = True
        cap = cv2.VideoCapture("webcamimage.avi")
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_counter = 0
        webcam_manager=WebcamManager()
        with mediapipe.solutions.holistic.Holistic(
            min_detection_confidence=0.3, min_tracking_confidence=0.3
        ) as holistic:
            while self.ThreadActive:
                
                # Read feed
                ret, frame = cap.read()
                if frame_counter == length:
                    frame_counter = 0
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                frame_counter+=1

                # Make detections
                if ret:
                    image, results = mediapipe_detection(frame, holistic)

                # Update the frame (draw landmarks & display result)
                    FlippedImage=webcam_manager.update2(frame,results,frame_counter,self.leftlist,self.rightlist)
                    ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_BGR888)
                    Pic = ConvertToQtFormat.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
                    self.ImageUpdate.emit(Pic)
                    key = cv2.waitKey(1)
                    if self.key1==True:
                        cv2.waitKey(500)
    def stop(self):
            self.ThreadActive = False
            self.quit()


class SubjectButton(QtWidgets.QPushButton):
    entered = pyqtSignal()
    left = pyqtSignal()

    def enterEvent(self, event):
        super().enterEvent(event)
        self.entered.emit()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.left.emit()

def load_param(np,all_data_sentences):
    np1,all_data_sentences=newer_load_reference_signs(np,all_data_sentences)
    return np1,all_data_sentences

def load_param2(np):
    np1=newload_reference_signs(np)
    return np1


if __name__ == "__main__":
    import start_logo
    import multiprocessing
    bc=multiprocessing.Process(target=start_logo.main, args=())
    bc.start()
    dataset=pathlib.Path.cwd().joinpath('data')
    data_len=os.listdir(dataset)
    start_time = time.time()
    
    all_data_sentences=pd.DataFrame(columns=["name", "sign_model", "distance"])
    for i in data_len:
        if i=="Alphabets_dataset"or i=='Basic_Phrases_dataset':
            print(i)
            temp=[root for root,dirs,files in os.walk(f'data\\{i}') if not dirs]
            temp1,all_data_sentences=load_param(temp,all_data_sentences)
            temp3=i.replace("dataset","signs")
            exec(f'{temp3}=temp1')
        # else:
        #     print(i)
        #     temp=[root for root,dirs,files in os.walk(f'data\\{i}') if not dirs]
        #     temp1=load_param2(temp)
        #     temp3=i.replace("dataset","signs")
        #     exec(f'{temp3}=temp1')   
    end_time = time.time()
    bc.terminate()

    print(f"The execution time for loading is: {end_time-start_time}")
    
    app = QtWidgets.QApplication([])
    app.setWindowIcon(QtGui.QIcon("logo.png"))
    application = window()
    application.showMaximized()
    sys.exit(app.exec())