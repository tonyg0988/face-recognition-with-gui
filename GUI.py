import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox,QLineEdit,QLabel, QProgressBar
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QBasicTimer
import time

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Record:- y' + sys.argv[2]
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 400
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.textbox0 = QLineEdit(self)
        self.textbox0.move(1,5)
        self.textbox0.resize(600,2)

        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(600,30)
        self.textbox1 = QLineEdit(self)
        self.textbox1.move(20,70)
        self.textbox1.resize(600,30)
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(20,110)
        self.textbox2.resize(600,30)

        label = QLabel(self)
        pixmap = QPixmap('./database/'+sys.argv[2]+'.jpg')
        label.setPixmap(pixmap)
        label.move(170,170)

        if(sys.argv[1]=="found"):
            print('before calling found function')
            self.found()
        if(sys.argv[1]=="not_found"):
            self.not_found()
        if(sys.argv[1]=="unknown"):
            self.unknown()
        if(sys.argv[1]=="progress"):
            self.progress()
    def not_found(self):
        buttonReply = QMessageBox.question(self, 'Face not Found', "Image did not match with any record, Exit?",QMessageBox.Ok , QMessageBox.Ok)
        if buttonReply == QMessageBox.Ok:
            sys.exit();
        
    def found(self):
        self.show()
        face_distance=float(sys.argv[3])
        #face_distance=int(face_distance)
        print('in found function')
        print('tolerence =',sys.argv[4])
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('Record Found, Image matched with a record- '+ sys.argv[2])
        #msg.setText("The test image has a distance of {:.2} from known image ".format(face_distance))
        retval = msg.exec_()
        msg.setWindowTitle("MessageBox demo")
        msg.setDetailedText("The details are as follows:")

        #buttonReply = QMessageBox.question(self, 'Record Found', "Image matched with a record- '"+ sys.argv[2]+ "'",QMessageBox.Ok , QMessageBox.Ok)
        
        self.textbox.setText("The test image has a distance of {:.2} from known image, Checked with tolerence of {}".format(face_distance,sys.argv[4]))
        self.textbox1.setText("- With a normal cutoff of 0.6, would the test image match the known image? {}".format(face_distance < 0.6))
        self.textbox2.setText("- With a very strict cutoff of 0.5, would the test image match the known image? {}".format(face_distance < 0.5))
        

        print("The test image has a distance of {:.2} from known image ".format(face_distance))
        print("- With a normal cutoff of 0.6, would the test image match the known image? {}".format(face_distance < 0.6))
        print("- With a very strict cutoff of 0.5, would the test image match the known image? {}".format(face_distance < 0.5))
        print()

    def unknown(self):
        buttonReply = QMessageBox.question(self, 'Alert', "No face found on input image",QMessageBox.Ok , QMessageBox.Ok)
        if buttonReply == QMessageBox.Ok:
            sys.exit();
        
        
    def progress(self):    
        #f-ed logic, dont know what was i thinking

        to_add=float(sys.argv[2])
        global final_add
        final_add=(100/to_add)
        print(final_add)

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)

        #calling constructor
        self.timer = QBasicTimer()
        self.step = 0
        
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QProgressBar')
        self.show()
        self.timer.start(100, self)
        
        #the start() method for pbar
    def timerEvent(self, e):
        global final_add
        if self.step >= 100:
            
            self.timer.stop()
            #self.btn.setText('Finished')
            return
            
        self.step = self.step + final_add
        self.pbar.setValue(self.step)
        time.sleep(final_add)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())  
