from PyQt5.QtWidgets import (QWidget, QProgressBar, 
    QPushButton, QApplication)
from PyQt5.QtCore import QBasicTimer
import sys
import time

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.progress()
        
        
    def progress(self):      
        to_add=float(sys.argv[1])
        print(to_add)
        global final_add
        final_add=(100/to_add)
        print(final_add)
        final_add=final_add+(final_add/15)
        print(final_add)

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 400, 25)


        self.timer = QBasicTimer()
        self.step = 0
        
        self.setGeometry(300,300, 450, 100)
        self.setWindowTitle('Processing video, Please Wait')
        self.show()
        self.timer.start(100, self)
        
        
    def timerEvent(self, e):
        global final_add
        if self.step >= 100:
            
            self.timer.stop()
            #self.btn.setText('Finished')
            return
            
        self.step = self.step + final_add
        self.pbar.setValue(self.step)
        time.sleep(final_add)
            
        

    
app = QApplication(sys.argv)
ex = Example()
sys.exit(app.exec_())