### Description
```
App desktop attendance use cv2
```

### Environment
```
- mysql: 8.0.19
- python: 3.10.10
```

### Pip install
```
$ pip install imagehash
$ pip install Pillow
$ pip install pywin32
$ pip install pymysql
$ pip install xlwt
$ pip install opencv-contrib-python
$ pip install opencv-python
```

### Database
```
- name: attendance
- table:
+ users (username, password)
+ label_face (ID, name)
+ history_attendance (ID, name, date, time)
```

### Run App
```
cd folder attendance => python app_main_gui.py
```