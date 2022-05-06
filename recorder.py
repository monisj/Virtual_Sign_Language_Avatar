from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import pathlib,os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import mediapipe as mp
import cv2
import numpy as np
from utils.mediapipe_utils import mediapipe_detection
from webcam_manager import WebcamManager


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame_28 = QtWidgets.QFrame(self.centralwidget)
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
        self.gridLayout_2.addWidget(self.frame_28, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 3, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 4, 0, 1, 1)
        
        
        
            
        self.widget_4 = QtWidgets.QLabel(self.centralwidget)
        self.widget_4.setMinimumSize(QtCore.QSize(640, 480))
        self.widget_4.setObjectName("widget_4")



        self.gridLayout_2.addWidget(self.widget_4, 1, 0, 1, 1)
            
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 0, 0, 1, 1)
        
        

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        

        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_19.setText(_translate("MainWindow", "Pause/Play"))
        self.pushButton.setText(_translate("MainWindow", "Exit"))
        #self.pushButton_19.clicked.connect(self.play)
        self.pushButton_19.setIcon(QtGui.QIcon('play-button.png'))
        self.pushButton.clicked.connect(self.exit)


        webcam_manager = WebcamManager()
        
        cap = cv2.VideoCapture("webcamimage.avi")
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_counter = 0
        
        with mp.solutions.holistic.Holistic(
            min_detection_confidence=0.3, min_tracking_confidence=0.3
        ) as holistic:
            while frame_counter!=0 or frame_counter==0:
                
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
                    FlippedImage=webcam_manager.update2(frame, results)
                    ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_BGR888)
                    Pic = ConvertToQtFormat.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
                    self.ImageUpdate(Pic)
        
        path=str(pathlib.Path.cwd())+'\\'+'webcamimage.avi'
        #self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(str(path))))
        #self.mediaPlayer.play()
        
        #self.draw_landmarks(self.mediaPlayer.mediaStream)
        #self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        #self.mediaPlayer.positionChanged.connect(self.positionChanged)
        #self.mediaPlayer.durationChanged.connect(self.durationChanged)
        #self.horizontalSlider_4.sliderMoved.connect(self.setPosition)

    


    # def play(self):
    #     if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
    #         self.mediaPlayer.pause()
    #     else:
    #         self.mediaPlayer.play()
 
    # def mediaStateChanged(self, state):
    #     if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
    #         self.pushButton_19.setIcon(QtGui.QIcon('pause-button.png'))
    #     else:
    #         self.pushButton_19.setIcon(QtGui.QIcon('play-button.png'))
  

    # def positionChanged(self, position):
    #     self.horizontalSlider_4.setValue(position)

    # def durationChanged(self, duration):
    #     self.horizontalSlider_4.setRange(0, duration)

    # def setPosition(self, position):
    #     self.mediaPlayer.setPosition(position)

    def exit(self):
        
        MainWindow.close() 
        print(1)


    
    def ImageUpdate(self,Image):
        self.widget_4.setPixmap(QPixmap.fromImage(Image))


    def draw_landmarks(image, results2,results):
        mp_holistic = mp.solutions.holistic  # Holistic model
        mp_drawing = mp.solutions.drawing_utils  # Drawing utilities

        # Draw left hand connections
        image = mp_drawing.draw_landmarks(
            image,
            landmark_list=results.left_hand_landmarks,
            connections=mp_holistic.HAND_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(
                color=(232, 254, 255), thickness=1, circle_radius=4
            ),
            connection_drawing_spec=mp_drawing.DrawingSpec(
                color=(255, 249, 161), thickness=2, circle_radius=2
            ),
        )
        # Draw right hand connections
        image = mp_drawing.draw_landmarks(
            image,
            landmark_list=results.right_hand_landmarks,
            connections=mp_holistic.HAND_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(
                color=(232, 254, 255), thickness=1, circle_radius=4
            ),
            connection_drawing_spec=mp_drawing.DrawingSpec(
                color=(255, 249, 161), thickness=2, circle_radius=2
            ),
        )
        return image


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())