from cmath import inf
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
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
        MainWindow.setObjectName("Virtual Sign Language Avatar")
        MainWindow.resize(1280, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_15 = QtWidgets.QFrame(self.page)
        self.frame_15.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_15.setObjectName("frame_15")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.frame_15)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_3 = QtWidgets.QLabel(self.frame_15)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_11.addWidget(self.label_3)
        self.verticalLayout_2.addWidget(self.frame_15)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.frame = QtWidgets.QFrame(self.page)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.usernameLabel = QtWidgets.QLabel(self.frame)
        self.usernameLabel.setObjectName("usernameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.usernameLabel)
        self.usernameLineEdit = QtWidgets.QLineEdit(self.frame)
        self.usernameLineEdit.setObjectName("usernameLineEdit")
        self.usernameLineEdit.setValidator(self.onlyInt)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.usernameLineEdit)
        self.passwordLabel = QtWidgets.QLabel(self.frame)
        self.passwordLabel.setObjectName("passwordLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.passwordLabel)
        self.passwordLineEdit = QtWidgets.QLineEdit(self.frame)
        self.passwordLineEdit.setInputMask("")
        self.passwordLineEdit.setText("")
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLineEdit.setClearButtonEnabled(False)
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.passwordLineEdit)
        self.horizontalLayout.addLayout(self.formLayout)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_2.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.page)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.pushButton_14 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_14.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_14.setObjectName("pushButton_14")
        self.horizontalLayout_2.addWidget(self.pushButton_14)
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout_2.addWidget(self.frame_2)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem5)
        self.stackedWidget.addWidget(self.page)

        #Main Teachers Page
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_3 = QtWidgets.QFrame(self.page_2)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_2.addWidget(self.pushButton_3, 0, 1, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_2.addWidget(self.pushButton_5, 1, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 0, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_2.addWidget(self.pushButton_4, 1, 0, 1, 1)
        self.pushButton_27 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_27.setObjectName("pushButton_27")
        self.gridLayout_2.addWidget(self.pushButton_27, 2, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.frame_3)
        self.stackedWidget.addWidget(self.page_2)

        #Teachers Info Page
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.page_3)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.page_3)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_7.addWidget(self.lineEdit_2)
        self.label_2 = QtWidgets.QLabel(self.page_3)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_7.addWidget(self.label_2)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.page_3)
        self.tableWidget_2.setGridStyle(QtCore.Qt.SolidLine)
        
        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.setObjectName("tableWidget_2")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        self.verticalLayout_7.addWidget(self.tableWidget_2)
        self.pushButton_26 = QtWidgets.QPushButton(self.page_3)
        self.pushButton_26.setObjectName("pushButton_26")
        self.verticalLayout_7.addWidget(self.pushButton_26)
        self.stackedWidget.addWidget(self.page_3)


        #Students Info Page
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.page_4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_5 = QtWidgets.QFrame(self.page_4)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.pushButton_66 = QtWidgets.QPushButton(self.frame_5)
        self.pushButton_66.setObjectName("pushButton_66")
        self.horizontalLayout_3.addWidget(self.pushButton_66)
        self.pushButton_67 = QtWidgets.QPushButton(self.frame_5)
        self.pushButton_67.setObjectName("pushButton_67")
        self.horizontalLayout_3.addWidget(self.pushButton_67)
        self.verticalLayout_4.addWidget(self.frame_5)
        self.frame_4 = QtWidgets.QFrame(self.page_4)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.verticalLayout_4.addWidget(self.lineEdit_3)
        self.tablewidget = QtWidgets.QTableWidget(self.frame_4)
        self.tablewidget.setObjectName("tablewidget")
        self.tablewidget.setColumnCount(7)

        item = QtWidgets.QTableWidgetItem()
        self.tablewidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablewidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablewidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablewidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablewidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablewidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablewidget.setHorizontalHeaderItem(6, item)

        self.verticalLayout_5.addWidget(self.tablewidget)
        self.verticalLayout_4.addWidget(self.frame_4)
        self.stackedWidget.addWidget(self.page_4)


        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.page_5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_10 = QtWidgets.QFrame(self.page_5)
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_10)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label = QtWidgets.QLabel(self.frame_10)
        self.label.setObjectName("label")
        self.horizontalLayout_8.addWidget(self.label)
        self.verticalLayout_6.addWidget(self.frame_10)
        self.frame_6 = QtWidgets.QFrame(self.page_5)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.studentNameLabel = QtWidgets.QLabel(self.frame_6)
        self.studentNameLabel.setObjectName("studentNameLabel")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.studentNameLabel)
        self.studentNameLineEdit = QtWidgets.QLineEdit(self.frame_6)
        self.studentNameLineEdit.setObjectName("studentNameLineEdit")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.studentNameLineEdit)
        self.fatherSNameLabel = QtWidgets.QLabel(self.frame_6)
        self.fatherSNameLabel.setObjectName("fatherSNameLabel")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.fatherSNameLabel)
        self.fatherSNameLineEdit = QtWidgets.QLineEdit(self.frame_6)
        self.fatherSNameLineEdit.setObjectName("fatherSNameLineEdit")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.fatherSNameLineEdit)
        self.rollNumberLabel = QtWidgets.QLabel(self.frame_6)
        self.rollNumberLabel.setObjectName("rollNumberLabel")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.rollNumberLabel)
        self.rollNumberLineEdit = QtWidgets.QLineEdit(self.frame_6)
        self.rollNumberLineEdit.setObjectName("rollNumberLineEdit")
        self.rollNumberLineEdit.setValidator(self.onlyInt)
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.rollNumberLineEdit)
        self.phoneNumberLabel = QtWidgets.QLabel(self.frame_6)
        self.phoneNumberLabel.setObjectName("phoneNumberLabel")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.phoneNumberLabel)
        self.phoneNumberLineEdit = QtWidgets.QLineEdit(self.frame_6)
        self.phoneNumberLineEdit.setObjectName("phoneNumberLineEdit")
        self.phoneNumberLineEdit.setValidator(self.onlyInt)
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.phoneNumberLineEdit)
        self.genderLabel = QtWidgets.QLabel(self.frame_6)
        self.genderLabel.setObjectName("genderLabel")
        self.formLayout_3.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.genderLabel)
        self.frame_8 = QtWidgets.QFrame(self.frame_6)
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.radioButton = QtWidgets.QRadioButton(self.frame_8)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_6.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.frame_8)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout_6.addWidget(self.radioButton_2)
        self.formLayout_3.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.frame_8)
        
        self.frame_7 = QtWidgets.QFrame(self.frame_6)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        
        self.formLayout_3.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.frame_7)
        self.gradeLabel = QtWidgets.QLabel(self.frame_6)
        self.gradeLabel.setObjectName("gradeLabel")
        self.formLayout_3.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.gradeLabel)
        self.gradeComboBox = QtWidgets.QComboBox(self.frame_6)
        self.gradeComboBox.setObjectName("gradeComboBox")
        self.gradeComboBox.addItem("")
        self.gradeComboBox.setItemText(0, "")
        self.gradeComboBox.addItem("")
        self.gradeComboBox.addItem("")
        self.gradeComboBox.addItem("")
        self.gradeComboBox.addItem("")
        self.gradeComboBox.addItem("")
        self.formLayout_3.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.gradeComboBox)
        self.fatherSPhoneNumberLabel = QtWidgets.QLabel(self.frame_6)
        self.fatherSPhoneNumberLabel.setWordWrap(False)
        self.fatherSPhoneNumberLabel.setObjectName("fatherSPhoneNumberLabel")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.fatherSPhoneNumberLabel)
        self.fatherSPhoneNumberLineEdit = QtWidgets.QLineEdit(self.frame_6)
        self.fatherSPhoneNumberLineEdit.setObjectName("fatherSPhoneNumberLineEdit")
        self.fatherSPhoneNumberLineEdit.setValidator(self.onlyInt)
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.fatherSPhoneNumberLineEdit)
        self.horizontalLayout_4.addLayout(self.formLayout_3)
        self.verticalLayout_6.addWidget(self.frame_6)
        self.frame_9 = QtWidgets.QFrame(self.page_5)
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_9)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem7)
        self.pushButton_8 = QtWidgets.QPushButton(self.frame_9)
        self.pushButton_8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout_7.addWidget(self.pushButton_8)
        self.pushButton_7 = QtWidgets.QPushButton(self.frame_9)
        self.pushButton_7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout_7.addWidget(self.pushButton_7)
        self.verticalLayout_6.addWidget(self.frame_9)
        self.stackedWidget.addWidget(self.page_5)
        self.page_6 = QtWidgets.QWidget()
        self.page_6.setObjectName("page_6")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.page_6)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.frame_11 = QtWidgets.QFrame(self.page_6)
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_11)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_20 = QtWidgets.QLabel(self.frame_11)
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_9.addWidget(self.label_20)
        self.verticalLayout_8.addWidget(self.frame_11)
        self.frame_12 = QtWidgets.QFrame(self.page_6)
        self.frame_12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_12)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.frame_13 = QtWidgets.QFrame(self.frame_12)
        self.frame_13.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_13.setObjectName("frame_13")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frame_13)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.pushButton_10 = QtWidgets.QPushButton(self.frame_13)
        self.pushButton_10.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_10.setObjectName("pushButton_10")
        self.verticalLayout_9.addWidget(self.pushButton_10)
        self.pushButton_13 = QtWidgets.QPushButton(self.frame_13)
        self.pushButton_13.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_13.setObjectName("pushButton_13")
        self.verticalLayout_9.addWidget(self.pushButton_13)
        self.pushButton_15 = QtWidgets.QPushButton(self.frame_13)
        self.pushButton_15.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_15.setObjectName("pushButton_15")
        self.verticalLayout_9.addWidget(self.pushButton_15)

        self.pushButton_22 = QtWidgets.QPushButton(self.frame_13)
        self.pushButton_22.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) #Sentences button
        self.pushButton_22.setObjectName("pushButton_15")
        self.verticalLayout_9.addWidget(self.pushButton_22)

        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem8)
        self.pushButton_20 = QtWidgets.QPushButton(self.frame_13)
        self.pushButton_20.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_20.setObjectName("pushButton_20")
        self.verticalLayout_9.addWidget(self.pushButton_20)
        self.horizontalLayout_10.addWidget(self.frame_13)
        
        
        self.stackedWidget_2 = QtWidgets.QStackedWidget(self.frame_12)
        self.stackedWidget_2.setObjectName("stackedWidget_2")
        self.page_15 = QtWidgets.QWidget()
        self.page_15.setObjectName("page_15")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.page_15)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.frame_14 = QtWidgets.QFrame(self.page_15)
        self.frame_14.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_14.setObjectName("frame_14")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_14)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_11 = QtWidgets.QPushButton(self.frame_14)
        self.pushButton_11.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons8-test-tube-96.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_11.setIcon(icon)
        self.pushButton_11.setIconSize(QtCore.QSize(200, 100))
        self.pushButton_11.setObjectName("pushButton_11")
        self.gridLayout.addWidget(self.pushButton_11, 3, 1, 1, 1)
        self.pushButton_12 = QtWidgets.QPushButton(self.frame_14)
        self.pushButton_12.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons8-computer-128.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_12.setIcon(icon1)
        self.pushButton_12.setIconSize(QtCore.QSize(200, 100))
        self.pushButton_12.setObjectName("pushButton_12")
        self.gridLayout.addWidget(self.pushButton_12, 1, 1, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(self.frame_14)
        self.pushButton_9.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons8-abc-96.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_9.setIcon(icon2)
        self.pushButton_9.setIconSize(QtCore.QSize(200, 100))
        self.pushButton_9.setCheckable(False)
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout.addWidget(self.pushButton_9, 0, 1, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem9, 0, 2, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem10, 0, 0, 1, 1)
        self.verticalLayout_10.addWidget(self.frame_14)
        self.stackedWidget_2.addWidget(self.page_15)
        self.page_16 = QtWidgets.QWidget()
        self.page_16.setObjectName("page_16")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.page_16)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.treeview = QtWidgets.QTreeView(self.page_16)
        self.treeview.setObjectName("treeView")
        #self.treeWidget.headerItem().setText(0, "1")
        self.verticalLayout_12.addWidget(self.treeview)
        self.frame_16 = QtWidgets.QFrame(self.page_16)
        self.frame_16.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_16.setObjectName("frame_16")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frame_16)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem11)
        self.pushButton_18 = QtWidgets.QPushButton(self.frame_16)
        self.pushButton_18.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_18.setObjectName("pushButton_18")
        self.horizontalLayout_11.addWidget(self.pushButton_18)
        self.pushButton_17 = QtWidgets.QPushButton(self.frame_16)
        self.pushButton_17.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_17.setObjectName("pushButton_17")
        self.horizontalLayout_11.addWidget(self.pushButton_17)
        self.pushButton_16 = QtWidgets.QPushButton(self.frame_16)
        self.pushButton_16.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_16.setObjectName("pushButton_16")
        self.horizontalLayout_11.addWidget(self.pushButton_16)
        self.verticalLayout_12.addWidget(self.frame_16)
        self.stackedWidget_2.addWidget(self.page_16)
        self.page_7 = QtWidgets.QWidget()
        self.page_7.setObjectName("page_7")
        self.verticalLayout_23 = QtWidgets.QVBoxLayout(self.page_7)
        self.verticalLayout_23.setObjectName("verticalLayout_23")

        


        self.page_8 = QtWidgets.QWidget()
        self.page_8.setObjectName("page_8")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.page_8)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.frame_18 = QtWidgets.QFrame(self.page_8)
        self.frame_18.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_18.setObjectName("frame_18")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_18)
        self.gridLayout_3.setObjectName("gridLayout_3")

        #self.label_4 = QtWidgets.QLabel(self.frame_18)
        #self.label_4.setObjectName("label_4")

        self.label_4 = QtWidgets.QLabel(self.frame_18)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(640, 480))
        self.label_4.setObjectName("label_4")

        self.gridLayout_3.addWidget(self.label_4, 1, 0, 1, 1)
        spacerItem13 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem13, 2, 0, 1, 1)
        self.gridLayout_4.addWidget(self.frame_18, 0, 0, 1, 5)
        self.label_5 = QtWidgets.QLabel(self.page_8)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 1, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.page_8)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_4.addWidget(self.textEdit, 2, 0, 1, 5)
        self.pushButton_24 = QtWidgets.QPushButton(self.page_8)
        self.pushButton_24.setObjectName("pushButton_24")
        self.gridLayout_4.addWidget(self.pushButton_24, 3, 1, 1, 1)
        self.pushButton_23 = QtWidgets.QPushButton(self.page_8)
        self.pushButton_23.setObjectName("pushButton_23")
        self.gridLayout_4.addWidget(self.pushButton_23, 3, 2, 1, 1)
        self.pushButton_224 = QtWidgets.QPushButton(self.page_8)
        self.pushButton_224.setObjectName("pushButton_224")
        self.gridLayout_4.addWidget(self.pushButton_224, 3, 3, 1, 1)
        self.pushButton_225 = QtWidgets.QPushButton(self.page_8)
        self.pushButton_225.setObjectName("pushButton_225")
        self.gridLayout_4.addWidget(self.pushButton_225, 3, 4, 1, 1)
        self.stackedWidget_2.addWidget(self.page_8)
        self.horizontalLayout_10.addWidget(self.stackedWidget_2)


        self.stackedWidget_2.addWidget(self.page_8)
        self.horizontalLayout_10.addWidget(self.stackedWidget_2)
        







        self.frame_23 = QtWidgets.QFrame(self.page_7)
        self.frame_23.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_23.setObjectName("frame_23")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.frame_23)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.frame_25 = QtWidgets.QFrame(self.frame_23)
        self.frame_25.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_25.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_25.setObjectName("frame_25")
        self.verticalLayout_29 = QtWidgets.QVBoxLayout(self.frame_25)
        self.verticalLayout_29.setObjectName("verticalLayout_29")
        self.VideoWidget_4 = QtWidgets.QWidget(self.frame_25)
        self.VideoWidget_4.setObjectName("VideoWidget_4")
        self.verticalLayout_30 = QtWidgets.QVBoxLayout(self.VideoWidget_4)
        self.verticalLayout_30.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_30.setSpacing(0)
        self.verticalLayout_30.setObjectName("verticalLayout_30")
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.verticalLayout_30.addWidget(self.videoWidget)
        self.videoWidget.setMinimumSize(QtCore.QSize(352, 240))
        self.frame_28 = QtWidgets.QFrame(self.VideoWidget_4)
        self.frame_28.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_28.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_28.setObjectName("frame_28")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.frame_28)
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_14.setSpacing(5)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.pushButton_19 = QtWidgets.QPushButton(self.frame_28)
        self.pushButton_19.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_19.setObjectName("pushButton_19")
        self.horizontalLayout_14.addWidget(self.pushButton_19)
        self.horizontalSlider_4 = QtWidgets.QSlider(self.frame_28)
        self.horizontalSlider_4.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_4.setObjectName("horizontalSlider_4")
        self.horizontalLayout_14.addWidget(self.horizontalSlider_4)
        self.verticalLayout_30.addWidget(self.frame_28)
        self.verticalLayout_30.setStretch(0, 1)
        self.verticalLayout_29.addWidget(self.VideoWidget_4)
        self.frame_30 = QtWidgets.QFrame(self.frame_25)
        self.frame_30.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_30.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_30.setObjectName("frame_30")
        self.formLayout_6 = QtWidgets.QFormLayout(self.frame_30)
        self.formLayout_6.setObjectName("formLayout_6")
        self.label_16 = QtWidgets.QLabel(self.frame_30)
        self.label_16.setObjectName("label_16")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_16)
        self.label_17 = QtWidgets.QLabel(self.frame_30)
        self.label_17.setObjectName("label_17")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_17)
        self.verticalLayout_29.addWidget(self.frame_30)
        self.horizontalLayout_17.addWidget(self.frame_25)
        self.label_6 = QtWidgets.QLabel(self.frame_25)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_29.addWidget(self.label_6)
        self.textEdit_2 = QtWidgets.QTextEdit(self.frame_25)
        self.textEdit_2.setObjectName("textEdit_2")
        self.verticalLayout_29.addWidget(self.textEdit_2)
        self.horizontalLayout_17.addWidget(self.frame_25)
        self.frame_31 = QtWidgets.QFrame(self.frame_23)
        self.frame_31.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_31.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_31.setObjectName("frame_31")
        self.verticalLayout_31 = QtWidgets.QVBoxLayout(self.frame_31)
        self.verticalLayout_31.setObjectName("verticalLayout_31")
        self.CameraFrame_4 = QtWidgets.QFrame(self.frame_31)
        self.CameraFrame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.CameraFrame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.CameraFrame_4.setObjectName("CameraFrame_4")
        self.verticalLayout_32 = QtWidgets.QVBoxLayout(self.CameraFrame_4)
        self.verticalLayout_32.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_32.setSpacing(0)
        self.verticalLayout_32.setObjectName("verticalLayout_32")
        self.label_18 = QtWidgets.QLabel(self.CameraFrame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setMinimumSize(QtCore.QSize(640, 480))
        self.label_18.setObjectName("label_18")
        self.verticalLayout_32.addWidget(self.label_18)
        self.verticalLayout_31.addWidget(self.CameraFrame_4)
        self.frame_32 = QtWidgets.QFrame(self.frame_31)
        self.frame_32.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_32.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_32.setObjectName("frame_32")
        self.verticalLayout_33 = QtWidgets.QVBoxLayout(self.frame_32)
        self.verticalLayout_33.setObjectName("verticalLayout_33")
        # self.label_19 = QtWidgets.QLabel(self.frame_32)
        # self.label_19.setObjectName("label_19")
        # self.verticalLayout_33.addWidget(self.label_19)
        self.tableWidget_3 = QtWidgets.QTableWidget(self.frame_32)
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(2)
        self.tableWidget_3.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(1, 1, item)
        self.verticalLayout_33.addWidget(self.tableWidget_3)
        self.verticalLayout_31.addWidget(self.frame_32)
        self.horizontalLayout_17.addWidget(self.frame_31)
        self.verticalLayout_23.addWidget(self.frame_23)
        self.frame_17 = QtWidgets.QFrame(self.page_7)
        self.frame_17.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_17.setObjectName("frame_17")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.frame_17)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        spacerItem12 = QtWidgets.QSpacerItem(503, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem12)
        self.pushButton_21 = QtWidgets.QPushButton(self.frame_17)
        self.pushButton_21.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_21.setObjectName("pushButton_21")
        self.horizontalLayout_16.addWidget(self.pushButton_21)
        self.verticalLayout_23.addWidget(self.frame_17)
        self.stackedWidget_2.addWidget(self.page_7)

        
        self.stackedWidget_2.addWidget(self.page_8)
        self.horizontalLayout_10.addWidget(self.stackedWidget_2)
        self.verticalLayout_8.addWidget(self.frame_12)
        self.stackedWidget.addWidget(self.page_6)
        self.verticalLayout.addWidget(self.stackedWidget)

        #Test Screen
        self.page_9 = QtWidgets.QWidget()
        self.page_9.setObjectName("page_9")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.page_9)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.frame_19 = QtWidgets.QFrame(self.page_9)
        self.frame_19.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_19.setObjectName("frame_19")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.frame_19)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_7 = QtWidgets.QLabel(self.frame_19)
        self.label_7.setObjectName("label_7")
        self.gridLayout_6.addWidget(self.label_7, 1, 0, 1, 1)
        spacerItem14 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem14, 2, 0, 1, 1)
        self.gridLayout_7.addWidget(self.frame_19, 0, 0, 1, 2)
        
        self.label_8 = QtWidgets.QLabel(self.page_9)
        self.label_8.setObjectName("label_8")
        self.gridLayout_7.addWidget(self.label_8, 1, 0, 1, 1)
        
        self.lineEdit_4 = QtWidgets.QLineEdit(self.page_9)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_7.addWidget(self.lineEdit_4, 2, 0, 1, 1)

        self.pushButton_334 = QtWidgets.QPushButton(self.page_9)
        self.pushButton_334.setObjectName("pushButton_334")
        self.gridLayout_7.addWidget(self.pushButton_334, 3, 1, 1, 1)

        self.pushButton_29 = QtWidgets.QPushButton(self.page_9)
        self.pushButton_29.setObjectName("pushButton_29")
        self.gridLayout_7.addWidget(self.pushButton_29, 3, 2, 1, 1)

        self.stackedWidget_2.addWidget(self.page_9)
        self.page_10 = QtWidgets.QWidget()
        self.page_10.setObjectName("page_10")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.page_10)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.treeWidget_2 = QtWidgets.QTreeWidget(self.page_10)
        self.treeWidget_2.setObjectName("treeWidget_2")
        self.treeWidget_2.setColumnCount(1)
        self.treeWidget_2.setHeaderLabel("Assigned Tests")
        self.gridLayout_8.addWidget(self.treeWidget_2, 0, 0, 1, 1)
        self.frame_20 = QtWidgets.QFrame(self.page_10)
        self.frame_20.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_20.setObjectName("frame_20")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.frame_20)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem15)
        self.pushButton_35 = QtWidgets.QPushButton(self.frame_20)
        self.pushButton_35.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_35.setObjectName("pushButton_35")
        self.horizontalLayout_13.addWidget(self.pushButton_35)
        self.gridLayout_8.addWidget(self.frame_20, 1, 0, 1, 1)
        self.stackedWidget_2.addWidget(self.page_10)
        self.horizontalLayout_10.addWidget(self.stackedWidget_2)
        self.verticalLayout_8.addWidget(self.frame_12)
        self.stackedWidget.addWidget(self.page_6)
        self.verticalLayout.addWidget(self.stackedWidget)

        #Students Progress
        self.page_11 = QtWidgets.QWidget()
        self.page_11.setObjectName("page_11")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.page_11)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.frame_21 = QtWidgets.QFrame(self.page_11)
        self.frame_21.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_21.setObjectName("frame_21")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.frame_21)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.pushButton_34 = QtWidgets.QPushButton(self.frame_21)
        self.pushButton_34.setObjectName("pushButton_34")
        self.gridLayout_10.addWidget(self.pushButton_34, 1, 1, 1, 1)
        spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_10.addItem(spacerItem16, 1, 0, 1, 1)
        self.frame_22 = QtWidgets.QFrame(self.frame_21)
        self.frame_22.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_22.setObjectName("frame_22")
        self.formLayout_2 = QtWidgets.QFormLayout(self.frame_22)
        self.formLayout_2.setObjectName("formLayout_2")
        self.tableWidget_4 = QtWidgets.QTableWidget(self.frame_22)
        self.tableWidget_4.setObjectName("tableWidget_4")
        self.tableWidget_4.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(3, item)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.tableWidget_4)
        self.gridLayout_10.addWidget(self.frame_22, 0, 0, 1, 2)
        self.gridLayout_9.addWidget(self.frame_21, 0, 0, 1, 1)
        self.stackedWidget_2.addWidget(self.page_11)
        self.horizontalLayout_10.addWidget(self.stackedWidget_2)
        self.verticalLayout_8.addWidget(self.frame_12)
        self.stackedWidget.addWidget(self.page_6)
        self.verticalLayout.addWidget(self.stackedWidget)

        #Teacher's Test Screen
        self.page_12 = QtWidgets.QWidget()
        self.page_12.setObjectName("page_12")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.page_12)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.frame_26 = QtWidgets.QFrame(self.page_12)
        self.frame_26.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_26.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_26.setObjectName("frame_26")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.frame_26)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.tableWidget_5 = QtWidgets.QTableWidget(self.frame_26)
        self.tableWidget_5.setObjectName("tableWidget_5")
        self.tableWidget_5.setColumnCount(7)
        self.tableWidget_5.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(6, item)

        self.verticalLayout_13.addWidget(self.tableWidget_5)
        self.frame_24 = QtWidgets.QFrame(self.frame_26)
        self.frame_24.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_24.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_24.setObjectName("frame_24")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout(self.frame_24)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_18.addItem(spacerItem7)
        self.pushButton_38 = QtWidgets.QPushButton(self.frame_24)
        self.pushButton_38.setObjectName("pushButton_38")
        self.horizontalLayout_18.addWidget(self.pushButton_38)
        self.verticalLayout_13.addWidget(self.frame_24)
        self.gridLayout_11.addWidget(self.frame_26, 4, 0, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.page_12)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout_11.addWidget(self.lineEdit_5, 2, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.page_12)
        self.label_9.setObjectName("label_9")
        self.gridLayout_11.addWidget(self.label_9, 3, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_12)

        #Teacher's 2nd Test Screen 
        self.page_13 = QtWidgets.QWidget()
        self.page_13.setObjectName("page_13")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.page_13)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.treeview_3 = QtWidgets.QTreeView(self.page_13)
        self.treeview_3.setObjectName("treeview_3")
        self.gridLayout_12.addWidget(self.treeview_3, 1, 0, 1, 1)
        self.frame_27 = QtWidgets.QFrame(self.page_13)
        self.frame_27.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_27.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_27.setObjectName("frame_27")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout(self.frame_27)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_19.addItem(spacerItem8)
        self.pushButton_40 = QtWidgets.QPushButton(self.frame_27)
        self.pushButton_40.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_40.setObjectName("pushButton_40")
        self.horizontalLayout_19.addWidget(self.pushButton_40)
        self.gridLayout_12.addWidget(self.frame_27, 2, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.page_13)
        self.label_10.setObjectName("label_10")
        self.gridLayout_12.addWidget(self.label_10, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_13)

        #Student Progress (User Teacher)
        self.page_14 = QtWidgets.QWidget()
        self.page_14.setObjectName("page_14")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.page_14)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.frame_33 = QtWidgets.QFrame(self.page_14)
        self.frame_33.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_33.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_33.setObjectName("frame_33")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.frame_33)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        spacerItem19 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem19)
        self.pushButton_31 = QtWidgets.QPushButton(self.frame_33)
        self.pushButton_31.setObjectName("pushButton_31")
        self.horizontalLayout_12.addWidget(self.pushButton_31)
        self.gridLayout_5.addWidget(self.frame_33, 0, 0, 1, 1)
        
        self.frame_29 = QtWidgets.QFrame(self.page_14)
        self.frame_29.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_29.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_29.setObjectName("frame_29")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.frame_29)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.tableWidget_6 = QtWidgets.QTableWidget(self.frame_29)
        self.tableWidget_6.setObjectName("tableWidget_6")
        self.tableWidget_6.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_6.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_6.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_6.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_6.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_6.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_6.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_6.setHorizontalHeaderItem(3, item)
        self.verticalLayout_14.addWidget(self.tableWidget_6)
        self.gridLayout_5.addWidget(self.frame_29, 2, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_14)
        self.verticalLayout.addWidget(self.stackedWidget)


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        ################## New widgets ######################
        self.dirModel = QFileSystemModel()
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)
        self.fileModel = QFileSystemModel()
        self.fileModel.setFilter(QDir.NoDotAndDotDot |  QDir.Files)
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.treeview.setModel(self.model)
        self.treeview.hideColumn(1)
        self.treeview.hideColumn(2)
        self.treeview.hideColumn(3)
        self.treeview.doubleClicked.connect(self.select_video)

        
        
        self.treeview_3.setModel(self.model)
        self.treeview_3.hideColumn(1)
        self.treeview_3.hideColumn(2)
        self.treeview_3.hideColumn(3)
        self.treeview_3.doubleClicked.connect(self.select_video_test)
        
        self.playlist = QMediaPlaylist()
        #self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile('videos/alphabet/a.mp4')))
        self.playlist.setPlaybackMode(self.playlist.Loop)
        self.mediaPlayer.setPlaylist(self.playlist)
        ################## Connections ######################
        self.pushButton.clicked.connect(self.login)
        self.pushButton_14.clicked.connect(self.New_User)
        self.pushButton_9.clicked.connect(self.aphabets_folder)
        self.pushButton_11.clicked.connect(self.science_folder)
        self.pushButton_12.clicked.connect(self.computer_folder)
        self.pushButton_16.clicked.connect(self.back_videos)
        self.pushButton_21.clicked.connect(self.back_video)
        self.pushButton_19.clicked.connect(self.play)
        self.pushButton_19.setIcon(QtGui.QIcon('play-button.png'))
        self.pushButton_17.clicked.connect(self.delete_video)
        self.pushButton_18.clicked.connect(self.add_video)
        self.horizontalSlider_4.sliderMoved.connect(self.setPosition)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.passwordLineEdit.returnPressed.connect(self.pushButton.click)
        self.pushButton_20.clicked.connect(self.logout)
        self.pushButton_22.clicked.connect(self.sentence_screen)

        self.current_folder=''
        self.user='Student'
        # if self.user=='Student':
        #     self.tableWidget_3.hide()
        #     self.pushButton_18.hide()
        #     self.pushButton_17.hide()
        #     self.label_20.setText('Student')


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow", "Virtual Sign Teacher"))
        self.usernameLabel.setText(_translate("MainWindow", "Username"))
        self.passwordLabel.setText(_translate("MainWindow", "Password"))
        self.pushButton_14.setText(_translate("MainWindow", "New User"))
        self.pushButton.setText(_translate("MainWindow", "Sign In"))
        self.pushButton_2.setText(_translate("MainWindow", "Manage Teachers"))
        self.pushButton_3.setText(_translate("MainWindow", "Manage students"))
        self.pushButton_4.setText(_translate("MainWindow", "Manage Tests"))
        self.pushButton_5.setText(_translate("MainWindow", "Manage Courses"))
        self.label_9.setText(_translate("MainWindow", "Select Student For Test Assignment"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "Search Id"))
        self.lineEdit_3.setPlaceholderText(_translate("MainWindow", "Search Id"))
        self.lineEdit_5.setPlaceholderText(_translate("MainWindow", "Search Id"))

        self.lineEdit_2.setValidator(self.onlyInt)
        self.lineEdit_3.setValidator(self.onlyInt)

        self.lineEdit_2.textChanged.connect(self.teachers_search)
        self.lineEdit_3.textChanged.connect(self.students_search)
        self.lineEdit_5.textChanged.connect(self.search_manage_tests)
        


        self.pushButton_2.clicked.connect(self.manage_teachers)
        self.pushButton_3.clicked.connect(self.manage_students)
        self.pushButton_4.clicked.connect(self.manage_tests)
        self.pushButton_5.clicked.connect(self.manage_courses)


        self.label_2.setText(_translate("MainWindow", "Teachers"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Assigned Subject"))


        

        self.label.setText(_translate("MainWindow", "New Account"))
        self.label_6.setText(_translate("MainWindow", "Points Information"))
        self.studentNameLabel.setText(_translate("MainWindow", "Student Name"))
        self.fatherSNameLabel.setText(_translate("MainWindow", "Father\'s Name"))
        self.rollNumberLabel.setText(_translate("MainWindow", "Roll Number"))
        self.phoneNumberLabel.setText(_translate("MainWindow", "Phone Number"))
        self.phoneNumberLineEdit.setPlaceholderText(_translate("MainWindow", "Phone-No"))
        self.genderLabel.setText(_translate("MainWindow", "Gender"))
        self.radioButton.setText(_translate("MainWindow", "Male"))
        self.radioButton_2.setText(_translate("MainWindow", "Female"))

        item = self.tableWidget_4.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableWidget_4.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Sign Name"))
        item = self.tableWidget_4.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Marks Obtained"))
        item = self.tableWidget_4.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Test Completed"))

        item = self.tablewidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Roll_No"))
        item = self.tablewidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Student_Name"))
        item = self.tablewidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Fathers_Name"))
        item = self.tablewidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Phone"))
        item = self.tablewidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Fathers_Phone"))
        item = self.tablewidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Gender"))
        item = self.tablewidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Class_Enroll"))
        self.tablewidget.cellDoubleClicked.connect(self.std_data_progress)


        item = self.tableWidget_5.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Roll_No"))
        item = self.tableWidget_5.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Student_Name"))
        item = self.tableWidget_5.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Fathers_Name"))
        item = self.tableWidget_5.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Phone"))
        item = self.tableWidget_5.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Fathers_Phone"))
        item = self.tableWidget_5.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Gender"))
        item = self.tableWidget_5.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Class_Enroll"))

        self.tableWidget_5.cellDoubleClicked.connect(self.std_data)
        
        
       
        self.gradeLabel.setText(_translate("MainWindow", "Class"))
        self.gradeComboBox.setItemText(1, _translate("MainWindow", "1"))
        self.gradeComboBox.setItemText(2, _translate("MainWindow", "2"))
        self.gradeComboBox.setItemText(3, _translate("MainWindow", "3"))
        self.gradeComboBox.setItemText(4, _translate("MainWindow", "4"))
        self.gradeComboBox.setItemText(5, _translate("MainWindow", "5"))
        
        self.fatherSPhoneNumberLabel.setText(_translate("MainWindow", "Father\'s Phone \n"
"Number"))
        self.fatherSPhoneNumberLineEdit.setPlaceholderText(_translate("MainWindow", "Phone-No"))
        self.pushButton_8.setText(_translate("MainWindow", "Cancel"))
        self.pushButton_7.setText(_translate("MainWindow", "Done"))

        self.pushButton_7.clicked.connect(self.Create_New_User)
        self.pushButton_8.clicked.connect(self.logout)
        self.label_20.setText(_translate("MainWindow", "Student"))
        self.pushButton_10.setText(_translate("MainWindow", "Courses"))
        self.pushButton_13.setText(_translate("MainWindow", "Tests"))
        self.pushButton_15.setText(_translate("MainWindow", "Progress"))
        self.pushButton_22.setText(_translate("MainWindow", "Sentences"))
        self.pushButton_11.setText(_translate("MainWindow", "Science"))
        self.pushButton_12.setText(_translate("MainWindow", "Computer"))
        self.pushButton_9.setText(_translate("MainWindow", "Alphabets"))
        self.pushButton_16.setText(_translate("MainWindow", "Back"))
        self.pushButton_18.setText(_translate("MainWindow", "Add Video"))
        self.pushButton_17.setText(_translate("MainWindow", "Delete Video"))
        self.pushButton_27.setText(_translate("MainWindow","Logout"))
        #self.pushButton_19.setText(_translate("MainWindow", "PushButton"))
        self.textEdit_2.setPlaceholderText(_translate("MainWindow", "If any Error in Gesture is made it will be displayed Here"))
        self.label_16.setText(_translate("MainWindow", "Closest Sign:"))
        self.label_17.setText(_translate("MainWindow", "None"))
        #self.label_18.setText(_translate("MainWindow", "TextLabel"))
        #self.label_19.setText(_translate("MainWindow", "TextLabel"))
        self.label_8.setText(_translate("MainWindow","Attempt Number"))
        self.pushButton_20.setText(_translate("MainWindow", "Log Out"))
        self.pushButton_21.setText(_translate("MainWindow", "Back"))
        self.pushButton_24.setText(_translate("MainWindow", "Clear All"))
        self.pushButton_23.setText(_translate("MainWindow", "BackSpace"))
        self.pushButton_26.setText(_translate("MainWindow","Back"))
        self.pushButton_29.setText(_translate("MainWindow", "Back"))
        self.pushButton_35.setText(_translate("MainWindow", "Back"))
        self.pushButton_334.setText(_translate("MainWindow", "Submit"))
        self.pushButton_34.setText(_translate("MainWindow", "Back"))
        self.pushButton_224.setText(_translate("MainWindow", "Add Space"))
        self.pushButton_225.setText(_translate("MainWindow", "Back"))
        self.pushButton_66.setText(_translate("MainWindow","Remove Student"))
        self.pushButton_67.setText(_translate("MainWindow","Back"))
        self.pushButton_38.setText(_translate("MainWindow", "Back")) #Teacher's Test Screen Buttons
        self.pushButton_40.setText(_translate("MainWindow", "Back")) #Teacher's Test Screen Buttons

        self.pushButton_31.setText(_translate("MainWindow", "Back"))
        
        
        item = self.tableWidget_6.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableWidget_6.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Sign"))
        item = self.tableWidget_6.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Marks_Obtained"))
        item = self.tableWidget_6.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Test_Completed"))

        self.pushButton_31.clicked.connect(self.std_teach_back)

        item = self.tableWidget_3.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Actual: No"))
        item = self.tableWidget_3.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Actual: Yes"))
        item = self.tableWidget_3.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Predicted:\nNo"))
        item = self.tableWidget_3.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Predicted:\nYes"))
        __sortingEnabled = self.tableWidget_3.isSortingEnabled()
        self.tableWidget_3.setSortingEnabled(False)
        item = self.tableWidget_3.item(0, 0)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget_3.item(0, 1)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget_3.item(1, 0)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget_3.item(1, 1)
        item.setText(_translate("MainWindow", "0"))
        self.tableWidget_3.setSortingEnabled(__sortingEnabled)
        self.pushButton_24.clicked.connect(self.clear_sentences)
        self.pushButton_23.clicked.connect(self.Back_sentences)
        self.pushButton_224.clicked.connect(self.add_space)
        self.pushButton_225.clicked.connect(self.sentence_back)
        self.pushButton_27.clicked.connect(self.logout)
        self.pushButton_26.clicked.connect(self.teachers_back)
        self.pushButton_66.clicked.connect(self.remove_student)
        self.pushButton_67.clicked.connect(self.students_info_back)
        self.pushButton_29.clicked.connect(self.test_back)
        self.pushButton_35.clicked.connect(self.test_back_screen)
        self.pushButton_13.clicked.connect(self.test_screen)
        self.pushButton_334.clicked.connect(self.submit_test)
        self.pushButton_34.clicked.connect(self.back_progress)
        self.pushButton_15.clicked.connect(self.progress)
        self.pushButton_38.clicked.connect(self.back_manage_test)
        self.pushButton_40.clicked.connect(self.back_assign_test)

    def test_screen(self):
        #self.std_roll_number
        self.stackedWidget_2.setCurrentIndex(5)
        self.treeWidget_2.clear()
        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
        conn = sqlite3.connect(f"{data_path}/Student_info.db")
        cur = conn.cursor()
        cur.execute(f'SELECT Sign_Name,Marks_Obtained,Test_Completed,Path FROM Student_Tests where ID == {self.std_roll_number};')
        passw=cur.fetchall()
        
        if passw==None:
            parent=QtWidgets.QTreeWidgetItem(1)
            parent.setText(0,"No Tests Are Assigned #Winning")
            self.treeWidget_2.addTopLevelItem(parent)
        else:
            for i in passw:
                if i[2]=="No":
                    parent=QtWidgets.QTreeWidgetItem(1)
                    parent.setText(0,f"{i[0]}")
                    self.treeWidget_2.addTopLevelItem(parent)
                    
                    conn.close()
            self.treeWidget_2.itemDoubleClicked.connect(self.perform_test)
            
            
        
        #     pass
        # elif passw[2]=="No":
        #     sign=passw[1]
        #     parent=QtWidgets.QTreeWidgetItem(1)
        #     parent.setText(0,sign)
        #     self.treeWidget_2.addTopLevelItem(parent)

        
        


        
        


        #self.treeWidget_2.expandAll()
        #self.treeWidget_2.itemClicked.connect(self.perform_test)
    def test_back_screen(self):
        self.stackedWidget_2.setCurrentIndex(0)

    def progress(self):
        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
        conn = sqlite3.connect(f"{data_path}/Student_info.db")
        cur = conn.cursor()
        cur.execute(f'SELECT ID,Sign_Name,Marks_Obtained,Test_Completed FROM Student_Tests where ID == {self.std_roll_number};')
        passw=cur.fetchall()
        conn.close()
        for details in passw:
            row_number = self.tableWidget_4.rowCount()
            if row_number == len(passw):
                pass
            else:
                self.tableWidget_4.insertRow(row_number)
            for column_number, data in enumerate(details):
                self.tableWidget_4.setItem(
                row_number, column_number, QTableWidgetItem(str(data)))
        self.stackedWidget_2.setCurrentIndex(6)
        
    def std_data(self):
        current_row = self.tableWidget_5.currentRow()
        current_column = self.tableWidget_5.currentColumn()
        if current_column!=0:
            pass
        else:
            self.test_roll_no = self.tableWidget_5.item(current_row, current_column).text()
            path=pathlib.Path(__file__).parent.absolute().joinpath('videos')
            path=str(path)
            self.dirModel.setRootPath(path)
            self.treeview_3.setRootIndex(self.model.index(path))
            self.stackedWidget.setCurrentIndex(7)

    def std_teach_back(self):
        self.tableWidget_6.setRowCount(0)
        self.stackedWidget.setCurrentIndex(3)

    def std_data_progress(self):
        current_row = self.tablewidget.currentRow()
        current_column = self.tablewidget.currentColumn()
        
        if current_column!=0:
            pass
        else:
            self.test_roll_no = self.tablewidget.item(current_row, current_column).text()
            self.stackedWidget.setCurrentIndex(3)
            data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
            conn = sqlite3.connect(f"{data_path}/Student_info.db")
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM Student_Tests Where ID = {self.test_roll_no};')
            passw=cur.fetchall()
            conn.close()
            for details in passw:
                row_number = self.tableWidget_6.rowCount()
                if row_number == len(passw):
                    pass
                else:
                    self.tableWidget_6.insertRow(row_number)
                for column_number, data in enumerate(details):
                    self.tableWidget_6.setItem(
                    row_number, column_number, QTableWidgetItem(str(data)))
            self.stackedWidget.setCurrentIndex(8)

    

                
            
    
        


    def perform_test(self):
        popup=QMessageBox()
        popup.setText(f"Please Put your hands down before the Camera is Turned On Press Ok When Ready")
        popup.setStandardButtons(QMessageBox.Ok)
        popup.setIcon(QMessageBox.Information)
        popup.exec_()
        sign=''
        for ix in self.treeWidget_2.selectedIndexes():
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
        self.stackedWidget_2.setCurrentIndex(4)
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
            self.stackedWidget_2.setCurrentIndex(5)
            self.test_accuracy=0
            self.test_attempt=0
        else:
            pass

        
    def test_back(self):
        if self.test_attempt<3:
            popup=QMessageBox()
            popup.setText(f"You Have not the completed the test Pressing Ok will not record the test marks")
            popup.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            popup.setIcon(QMessageBox.Information)
            popup.buttonClicked.connect(self.test_back_button)
            popup.exec_()
        elif self.test_attempt==3:
            popup=QMessageBox()
            popup.setText(f"Press the Submit Button to record the marks the test is completed")
            popup.setStandardButtons(QMessageBox.Ok )
            popup.setIcon(QMessageBox.Information)
            popup.exec_()


    def teachers_back(self):
        self.stackedWidget.setCurrentIndex(1)
        self.tableWidget_2.setRowCount(0)

    def students_info_back(self):
        self.stackedWidget.setCurrentIndex(1)
        self.tablewidget.setRowCount(0)

    def manage_teachers(self):
        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
        conn = sqlite3.connect(f"{data_path}/Teachers_info.db")
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM Teacher_Info;')
        passw=cur.fetchall()
        conn.close()
        for details in passw:
            row_number = self.tableWidget_2.rowCount()
            if row_number == len(passw):
                pass
            else:
                self.tableWidget_2.insertRow(row_number)
            for column_number, data in enumerate(details):
                self.tableWidget_2.setItem(
                row_number, column_number, QTableWidgetItem(str(data)))

        self.stackedWidget.setCurrentIndex(2)

    def teachers_search(self):
        self.tableWidget_2.setRowCount(0)
        data=self.lineEdit_2.text()
        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
        conn = sqlite3.connect(f"{data_path}/Teachers_info.db")
        cur = conn.cursor()
        if data:
            cur.execute(f'SELECT * FROM Teacher_Info WHERE ID LIKE {data};')
            passw=cur.fetchall()
            conn.close()
            for details in passw:
                row_number = self.tableWidget_2.rowCount()
                if row_number == len(passw):
                    pass
                else:
                    self.tableWidget_2.insertRow(row_number)
                for column_number, data in enumerate(details):
                    self.tableWidget_2.setItem(
                    row_number, column_number, QTableWidgetItem(str(data)))
        else:
            conn.close()
            self.manage_teachers()

    def manage_students(self):
        data=self.lineEdit_3.text()
        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
        conn = sqlite3.connect(f"{data_path}/Student_info.db")
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM Std_In ;')
        passw=cur.fetchall()
        conn.close()
        for details in passw:
            row_number = self.tablewidget.rowCount()
            if row_number == len(passw):
                pass
            else:
                self.tablewidget.insertRow(row_number)
            for column_number, data in enumerate(details):
                self.tablewidget.setItem(
                row_number, column_number, QTableWidgetItem(str(data)))

        self.stackedWidget.setCurrentIndex(3)

    def students_search(self):
        self.tablewidget.setRowCount(0)
        data=self.lineEdit_3.text()
        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
        conn = sqlite3.connect(f"{data_path}/Student_info.db")
        cur = conn.cursor()
        if data:
            cur.execute(f'SELECT * FROM Std_In WHERE Roll_No LIKE {data};')
            passw=cur.fetchall()
            conn.close()
            for details in passw:
                row_number = self.tablewidget.rowCount()
                if row_number == len(passw):
                    pass
                else:
                    self.tablewidget.insertRow(row_number)
                for column_number, data in enumerate(details):
                    self.tablewidget.setItem(
                    row_number, column_number, QTableWidgetItem(str(data)))

        else:
            conn.close()
            self.manage_students()

    def back_progress(self):
        self.stackedWidget_2.setCurrentIndex(0)
        self.tableWidget_4.setRowCount(0)

    def submit_test(self):
        if self.test_attempt==3:
            popup=QMessageBox()
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
            


            self.stackedWidget_2.setCurrentIndex(0)
        else:
            popup=QMessageBox()
            popup.setText(f"First Attempt the Test")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Information)
            popup.exec_()
        

    def manage_tests(self):
        data=self.lineEdit_5.text()
        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
        conn = sqlite3.connect(f"{data_path}/Student_info.db")
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM Std_In ;')
        passw=cur.fetchall()
        conn.close()
        for details in passw:
            row_number = self.tableWidget_5.rowCount()
            if row_number == len(passw):
                pass
            else:
                self.tableWidget_5.insertRow(row_number)
            for column_number, data in enumerate(details):
                 self.tableWidget_5.setItem(
                row_number, column_number, QTableWidgetItem(str(data)))
        self.stackedWidget.setCurrentIndex(6)

    def search_manage_tests(self):
        self.tableWidget_5.setRowCount(0)
        data=self.lineEdit_5.text()
        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
        conn = sqlite3.connect(f"{data_path}/Student_info.db")
        cur = conn.cursor()
        if data:
            cur.execute(f'SELECT * FROM Std_In WHERE Roll_No LIKE {data};')
            passw=cur.fetchall()
            conn.close()
            for details in passw:
                row_number = self.tableWidget_5.rowCount()
                if row_number == len(passw):
                    pass
                else:
                    self.tableWidget_5.insertRow(row_number)
                for column_number, data in enumerate(details):
                    self.tableWidget_5.setItem(
                    row_number, column_number, QTableWidgetItem(str(data)))

        else:
            conn.close()
            self.manage_tests()


    def back_manage_test(self):
        self.stackedWidget.setCurrentIndex(1)

    def back_assign_test(self):
        self.stackedWidget.setCurrentIndex(6)

    def manage_courses(self):
        self.stackedWidget.setCurrentIndex(5)
        
    def remove_student(self):
        pass

    def login(self):
        data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')
        conn = sqlite3.connect(f"{data_path}/Login.db")
        cur = conn.cursor()
        
        a=self.usernameLineEdit.text()
        b=self.passwordLineEdit.text()
        popup=QMessageBox()
        if a=="" or b=="":
            popup.setText("Username or Password not entered!")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
        else:
            cur.execute(f'SELECT Roll_no ,Password FROM Login_S where Roll_no == {a} AND Password == "{b}";')
            passw=cur.fetchone()
            conn.close()
            if passw==None:
                popup.setText("Incorrect Username or Password!")
                popup.setStandardButtons(QMessageBox.Ok)
                popup.setIcon(QMessageBox.Critical)
                popup.exec_()
            else:
                #print("Credentails Accepted")
                #print(pathlib.Path.cwd().joinpath('videos\Alphabets'))
                if int(a)==900:
                    self.user='Teacher'
                    self.tableWidget_3.show()
                    self.pushButton_18.show()
                    self.pushButton_17.show()
                    self.pushButton_10.hide()
                    self.pushButton_13.hide()
                    self.pushButton_15.hide()
                    self.label_20.setText('Teacher')
                    self.stackedWidget.setCurrentIndex(1)
                else:
                    self.user='Student'
                    self.std_roll_number=a
                    self.tableWidget_3.hide()
                    self.pushButton_10.hide()
                    self.pushButton_18.hide()
                    self.pushButton_13.show()
                    self.pushButton_15.show()
                    self.pushButton_17.hide()
                    self.label_20.setText('Student')
                    self.stackedWidget.setCurrentIndex(5)
                    self.stackedWidget_2.setCurrentIndex(0)
    def logout(self):
        self.std_roll_number=0
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(0)
        
    def New_User(self):
        self.stackedWidget.setCurrentIndex(4)

    def Create_New_User(self):
        popup=QMessageBox()
        if self.studentNameLineEdit.text()=="" or self.fatherSNameLineEdit.text()=="" or self.rollNumberLineEdit.text()=="" or self.phoneNumberLineEdit.text()=="" or self.fatherSPhoneNumberLineEdit.text()=="" or self.gradeComboBox.currentText()=="":
            popup.setText("Please Enter All Fields")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
        else:
            std_name=self.studentNameLineEdit.text()
            fath_name=self.fatherSNameLineEdit.text()
            roll_no=int(self.rollNumberLineEdit.text())
            phone=int(self.phoneNumberLineEdit.text())
            fath_phone=int(self.fatherSPhoneNumberLineEdit.text())
            class_enroll=int(self.gradeComboBox.currentText())
            
            if self.radioButton.isChecked():
                gender="Male"
            elif self.radioButton_2.isChecked():
                gender='Female'
            else:
                popup.setText("Please Enter All Fields")
                popup.setStandardButtons(QMessageBox.Ok)
                popup.setIcon(QMessageBox.Critical)
                popup.exec_()



            data=(roll_no,std_name,fath_name,phone,fath_phone,gender,class_enroll)

            if std_name == '' or fath_name == '' or roll_no =='' or phone == '':
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
                    sql2=''' INSERT INTO LOGIN_s (Roll_No,Password) VALUES (?,?) '''
                    task2=(roll_no,passw)
                    cur2.execute(sql2,task2)
                    conn1.commit()
                    conn1.close()
                    popup.setText(f"Information of Person {std_name} has been Added")
                    popup.setStandardButtons(QMessageBox.Ok)
                    popup.setIcon(QMessageBox.Information)
                    popup.exec_()
                    self.stackedWidget_2.setCurrentIndex(0)
                    self.stackedWidget.setCurrentIndex(0)
                    #print("Data has been Entered")
                    
                    # MainWindow.close()
                    # call(["python","Login.py"])
                else:
                    popup.setText("Roll Number Already Exists!")
                    popup.setStandardButtons(QMessageBox.Ok)
                    popup.setIcon(QMessageBox.Critical)
                    popup.exec_()
    
    def aphabets_folder(self):
        path=pathlib.Path(__file__).parent.absolute().joinpath('videos','Alphabets')
        path=str(path)
        self.dirModel.setRootPath(path)
        self.treeview.setRootIndex(self.model.index(path))
        self.stackedWidget_2.setCurrentIndex(1)
        self.frame_13.hide()
        self.current_folder='Alphabets'
    def science_folder(self):
        path=pathlib.Path(__file__).parent.absolute().joinpath('videos','Science')
        path=str(path)
        self.dirModel.setRootPath(path)
        self.treeview.setRootIndex(self.model.index(path))
        self.stackedWidget_2.setCurrentIndex(1)
        self.frame_13.hide()
        self.current_folder='Science'
    def computer_folder(self):
        path=pathlib.Path(__file__).parent.absolute().joinpath('videos','Computer')
        path=str(path)
        self.dirModel.setRootPath(path)
        self.treeview.setRootIndex(self.model.index(path))
        self.stackedWidget_2.setCurrentIndex(1)
        self.frame_13.hide()
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
        self.stackedWidget_2.setCurrentIndex(3)
        
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
            popup.setText(f"Test of Sign={path2} has been Assigned to Roll_No {self.test_roll_no}")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Information)
            popup.exec_()
            self.stackedWidget.setCurrentIndex(6)
        elif passw[0]=="No":
            popup=QMessageBox()
            popup.setText(f"Test of Sign={path2} has Already been Assigned to Roll_No {self.test_roll_no}")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
        else:
            cur.execute(sql,data)
            conn.commit()
            conn.close()
            popup=QMessageBox()
            popup.setText(f"Test of Sign={path2} has been Assigned to Roll_No {self.test_roll_no}")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Information)
            popup.exec_()
            self.stackedWidget.setCurrentIndex(6)
            








            

        


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
        self.camerathread.attempt_no=4
        self.test_attempt=4
        self.camerathread.ImageUpdate.connect(self.ImageUpdateSlot)
        self.camerathread.accuracyUpdate.connect(self.accuracyUpdateSlot)
        self.camerathread.accuracy_reset.connect(self.accuracy_reset)
        self.stackedWidget_2.setCurrentIndex(2)
        self.sentences_pass=0
        self.camerathread.sentences_pass_on=False
    
    def back_video(self):
        self.playlist.clear()
        self.camerathread.stop()
        self.label_16.setText('Closest Sign:')
        self.label_17.setText('None')
        __sortingEnabled = self.tableWidget_3.isSortingEnabled()
        self.tableWidget_3.setSortingEnabled(False)
        item = self.tableWidget_3.item(1, 1)
        item = self.tableWidget_3.item(0, 0)
        item.setText("0")
        item = self.tableWidget_3.item(0, 1)
        item.setText("0")
        item = self.tableWidget_3.item(1, 0)
        item.setText("0")
        item = self.tableWidget_3.item(1, 1)
        item.setText("0")
        self.tableWidget_3.setSortingEnabled(__sortingEnabled)
        self.stackedWidget_2.setCurrentIndex(1)
        self.test_attempt=4
    def back_videos(self):
        self.stackedWidget_2.setCurrentIndex(0)
        self.frame_13.show()
        self.sentences_pass=0
        self.sentences=[]

    def sentence_back(self):
        self.camerathread.stop()
        self.stackedWidget_2.setCurrentIndex(0)
        self.sentences_pass=0
        self.test_attempt=4
        self.sentences=[]
        self.camerathread.sentences_pass_on=False
        
    def new_account_cancel(self):
        self.stackedWidget.setCurrentIndex(0)
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
        #progress=QMessageBox()
        # progress.setText("Video Has Been Added")
        # progress.setStandardButtons(QMessageBox.Ok)
        # progress.setIcon(QMessageBox.Information)
        if fileName:
            #print(fileName)
            #print(self.path_video)
            #url = QUrl.fromLocalFile(fileName)
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
            self.treeview.setRootIndex(self.model.index(str(folder_path)))
            # self.treeview.setSortingEnabled(1)
            # self.treeview.sortByColumn(0,Qt.AscendingOrder)
            # self.treeview.setSortingEnabled(0)
            #progress.exec_()
            #progress.cancel()
            
            
            
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
        self.label_18.setPixmap(QPixmap.fromImage(Image))
        self.camerathread.sentences_pass_on=False

    def ImageUpdateSlot_sentences(self, Image):
        self.camerathread.sentences_pass_on=True
        self.label_4.setPixmap(QPixmap.fromImage(Image))
        self.label_7.setPixmap(QPixmap.fromImage(Image))
    
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
                        self.textEdit.insertPlainText(str(predicted))
                    else:
                        self.sentences.append(" ")
                        self.sentences.append(predicted)
                        self.textEdit.insertPlainText(str(" "))
                        self.textEdit.insertPlainText(str(predicted))
                    self.sentences_pass=0
                    
                
                sign=sign[:4]
                dist=dist[:4]
                pre_val=0
                list1=[]
                #self.label_17.setText(str(acc1))
                for i in range(len(sign)):
                    if sign[i]==self.video:
                        pass            
                    else:
                        if dist[0]==float('inf'):
                            self.label_16.setText('No Close Signs Predicted')
                            self.label_17.setText('')
                        else:
                            acc1=((int(dist[i])-60)/60)*100
                            if int(dist[i])<60:
                                acc1=round(acc1,2)
                                self.label_16.setText(str(f"Closest Sign Predicted is {sign[i]} with accuracy ="))
                                self.label_17.setText(str('98.5'))
                                break
                            else:
                                if acc1>100:
                                    acc1=(acc1)//100
                                    acc1=round(acc1,2)
                                    self.label_16.setText(str(f"Closest Sign Predicted is {sign[i]} with accuracy ="))
                                    self.label_17.setText(str(100-acc1))
                                    break
                                else:
                                    acc1=round(acc1,2)
                                    self.label_16.setText(str(f"Closest Sign Predicted is {sign[i]} with accuracy ="))
                                    self.label_17.setText(str(100-acc1))
                                    break

                
                if float(acc)>50 and predicted==self.video:
                    __sortingEnabled = self.tableWidget_3.isSortingEnabled()
                    self.tableWidget_3.setSortingEnabled(False)
                    item = self.tableWidget_3.item(0, 0)
                    item.setText("0")
                    item = self.tableWidget_3.item(0, 1)
                    item.setText("0")
                    item = self.tableWidget_3.item(1, 0)
                    item.setText("0")
                    item = self.tableWidget_3.item(1, 1)
                    item.setText("1")
                    self.tableWidget_3.setSortingEnabled(__sortingEnabled)
                elif float(acc)>50 and predicted!=self.video:
                    __sortingEnabled = self.tableWidget_3.isSortingEnabled()
                    self.tableWidget_3.setSortingEnabled(False)
                    item = self.tableWidget_3.item(0, 0)
                    item.setText("0")
                    item = self.tableWidget_3.item(0, 1)
                    item.setText("0")
                    item = self.tableWidget_3.item(1, 0)
                    item.setText("1")
                    item = self.tableWidget_3.item(1, 1)
                    item.setText("0")
                    self.tableWidget_3.setSortingEnabled(__sortingEnabled)
                elif float(acc)<50 and predicted==self.video:
                    __sortingEnabled = self.tableWidget_3.isSortingEnabled()
                    self.tableWidget_3.setSortingEnabled(False)
                    item = self.tableWidget_3.item(0, 0)
                    item.setText("0")
                    item = self.tableWidget_3.item(0, 1)
                    item.setText("1")
                    item = self.tableWidget_3.item(1, 0)
                    item.setText("0")
                    item = self.tableWidget_3.item(1, 1)
                    item.setText("0")
                    self.tableWidget_3.setSortingEnabled(__sortingEnabled)
                elif float(acc)<50 and predicted!=self.video:
                    __sortingEnabled = self.tableWidget_3.isSortingEnabled()
                    self.tableWidget_3.setSortingEnabled(False)
                    item = self.tableWidget_3.item(0, 0)
                    item.setText("1")
                    item = self.tableWidget_3.item(0, 1)
                    item.setText("0")
                    item = self.tableWidget_3.item(1, 0)
                    item.setText("0")
                    item = self.tableWidget_3.item(1, 1)
                    item.setText("0")
                    self.tableWidget_3.setSortingEnabled(__sortingEnabled)

                else:
                    __sortingEnabled = self.tableWidget_3.isSortingEnabled()
                    self.tableWidget_3.setSortingEnabled(False)
                    item = self.tableWidget_3.item(1, 1)
                    item = self.tableWidget_3.item(0, 0)
                    item.setText("0")
                    item = self.tableWidget_3.item(0, 1)
                    item.setText("0")
                    item = self.tableWidget_3.item(1, 0)
                    item.setText("0")
                    item = self.tableWidget_3.item(1, 1)
                    item.setText("0")
                    self.tableWidget_3.setSortingEnabled(__sortingEnabled)
    def accuracy_reset(self):
        self.label_16.setText('Recording Signs')
        self.label_17.setText('')
        self.sentences_pass=1
        
    
    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
 
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.pushButton_19.setIcon(QtGui.QIcon('pause-button.png'))
        else:
            self.pushButton_19.setIcon(QtGui.QIcon('play-button.png'))

    def positionChanged(self, position):
        self.horizontalSlider_4.setValue(position)

    def durationChanged(self, duration):
        self.horizontalSlider_4.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def clear_sentences(self):
        self.textEdit.clear()
        self.sentences=[]
    def Back_sentences(self):
        if len(self.sentences) <1:
            pass
        else:
            self.sentences.remove(self.sentences[-1])
            print(self.sentences)
            self.textEdit.clear()
            for i in self.sentences:
                self.textEdit.insertPlainText(str(i))
        self.sentences_pass=0
    def add_space(self):
        self.sentences.append(" ")
        self.textEdit.insertPlainText(str(" "))

        
 
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
                    

                # pressedKey = cv2.waitKey(1) & 0xFF
                # if pressedKey == ord("r"):  # Record pressing r
                #     sign_recorder.record()
        
                # try:
                #     self.accuracyUpdate.emit(accuracy)
                # except:
                #     pass
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
    #all_data_vid=[root for root,dirs,files in os.walk('data') if not dirs] #Collecting All data of the 6000+ signs
    return n

def load_param(np,all_data_sentences):
    np1,all_data_sentences=newer_load_reference_signs(np,all_data_sentences)
    return np1,all_data_sentences
#def thread3():


if __name__ == "__main__":
    import sys
    import time
    import pandas as pd
    dataset=pathlib.Path.cwd().joinpath('data')
    data_len=os.listdir(dataset)
    start_time = time.time()
    
    all_data_sentences=pd.DataFrame(columns=["name", "sign_model", "distance"])
    for i in data_len:
        if i=="Science_dataset" or i=="Alphabets_dataset" or i=="Computer_dataset":
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
    #temp=[root for root,dirs,files in os.walk(f'data') if not dirs]       
    #all_data_sentences=load_param(temp)
        
    #print(dataset_load_dictonary['Alphabet_dataset'])
    #temp=pool.apply_async(all_data_load, (temp.get(),i)) #Collecting All data of the 6000+ signs
    #all_data_sentences=pool.apply_async(all_data_load, (temp.get(),i))
   
    
    

    
    
    #alphabet_dataset = [
    #    file_name.replace(".pickle", "").replace("lh_", "")
    #    for root, dirs, files in os.walk(os.path.join("data", "Alphabets_dataset"))
    #    for file_name in files
    #    if file_name.endswith(".pickle") and file_name.startswith("lh_")
    #]
    #computer_dataset = [
    #    file_name.replace(".pickle", "").replace("lh_", "")
    #    for root, dirs, files in os.walk(os.path.join("data", "Computer_dataset"))
    #    for file_name in files
    #    if file_name.endswith(".pickle") and file_name.startswith("lh_")
    #]
    #science_dataset = [
    #    file_name.replace(".pickle", "").replace("lh_", "")
    #    for root, dirs, files in os.walk(os.path.join("data", "Science_dataset"))
    #    for file_name in files
    #    if file_name.endswith(".pickle") and file_name.startswith("lh_")
    #]
    
    #all_data_vid=[root for root,dirs,files in os.walk('data') if not dirs] #Collecting All data of the 6000+ signs


    #alphabet_signs=new_load_reference_signs(alphabet_dataset,"Alphabets")
    #computer_signs=new_load_reference_signs(computer_dataset,'Computer')
    #science_signs=new_load_reference_signs(science_dataset,'Science')
    #all_data_sentences=newer_load_reference_signs(all_data_vid) #This line send the parameters to a different function in dataset_utls
    end_time = time.time()

    print(f"The execution time for loading is: {end_time-start_time}")


    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
