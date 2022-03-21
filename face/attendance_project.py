from datetime import datetime
import cv2
import numpy as np
import face_recognition
import os

path = "images"
images = []
classNames = []
mylist = os.listdir(path)


for image in mylist:
    current_image = cv2.imread(f'{path}/{image}')
    images.append(current_image)
    classNames.append(os.path.splitext(image)[0])



def get_encodings(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list


def mark_attendance(name):
    with open('attendance.csv', 'r+') as f:
        mydatalist = f.readlines()
        nameList = []
        for line in mydatalist:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            date_string = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name}, {date_string}')



encode_list_for_known_faces = get_encodings(images)


#capturing images through webcam
capture = cv2.VideoCapture(0)

while True:
    success, img = capture.read()       #this is to capture the image
    img_small = cv2.resize(img, (0,0), None, 0.25, 0.25)        #reducing image to one fourth
    img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)
    faces_in_current_frame = face_recognition.face_locations(img_small)
    encoding_in_current_frame = face_recognition.face_encodings(img_small, faces_in_current_frame)

    for encodeface, faceloc in zip(encoding_in_current_frame, faces_in_current_frame):
        matches = face_recognition.compare_faces(encode_list_for_known_faces, encodeface)
        face_dist = face_recognition.face_distance(encode_list_for_known_faces, encodeface)
        matchIndex = np.argmin(face_dist)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceloc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (255,0,0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
            mark_attendance(name)
        else:
            print("Face not registered")
            y1, x2, y2, x1 = faceloc
            y1, x2, y2, x1 = y1*4, x2*5, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (255,0,0), cv2.FILLED)
            cv2.putText(img, "Face not registered", (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)

    cv2.imshow('Webcam Image', img)
    cv2.waitKey(1)

    