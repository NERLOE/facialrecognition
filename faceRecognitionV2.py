import face_recognition
import cv2
import os
from datetime import datetime
from pygame import mixer

mixer.init(48500)
mixer.music.load("song1.mp3")
mixer.music.play(-1)

cam = cv2.VideoCapture(0)

# Mappen som alle billederne af ansigtsgenkendelsen ligger
path = 'images'

imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

knownFaceEncodings = []
knownFaceNames = []

persons = [
    'Marcus',
    'Julie'
    ]

for imagePath in imagePaths:
    img = face_recognition.load_image_file(imagePath)
    name = imagePath.replace(".jpg", "").replace(path+"/", "").title()


    imgFaceEncoding = face_recognition.face_encodings(img)[0]
    knownFaceEncodings.append(imgFaceEncoding)

    knownFaceNames.append(name)


faceLocations = []
faceEncodings = []
faceNames = []
processThisFrame = True

totalFacesRead = []

while True:
    ret, frame = cam.read()

    totalFacesRead = []

    smallFrame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    rgbSmallFrame = smallFrame[:, :, ::-1]

    faceLocations = face_recognition.face_locations(rgbSmallFrame)
    faceEncodings = face_recognition.face_encodings(rgbSmallFrame, faceLocations)

    font = cv2.FONT_HERSHEY_DUPLEX

    faceNames = []
    for faceEncoding in faceEncodings:
        matches = face_recognition.compare_faces(knownFaceEncodings, faceEncoding)
        name = "Ukendt"

        if True in matches:
            firstMatchIndex = matches.index(True)
            name = knownFaceNames[firstMatchIndex]

            if persons.__contains__(name):
                if not totalFacesRead.__contains__(name):
                    #print("{0} er nu godkendt.".format(name))
                    totalFacesRead.append(name)

                if len(totalFacesRead) >= len(persons):
                    mixer.music.stop()
                    cv2.putText(frame, "ALLE GODKENDT", (0, 700), font, 5, (40, 126, 235), 6)
                    print("Alle ansigter godkendt.")

        faceNames.append(name)



    # GODKENDT
    cv2.rectangle(frame, (200, 10), (220, 30), (74, 163, 69), cv2.FILLED)
    cv2.putText(frame, "GODKENDT", (180, 45), font, 0.4, (74, 163, 69), 1)

    # IKKE GODKENDT
    cv2.rectangle(frame, (300, 10), (320, 30), (52, 85, 213), cv2.FILLED)
    cv2.putText(frame, "IKKE GODKENDT", (260, 45), font, 0.4, (52, 85, 213), 1)

    # REGISTRERET
    cv2.rectangle(frame, (400, 10), (420, 30), (155, 155, 155), cv2.FILLED)
    cv2.putText(frame, "REGISTRERET", (370, 45), font, 0.4, (155, 155, 155), 1)

    # UKENDT
    cv2.rectangle(frame, (480, 10), (500, 30), (152, 54, 121), cv2.FILLED)
    cv2.putText(frame, "UKENDT", (465, 45), font, 0.4, (152, 54, 121), 1)

    if len(totalFacesRead) > 0:
        cv2.putText(frame, "{0}/{1} fundet.".format(len(totalFacesRead), len(persons)), (1080, 30), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2)
    else:
        cv2.putText(frame, "Ingen personer fundet.".format(len(totalFacesRead), len(persons)), (900, 30), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2)

    cv2.putText(frame, "Personer:", (10, 30), font, 1.0, (255, 255, 255), 2, cv2.LINE_AA)
    top = 30

    for person in persons:
        top += 30
        if totalFacesRead.__contains__(person):
            cv2.putText(frame, person, (10, top), font, 1.0, (74, 163, 69), 1, cv2.LINE_AA)
        else:
            if knownFaceNames.__contains__(person):
                cv2.putText(frame, person, (10, top), font, 1.0, (52, 85, 213), 1, cv2.LINE_AA)
            else:
                cv2.putText(frame, person, (10, top), font, 1.0, (152, 54, 121), 1, cv2.LINE_AA)


    for p in knownFaceNames:
        if not persons.__contains__(p):
            top += 30
            cv2.putText(frame, p, (10, top), font, 0.6, (155, 155, 155), 1, cv2.LINE_AA)


    for (top, right, bottom, left), name in zip(faceLocations, faceNames):

        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        color = (0, 0, 0)

        # Sætter farven på borderen, og skiltet til teksten.
        if name == "Ukendt": # LILLA
            color = (152, 54, 121)
        elif not persons.__contains__(name): # GRÅ
            color = (155, 155, 155)
        else: # GRØN
            color = (74, 163, 69)


        # Laver formen rundt om ansigtet.
        cv2.rectangle(frame, (left, top), (right, bottom), color, 5)

        # Laver et rektangel til teksten med navn.
        cv2.rectangle(frame, (left, bottom), (right, bottom - 35), color, cv2.FILLED)

        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow('Face Recognition', frame)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    elif k == 32:
        cv2.imwrite('img/{0}.png'.format(datetime.now()), frame)

cam.release()
cv2.destroyAllWindows()

