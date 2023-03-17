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
from view_image import Xem_Image
from excel import Export
from date import SearchDate, CurrentDate
from accuracy import Accuracy
from get_camera import Camera
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
            def rtsp_cam_buffer(cap):
                global latestFrame, lo, lastRet
                while True:
                    with lo:
                        try:
                            lastRet, latestFrame = cap.read()
                        except:
                            print('error exception')
            t1 = threading.Thread(target=rtsp_cam_buffer,args=(cap,),name='rtsp_read_thread')
            t1.daemon=True
            t1.start()

            cameraOptionScreen.destroy()
            tk_main = Tk()
            tk_main.geometry('1350x700')
            tk_main.resizable(False,False)
            background_main=ImageTk.PhotoImage(Image.open('image_background_app/background.jpg'))
            panel = Label(tk_main, image = background_main)
            panel.image = background_main
            panel.place(x = 0, y = 0)

            lbl_main = Label(tk_main)
            lbl_main.place(x=20,y=10)
            #video_mylove.mp4 đọc và nhận dạng nhưng tốc độ quá nhanh
            def show_face():
                try:
                    global face
                    if((optionCamera.isnumeric and len(optionCamera)==1) or len(optionCamera)==0):
                        _,face = cap.read()
                    else:
                        face = latestFrame.copy()
                    face= cv2.flip(face, 1)
                    image = cv2.cvtColor(face, cv2.COLOR_BGR2RGBA)
                    img = Image.fromarray(image)
                    img = img.resize((620, 480),Image.ANTIALIAS)
                    imgtk = ImageTk.PhotoImage(image=img)
                    lbl_main.imgtk = imgtk
                    lbl_main.configure(image=imgtk)
                    lbl_main.after(10, show_face)
                except:
                    print('error exception')
            show_face()
            global recognizer
            def trainningModelFunc():
                Ids, faces = GetInfoImage.getImagesAndLabels(path)
                recognizer.train(faces, np.array(Ids))
                recognizer.save('trainning_result/trainning_model.yml')
                messagebox.showinfo('message', 'Finish trainning model')

            def btn_themNguoiMoi():                  
                tk_themNguoi = Tk()
                tk_themNguoi.geometry('500x150')
                tk_themNguoi.resizable(False,False)
                tk_themNguoi.configure(bg='CornflowerBlue')
                def btn_themNguoi():
                    id= lbl_NID_nguoiMoi.get()
                    name= lbl_T_nguoiMoi.get()
                    if(len(id)==0 or len(name)==0):
                        messagebox.showinfo('message', 'Vui lòng nhập thông tin vào')
                    elif id.isdecimal:
                        arr_check_id = QuerySql.selectLabelfaceById(id)
                        if(len(arr_check_id)==0):
                            QuerySql.insertLabelface(id, name)
                            sampleNum = 0
                            while(True):
                                if (lastRet is not None) and (latestFrame is not None):
                                    img = latestFrame.copy()
                                    gray = cv2.fastNlMeansDenoising(img,None,4,5,11)
                                    faces = detector.detectMultiScale(gray,1.3,5)
                                    if(len(faces)==1):
                                        for (x,y,w,h) in faces:
                                            sampleNum=sampleNum+1
                                            cv2.imwrite('image_trainning_model/User.'+ id +'.'+ str(sampleNum) + '.jpg', gray[y:y+h,x:x+w])
                                            cv2.imwrite('image_compare/User.'+ id +'.'+'.jpg', gray[y:y+h,x:x+w])
                                        if(sampleNum>49):
                                            speaker = win32com.client.Dispatch('SAPI.SpVoice')
                                            speaker.Speak('Save success please check')
                                            messagebox.showinfo('message', 'Thêm thành công vui lòng kiểm tra thư mục')
                                            break
                                    elif(len(faces)==0):
                                        print('Không tìm thấy khuôn mặt')
                                        continue
                                    else: 
                                        # speaker = win32com.client.Dispatch('SAPI.SpVoice')
                                        # speaker.Speak('Detected two face in frame, please restarted')
                                        messagebox.showinfo('message','Tìm thấy 2 gương mặt trong cùng frame')
                                        QuerySql.deleteLabelface(id)
                                        path = 'image_trainning_model'
                                        DeleteFile(path, id).delete()
                                        path_ss = 'image_compare'
                                        DeleteFile(path_ss, id).delete()
                                        break
                                        #detroy frame thêm người mới
                                    cv2.imshow('img',img)
                                    k = cv2.waitKey(30)
                                    if k == 27:
                                        break
                                    elif k ==-1:
                                        continue
                                else:
                                    print('không lấy được video')
                                    time_out.sleep(0.2)
                                    continue                                    
                        else:
                            messagebox.showinfo('message', 'ID đã có rồi vui lòng nhập ID khác')
                    else:
                        messagebox.showinfo('message', 'Thêm không thành công')
                    tk_themNguoi.destroy()
                
                def btn_them_data_test():
                    id_test = lbl_NID_nguoiMoi.get()
                    name= lbl_T_nguoiMoi.get()
                    if(id_test == ''):
                        messagebox.showinfo('message','Nhập vào ID giống với ID có trong thư mục train model')
                    else:
                        sampleNum = 0
                        while(True):
                            if (lastRet is not None) and (latestFrame is not None):
                                img = latestFrame.copy()
                                img1 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                                gray = cv2.fastNlMeansDenoising(img1,None,4,5,11)
                                faces = detector.detectMultiScale(gray,1.3,5)
                                if(len(faces)==1):
                                    for (x,y,w,h) in faces:
                                        sampleNum=sampleNum+1
                                        cv2.imwrite('image_test/'+name +'.'+ id_test +'.'+ str(sampleNum) + '.jpg', gray[y:y+h,x:x+w])
                                    if(sampleNum>99):
                                        messagebox.showinfo('message', 'Đã thêm vào tập test thành công')
                                        break
                                elif(len(faces)==0):
                                    print('Không tìm thấy khuôn mặt')
                                    continue
                                else: 
                                    messagebox.showinfo('message', 'Tìm thấy 2 khuôn mặt trong frame')
                                    path = 'image_test'
                                    DeleteFile(path, id_test).delete()
                                    break
                                    #detroy frame thêm người mới
                                cv2.imshow('img',img)
                                k = cv2.waitKey(30)
                                if k == 27:
                                    break
                                elif k ==-1:
                                    continue
                            else:
                                print('không lấy được video')
                                time_out.sleep(0.2)
                                continue
                    messagebox.showinfo('message', 'Thêm vào tập test thành công')
                lbl_ID_nguoiMoi = Label(tk_themNguoi, text='Mã số', bd= 4, fg='white', font=(fontTypeApp, 16), width= 10, bg='green')
                lbl_ID_nguoiMoi.place(x= 15, y= 10)
                lbl_NID_nguoiMoi = Entry(tk_themNguoi, bd=5,width=35, font=(fontTypeApp, 14))
                lbl_NID_nguoiMoi.place(x= 150, y= 10)
                lbl_Ten_nguoiMoi = Label(tk_themNguoi, text='Họ tên', bd=4, fg='white', font=(fontTypeApp, 16), width= 10, bg='green')
                lbl_Ten_nguoiMoi.place(x= 15, y= 45)
                lbl_T_nguoiMoi = Entry(tk_themNguoi, width=35, bd=5,font=(fontTypeApp, 14))
                lbl_T_nguoiMoi.place(x= 150, y= 45)
                btn_themNguoi = Button(tk_themNguoi, text='Thêm người', font=(fontTypeApp, 14), fg='white', bg='green',
                    width=15, height=1, command=btn_themNguoi)
                btn_themNguoi.place(x= 100, y= 90)
                btn_them_data_test = Button(tk_themNguoi, text='Thêm vào tập test', font=(fontTypeApp, 14), fg='white', bg='green',
                    width=15, height=1, command=btn_them_data_test)
                btn_them_data_test.place(x= 300, y=90)
            #space+tab => lùi vào 1 space còn shift+tab ngược lại
            def btn_danhsachNguoi():
                rows = QuerySql.fetchAllLabelface()
                tk_ds = Tk()
                tk_ds.title('Danh sách nhân viên')
                tk_ds.geometry('550x550')
                tk_ds.resizable(False,False)
                tk_ds.configure(bg='CornflowerBlue')
                lbl_title_ds = Label(tk_ds, text = 'DANH SÁCH NHÂN VIÊN CÔNG TY', font = (fontTypeApp, 18),fg='green')
                lbl_title_ds.place(x=100, y =10)
                entry_1 = Label(tk_ds, text='',font = (fontTypeApp, 14))
                entry_1.place(x=10,y =60)
                entry_2 = Label(tk_ds, text='',font = (fontTypeApp, 14))
                entry_2.place(x=80, y =60)

                frm = Frame(tk_ds)
                frm.pack(side = tkinter.LEFT, padx=50)
                tv = ttk.Treeview(frm, columns = (1,2), show ='headings', height = '15', padding='Centimeters')
                tv.pack(side ='right')
                verscrlbar = ttk.Scrollbar(tk_ds, orient ='vertical', command = tv.yview)
                verscrlbar.pack(side ='right', fill ='x') 
                tv.configure(xscrollcommand = verscrlbar.set)
                tv.heading(1, text = 'Mã số nhân viên')
                tv.heading(2, text = 'Họ và tên')
                for i in rows:
                    tv.insert('','end',values=i)
                def selectItem(event):
                    curItem = tv.focus()
                    get_value = tv.item(curItem)
                    a = get_value['values']
                    dv = []
                    for i in a:
                        dv.append(i)
                    try:
                        entry_1.configure(text=dv[0])
                        entry_2.configure(text=dv[1])
                    except:
                        print('error exception')
                    def btn_xoa():
                        try:
                            row = tv.selection()[0]
                            id_f = int(dv[0])
                            tv.delete(row)
                        except:
                            print('error exception')
                        QuerySql.deleteLabelface(id_f)
                        DeleteFile(path, id_f).delete()
                        path_xoaNV = 'image_compare'
                        DeleteFile(path_xoaNV, id_f).delete()                                   
                        messagebox.showinfo('message', 'Xóa thành công')
                    def btn_xemAnh():
                        path1 = 'image_compare'
                        Xem_Image(path1, int(dv[0])).Xem()
                    btn_xemAnh= Button(tk_ds, text='Xem ảnh', font=(fontTypeApp, 14), fg='white', bg='green',
                                    width=10, height=1, command=btn_xemAnh)
                    btn_xemAnh.place(x=300, y=60)
                    btn_recog= Button(tk_ds, text='Xóa', font=(fontTypeApp, 14), fg='white', bg='green',
                                    width=10, height=1, command=btn_xoa)
                    btn_recog.place(x=420, y=60)
                
                tv.bind('<Button-1>', selectItem)
            
            def btn_diemdanhrealtime():
                image_dd = 0
                img_unknow = 0
                global img
                try:
                    while True:
                        if((lastRet is not None) and (latestFrame is not None)):
                            img = latestFrame.copy()                            
                        else:
                            print('không lấy được video')
                            time_out.sleep(0.2)
                            continue
                        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                        gray = cv2.fastNlMeansDenoising(gray,None,4,5,11)
                        faces=detector.detectMultiScale(gray,1.3,5)
                        Ngay, Gio,start_dd_sang, end_dd_sang,start_dd_chieu,end_dd_chieu = CurrentDate.dateHourTimeAttendance()
                        gio_to_excel,gio_end_to_excel = CurrentDate.setupHourAutoExport()
                        info_tt = QuerySql.fetchHistoryAttendanceByCurrentDate()
                        ids = []
                        for i in info_tt:
                            ids.append(i[0])
                        for(x,y,w,h) in faces:
                            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),1)
                            id,conf=recognizer.predict(gray[y:y+h,x:x+w])
                            print('He so confident: ',round(conf,2))
                            profile = GetInfoImage.getProfile(id)
                            Id='Uknown'
                            conf = round(100*(1-(conf/300)),2)
                            print('Độ chính xác (%): ',conf)
                            if(conf > 70):     
                                cv2.putText(img, str(conf) + '% : ' + str(profile[1]), (x+10,y-20), fontface, fontscale, fontcolor ,2)  
                                dem = 0
                                if((Gio > start_dd_sang and Gio < end_dd_sang) or (Gio > start_dd_chieu and Gio < end_dd_chieu)):
                                    print('profile ID: ',profile[0])
                                    for n in ids:
                                        if(int(n) == int(profile[0])):
                                            dem=dem+1
                                    if(dem < 1):
                                        print('Danh sách ID đã điểm danh: ',ids)
                                        image_dd=image_dd+1        
                                        img_cv = cv2.cvtColor(gray[y:y+h,x:x+w], cv2.COLOR_GRAY2RGB)
                                        cv2.imwrite('image_attendance/'+str(profile[1])+'.'+str(profile[0]) +'.'+ str(image_dd) + '.jpg', img_cv)
                                        path2 = 'image_compare'
                                        imagePaths=[os.path.join(path2,f) for f in os.listdir(path2)] 
                                        for imagePath in imagePaths:
                                            ID_ss=int(os.path.split(imagePath)[-1].split('.')[1])
                                            hashs = imagehash.average_hash(Image.open('image_attendance/'+str(profile[1])+'.'+str(profile[0])+'.'+str(image_dd)+'.jpg'))
                                            otherhash = imagehash.average_hash(Image.open(imagePath))
                                            c = hashs - otherhash
                                            print('gia tri so sánh 2 bức ảnh: ',c)
                                            if(c < 24 and (ID_ss == int(profile[0]))):
                                                print('Điểm danh đúng rồi')
                                                QuerySql.insert_ttdiemdanh(profile[0],profile[1],Ngay,Gio)
                                                #Xóa ảnh cũ cùng ID để thêm ảnh mới vào
                                                path2 = 'image_correct'
                                                DeleteFile(path2, int(profile[0])).delete()
                                                cv2.imwrite('image_correct/'+str(profile[1])+'.'+str(profile[0]) +'.'+ str(image_dd) + '.jpg', img_cv)
                                            elif(c > 24 and ID_ss!=int(profile[0])):
                                                print('Điểm danh sai rồi: ', profile[1])
                                                cv2.imwrite('image_incorrect/'+str(profile[1])+'.'+str(profile[0]) +'.'+ str(image_dd) + '.jpg', img_cv)
                                # else:
                                #     messagebox.showinfo('message', 'Không nằm trong khung giờ điểm danh')
                            else: 
                                img_unknow = img_unknow+1
                                cv2.putText(img, 'Name: '+ str(Id),(x-30,y-20), fontface, fontscale, fontcolor ,2)
                                cv2.imwrite('image_unknown/'+str(Id)+'.' + str(img_unknow) + '.jpg', img)
                            img = cv2.resize(img, (780,480))
                            cv2.imshow('Frame',img) 
                        if(Gio>gio_to_excel and Gio<gio_end_to_excel):
                            msnv, hotennv, list_day, list_gio = QuerySql.exportHistoryAttendance()
                            file_name = 'result_attendance.xls'
                            Export.Excel(msnv,hotennv,list_day,list_gio,file_name)
                        k = cv2.waitKey(30)
                        if k == 27:
                            break
                        elif k ==-1:
                            continue   
                except:
                    messagebox.showinfo('message', 'Vui lòng trainning trước!')
            def btn_dsdiemdanh():
                Tim_ngay = str(Entry_dsdiemdanh.get())
                global x
                x = SearchDate.formatDate(Tim_ngay)
                rows_ds = QuerySql.queryHistoryByDate(x)
                tk_ds = Tk()
                tk_ds.title('Danh sách điểm danh')
                tk_ds.geometry('950x550')
                tk_ds.resizable(False,False)
                tk_ds.configure(bg='CornflowerBlue')
                lbl_title_ds = Label(tk_ds, text = 'DANH SÁCH ĐIỂM DANH NGAY '+str(x), font = (fontTypeApp, 18),fg='green')
                lbl_title_ds.place(x=200, y =10)
                entry_1 = Label(tk_ds, text='',font = (fontTypeApp, 14))
                entry_1.place(x=10,y =60)
                entry_2 = Label(tk_ds, text='',font = (fontTypeApp, 14))
                entry_2.place(x=80, y =60)
                entry_3 = Label(tk_ds, text='',font = (fontTypeApp, 14))
                entry_3.place(x=300, y =60)
                entry_4 = Label(tk_ds, text='', font = (fontTypeApp, 14))
                entry_4.place(x=500, y =60)

                frm = Frame(tk_ds)
                frm.pack(side = tkinter.LEFT, padx=50)
                tv = ttk.Treeview(frm, columns = (1,2,3,4), show ='headings', height = '15', padding='Centimeters')
                tv.pack(side ='right')
                verscrlbar = ttk.Scrollbar(tk_ds, orient ='vertical', command = tv.yview)
                verscrlbar.pack(side ='right', fill ='x') 
                tv.configure(xscrollcommand = verscrlbar.set)
                tv.heading(1, text = 'Mã số nhân viên')
                tv.heading(2, text = 'Họ và tên')
                tv.heading(3, text = 'Ngày điểm danh')
                tv.heading(4, text = 'Giờ điểm danh')
                for i in rows_ds:
                    tv.insert('','end',values=i)
                
                def selectItem(event):
                    curItem = tv.focus()
                    get_value = tv.item(curItem)
                    a = get_value['values']
                    dv = []
                    for i in a:
                        dv.append(i)
                    try:
                        entry_1.configure(text=dv[0])
                        entry_2.configure(text=dv[1])
                        entry_3.configure(text=dv[2])
                        entry_4.configure(text=dv[3])
                    except:
                        print('error exception')
                    def btn_xoa_dd():
                        try:
                            row = tv.selection()[0]
                            id_f = int(dv[0])
                            gio_d = dv[3]
                        except:
                            print('error exception')
                        tv.delete(row)
                        QuerySql.deleteHistoryAttendance(id_f,gio_d)
                        messagebox.showinfo('message', 'Xóa thành công')
                    def btn_xemAnh_dd():
                        path2 = 'image_correct'
                        Xem_Image(path2,int(dv[0])).Xem()

                    btn_xemAnh_dd= Button(tk_ds, text='Xem ảnh', font=(fontTypeApp, 14), fg='white', bg='green',
                                    width=10, height=1, command=btn_xemAnh_dd)
                    btn_xemAnh_dd.place(x=650, y=60)
                    btn_recog_dd= Button(tk_ds, text='Xóa', font=(fontTypeApp, 14), fg='white', bg='green',
                                    width=10, height=1, command=btn_xoa_dd)
                    btn_recog_dd.place(x=770, y=60)
                def btn_thongke():
                    arr_lb, arr_tt, arr_chuadd = QuerySql.statictisHistoryByDate(x)
                    tk_tk = Tk()
                    tk_tk.title('Danh sách nhân viên chưa điểm danh')
                    tk_tk.geometry('600x550')
                    tk_tk.resizable(False,False)
                    tk_tk.configure(bg='CornflowerBlue')
                    lbl_title_ds_ch = Label(tk_tk, text = 'DANH SÁCH NHÂN VIÊN CHƯA ĐIỂM DANH', font = (fontTypeApp, 18),fg='green')
                    lbl_title_ds_ch.place(x=50, y =10)

                    frm1 = Frame(tk_tk)
                    frm1.pack(side = tkinter.LEFT, padx=30)
                    tv1 = ttk.Treeview(frm1, columns = (1,2), show ='headings', height = '15', padding='Centimeters')
                    tv1.pack(side ='right')
                    verscrlbar1 = ttk.Scrollbar(tk_tk, orient ='vertical', command = tv1.yview)
                    verscrlbar1.pack(side ='right', fill ='x') 
                    tv1.configure(xscrollcommand = verscrlbar1.set)
                    tv1.heading(1, text = 'Mã số nhân viên')
                    tv1.heading(2, text = 'Họ và tên')
                    
                    lbl_tk = Label(tk_tk, text='Chưa điểm danh: ', font=(fontTypeApp, 16), fg='red')
                    lbl_tk.place(x=100,y=60)
                    lbl_tk_va = Label(tk_tk, text=' ', font=(fontTypeApp, 16), fg='red')
                    lbl_tk_va.place(x=300,y=60)
                    lbl_tk_roi = Label(tk_tk, text='Điểm danh rồi: ', font=(fontTypeApp, 16), fg='red')
                    lbl_tk_roi.place(x=400,y=60)
                    lbl_tk_vaRoi = Label(tk_tk, text=' ', font=(fontTypeApp, 16), fg='red')
                    lbl_tk_vaRoi.place(x=550,y=60)
                    if(len(arr_tt)==0):
                        for y in arr_lb:
                            tv1.insert('','end',values=(y[0],y[1]))
                        lbl_tk_va.configure(text = len(arr_lb))
                        lbl_tk_vaRoi.configure(text = len(arr_tt))
                    elif(len(arr_tt)==len(arr_lb)):
                        for i in arr_chuadd:
                            tv1.insert('','end',values='')
                        lbl_tk_va.configure(text = 0)
                        lbl_tk_vaRoi.configure(text = len(arr_tt))
                    else:
                        for i in arr_chuadd:
                            tv1.insert('','end',values=(i[0],i[1]))
                        lbl_tk_va.configure(text = len(arr_chuadd))
                        lbl_tk_vaRoi.configure(text = len(arr_tt))

                btn_thongke= Button(tk_ds, text='Thống kê', font=(fontTypeApp, 14), fg='white', bg='green',
                                    width=10, height=1, command=btn_thongke)
                btn_thongke.place(x=350, y=480)
                
                tv.bind('<Button-1>', selectItem)

            def btn_ddhomnay():
                rows_hn = QuerySql.fetchHistoryAttendanceByCurrentDate()
                tk_hn = Tk()
                tk_hn.title('Danh sách điểm danh hôm nay')
                tk_hn.geometry('950x550')
                tk_hn.resizable(False,False)
                tk_hn.configure(bg='CornflowerBlue')
                lbl_title_dshn = Label(tk_hn, text = 'DANH SÁCH ĐIỂM DANH NGAY HÔM NAY', font = (fontTypeApp, 18),fg='green')
                lbl_title_dshn.place(x=200, y =10)
                entry_1hn = Label(tk_hn, text='',font = (fontTypeApp, 14))
                entry_1hn.place(x=10,y =60)
                entry_2hn = Label(tk_hn, text='',font = (fontTypeApp, 14))
                entry_2hn.place(x=80, y =60)
                entry_3hn = Label(tk_hn, text='',font = (fontTypeApp, 14))
                entry_3hn.place(x=300, y =60)
                entry_4hn = Label(tk_hn, text='', font = (fontTypeApp, 14))
                entry_4hn.place(x=500, y =60)

                frmhn = Frame(tk_hn)
                frmhn.pack(side = tkinter.LEFT, padx=50)
                tvhn = ttk.Treeview(frmhn, columns = (1,2,3,4), show ='headings', height = '15', padding='Centimeters')
                tvhn.pack(side ='right')
                verscrlbarhn = ttk.Scrollbar(tk_hn, orient ='vertical', command = tvhn.yview)
                verscrlbarhn.pack(side ='right', fill ='x') 
                tvhn.configure(xscrollcommand = verscrlbarhn.set)
                tvhn.heading(1, text = 'Mã số nhân viên')
                tvhn.heading(2, text = 'Họ và tên')
                tvhn.heading(3, text = 'Ngày điểm danh')
                tvhn.heading(4, text = 'Giờ điểm danh')
                for i in rows_hn:
                    tvhn.insert('','end',values=i)

                def selectItem(event):
                    curItem = tvhn.focus()
                    get_value = tvhn.item(curItem)
                    a = get_value['values']
                    dv = []
                    for i in a:
                        dv.append(i)
                    try:
                        entry_1hn.configure(text=dv[0])
                        entry_2hn.configure(text=dv[1])
                        entry_3hn.configure(text=dv[2])
                        entry_4hn.configure(text=dv[3])
                    except:
                        print('error exception')
                    def btn_xoa_ddhn():
                        try:
                            row = tvhn.selection()[0]
                            id_f = int(dv[0])
                            gio_d = dv[3]
                        except:
                            print('error exception')
                        tvhn.delete(row)
                        QuerySql.deleteHistoryAttendance(id_f,gio_d)
                        path2 = 'image_correct'
                        DeleteFile(path2, int(dv[0])).delete()
                        messagebox.showinfo('message', 'Xóa thành công')
                    def btn_xemAnh_ddhn():
                        path2 = 'image_correct'
                        Xem_Image(path2, int(dv[0])).Xem()

                    btn_xemAnh_ddhn= Button(tk_hn, text='Xem ảnh', font=(fontTypeApp, 14), fg='white', bg='green',
                                    width=10, height=1, command=btn_xemAnh_ddhn)
                    btn_xemAnh_ddhn.place(x=650, y=60)
                    btn_recog_ddhn= Button(tk_hn, text='Xóa', font=(fontTypeApp, 14), fg='white', bg='green',
                                    width=10, height=1, command=btn_xoa_ddhn)
                    btn_recog_ddhn.place(x=770, y=60)
                def btn_ExToExcel():
                    msnv, hotennv, list_day, list_gio = QuerySql.exportHistoryAttendance()
                    file_name = 'attendance_today.xls'
                    Export.Excel(msnv,hotennv,list_day,list_gio,file_name)
                    messagebox.showinfo('TB','Export đến file exel thành công')

                btn_ExToExcel= Button(tk_hn, text='Export to excel', font=(fontTypeApp, 14), fg='white', bg='green',
                                    width=15, height=1, command=btn_ExToExcel)
                btn_ExToExcel.place(x=350, y=480)
                
                tvhn.bind('<Button-1>', selectItem)
            
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

            def btn_ddhinhanh():
                image1 = latestFrame.copy()
                cv2.imwrite('anhchupnhandang.jpg', image1)
                img_nd = ImageTk.PhotoImage(Image.open('anhchupnhandang.jpg').resize((620, 480),Image.ANTIALIAS))
                panel = Label(tk_main, image = img_nd)
                panel.image = img_nd
                panel.place(x = 700, y = 10)
                img = cv2.imread('anhchupnhandang.jpg')

                gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                gray = cv2.fastNlMeansDenoising(gray,None,4,5,11)
                faces=detector.detectMultiScale(gray,1.3,5)
                global ID, Name, Ngay,Gio
                Ngay, Gio,start_dd_sang, end_dd_sang,start_dd_chieu,end_dd_chieu = CurrentDate.dateHourTimeAttendance()                   
                info_tt = QuerySql.fetchHistoryAttendanceByCurrentDate()
                ids = []
                for i in info_tt:
                    ids.append(i[0])
                image_dd = 0   
                try:
                    for(x,y,w,h) in faces:
                        id,conf=recognizer.predict(gray[y:y+h,x:x+w])
                        profile = GetInfoImage.getProfile(id)
                        if(conf<90):    
                            dem = 0
                            if((Gio > start_dd_sang and Gio < end_dd_sang) or (Gio > start_dd_chieu and Gio < end_dd_chieu)):
                                for n in ids:
                                    if(int(n) == int(profile[0])):
                                        dem=dem+1
                                if(dem < 1):
                                    image_dd=image_dd+1
                                    img_cv = cv2.cvtColor(gray[y:y+h,x:x+w], cv2.COLOR_GRAY2RGB)
                                    cv2.imwrite('image_attendance/anhchup'+'.'+str(profile[0]) +'.'+ str(image_dd) + '.jpg', img_cv)
                                    path2 = 'image_compare'
                                    imagePaths=[os.path.join(path2,f) for f in os.listdir(path2)] 
                                    for imagePath in imagePaths:
                                        ID_ss=int(os.path.split(imagePath)[-1].split('.')[1])
                                        hashs = imagehash.average_hash(Image.open('image_attendance/anhchup'+'.'+str(profile[0])+'.'+str(image_dd)+'.jpg'))
                                        otherhash = imagehash.average_hash(Image.open(imagePath))
                                        c = hashs - otherhash
                                        if(c<22 and (ID_ss == int(profile[0]))):
                                            QuerySql.insert_ttdiemdanh(profile[0],profile[1],Ngay,Gio)
                                            cv2.imwrite('image_correct/'+str(profile[1])+'.'+str(profile[0]) +'.'+ str(image_dd) + '.jpg', img_cv)
                                            messagebox.showinfo('message', 'Điểm danh đúng rồi')
                                        else:
                                            messagebox.showinfo('message', 'Điểm danh sai')
                                else:
                                    messagebox.showinfo('message', 'Đã điểm danh rồi')
                            else:
                                messagebox.showinfo('message', 'Không nằm trong khung giờ điểm danh')
                            name = str(profile[1])
                            ids = str(profile[0])
                        else:
                            name = 'unknow'
                            ids = 'unknow'
                
                    b = 'Họ tên nv : ' + name
                    a = 'Mã số nv : ' + ids
                    lbl_showTT_ten.configure(text = b)
                    lbl_showTT_Ms.configure(text = a)
                except:
                    messagebox.showinfo('message', 'Vui lòng trainning trước!')
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

            btn_themNguoiMoi= Button(tk_main, text='Thêm người mới', font=(fontTypeApp, 14), fg='white', bg='green',
            width=18, height=1, command=btn_themNguoiMoi)
            btn_themNguoiMoi.place(x=10, y=500)
            btn_danhsachNguoi= Button(tk_main, text='Danh sách nhân viên', font=(fontTypeApp, 14), fg='white', bg='green',
            width=18, height=1, command=btn_danhsachNguoi)
            btn_danhsachNguoi.place(x=10, y=550)
            btn_ddhomnay= Button(tk_main, text='Điểm danh hôm nay', font=(fontTypeApp, 14), fg='white', bg='green',
            width=18, height=1, command=btn_ddhomnay)
            btn_ddhomnay.place(x=250, y=500)
            btncalculateAccuracyFunc= Button(tk_main, text='Calculate accuracy', font = (fontTypeApp, 14), fg = 'white', bg = 'green',
                width = 15, height=1, command = calculateAccuracyFunc)
            btncalculateAccuracyFunc.place(x=490, y=500)
            btnTrainModel= Button(tk_main, text='Trainning data', font = (fontTypeApp, 14), fg='white', bg='green',
                width = 15, height = 1, command = trainningModelFunc)
            btnTrainModel.place(x=490, y=550)
            btn_doiPass= Button(tk_main, text='Đổi mật khẩu', font=(fontTypeApp, 14), fg='white', bg='green',
            width=18, height=1, command=btn_doiAdmin)
            btn_doiPass.place(x=250, y=550)
            btn_ddhinhanh= Button(tk_main, text='Chụp hình điểm danh', font=(fontTypeApp, 14), fg='white', bg='green',
            width=18, height=1, command=btn_ddhinhanh)
            btn_ddhinhanh.place(x=250, y=600)
            btn_diemdanhrealtime= Button(tk_main, text='Điểm danh real time', font=(fontTypeApp, 14), fg='white', bg='green',
            width=18, height=1, command=btn_diemdanhrealtime)
            btn_diemdanhrealtime.place(x=10, y=600)
            btn_dsdiemdanh= Button(tk_main, text='Danh sách theo ngày', font=(fontTypeApp, 14), fg='white', bg='green',
            width=18, height=1, command=btn_dsdiemdanh)
            btn_dsdiemdanh.place(x=10, y=650)
            Entry_dsdiemdanh = Entry(tk_main, width=20, bd=5,font=(fontTypeApp, 14))
            Entry_dsdiemdanh.place(x= 250, y=650)
            lbl_showTT_ten = Label(tk_main, text='', font=(fontTypeApp, 16), fg='red')
            lbl_showTT_ten.place(x=1050, y=510)
            lbl_showTT_Ms = Label(tk_main, text='', font=(fontTypeApp, 16), fg='red')
            lbl_showTT_Ms.place(x=1050, y=550)
        
        lableOptionCamera = Label(cameraOptionScreen, text = 'Enter path video or stream (to open camera computer enter 0 or empty)', font = (fontTypeApp, 18), fg = 'green', bg = 'white')
        lableOptionCamera.place(x = 10, y = 10)                
        buttonOptionCamera = Button(cameraOptionScreen, text = 'Option camera', font = (fontTypeApp,14),fg = 'white', bg = 'green',
                    width = 15, height = 1, bd = 2, command = optionCameraFunc)  
        buttonOptionCamera.place(x = 10, y = 60)
        inputOptionCamera = Entry(cameraOptionScreen, width = 45, bd = 5, font = (fontTypeApp, 14))
        inputOptionCamera.place(x = 210, y = 60)
                 
lableTitle = Label(root, text='ATTENDANCE APP USE FACE RECOGNITION TECH (OPENCV)', font = (fontTypeApp, 20), fg = 'red')
lableTitle.place(x = 40, y = 10)
lableUsername = Label(root, text='username: ', width = 10, bd = 4, font = (fontTypeApp, 16), fg = 'green')
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