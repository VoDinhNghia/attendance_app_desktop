import os
import tkinter
from tkinter import*
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import numpy as np
import cv2
from cv2 import *
import win32com.client
import imagehash
import hashlib
import threading 
from threading import Lock
import time as time_out
from connect_db import QuerySql
from db_image import GetInfoImage
from delete_file import DeleteFile
from view_image import ViewImage
from excel import Export
from date import CurrentDate
from accuracy import Accuracy
from get_camera import Camera
from add_new_user import AddNewUser
from add_data_test import AddNewDataTest
from frame_data_user_list import FrameDateUserList
from frame_search_by_date import FrameSearchByDate
from frame_attendance_today import FrameAttendanceToday
from frame_attendance_image import FrameAttendanceImage
# if not yet tranning model then enter trainning model when start app => action

root = Tk()
root.title('Attendance app')
root.iconbitmap('image_background_app/icon.jpg')
root.geometry('890x500')
root.resizable(False,False)
imgBackgroundLogin = ImageTk.PhotoImage(Image.open('image_background_app/login.jpg'))
panel = Label(root, image = imgBackgroundLogin)
panel.image = imgBackgroundLogin
panel.place(x = 0, y = 0)

#cap = cv2.VideoCapture('rtsp://192.168.1.56:554/ch0_0.h264')
cascPath = 'haarcascade/haarcascade_frontalface_default.xml'
detector  = cv2.CascadeClassifier(cascPath)
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 1
fontcolor = (250,0,0)
fontTypeApp = 'Times New Roman'
recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'image_trainning_model'
md5 = hashlib.md5()
password = 'Nghia123'
md5.update(password.encode())
password = md5.hexdigest()
print(password)
def loginApp():
    username = inputUsername.get()
    password = inputPassword.get()
    resultQueryLogin = QuerySql.login()
    md5 = hashlib.md5()
    md5.update(password.encode())
    password = md5.hexdigest()
    print('password cryto: ', password)
    if(username == '' or password == ''):
        messagebox.showinfo('message', 'Please fill username and password')
    elif(resultQueryLogin[0] != username or resultQueryLogin[1] != password):
        messagebox.showinfo('message','username or password incorrect')
    elif(resultQueryLogin[0] == username and resultQueryLogin[1] == password):
        speaker = win32com.client.Dispatch('SAPI.SpVoice')
        speaker.Speak('Hello, wellcome you to attendance app')
        root.destroy()
        cameraOptionScreen = Tk()
        cameraOptionScreen.geometry('730x150')
        cameraOptionScreen.configure(bg = 'CornflowerBlue')
        
        def optionCameraFunc():
            global optionCamera, cap, latestFrame, lo, lastRet
            optionCamera = str(inputOptionCamera.get()) 
            cap = Camera.get(optionCamera)
            latestFrame = None
            lastRet = None
            lo = Lock()
            def rtspProtocolbuffer(cap):
                global latestFrame, lo, lastRet
                while True:
                    with lo:
                        try:
                            lastRet, latestFrame = cap.read()
                        except:
                            print('error exception')
            t1 = threading.Thread(target = rtspProtocolbuffer, args = (cap,), name = 'rtsp_read_thread')
            t1.daemon = True
            t1.start()

            cameraOptionScreen.destroy()
            mainAppScreen = Tk()
            mainAppScreen.geometry('1200x600')
            mainAppScreen.resizable(False,False)
            background_main=ImageTk.PhotoImage(Image.open('image_background_app/background.jpg'))
            panel = Label(mainAppScreen, image = background_main)
            panel.image = background_main
            panel.place(x = 0, y = 0)

            lableShowFace = Label(mainAppScreen)
            lableShowFace.place(x = 20, y = 10)
            #video_mylove.mp4 đọc và nhận dạng nhưng tốc độ quá nhanh
            def showFaceStream():
                try:
                    global faceStream
                    if((optionCamera.isnumeric and len(optionCamera)==1) or len(optionCamera)==0):
                        _,faceStream = cap.read()
                    else:
                        faceStream = latestFrame.copy()
                    faceStream = cv2.flip(faceStream, 1)
                    imageStream = cv2.cvtColor(faceStream, cv2.COLOR_BGR2RGBA)
                    imgFace = Image.fromarray(imageStream)
                    imgFace = imgFace.resize((550, 350), Image.LANCZOS)
                    imgShowFace = ImageTk.PhotoImage(image = imgFace)
                    lableShowFace.imgShowFace = imgShowFace
                    lableShowFace.configure(image = imgShowFace)
                    lableShowFace.after(10, showFaceStream)
                except:
                    print('error exception')
            showFaceStream()
            global recognizer
            def trainningModelFunc():
                Ids, faces = GetInfoImage.getImagesAndLabels(path)
                recognizer.train(faces, np.array(Ids))
                recognizer.save('trainning_result/trainning_model.yml')
                messagebox.showinfo('message', 'Finish trainning model')

            def addNewUserTrainModelFunc():                  
                addNewUserTrainModelScreen = Tk()
                addNewUserTrainModelScreen.geometry('500x150')
                addNewUserTrainModelScreen.resizable(False, False)
                addNewUserTrainModelScreen.configure(bg = 'CornflowerBlue')
                def addNewUserFunc():
                    getValueNumberIdAddNew = inputNewNumberId.get()
                    getValueNameAddNew = inputNewNameUser.get()
                    if(len(getValueNumberIdAddNew) == 0 or len(getValueNameAddNew) == 0):
                        messagebox.showinfo('message', 'Please fill all fields')
                    elif getValueNumberIdAddNew.isdecimal:
                        AddNewUser(getValueNumberIdAddNew, getValueNameAddNew, latestFrame, lastRet).add()
                    else:
                        messagebox.showinfo('message', 'Number Id must is isdecimal.')
                    addNewUserTrainModelScreen.destroy()
                
                def addNewDataTestFunc():
                    getIdAddTest = inputNewNumberId.get()
                    getNameTest = inputNewNameUser.get()
                    AddNewDataTest(getIdAddTest, getNameTest , latestFrame, lastRet).add()
                    
                lbl_ID_nguoiMoi = Label(addNewUserTrainModelScreen, text = 'number Id', bd = 4, fg = 'white', font = (fontTypeApp, 16), width = 10, bg = 'green')
                lbl_ID_nguoiMoi.place(x = 15, y = 10)
                inputNewNumberId = Entry(addNewUserTrainModelScreen, bd = 5, width = 35, font = (fontTypeApp, 14))
                inputNewNumberId.place(x = 150, y = 10)
                lbl_Ten_nguoiMoi = Label(addNewUserTrainModelScreen, text='name', bd=4, fg='white', font=(fontTypeApp, 16), width= 10, bg='green')
                lbl_Ten_nguoiMoi.place(x= 15, y= 45)
                inputNewNameUser = Entry(addNewUserTrainModelScreen, width=35, bd=5,font=(fontTypeApp, 14))
                inputNewNameUser.place(x= 150, y= 45)
                buttonAddNewUser = Button(addNewUserTrainModelScreen, text = 'Add new user', font = (fontTypeApp, 14), fg = 'white', bg = 'green',
                    width = 15, height = 1, command = addNewUserFunc)
                buttonAddNewUser.place(x = 100, y = 90)
                buttonAddNewDataTest = Button(addNewUserTrainModelScreen, text = 'Add data test', font = (fontTypeApp, 14), fg = 'white', bg = 'green',
                    width = 15, height = 1, command = addNewDataTestFunc)
                buttonAddNewDataTest.place(x = 300, y = 90)
            def btn_danhsachNguoi():
                FrameDateUserList.show()
                
            
            def attendanceRealtimeFunc():
                numberPathAttendance = 0
                numberPathUnknown = 0
                global imgRealtime
                try:
                    while True:
                        if((lastRet is not None) and (latestFrame is not None)):
                            imgRealtime = latestFrame.copy()                            
                        else:
                            print('Not take of video')
                            time_out.sleep(0.2)
                            continue
                        grayImageRealtime = cv2.cvtColor(imgRealtime, cv2.COLOR_BGR2GRAY)
                        grayImageRealtime = cv2.fastNlMeansDenoising(grayImageRealtime, None, 4, 5, 11)
                        faces = detector.detectMultiScale(grayImageRealtime, 1.3, 5)
                        today, currentTime, startMorning, endMorning, startAfternoon, endAfternoon = CurrentDate.dateHourTimeAttendance()
                        startExport, endExport = CurrentDate.setupHourAutoExport()
                        fetchInfoAttendance = QuerySql.fetchHistoryAttendanceByCurrentDate()
                        idListAttendance = []
                        for i in fetchInfoAttendance:
                            idListAttendance.append(i[0])
                        for(x, y, w, h) in faces:
                            cv2.rectangle(imgRealtime, (x,y), (x+w,y+h), (0,255,255), 1)
                            id, conf = recognizer.predict(grayImageRealtime[y:y+h,x:x+w])
                            profile = GetInfoImage.getProfile(id)
                            idPredict = 'Uknown'
                            conf = round(100 * (1 - (conf / 300)), 2)
                            if(conf > 70):
                                cv2.putText(imgRealtime, str(conf) + '% : ' + str(profile[1]), (x+10,y-20), fontface, fontscale, fontcolor ,2)  
                                countAttendance = 0
                                if((currentTime > startMorning and currentTime < endMorning) or (currentTime > startAfternoon and currentTime < endAfternoon)):
                                    print('profile ID: ', profile[0])
                                    for n in idListAttendance:
                                        if(int(n) == int(profile[0])):
                                            countAttendance += 1
                                    if(countAttendance < 1):
                                        print('list ids attendance already: ', idListAttendance)
                                        numberPathAttendance += 1        
                                        grayConvertRgb = cv2.cvtColor(grayImageRealtime[y:y+h,x:x+w], cv2.COLOR_GRAY2RGB)
                                        cv2.imwrite('image_attendance/'+str(profile[1])+'.'+str(profile[0]) +'.'+ str(numberPathAttendance) + '.jpg', grayConvertRgb)
                                        pathCompareImgRealtime = 'image_compare'
                                        imagePaths = [os.path.join(pathCompareImgRealtime, f) for f in os.listdir(pathCompareImgRealtime)] 
                                        for imagePath in imagePaths:
                                            getIdsFromPathFolder = int(os.path.split(imagePath)[-1].split('.')[1])
                                            hashs = imagehash.average_hash(Image.open('image_attendance/'+str(profile[1])+'.'+str(profile[0])+'.'+str(numberPathAttendance)+'.jpg'))
                                            otherhash = imagehash.average_hash(Image.open(imagePath))
                                            compareTwoImg = hashs - otherhash
                                            print('value compare two image is: ', compareTwoImg)
                                            if(compareTwoImg < 24 and (getIdsFromPathFolder == int(profile[0]))):
                                                print('attendance correcr')
                                                QuerySql.insertHistoryAttendance(profile[0], profile[1], today, currentTime)
                                                pathImgCorrectRealtime = 'image_correct'
                                                DeleteFile(pathImgCorrectRealtime, int(profile[0])).delete()
                                                cv2.imwrite('image_correct/'+str(profile[1])+'.'+str(profile[0]) +'.'+ str(numberPathAttendance) + '.jpg', grayConvertRgb)
                                            elif(compareTwoImg > 24 and getIdsFromPathFolder != int(profile[0])):
                                                print('attendance incorrect: ', profile[1])
                                                cv2.imwrite('image_incorrect/'+str(profile[1])+'.'+str(profile[0]) +'.'+ str(numberPathAttendance) + '.jpg', grayConvertRgb)
                            else: 
                                numberPathUnknown += 1
                                cv2.putText(imgRealtime, 'name: '+ str(idPredict), (x-30, y-20), fontface, fontscale, fontcolor , 2)
                                cv2.imwrite('image_unknown/'+str(idPredict)+'.' + str(numberPathUnknown) + '.jpg', imgRealtime)
                            imgRealtime = cv2.resize(imgRealtime, (780, 480))
                            cv2.imshow('Frame', imgRealtime) 
                        if(currentTime > startExport and currentTime < endExport):
                            numberIds, names, dateList, timeList = QuerySql.exportHistoryAttendance()
                            fileName = 'export_excel/result_attendance.xls'
                            Export.excel(numberIds, names, dateList, timeList, fileName)
                        k = cv2.waitKey(30)
                        if k == 27:
                            break
                        elif k ==-1:
                            continue   
                except:
                    messagebox.showinfo('message', 'Please enter button trainning model!')
            def searchByDateFunc():
                searchKey = str(inputSearchByDate.get())
                FrameSearchByDate(searchKey).show()

            def attendanceTodayListFunc():
                FrameAttendanceToday.show()
            
            def btn_doiAdmin():
                tk_doiPass = Tk()
                tk_doiPass.geometry('550x150')
                tk_doiPass.resizable(False,False)
                tk_doiPass.configure(bg='CornflowerBlue')

                def btn_newPass():
                    new_username = lbl_NID_user.get()
                    new_pass = lbl_T_pass.get()
                    if((new_username == '' and new_pass=='') or new_username == '' or new_pass==''):
                        messagebox.showinfo('message', 'Vui lòng nhập thông tin đầy đủ')
                    elif(len(new_pass) < 6 and len(new_pass)>10):
                        messagebox.showinfo('message', 'Pass phải có độ dài từ 6 đến 10 ký tự')
                    else:
                        md = hashlib.md5()
                        md.update(new_pass.encode())
                        new_pass = md.hexdigest()
                        QuerySql.updateAdmin(new_username, new_pass)
                        messagebox.showinfo('message', 'Thay đổi thành công')
                        tk_doiPass.destroy()

                lbl_new_username = Label(tk_doiPass, text='UserName new', bd=4, fg='white', font=(fontTypeApp, 16), width= 10, bg='green')
                lbl_new_username.place(x= 15, y= 10)
                lbl_NID_user = Entry(tk_doiPass, width=35, bd=5, font=(fontTypeApp, 14))
                lbl_NID_user.place(x= 200, y= 10)
                lbl_pass_new = Label(tk_doiPass, text='PassWord new', bd=4, fg='white', font=(fontTypeApp, 16), width= 10, bg='green')
                lbl_pass_new.place(x= 15, y= 50)
                lbl_T_pass = Entry(tk_doiPass, width=35, bd=5, font=(fontTypeApp, 14), show='*')
                lbl_T_pass.place(x= 200, y= 50)

                btn_newPass = Button(tk_doiPass, text='Đổi Admin', font=(fontTypeApp, 14), fg='white', bg='red',
                    width=15, height=1, command=btn_newPass)
                btn_newPass.place(x= 250, y= 90)

            def recognitionImageFunc():
                FrameAttendanceImage(mainAppScreen, latestFrame, lableShowNameCapReco, lableShowNumberIdCapReco, recognizer).show()
                
            def calculateAccuracyFunc():
                pathFolderImageTest = 'image_test'
                idLists, faceLists = GetInfoImage.getImagesAndLabels(pathFolderImageTest) 
                resultPredict = []
                for img in faceLists:
                    gray = cv2.fastNlMeansDenoising(img, None, 4, 5, 11)
                    predict, conf = recognizer.predict(gray)
                    resultPredict.append(predict)
                resultCalculate = Accuracy.calculate(np.array(idLists), np.array(resultPredict))
                messagebox.showinfo('message','Accuracy of 100 image test is: '+str(resultCalculate) + '%')

            buttonAddNewUserTrainModel = Button(mainAppScreen, text = 'Add new data train', font = (fontTypeApp, 14), fg = 'white', bg = 'green',
            width = 18, height = 1, command = addNewUserTrainModelFunc)
            buttonAddNewUserTrainModel.place(x = 10, y = 400)
            btn_danhsachNguoi= Button(mainAppScreen, text='Danh sách nhân viên', font=(fontTypeApp, 14), fg='white', bg='green',
            width=18, height=1, command=btn_danhsachNguoi)
            btn_danhsachNguoi.place(x=10, y = 450)
            buttonAttendanceToday = Button(mainAppScreen, text='List Attendance today', font=(fontTypeApp, 14), fg='white', bg='green',
                width = 18, height = 1, command = attendanceTodayListFunc)
            buttonAttendanceToday.place(x=250, y = 400)
            btncalculateAccuracyFunc= Button(mainAppScreen, text='Calculate accuracy', font = (fontTypeApp, 14), fg = 'white', bg = 'green',
                width = 15, height=1, command = calculateAccuracyFunc)
            btncalculateAccuracyFunc.place(x = 490, y = 400)
            btnTrainModel= Button(mainAppScreen, text='Trainning data', font = (fontTypeApp, 14), fg='white', bg='green',
                width = 15, height = 1, command = trainningModelFunc)
            btnTrainModel.place(x=490, y = 450)
            btn_doiPass= Button(mainAppScreen, text='Đổi mật khẩu', font=(fontTypeApp, 14), fg='white', bg='green',
            width=18, height=1, command=btn_doiAdmin)
            btn_doiPass.place(x=250, y = 450)
            buttonRecognitionImage= Button(mainAppScreen, text = 'Capture attendance', font = (fontTypeApp, 14), fg = 'white', bg='green',
            width = 18, height = 1, command = recognitionImageFunc)
            buttonRecognitionImage.place(x = 250, y = 500)
            buttonAttendanceRealtime = Button(mainAppScreen, text = 'Attendance realtime', font = (fontTypeApp, 14), fg = 'white', bg = 'green',
            width = 18, height = 1, command = attendanceRealtimeFunc)
            buttonAttendanceRealtime.place(x = 10, y = 500)
            buttonSearchByDate= Button(mainAppScreen, text = 'Search By Date', font = (fontTypeApp, 14), fg = 'white', bg='green',
            width = 18, height = 1, command = searchByDateFunc)
            buttonSearchByDate.place(x = 10, y = 550)
            inputSearchByDate = Entry(mainAppScreen, width = 20, bd = 5,font = (fontTypeApp, 14))
            inputSearchByDate.place(x = 250, y = 550)
            lableShowNameCapReco = Label(mainAppScreen, text = '', font = (fontTypeApp, 16), fg = 'red')
            lableShowNameCapReco.place(x = 900, y = 410)
            lableShowNumberIdCapReco = Label(mainAppScreen, text = '', font = (fontTypeApp, 16), fg = 'red')
            lableShowNumberIdCapReco.place(x = 900, y = 450)
        
        lableOptionCamera = Label(cameraOptionScreen, text = 'Enter path video or stream (to open camera computer enter 0 or empty)', font = (fontTypeApp, 18), fg = 'green', bg = 'white')
        lableOptionCamera.place(x = 10, y = 10)                
        buttonOptionCamera = Button(cameraOptionScreen, text = 'Option camera', font = (fontTypeApp,14),fg = 'white', bg = 'green',
                    width = 15, height = 1, bd = 2, command = optionCameraFunc)  
        buttonOptionCamera.place(x = 10, y = 60)
        inputOptionCamera = Entry(cameraOptionScreen, width = 45, bd = 5, font = (fontTypeApp, 14))
        inputOptionCamera.place(x = 210, y = 60)
                 
lableTitle = Label(root, text ='ATTENDANCE APP USE FACE RECOGNITION TECH (OPENCV)', font = (fontTypeApp, 20), fg = 'red')
lableTitle.place(x = 45, y = 10)
lableUsername = Label(root, text = 'username: ', width = 10, bd = 4, font = (fontTypeApp, 16), fg = 'green')
lableUsername.place(x = 160, y = 200)
inputUsername = Entry(root, width = 50, bd = 5, font = (fontTypeApp, 14))
inputUsername.place(x = 300,y = 200)
lablePassword = Label(root, text = 'password: ', width = 10, bd = 4, font = (fontTypeApp, 16), fg = 'green')
lablePassword.place(x = 160, y = 250)
inputPassword = Entry(root, width = 50, bd = 5,font = (fontTypeApp, 14), show = '*')
inputPassword.place(x=300,y=250)
buttonLogin = Button(root, text='Login', font = (fontTypeApp, 14), fg = 'white', bg = 'red',
    width = 20, height = 1, bd = 4, command = loginApp)
buttonLogin.place(x = 340, y = 400)
root.mainloop()