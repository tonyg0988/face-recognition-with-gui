import face_recognition
import cv2
import sys
import os
import re
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QInputDialog, QLineEdit, QFileDialog, QProgressBar
from PyQt5.QtCore import QBasicTimer
import sys
from subprocess import call
import threading
# This is a demo of running face recognition on a video file and saving the results to a new video file.
#
# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this

# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.


print('successfully called')
known_people_folder='./database'
def scan_known_people(known_people_folder):
    known_names = []
    known_face_encodings = []

    for file in image_files_in_folder(known_people_folder):
        basename = os.path.splitext(os.path.basename(file))[0]
        img = face_recognition.load_image_file(file)
        encodings = face_recognition.face_encodings(img)
        print('in face finding function')
        if len(encodings) > 1:
            click.echo("WARNING: More than one face found in {}. Only considering the first face.".format(file))

        if len(encodings) == 0:
            click.echo("WARNING: No faces found in {}. Ignoring file.".format(file))
        else:
            known_names.append(basename)
            known_face_encodings.append(encodings[0])

    def main(known_people_folder, image_to_check, cpus, tolerance, show_distance):
            print('in second main')
            known_face_encodings.append(encodings[0])

    return known_names, known_face_encodings
def image_files_in_folder(folder):
    print('in image files in folder fucntion')
    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]

#getting paths for saving and opening file
ip_file= sys.argv[1]
out_path=sys.argv[2]
ip_tolerence =float(sys.argv[3])

# Open the input movie file
input_movie = cv2.VideoCapture(ip_file)
length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

def call_func():
    call(["python","progress.py",str(length)])

#creating a seperate thread for progress bar
t1 = threading.Thread(target=call_func, args=())
t1.start()


# Create an output movie file (make sure resolution/frame rate matches input video!)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_movie = cv2.VideoWriter(out_path+'.avi', fourcc, 29.97, (640, 360))

# Load some sample pictures and learn how to recognize them.

known_names,known_faces = scan_known_people(known_people_folder)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
frame_number = 0

while True:
    # Grab a single frame of video
    ret, frame = input_movie.read()
    frame_number += 1

    # Quit when the input video file ends
    if not ret:
        break

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.50)

        # If you had more than 2 faces, you could make this logic a lot prettier
        # but I kept it simple for the demo
        name = None
        for i,result in enumerate(match):
            
            if result:
                name = known_names[i]
        #elif match[1]:
        #    name = "Alex Lacamoire"

        face_names.append(name)

    # Label the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if not name:
            continue

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Write the resulting image to the output video file
    print("Writing frame {} / {}".format(frame_number, length))
    
    #step=step+1
    #frame_msg="writing frame " + str(frame_number) + "/" str(length)
    output_movie.write(frame)



# All done!
input_movie.release()
cv2.destroyAllWindows()

