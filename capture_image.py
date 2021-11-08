import cv2
import json
from pathlib import Path
import numpy as np
from os import path, listdir
from PIL import Image

Path("student_images").mkdir(exist_ok=True)
NUMBER_OF_SAMPLES = 100
STUDENT_DETAILS_FILE_PATH = "student_details.json"

if not Path(STUDENT_DETAILS_FILE_PATH).exists():
    json.dump({}, open("student_details.json", "w"))


def take_images():
    json_config = json.load(open("student_details.json", "r"))
    while True:
        id = input("Enter Your id: ")
        if id not in json_config.keys() and id.isnumeric():
            break
        print("*** Id already present or not valid, enter different id ***")
    name = input("Enter Your Name: ")
    json_config[id] = {
        "id": id,
        "name": name
    }
    json.dump(json_config, open("student_details.json", "w"))
    cam = cv2.VideoCapture(0)
    harcascadePath = "haarcascade_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    sample_num = 0
    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(
            gray, 1.3, 5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
        for(x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (10, 159, 255), 2)
            cv2.imwrite(
                f"student_images/{id}---{sample_num}---{name}.jpg", gray[y:y+h, x:x+w])
            cv2.imshow('frame', img)
            sample_num += 1
        if cv2.waitKey(1) == 27:
            break
        elif sample_num > NUMBER_OF_SAMPLES:
            break
    cam.release()
    cv2.destroyAllWindows()
    print(35*"=")
    print("Training the newly loaded images")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    output = [[], []]
    for imagePath in listdir("student_images"):
        imagePath = path.join("student_images", imagePath)
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        uid = path.basename(imagePath).split("---")[0]
        if uid in json_config.keys():
            output[0].append(imageNp)
            output[1].append(int(uid))
    recognizer.train(output[0], np.array(output[1]))
    recognizer.save("student_images_trained.yml")
    print(35*"=")
