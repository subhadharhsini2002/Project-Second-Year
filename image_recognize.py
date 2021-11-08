import cv2
import json
from pathlib import Path
from datetime import datetime
FONT = cv2.FONT_HERSHEY_SIMPLEX

ATTENDANCE_FILE_PATH = "student_attendance.json"
if not Path(ATTENDANCE_FILE_PATH).exists():
    json.dump([], open(ATTENDANCE_FILE_PATH, "w"))


def recognize_attendence():
    json_config = json.load(open("student_details.json", "r"))
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("student_images_trained.yml")
    harcascadePath = "haarcascade_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)
    is_recognized = False
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5, minSize=(
            int(minW), int(minH)), flags=cv2.CASCADE_SCALE_IMAGE)
        for(x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (10, 159, 255), 2)
            id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if abs(100-conf) > 50.0:
                attendance_json = json.load(open(ATTENDANCE_FILE_PATH, "r"))
                attendance_json.append([
                    json_config[str(id)]["id"],
                    json_config[str(id)]["name"],
                    str(datetime.now())
                ])
                json.dump(attendance_json, open(ATTENDANCE_FILE_PATH, "w"))
                is_recognized = True
            confstr = f"{json_config[str(id)]['name']} - {round(100 - conf)}%"
            cv2.putText(im, str(confstr), (x + 5, y + h - 5),
                        FONT, 1, (0, 255, 0), 1)
        cv2.imshow('Attendance', im)
        if cv2.waitKey(1) == 27 or is_recognized:
            break
    cam.release()
    cv2.destroyAllWindows()
