import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = "Dataset"
images = []
names = []
myList = os.listdir(path)
# print(myList)

for name in myList:
    currentImg = cv2.imread(f"{path}/{name}")
    images.append(currentImg)
    names.append(os.path.splitext(name)[0])
# print(names)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


def markAttendance(name):
    with open('attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        # print(myDataList)
        nameList, timeList = [], []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime("%H:%M:%S")
            f.writelines(f"\n{name}, {dtString}")


if __name__ == "__main__":
    encodeListForKnownFaces = findEncodings(images)
    # print(len(encodeListForKnownFaces))
    print("Encoding completed")

    cap = cv2.VideoCapture(2)
    while True:
        success, img = cap.read()
        imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

        facesInCurrentFrame = face_recognition.face_locations(imgSmall)
        encodesCurrentFrame = face_recognition.face_encodings(imgSmall, facesInCurrentFrame)

        for encodeFace, faceLocation in zip(encodesCurrentFrame, facesInCurrentFrame):
            matches = face_recognition.compare_faces(encodeListForKnownFaces, encodeFace)
            faceDistance = face_recognition.face_distance(encodeListForKnownFaces, encodeFace)
            # print(faceDistance)
            matchIndex = np.argmin(faceDistance)

            if matches[matchIndex]:
                name = names[matchIndex].upper()
                print(name)
                y1, x1, y2, x2 = faceLocation
                y1, x1, y2, x2 = y1*4, x1*4, y2*4, x2*4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                markAttendance(name)

            else:
                print("Not identified")
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                cv2.putText(img, "Person is unknown",
                            (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Camera feed", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# faceLocTest = face_recognition.face_locations(imgTest)[0]
# encodeTest = face_recognition.face_encodings(imgTest)[0]
# cv2.rectangle(imgTest, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (0, 0, 255), 5)
#
# results = face_recognition.compare_faces([encodeElon], encodeTest)
# faceDis = face_recognition.face_distance([encodeElon], encodeTest)
# print(results, faceDis)
# cv2.putText(imgTest, f"{results} {round(faceDis[0], 2)}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)