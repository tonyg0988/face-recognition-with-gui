import face_recognition
import cv2
import numpy as np
import os
import re
from itertools import chain


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

#improved:-
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.
    #There you go, i pulled a little sneaky on you.
known_people_folder='./database'
# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)


# Create arrays of known face encodings and their names
known_face_names,known_face_encodings = scan_known_people(known_people_folder)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    #Converting the imgage to HLS for brightness(Light intersity) Detection
    imgHLS = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    Lchannel = imgHLS[:,:,1]
    
    a=list(chain.from_iterable(Lchannel))
    brightness=sum(a)/len(a)
    if(brightness<=75):
        condition="Very Poor"
    if(brightness<=85 and brightness >75):
        condition=" Poor"
    if(brightness<=95 and brightness >85):
        condition="Good"
    
    if(brightness <=105 and brightness >95):
        condition="Very Poor"
    if(brightness >105):
        condition="Excellent"

    print(condition)
    #print(brightness)



    #np.array(Lchannel).tolist()
    #print(type(Lchannel))
   
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        cv2.putText(frame,'Brightness/Visiblity: '+condition,(80,30), font,1,(255,255,255),1,cv2.LINE_AA)
        cv2.putText(frame,'Press Q to Quit',(5,470), font,0.5,(255,255,255),1,cv2.LINE_AA)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
