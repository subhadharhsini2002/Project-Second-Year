import sys
sys.dont_write_bytecode = True

from prettytable import PrettyTable
from image_recognize import recognize_attendence
from capture_image import take_images
from check_camera import camera
import json
import os


def title_bar():
    os.system('cls')
    print(35 * "=")
    print("Face Recognition Attendance System")
    print(35 * "=")
    print("[1] Check Camera")
    print("[2] Capture Faces")
    print("[3] Take Attendance")
    print("[4] Show Attendance")
    print("[5] Quit")
    print(35 * "=")


while True:
    title_bar()
    choice = int(input("Enter Choice: "))
    print(35 * "=")
    if choice == 1:
        print("*** Focus the camera window and press ESC key to quit ***")
        camera()
    elif choice == 2:
        take_images()
    elif choice == 3:
        recognize_attendence()
    elif choice == 4:
        attendance_json = json.load(open("student_attendance.json", "r"))
        tmp = PrettyTable()
        tmp.field_names = ["id", "name", "datetime"]
        tmp.add_rows(attendance_json[::-1])
        print("\nAttendance:")
        print(tmp.get_string())
        input("\n\nPress Enter to go back to main app")
    elif choice == 5:
        print("Closing Application")
        break
    else:
        print("Invalid Choice. Enter 1-3")
