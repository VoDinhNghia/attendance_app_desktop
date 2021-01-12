"""
Title: File giao diện chính của ứng dụng. (contains gui file main of app)
author: Võ Đình Nghĩa. (git name: VoDinhNghia, youtube: https://www.youtube.com/watch?v=2I5mN3nljB0, facebook: https://www.facebook.com/dinhnghia.95)
Day: 15-09-2020.
Note: Viết document cho mỗi lớp và function. (write document for class and function.)
"""
import tkinter
from tkinter import*
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import numpy as np
import pickle
from tkinter.filedialog import askopenfilename
from cv2 import *
import win32com.client
import imagehash
import hashlib
import threading 
from threading import Lock
import time as time_out
from Class_conn_DB import connect_DB, sql_DB
from Class_DB_Image import get_DB_image
from Class_delete_file import Delete_file
from Class_Xem_image import Xem_Image
from Class_to_excel import Export
from Class_Ngay import NgayTim, Ngay_today
from Class_accuracy import Accuracy
from Class_get_camera import get_Camera

root = Tk()
root.title('Ứng dụng điểm danh')
root.iconbitmap('icon.jpg')
root.geometry("890x500")
root.resizable(False,False)
img1=ImageTk.PhotoImage(Image.open('nen1.jpg'))
panel = Label(root, image = img1)
panel.image = img1
panel.place(x = 0, y = 0)

#cap = cv2.VideoCapture("rtsp://192.168.1.56:554/ch0_0.h264")
cascPath = "haarcascade/haarcascade_frontalface_default.xml"
detector  = cv2.CascadeClassifier(cascPath)
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 1
fontcolor = (250,0,0)
recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'anh_data_hinh'
md5 = hashlib.md5()
password = 'Nghia123'
md5.update(password.encode())
password = md5.hexdigest()
print(password)
def FC_DangNhap():
    username = Ent_username.get()
    password = Ent_password.get()
    myresult = sql_DB.table_DN()
    for i in myresult:
        md5 = hashlib.md5()
        md5.update(password.encode())
        password = md5.hexdigest()
        print("Pass mã hóa: ", password)
        if(username == "" or password == ""):
            messagebox.showinfo("Thông báo", "Vui lòng điền đầy đủ username và password")
        elif(i[0] != username or i[1] != password):
            messagebox.showinfo("TB","Tên đăng nhập hoặc mật khẩu không đúng")
        elif(i[0] == username and i[1] == password):
            
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak("Hello, wellcome you to app")
            root.destroy()
            tk_cam = Tk()
            tk_cam.geometry("650x150")
            tk_cam.configure(bg="CornflowerBlue")
            
            def btn_ChonCamera():
                global cam_str, cap, latest_frame, lo, last_ret
                cam_str = str(Entry_camera.get()) 
                cap = get_Camera.getCam(cam_str)
                latest_frame = None
                last_ret = None
                lo = Lock()
                def rtsp_cam_buffer(cap):
                    global latest_frame, lo, last_ret
                    while True:
                        with lo:
                            try:
                                last_ret, latest_frame = cap.read()
                            except:
                                print('error exception')
                t1 = threading.Thread(target=rtsp_cam_buffer,args=(cap,),name="rtsp_read_thread")
                t1.daemon=True
                t1.start()

                tk_cam.destroy()
                tk_main = Tk()
                tk_main.geometry("1350x700")
                tk_main.resizable(False,False)
                background_main=ImageTk.PhotoImage(Image.open('nen.jpg'))
                panel = Label(tk_main, image = background_main)
                panel.image = background_main
                panel.place(x = 0, y = 0)

                lbl_main = Label(tk_main)
                lbl_main.place(x=20,y=10)
                #video_mylove.mp4 đọc và nhận dạng nhưng tốc độ quá nhanh
                def show_face():
                    try:
                        global face
                        if((cam_str.isnumeric and len(cam_str)==1) or len(cam_str)==0):
                            _,face = cap.read()
                        else:
                            face = latest_frame.copy()
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
                def btn_train_data():
                    Ids,faces = get_DB_image.getImagesAndLabels(path)
                    recognizer.train(faces,np.array(Ids))
                    recognizer.save('reco_anh/trainningData.yml')
                    messagebox.showinfo("Thông báo", "Đã hoàn thành việc trainning data")

                def btn_themNguoiMoi():                  
                    tk_themNguoi = Tk()
                    tk_themNguoi.geometry("500x150")
                    tk_themNguoi.resizable(False,False)
                    tk_themNguoi.configure(bg='CornflowerBlue')
                    def btn_themNguoi():
                        id= lbl_NID_nguoiMoi.get()
                        name= lbl_T_nguoiMoi.get()
                        if(len(id)==0 or len(name)==0):
                            messagebox.showinfo("Thông báo", "Vui lòng nhập thông tin vào")
                        elif id.isdecimal:
                            arr_check_id = sql_DB.sql_Labelface(id)
                            if(len(arr_check_id)==0):
                                sql_DB.insert_labelface(id,name)
                                sampleNum = 0
                                while(True):
                                    if (last_ret is not None) and (latest_frame is not None):
                                        img = latest_frame.copy()
                                        gray = cv2.fastNlMeansDenoising(img,None,4,5,11)
                                        faces = detector.detectMultiScale(gray,1.3,5)
                                        if(len(faces)==1):
                                            for (x,y,w,h) in faces:
                                                sampleNum=sampleNum+1
                                                cv2.imwrite("anh_data_hinh/User."+ id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                                                cv2.imwrite("data_sosanh/User."+ id +'.'+".jpg", gray[y:y+h,x:x+w])
                                            if(sampleNum>49):
                                                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                                                speaker.Speak("Save success please check")
                                                messagebox.showinfo("Thông báo", "Thêm thành công vui lòng kiểm tra thư mục")
                                                break
                                        elif(len(faces)==0):
                                            print("Không tìm thấy khuôn mặt")
                                            continue
                                        else: 
                                            # speaker = win32com.client.Dispatch("SAPI.SpVoice")
                                            # speaker.Speak("Detected two face in frame, please restarted")
                                            messagebox.showinfo('Thông báo',"Tìm thấy 2 gương mặt trong cùng frame")
                                            sql_DB.del_labelface(id)
                                            path = 'anh_data_hinh'
                                            Delete_file(path,id).delete()
                                            path_ss = 'data_sosanh'
                                            Delete_file(path_ss,id).delete()
                                            break
                                            #detroy frame thêm người mới
                                        cv2.imshow("img",img)
                                        k = cv2.waitKey(30)
                                        if k == 27:
                                            break
                                        elif k ==-1:
                                            continue
                                    else:
                                        print("không lấy được video")
                                        time_out.sleep(0.2)
                                        continue                                    
                            else:
                                messagebox.showinfo("Thông báo", "ID đã có rồi vui lòng nhập ID khác")
                        else:
                            messagebox.showinfo("Thông báo", "Thêm không thành công")
                        tk_themNguoi.destroy()
                    
                    def btn_them_data_test():
                        id_test = lbl_NID_nguoiMoi.get()
                        name= lbl_T_nguoiMoi.get()
                        if(id_test == ''):
                            messagebox.showinfo('Thông báo',"Nhập vào ID giống với ID có trong thư mục train model")
                        else:
                            sampleNum = 0
                            while(True):
                                if (last_ret is not None) and (latest_frame is not None):
                                    img = latest_frame.copy()
                                    img1 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                                    gray = cv2.fastNlMeansDenoising(img1,None,4,5,11)
                                    faces = detector.detectMultiScale(gray,1.3,5)
                                    if(len(faces)==1):
                                        for (x,y,w,h) in faces:
                                            sampleNum=sampleNum+1
                                            cv2.imwrite("data_test1/"+name +"."+ id_test +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                                        if(sampleNum>99):
                                            messagebox.showinfo("Thông báo", "Đã thêm vào tập test thành công")
                                            break
                                    elif(len(faces)==0):
                                        print("Không tìm thấy khuôn mặt")
                                        continue
                                    else: 
                                        messagebox.showinfo('Thông báo', "Tìm thấy 2 khuôn mặt trong frame")
                                        path = 'data_test1'
                                        Delete_file(path,id_test).delete()
                                        break
                                        #detroy frame thêm người mới
                                    cv2.imshow("img",img)
                                    k = cv2.waitKey(30)
                                    if k == 27:
                                        break
                                    elif k ==-1:
                                        continue
                                else:
                                    print("không lấy được video")
                                    time_out.sleep(0.2)
                                    continue
                        messagebox.showinfo("Thông báo", "Thêm vào tập test thành công")
                    lbl_ID_nguoiMoi = Label(tk_themNguoi, text="Mã số", bd= 4, fg="white", font=("Times New Roman", 16), width= 10, bg="green")
                    lbl_ID_nguoiMoi.place(x= 15, y= 10)
                    lbl_NID_nguoiMoi = Entry(tk_themNguoi, bd=5,width=35, font=("Times New Roman", 14))
                    lbl_NID_nguoiMoi.place(x= 150, y= 10)
                    lbl_Ten_nguoiMoi = Label(tk_themNguoi, text="Họ tên", bd=4, fg="white", font=("Times New Roman", 16), width= 10, bg="green")
                    lbl_Ten_nguoiMoi.place(x= 15, y= 45)
                    lbl_T_nguoiMoi = Entry(tk_themNguoi, width=35, bd=5,font=("Times New Roman", 14))
                    lbl_T_nguoiMoi.place(x= 150, y= 45)
                    btn_themNguoi = Button(tk_themNguoi, text="Thêm người", font=("Times New Roman", 14), fg="white", bg="green",
                       width=15, height=1, command=btn_themNguoi)
                    btn_themNguoi.place(x= 100, y= 90)
                    btn_them_data_test = Button(tk_themNguoi, text="Thêm vào tập test", font=("Times New Roman", 14), fg="white", bg="green",
                       width=15, height=1, command=btn_them_data_test)
                    btn_them_data_test.place(x= 300, y=90)
                #space+tab => lùi vào 1 space còn shift+tab ngược lại
                def btn_danhsachNguoi():
                    rows = sql_DB.ds_sql_Labelface()
                    tk_ds = Tk()
                    tk_ds.title("Danh sách nhân viên")
                    tk_ds.geometry("550x550")
                    tk_ds.resizable(False,False)
                    tk_ds.configure(bg="CornflowerBlue")
                    lbl_title_ds = Label(tk_ds, text = "DANH SÁCH NHÂN VIÊN CÔNG TY", font = ("Times New Roman", 18),fg="green")
                    lbl_title_ds.place(x=100, y =10)
                    entry_1 = Label(tk_ds, text='',font = ("Times New Roman", 14))
                    entry_1.place(x=10,y =60)
                    entry_2 = Label(tk_ds, text='',font = ("Times New Roman", 14))
                    entry_2.place(x=80, y =60)

                    frm = Frame(tk_ds)
                    frm.pack(side = tkinter.LEFT, padx=50)
                    tv = ttk.Treeview(frm, columns = (1,2), show ="headings", height = "15", padding="Centimeters")
                    tv.pack(side ='right')
                    verscrlbar = ttk.Scrollbar(tk_ds, orient ="vertical", command = tv.yview)
                    verscrlbar.pack(side ='right', fill ='x') 
                    tv.configure(xscrollcommand = verscrlbar.set)
                    tv.heading(1, text = "Mã số nhân viên")
                    tv.heading(2, text = "Họ và tên")
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
                            sql_DB.del_labelface(id_f)
                            Delete_file(path, id_f).delete()
                            path_xoaNV = 'data_sosanh'
                            Delete_file(path_xoaNV, id_f).delete()                                   
                            messagebox.showinfo("Thông báo", "Xóa thành công")
                        def btn_xemAnh():
                            path1 = 'data_sosanh'
                            Xem_Image(path1, int(dv[0])).Xem()
                        btn_xemAnh= Button(tk_ds, text="Xem ảnh", font=("Times New Roman", 14), fg="white", bg="green",
                                        width=10, height=1, command=btn_xemAnh)
                        btn_xemAnh.place(x=300, y=60)
                        btn_recog= Button(tk_ds, text="Xóa", font=("Times New Roman", 14), fg="white", bg="green",
                                        width=10, height=1, command=btn_xoa)
                        btn_recog.place(x=420, y=60)
                    
                    tv.bind('<Button-1>', selectItem)
                
                def btn_diemdanhrealtime():
                    image_dd = 0
                    img_unknow = 0
                    global img
                    try:
                        while True:
                            if((last_ret is not None) and (latest_frame is not None)):
                                img = latest_frame.copy()                            
                            else:
                                print("không lấy được video")
                                time_out.sleep(0.2)
                                continue
                            gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                            gray = cv2.fastNlMeansDenoising(gray,None,4,5,11)
                            faces=detector.detectMultiScale(gray,1.3,5)
                            Ngay, Gio,start_dd_sang, end_dd_sang,start_dd_chieu,end_dd_chieu = Ngay_today.return_Ngay()
                            gio_to_excel,gio_end_to_excel = Ngay_today.gioToExcel()
                            info_tt = sql_DB.sql_ttdiemdanh_curdate()
                            ids = []
                            for i in info_tt:
                                ids.append(i[0])
                            for(x,y,w,h) in faces:
                                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),1)
                                id,conf=recognizer.predict(gray[y:y+h,x:x+w])
                                print("He so confident: ",round(conf,2))
                                profile = get_DB_image.getProfile(id)
                                Id="Uknown"
                                conf = round(100*(1-(conf/300)),2)
                                print("Độ chính xác (%): ",conf)
                                if(conf > 70):     
                                    cv2.putText(img, str(conf) + "% : " + str(profile[1]), (x+10,y-20), fontface, fontscale, fontcolor ,2)  
                                    dem = 0
                                    if((Gio > start_dd_sang and Gio < end_dd_sang) or (Gio > start_dd_chieu and Gio < end_dd_chieu)):
                                        print("profile ID: ",profile[0])
                                        for n in ids:
                                            if(int(n) == int(profile[0])):
                                                dem=dem+1
                                        if(dem < 1):
                                            print("Danh sách ID đã điểm danh: ",ids)
                                            image_dd=image_dd+1        
                                            img_cv = cv2.cvtColor(gray[y:y+h,x:x+w], cv2.COLOR_GRAY2RGB)
                                            cv2.imwrite("data_hinh_diemdanh/"+str(profile[1])+'.'+str(profile[0]) +'.'+ str(image_dd) + ".jpg", img_cv)
                                            path2 = 'data_sosanh'
                                            imagePaths=[os.path.join(path2,f) for f in os.listdir(path2)] 
                                            for imagePath in imagePaths:
                                                ID_ss=int(os.path.split(imagePath)[-1].split('.')[1])
                                                hashs = imagehash.average_hash(Image.open("data_hinh_diemdanh/"+str(profile[1])+'.'+str(profile[0])+'.'+str(image_dd)+".jpg"))
                                                otherhash = imagehash.average_hash(Image.open(imagePath))
                                                c = hashs - otherhash
                                                print("gia tri so sánh 2 bức ảnh: ",c)
                                                if(c < 24 and (ID_ss == int(profile[0]))):
                                                    print("Điểm danh đúng rồi")
                                                    sql_DB.insert_ttdiemdanh(profile[0],profile[1],Ngay,Gio)
                                                    #Xóa ảnh cũ cùng ID để thêm ảnh mới vào
                                                    path2 = 'data_diemdanh_dung'
                                                    Delete_file(path2, int(profile[0])).delete()
                                                    cv2.imwrite("data_diemdanh_dung/"+str(profile[1])+'.'+str(profile[0]) +'.'+ str(image_dd) + ".jpg", img_cv)
                                                elif(c > 24 and ID_ss!=int(profile[0])):
                                                    print("Điểm danh sai rồi: ", profile[1])
                                                    cv2.imwrite("data_diemdanh_sai/"+str(profile[1])+'.'+str(profile[0]) +'.'+ str(image_dd) + ".jpg", img_cv)
                                    # else:
                                    #     messagebox.showinfo('Thông báo', "Không nằm trong khung giờ điểm danh")
                                else: 
                                    img_unknow = img_unknow+1
                                    cv2.putText(img, "Name: "+ str(Id),(x-30,y-20), fontface, fontscale, fontcolor ,2)
                                    cv2.imwrite("data_hinh_unknown/"+str(Id)+'.' + str(img_unknow) + ".jpg", img)
                                img = cv2.resize(img, (780,480))
                                cv2.imshow('Frame',img) 
                            if(Gio>gio_to_excel and Gio<gio_end_to_excel):
                                msnv, hotennv, list_day, list_gio = sql_DB.ttdiemdanhToExcel()
                                file_name = 'DS_save_auto.xls'
                                Export.Excel(msnv,hotennv,list_day,list_gio,file_name)
                            k = cv2.waitKey(30)
                            if k == 27:
                                break
                            elif k ==-1:
                                continue   
                    except:
                        messagebox.showinfo("Thông báo", "Vui lòng trainning trước!")
                def btn_dsdiemdanh():
                    Tim_ngay = str(Entry_dsdiemdanh.get())
                    global x
                    x = NgayTim.format_ngay(Tim_ngay)
                    rows_ds = sql_DB.sql_ttdiemdanh_theoNgay(x)
                    tk_ds = Tk()
                    tk_ds.title("Danh sách điểm danh")
                    tk_ds.geometry("950x550")
                    tk_ds.resizable(False,False)
                    tk_ds.configure(bg="CornflowerBlue")
                    lbl_title_ds = Label(tk_ds, text = "DANH SÁCH ĐIỂM DANH NGAY "+str(x), font = ("Times New Roman", 18),fg="green")
                    lbl_title_ds.place(x=200, y =10)
                    entry_1 = Label(tk_ds, text='',font = ("Times New Roman", 14))
                    entry_1.place(x=10,y =60)
                    entry_2 = Label(tk_ds, text='',font = ("Times New Roman", 14))
                    entry_2.place(x=80, y =60)
                    entry_3 = Label(tk_ds, text='',font = ("Times New Roman", 14))
                    entry_3.place(x=300, y =60)
                    entry_4 = Label(tk_ds, text='', font = ("Times New Roman", 14))
                    entry_4.place(x=500, y =60)

                    frm = Frame(tk_ds)
                    frm.pack(side = tkinter.LEFT, padx=50)
                    tv = ttk.Treeview(frm, columns = (1,2,3,4), show ="headings", height = "15", padding="Centimeters")
                    tv.pack(side ='right')
                    verscrlbar = ttk.Scrollbar(tk_ds, orient ="vertical", command = tv.yview)
                    verscrlbar.pack(side ='right', fill ='x') 
                    tv.configure(xscrollcommand = verscrlbar.set)
                    tv.heading(1, text = "Mã số nhân viên")
                    tv.heading(2, text = "Họ và tên")
                    tv.heading(3, text = "Ngày điểm danh")
                    tv.heading(4, text = "Giờ điểm danh")
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
                            sql_DB.del_ttdiemdanh(id_f,gio_d)
                            messagebox.showinfo("Thông báo", "Xóa thành công")
                        def btn_xemAnh_dd():
                            path2 = 'data_diemdanh_dung'
                            Xem_Image(path2,int(dv[0])).Xem()

                        btn_xemAnh_dd= Button(tk_ds, text="Xem ảnh", font=("Times New Roman", 14), fg="white", bg="green",
                                        width=10, height=1, command=btn_xemAnh_dd)
                        btn_xemAnh_dd.place(x=650, y=60)
                        btn_recog_dd= Button(tk_ds, text="Xóa", font=("Times New Roman", 14), fg="white", bg="green",
                                        width=10, height=1, command=btn_xoa_dd)
                        btn_recog_dd.place(x=770, y=60)
                    def btn_thongke():
                        arr_lb, arr_tt, arr_chuadd = sql_DB.sql_thongke(x)
                        tk_tk = Tk()
                        tk_tk.title("Danh sách nhân viên chưa điểm danh")
                        tk_tk.geometry("600x550")
                        tk_tk.resizable(False,False)
                        tk_tk.configure(bg="CornflowerBlue")
                        lbl_title_ds_ch = Label(tk_tk, text = "DANH SÁCH NHÂN VIÊN CHƯA ĐIỂM DANH", font = ("Times New Roman", 18),fg="green")
                        lbl_title_ds_ch.place(x=50, y =10)

                        frm1 = Frame(tk_tk)
                        frm1.pack(side = tkinter.LEFT, padx=30)
                        tv1 = ttk.Treeview(frm1, columns = (1,2), show ="headings", height = "15", padding="Centimeters")
                        tv1.pack(side ='right')
                        verscrlbar1 = ttk.Scrollbar(tk_tk, orient ="vertical", command = tv1.yview)
                        verscrlbar1.pack(side ='right', fill ='x') 
                        tv1.configure(xscrollcommand = verscrlbar1.set)
                        tv1.heading(1, text = "Mã số nhân viên")
                        tv1.heading(2, text = "Họ và tên")
                        
                        lbl_tk = Label(tk_tk, text='Chưa điểm danh: ', font=("Times New Roman", 16), fg="red")
                        lbl_tk.place(x=100,y=60)
                        lbl_tk_va = Label(tk_tk, text=' ', font=("Times New Roman", 16), fg="red")
                        lbl_tk_va.place(x=300,y=60)
                        lbl_tk_roi = Label(tk_tk, text='Điểm danh rồi: ', font=("Times New Roman", 16), fg="red")
                        lbl_tk_roi.place(x=400,y=60)
                        lbl_tk_vaRoi = Label(tk_tk, text=' ', font=("Times New Roman", 16), fg="red")
                        lbl_tk_vaRoi.place(x=550,y=60)
                        if(len(arr_tt)==0):
                            for y in arr_lb:
                                tv1.insert('','end',values=(y[0],y[1]))
                            lbl_tk_va.configure(text = len(arr_lb))
                            lbl_tk_vaRoi.configure(text = len(arr_tt))
                        elif(len(arr_tt)==len(arr_lb)):
                            for i in arr_chuadd:
                                tv1.insert('','end',values="")
                            lbl_tk_va.configure(text = 0)
                            lbl_tk_vaRoi.configure(text = len(arr_tt))
                        else:
                            for i in arr_chuadd:
                                tv1.insert('','end',values=(i[0],i[1]))
                            lbl_tk_va.configure(text = len(arr_chuadd))
                            lbl_tk_vaRoi.configure(text = len(arr_tt))

                    btn_thongke= Button(tk_ds, text="Thống kê", font=("Times New Roman", 14), fg="white", bg="green",
                                        width=10, height=1, command=btn_thongke)
                    btn_thongke.place(x=350, y=480)
                    
                    tv.bind('<Button-1>', selectItem)

                def btn_ddhomnay():
                    rows_hn = sql_DB.sql_ttdiemdanh_curdate()
                    tk_hn = Tk()
                    tk_hn.title("Danh sách điểm danh hôm nay")
                    tk_hn.geometry("950x550")
                    tk_hn.resizable(False,False)
                    tk_hn.configure(bg="CornflowerBlue")
                    lbl_title_dshn = Label(tk_hn, text = "DANH SÁCH ĐIỂM DANH NGAY HÔM NAY", font = ("Times New Roman", 18),fg="green")
                    lbl_title_dshn.place(x=200, y =10)
                    entry_1hn = Label(tk_hn, text='',font = ("Times New Roman", 14))
                    entry_1hn.place(x=10,y =60)
                    entry_2hn = Label(tk_hn, text='',font = ("Times New Roman", 14))
                    entry_2hn.place(x=80, y =60)
                    entry_3hn = Label(tk_hn, text='',font = ("Times New Roman", 14))
                    entry_3hn.place(x=300, y =60)
                    entry_4hn = Label(tk_hn, text='', font = ("Times New Roman", 14))
                    entry_4hn.place(x=500, y =60)

                    frmhn = Frame(tk_hn)
                    frmhn.pack(side = tkinter.LEFT, padx=50)
                    tvhn = ttk.Treeview(frmhn, columns = (1,2,3,4), show ="headings", height = "15", padding="Centimeters")
                    tvhn.pack(side ='right')
                    verscrlbarhn = ttk.Scrollbar(tk_hn, orient ="vertical", command = tvhn.yview)
                    verscrlbarhn.pack(side ='right', fill ='x') 
                    tvhn.configure(xscrollcommand = verscrlbarhn.set)
                    tvhn.heading(1, text = "Mã số nhân viên")
                    tvhn.heading(2, text = "Họ và tên")
                    tvhn.heading(3, text = "Ngày điểm danh")
                    tvhn.heading(4, text = "Giờ điểm danh")
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
                            sql_DB.del_ttdiemdanh(id_f,gio_d)
                            path2 = 'data_diemdanh_dung'
                            Delete_file(path2, int(dv[0])).delete()
                            messagebox.showinfo("Thông báo", "Xóa thành công")
                        def btn_xemAnh_ddhn():
                            path2 = 'data_diemdanh_dung'
                            Xem_Image(path2, int(dv[0])).Xem()

                        btn_xemAnh_ddhn= Button(tk_hn, text="Xem ảnh", font=("Times New Roman", 14), fg="white", bg="green",
                                        width=10, height=1, command=btn_xemAnh_ddhn)
                        btn_xemAnh_ddhn.place(x=650, y=60)
                        btn_recog_ddhn= Button(tk_hn, text="Xóa", font=("Times New Roman", 14), fg="white", bg="green",
                                        width=10, height=1, command=btn_xoa_ddhn)
                        btn_recog_ddhn.place(x=770, y=60)
                    def btn_ExToExcel():
                        msnv, hotennv, list_day, list_gio = sql_DB.ttdiemdanhToExcel()
                        file_name = 'DShomNay.xls'
                        Export.Excel(msnv,hotennv,list_day,list_gio,file_name)
                        messagebox.showinfo("TB","Export đến file exel thành công")

                    btn_ExToExcel= Button(tk_hn, text="Export to excel", font=("Times New Roman", 14), fg="white", bg="green",
                                        width=15, height=1, command=btn_ExToExcel)
                    btn_ExToExcel.place(x=350, y=480)
                    
                    tvhn.bind('<Button-1>', selectItem)
                
                def btn_doiAdmin():
                    tk_doiPass = Tk()
                    tk_doiPass.geometry("550x150")
                    tk_doiPass.resizable(False,False)
                    tk_doiPass.configure(bg='CornflowerBlue')

                    def btn_newPass():
                        new_username = lbl_NID_user.get()
                        new_pass = lbl_T_pass.get()
                        if((new_username == '' and new_pass=='') or new_username == '' or new_pass==''):
                            messagebox.showinfo("Thông báo", "Vui lòng nhập thông tin đầy đủ")
                        elif(len(new_pass) < 6 and len(new_pass)>10):
                            messagebox.showinfo("Thông báo", "Pass phải có độ dài từ 6 đến 10 ký tự")
                        else:
                            md = hashlib.md5()
                            md.update(new_pass.encode())
                            new_pass = md.hexdigest()
                            sql_DB.update_Admin(new_username, new_pass)
                            messagebox.showinfo("Thông báo", "Thay đổi thành công")
                            tk_doiPass.destroy()

                    lbl_new_username = Label(tk_doiPass, text="UserName new", bd=4, fg="white", font=("Times New Roman", 16), width= 10, bg="green")
                    lbl_new_username.place(x= 15, y= 10)
                    lbl_NID_user = Entry(tk_doiPass, width=35, bd=5, font=("Times New Roman", 14))
                    lbl_NID_user.place(x= 200, y= 10)
                    lbl_pass_new = Label(tk_doiPass, text="PassWord new", bd=4, fg="white", font=("Times New Roman", 16), width= 10, bg="green")
                    lbl_pass_new.place(x= 15, y= 50)
                    lbl_T_pass = Entry(tk_doiPass, width=35, bd=5, font=("Times New Roman", 14), show='*')
                    lbl_T_pass.place(x= 200, y= 50)
    
                    btn_newPass = Button(tk_doiPass, text="Đổi Admin", font=("Times New Roman", 14), fg="white", bg="red",
                        width=15, height=1, command=btn_newPass)
                    btn_newPass.place(x= 250, y= 90)

                def btn_ddhinhanh():
                    image1 = latest_frame.copy()
                    cv2.imwrite('anhchupnhandang.jpg', image1)
                    img_nd = ImageTk.PhotoImage(Image.open("anhchupnhandang.jpg").resize((620, 480),Image.ANTIALIAS))
                    panel = Label(tk_main, image = img_nd)
                    panel.image = img_nd
                    panel.place(x = 700, y = 10)
                    img = cv2.imread("anhchupnhandang.jpg")

                    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    gray = cv2.fastNlMeansDenoising(gray,None,4,5,11)
                    faces=detector.detectMultiScale(gray,1.3,5)
                    global ID, Name, Ngay,Gio
                    Ngay, Gio,start_dd_sang, end_dd_sang,start_dd_chieu,end_dd_chieu = Ngay_today.return_Ngay()                   
                    info_tt = sql_DB.sql_ttdiemdanh_curdate()
                    ids = []
                    for i in info_tt:
                        ids.append(i[0])
                    image_dd = 0   
                    try:
                        for(x,y,w,h) in faces:
                            id,conf=recognizer.predict(gray[y:y+h,x:x+w])
                            profile = get_DB_image.getProfile(id)
                            if(conf<90):    
                                dem = 0
                                if((Gio > start_dd_sang and Gio < end_dd_sang) or (Gio > start_dd_chieu and Gio < end_dd_chieu)):
                                    for n in ids:
                                        if(int(n) == int(profile[0])):
                                            dem=dem+1
                                    if(dem < 1):
                                        image_dd=image_dd+1
                                        img_cv = cv2.cvtColor(gray[y:y+h,x:x+w], cv2.COLOR_GRAY2RGB)
                                        cv2.imwrite("data_hinh_diemdanh/anhchup"+'.'+str(profile[0]) +'.'+ str(image_dd) + ".jpg", img_cv)
                                        path2 = 'data_sosanh'
                                        imagePaths=[os.path.join(path2,f) for f in os.listdir(path2)] 
                                        for imagePath in imagePaths:
                                            ID_ss=int(os.path.split(imagePath)[-1].split('.')[1])
                                            hashs = imagehash.average_hash(Image.open("data_hinh_diemdanh/anhchup"+'.'+str(profile[0])+'.'+str(image_dd)+".jpg"))
                                            otherhash = imagehash.average_hash(Image.open(imagePath))
                                            c = hashs - otherhash
                                            if(c<22 and (ID_ss == int(profile[0]))):
                                                sql_DB.insert_ttdiemdanh(profile[0],profile[1],Ngay,Gio)
                                                cv2.imwrite("data_diemdanh_dung/"+str(profile[1])+'.'+str(profile[0]) +'.'+ str(image_dd) + ".jpg", img_cv)
                                                messagebox.showinfo("Thông báo", "Điểm danh đúng rồi")
                                            else:
                                                messagebox.showinfo("Thông báo", "Điểm danh sai")
                                    else:
                                        messagebox.showinfo("Thông báo", "Đã điểm danh rồi")
                                else:
                                    messagebox.showinfo("Thông báo", "Không nằm trong khung giờ điểm danh")
                                name = str(profile[1])
                                ids = str(profile[0])
                            else:
                                name = 'unknow'
                                ids = 'unknow'
                    
                        b = "Họ tên nv : " + name
                        a = "Mã số nv : " + ids
                        lbl_showTT_ten.configure(text = b)
                        lbl_showTT_Ms.configure(text = a)
                    except:
                        messagebox.showinfo("Thông báo", "Vui lòng trainning trước!")
                def btn_test_acc():
                    path_test = 'data_test1'
                    id_test, faces = get_DB_image.getImagesAndLabels(path_test)  
                    arr_pre_test = []
                    for img in faces:
                        gray = cv2.fastNlMeansDenoising(img,None,4,5,11)
                        id_pre_test,conf=recognizer.predict(gray)
                        arr_pre_test.append(id_pre_test)
                    print(np.array(id_test))
                    print(np.array(arr_pre_test))
                    acc = Accuracy.acc(np.array(id_test),np.array(arr_pre_test))
                    messagebox.showinfo("Thông báo","Độ chính xác của tập test là: "+str(acc)+"%")

                btn_themNguoiMoi= Button(tk_main, text="Thêm người mới", font=("Times New Roman", 14), fg="white", bg="green",
                width=18, height=1, command=btn_themNguoiMoi)
                btn_themNguoiMoi.place(x=10, y=500)
                btn_danhsachNguoi= Button(tk_main, text="Danh sách nhân viên", font=("Times New Roman", 14), fg="white", bg="green",
                width=18, height=1, command=btn_danhsachNguoi)
                btn_danhsachNguoi.place(x=10, y=550)
                btn_ddhomnay= Button(tk_main, text="Điểm danh hôm nay", font=("Times New Roman", 14), fg="white", bg="green",
                width=18, height=1, command=btn_ddhomnay)
                btn_ddhomnay.place(x=250, y=500)
                btn_test_acc= Button(tk_main, text="Accuracy (opencv)", font=("Times New Roman", 14), fg="white", bg="green",
                  width=15, height=1, command=btn_test_acc)
                btn_test_acc.place(x=490, y=500)
                btn_train_data= Button(tk_main, text="Trainning data", font=("Times New Roman", 14), fg="white", bg="green",
                  width=15, height=1, command=btn_train_data)
                btn_train_data.place(x=490, y=550)
                btn_doiPass= Button(tk_main, text="Đổi mật khẩu", font=("Times New Roman", 14), fg="white", bg="green",
                width=18, height=1, command=btn_doiAdmin)
                btn_doiPass.place(x=250, y=550)
                btn_ddhinhanh= Button(tk_main, text="Chụp hình điểm danh", font=("Times New Roman", 14), fg="white", bg="green",
                width=18, height=1, command=btn_ddhinhanh)
                btn_ddhinhanh.place(x=250, y=600)
                btn_diemdanhrealtime= Button(tk_main, text="Điểm danh real time", font=("Times New Roman", 14), fg="white", bg="green",
                width=18, height=1, command=btn_diemdanhrealtime)
                btn_diemdanhrealtime.place(x=10, y=600)
                btn_dsdiemdanh= Button(tk_main, text="Danh sách theo ngày", font=("Times New Roman", 14), fg="white", bg="green",
                width=18, height=1, command=btn_dsdiemdanh)
                btn_dsdiemdanh.place(x=10, y=650)
                Entry_dsdiemdanh = Entry(tk_main, width=20, bd=5,font=("Times New Roman", 14))
                Entry_dsdiemdanh.place(x= 250, y=650)
                lbl_showTT_ten = Label(tk_main, text="", font=("Times New Roman", 16), fg="red")
                lbl_showTT_ten.place(x=1050, y=510)
                lbl_showTT_Ms = Label(tk_main, text="", font=("Times New Roman", 16), fg="red")
                lbl_showTT_Ms.place(x=1050, y=550)
            
            lbl_title = Label(tk_cam, text="Nhập path video or stream camera (0 or ' ' camera máy tính)", font=("Times New Roman", 18), fg="green", bg="white")
            lbl_title.place(x=30, y=10)                
            btn_ChonCamera = Button(tk_cam, text="Chọn thiết bị video/stream", font=("Times New Roman",14),fg="white", bg="green",
                        width= 20, height=1, bd =2, command=btn_ChonCamera)  
            btn_ChonCamera.place(x=10, y =60)
            Entry_camera = Entry(tk_cam, width=40, bd=5,font=("Times New Roman",14))
            Entry_camera.place(x=250,y=60)         
lbl_title = Label(root, text="ỨNG DỤNG ĐIỂM DANH VỚI CÔNG NGHỆ NHẬN DẠNG KHUÔN MẶT", font=("Times New Roman", 20), fg="red")
lbl_title.place(x=10, y=10)
lbl_username = Label(root, text="UserName: ", width = 10, bd=4, font=("Times New Roman", 16), fg="green")
lbl_username.place(x=160, y=200)
Ent_username = Entry(root, width=50, bd=5, font=("Times New Roman", 14))
Ent_username.place(x=300,y=200)
lbl_password = Label(root, text="PassWord: ", width = 10, bd=4, font=("Times New Roman", 16), fg="green")
lbl_password.place(x=160, y=250)
Ent_password = Entry(root, width=50, bd=5,font=("Times New Roman", 14), show='*')
Ent_password.place(x=300,y=250)
btn_dangnhap = Button(root, text="Đăng Nhập", font=("Times New Roman", 14), fg="white", bg="red",
    width=20, height=1, bd=4, command=FC_DangNhap)
btn_dangnhap.place(x=340, y=400)
root.mainloop()