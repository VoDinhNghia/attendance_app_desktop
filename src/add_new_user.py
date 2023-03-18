from tkinter import*
from tkinter import messagebox
import cv2
from cv2 import *
import win32com.client
import time as time_out
from connect_db import QuerySql
from delete_file import DeleteFile

class AddNewUser:
    def __init__(self, id, name, latestFrame, lastRet):
        self.id = id
        self.name = name
        self.latestFrame = latestFrame
        self.lastRet = lastRet

    def add(self):
        cascPath = 'haarcascade/haarcascade_frontalface_default.xml'
        detector  = cv2.CascadeClassifier(cascPath)
        getLableFaceById = QuerySql.selectLabelfaceById(self.id)
        if(getLableFaceById is None):
            QuerySql.insertLabelface(self.id, self.name)
            sampleNum = 0
            while(True):
                if (self.lastRet is not None) and (self.latestFrame is not None):
                    img = self.latestFrame.copy()
                    gray = cv2.fastNlMeansDenoising(img, None, 4, 5, 11)
                    faces = detector.detectMultiScale(gray, 1.3, 5)
                    if(len(faces) == 1):
                        for (x, y, w, h) in faces:
                            sampleNum += 1
                            print('sampleNum', sampleNum)
                            cv2.imwrite('image_trainning_model/User.'+ self.id +'.'+ str(sampleNum) + '.jpg', gray[y:y+h,x:x+w])
                            cv2.imwrite('image_compare/User.'+ self.id +'.'+'.jpg', gray[y:y+h,x:x+w])
                        if(sampleNum > 49):
                            speaker = win32com.client.Dispatch('SAPI.SpVoice')
                            speaker.Speak('Save success please check')
                            messagebox.showinfo('message', 'Add success, please check in folder image_trainning_model')
                            break
                    elif(len(faces) == 0):
                        print('face not found.')
                        continue
                    else: 
                        messagebox.showinfo('message','Find tow faces in frame, please add again.')
                        QuerySql.deleteLabelface(self.id)
                        path = 'image_trainning_model'
                        DeleteFile(path, self.id).delete()
                        path_ss = 'image_compare'
                        DeleteFile(path_ss, self.id).delete()
                        break
                    cv2.imshow('img', img)
                    k = cv2.waitKey(30)
                    if k == 27:
                        break
                    elif k ==-1:
                        continue
                else:
                    print('Not take of video')
                    time_out.sleep(0.2)
                    continue                                    
        else:
            messagebox.showinfo('message', 'ID existed in system, please enter ID diff.')

    