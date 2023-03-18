from tkinter import*
from tkinter import messagebox
import cv2
from cv2 import *
import win32com.client
import time as time_out
from connect_db import QuerySql
from delete_file import DeleteFile

class AddNewDataTest:
    def __init__(self, id, name, latestFrame, lastRet):
        self.id = id
        self.name = name
        self.latestFrame = latestFrame
        self.lastRet = lastRet

    def add(self):
        cascPath = 'haarcascade/haarcascade_frontalface_default.xml'
        detector  = cv2.CascadeClassifier(cascPath)
        checkLableInfo = QuerySql.selectLabelfaceById(self.id)
        if(checkLableInfo is None):
            messagebox.showinfo('message','ID not found in system.')
        else:
            sampleNum = 0
            while(True):
                if (self.lastRet is not None) and (self.latestFrame is not None):
                    imgTest = self.latestFrame.copy()
                    grayImageTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2GRAY)
                    grayImageTest = cv2.fastNlMeansDenoising(grayImageTest, None, 4, 5, 11)
                    faces = detector.detectMultiScale(grayImageTest, 1.3, 5)
                    if(len(faces) == 1):
                        for (x,y,w,h) in faces:
                            sampleNum += 1
                            cv2.imwrite('image_test/'+self.name +'.'+ self.id +'.'+ str(sampleNum) + '.jpg', grayImageTest[y:y+h,x:x+w])
                        if(sampleNum > 99):
                            messagebox.showinfo('message', 'Add image into data test success.')
                            break
                    elif(len(faces) == 0):
                        print('Face not found.')
                        continue
                    else: 
                        messagebox.showinfo('message', 'Find tow faces in frame, please add again.')
                        path = 'image_test'
                        DeleteFile(path, self.id).delete()
                        break
                    cv2.imshow('img', imgTest)
                    k = cv2.waitKey(30)
                    if k == 27:
                        break
                    elif k ==-1:
                        continue
                else:
                    print('Not take of video')
                    time_out.sleep(0.2)
                    continue