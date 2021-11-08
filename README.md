# Smart Attendance

## Install
```sh
python -m pip install -r requirements.txt
```

## Run
```sh
python main.py
```

## Cleanup files
```python
import shutil, os
shutil.rmtree("student_images")
os.remove("student_attendance.json")
os.remove("student_details.json")
os.remove("student_images_trained.yml")
```
