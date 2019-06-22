import cv2
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


imagePath = sys.argv[1]

image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.3,
    minNeighbors=3,
    minSize=(30, 30)
)

print("[INFO] Found {0} Faces.".format(len(faces)))

for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    roi_color = image[y:y + h, x:x + w]
    print("[INFO] Object found. Saving locally.")

print('reached before class')

class App(QWidget):

    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        if(len(faces)>0):
            buttonReply = QMessageBox.question(self, 'Promt', "Face Detected, save to database?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                print('Yes clicked.')
                
                file_name=self.saveFileDialog()
                cv2.imwrite(file_name+'.jpg', roi_color)
                sys.exit()
            else:
                cv2.destroyAllWindows()
                
        else:
            print('no faces found , exiting')
            cv2.destroyAllWindows()

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)
            return fileName

        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())  
    #status = cv2.imwrite('faces_detected.jpg', image)
    #print("[INFO] Image faces_detected.jpg written to filesystem: ", status)
    
