import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout, QLabel, QHBoxLayout, QInputDialog, QLineEdit, QFileDialog, QSlider, QStatusBar, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot
import os
from subprocess import call
from PyQt5.QtCore import Qt


tolerence=0.55
class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'face Recognition'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        label = QLabel(self)
        pixmap = QPixmap('./images/background.jpg')
        label.setPixmap(pixmap)
        # Optional, resize window to image size
        self.resize(pixmap.width(),pixmap.height())
        a=10
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.statusBar().showMessage('Select level From slider: Low Tolerence-Strict Matching , High Tolerence-Loose Matching')
        self.show()
    
class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,300)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"Webcam")
        self.tabs.addTab(self.tab2,"Local")

        #creating slider
        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setFocusPolicy(Qt.NoFocus)
        self.sld.setGeometry(30, 40, 100, 30)
        self.sld.valueChanged[int].connect(self.changeValue)
        
        # Create first tab
        self.tab1.layout = QHBoxLayout(self)
        self.pushButton1 = QPushButton("Live Feed")
        self.pushButton1.setToolTip('Identify from live feed')
        self.pushButton1.move(50,50)
        self.pushButton1.clicked.connect(self.web_cam)

        #self.tab2.layout=QHBoxLayout(self)
        self.pushButton2=QPushButton("Generate database")
        self.pushButton2.setToolTip('Generate a Database from webcam')
        self.pushButton2.move(100,100)
        self.pushButton2.clicked.connect(self.Generate)
        
        #self.tab1.layout.addWidget(self.sld)
        self.tab1.layout.addWidget(self.pushButton1)
        self.tab1.layout.addWidget(self.pushButton2)
        
        self.tab1.setLayout(self.tab1.layout)

        #self.l1 = QLabel()
        #self.l1.setText("tolerence")
        #self.l1.setGeometry(10,10,10,10)
        #self.l1.setAlignment(Qt.AlignCenter)

        #vertical layout for tab2
        self.tab2.layout=QVBoxLayout(self)
        self.pushButton3=QPushButton("Import Image")
        self.pushButton3.setToolTip('Import faces to Database')
        self.pushButton3.move(50,50)
        self.pushButton3.clicked.connect(self.import_to_db)
        
        

        self.pushButton4=QPushButton("Browse Image")
        self.pushButton4.setToolTip('Browse to search in database')
        self.pushButton4.move(100,100)
        self.pushButton4.clicked.connect(self.Browse)

        self.pushButton5=QPushButton('Recognize from video')
        self.pushButton5.setToolTip('select a video to detect faces')
        self.pushButton5.move(150,150)
        self.pushButton5.clicked.connect(self.from_video)
        

        #Adding widgets to tab
        #self.tab2.layout.addWidget(self.l1)
        self.tab2.layout.addWidget(self.sld)
        self.tab2.layout.addWidget(self.pushButton3)
        self.tab2.layout.addWidget(self.pushButton4)
        self.tab2.layout.addWidget(self.pushButton5)
        #self.tab2.layout.addWidget(self.statusbar)
        self.tab2.setLayout(self.tab2.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


        
    @pyqtSlot()
    def web_cam(self):
        call(["python", "facerecog_from_webcam(improved).py",])
    def import_to_db(self):
        filename=self.openFileNameDialog()
        call(["python", "import_faces.py",filename])



    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Select the appropriate file", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
        return fileName
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Choose file name and location","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)
            return fileName


    def Generate(self):
        call(["python","generate_db_from_webcam.py"])

    def Browse(self):
        filename1=self.openFileNameDialog()
        call(["python","facial_recognition.py","./database" ,filename1,str(tolerence)])
    
    def from_video(self):
        filename2=self.openFileNameDialog()
        out_file_path=self.saveFileDialog()
        call(["python","facerecog_from_videofile.py",filename2,out_file_path,str(tolerence)])

    #slider PYQT function(sets value from slider for global tolerence)
    def changeValue(self, value):
        global tolerence
        if value == 0:
            tolerence=0.4
            print(tolerence)
            
        elif value > 0 and value <= 30:
            tolerence=0.5
            print(tolerence)
            
        elif value > 30 and value < 70:
            tolerence=0.6
            print(tolerence)
            
        else:
            tolerence=0.65
            print(tolerence)
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
