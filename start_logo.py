import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt
  
  
class LoadingGif(object):
  
    def mainUI(self, FrontWindow):
        FrontWindow.setObjectName("FTwindow")
        FrontWindow.resize(320, 300)
        FrontWindow.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(FrontWindow)
        self.centralwidget.setObjectName("main-widget")
        FrontWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        FrontWindow.setAttribute(Qt.WA_TranslucentBackground, True)
        # Label Create
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(25, 25, 200, 200))
        self.label.setMinimumSize(QtCore.QSize(250, 250))
        self.label.setMaximumSize(QtCore.QSize(250, 250))
        self.label.setObjectName("lb1")
        FrontWindow.setCentralWidget(self.centralwidget)
  
        # Loading the GIF
        self.movie = QMovie("loader.gif")
        self.label.setMovie(self.movie)
  
        self.startAnimation()
  
    # Start Animation
  
    def startAnimation(self):
        self.movie.start()
  
    # Stop Animation(According to need)
    def stopAnimation(self):
        self.movie.stop()
  
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    demo = LoadingGif()
    demo.mainUI(window)
    window.show()
    sys.exit(app.exec_())