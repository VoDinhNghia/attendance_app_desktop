import tkinter
from tkinter import*
from tkinter import ttk, messagebox
from connect_db import QuerySql
from delete_file import DeleteFile
from view_image import ViewImage

fontTypeApp = 'Times New Roman'
path = 'image_trainning_model'

class FrameDateUserList:
    def show():
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
                ViewImage(path1, int(dv[0])).view()
            btn_xemAnh= Button(tk_ds, text='Xem ảnh', font=(fontTypeApp, 14), fg='white', bg='green',
                            width=10, height=1, command=btn_xemAnh)
            btn_xemAnh.place(x=300, y=60)
            btn_recog= Button(tk_ds, text='Xóa', font=(fontTypeApp, 14), fg='white', bg='green',
                            width=10, height=1, command=btn_xoa)
            btn_recog.place(x=420, y=60)
        
        tv.bind('<Button-1>', selectItem)
