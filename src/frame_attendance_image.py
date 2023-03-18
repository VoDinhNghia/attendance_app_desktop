import os
from tkinter import*
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
from cv2 import *
import imagehash
from connect_db import QuerySql
from db_image import GetInfoImage
from date import CurrentDate

fontTypeApp = 'Times New Roman'
cascPath = 'haarcascade/haarcascade_frontalface_default.xml'
detector  = cv2.CascadeClassifier(cascPath)

class FrameAttendanceImage:
    def __init__(self, mainAppScreen, latestFrame, lableShowNameCapReco, lableShowNumberIdCapReco, recognizer):
        self.mainAppScreen = mainAppScreen
        self.latestFrame = latestFrame
        self.lableShowNameCapReco = lableShowNameCapReco
        self.lableShowNumberIdCapReco = lableShowNumberIdCapReco
        self.recognizer = recognizer
    
    def show(self):
        capImageRecognition = self.latestFrame.copy()
        cv2.imwrite('image_cap_recognition/capImage.jpg', capImageRecognition)
        openImageCap = ImageTk.PhotoImage(Image.open('image_cap_recognition/capImage.jpg').resize((550, 350), Image.LANCZOS))
        panel = Label(self.mainAppScreen, image = openImageCap)
        panel.image = openImageCap
        panel.place(x = 600, y = 10)
        readImageCap = cv2.imread('image_cap_recognition/capImage.jpg')
        grayImageCap = cv2.cvtColor(readImageCap, cv2.COLOR_BGR2GRAY)
        grayImageCap = cv2.fastNlMeansDenoising(grayImageCap, None, 4, 5, 11)
        faceImageCap = detector.detectMultiScale(grayImageCap, 1.3, 5)
        today, currentTime, startMorning, endMorning, startAfternoon, endAfternoon = CurrentDate.dateHourTimeAttendance()                   
        fetchHistoryAttendance = QuerySql.fetchHistoryAttendanceByCurrentDate()
        idAttendanceds = []
        for i in fetchHistoryAttendance:
            if (i[0] != None): idAttendanceds.append(i[0])
        imageRecognitionCap = 0
        try:
            for(x,y,w,h) in faceImageCap:
                idPredict, confident = self.recognizer.predict(grayImageCap[y:y+h,x:x+w])
                profileCap = GetInfoImage.getProfile(idPredict)
                nameResultPredict = str(profileCap[1])
                numberIdPredict = str(profileCap[0])
                if(confident < 90):    
                    countCapReco = 0
                    if((currentTime > startMorning and currentTime < endMorning) or (currentTime > startAfternoon and currentTime < endAfternoon)):
                        for n in idAttendanceds:
                            if(int(n) == int(profileCap[0])):
                                countCapReco += 1
                        if(countCapReco < 1):
                            imageRecognitionCap += 1
                            grayToRgbImage = cv2.cvtColor(grayImageCap[y:y+h,x:x+w], cv2.COLOR_GRAY2RGB)
                            cv2.imwrite('image_attendance/anhchup'+'.'+str(profileCap[0]) +'.'+ str(imageRecognitionCap) + '.jpg', grayToRgbImage)
                            pathImageCompareCap = 'image_compare'
                            imagePathCaps = [os.path.join(pathImageCompareCap, f) for f in os.listdir(pathImageCompareCap)] 
                            for imagePath in imagePathCaps:
                                idCompareCap = int(os.path.split(imagePath)[-1].split('.')[1])
                                hashs = imagehash.average_hash(Image.open('image_attendance/anhchup'+'.'+str(profileCap[0])+'.'+str(imageRecognitionCap)+'.jpg'))
                                otherhash = imagehash.average_hash(Image.open(imagePath))
                                numberConfidentCap = hashs - otherhash
                                if(numberConfidentCap < 22 and (idCompareCap == int(profileCap[0]))):
                                    QuerySql.insertHistoryAttendance(profileCap[0], profileCap[1], today, currentTime)
                                    cv2.imwrite('image_correct/'+str(profileCap[1])+'.'+str(profileCap[0]) +'.'+ str(imageRecognitionCap) + '.jpg', grayToRgbImage)
                                    messagebox.showinfo('message', 'attendance correct')
                                else:
                                    messagebox.showinfo('message', 'attendance incorrect')
                        else:
                            nameResultPredict = ''
                            numberIdPredict = ''
                            messagebox.showinfo('message', 'attendance already')
                    else:
                        nameResultPredict = ''
                        numberIdPredict = ''
                        messagebox.showinfo('message', 'Not in the attendance time frame')
                else:
                    nameResultPredict = 'unknow'
                    numberIdPredict = 'unknow'
        
            nameCapPredict = 'name : ' + nameResultPredict
            numberIdCapPredict = 'number Id : ' + numberIdPredict
            self.lableShowNameCapReco.configure(text = nameCapPredict)
            self.lableShowNumberIdCapReco.configure(text = numberIdCapPredict)
        except ValueError:
            messagebox.showinfo('message', 'Please enter button trainning model!')