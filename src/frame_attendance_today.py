import tkinter
from tkinter import*
from tkinter import ttk, messagebox
from connect_db import QuerySql
from view_image import ViewImage
from delete_file import DeleteFile
from view_image import ViewImage
from excel import Export

fontTypeApp = 'Times New Roman'
path = 'image_trainning_model'

class FrameAttendanceToday:
    def show():
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
                ViewImage(path2, int(dv[0])).view()

            btn_xemAnh_ddhn= Button(tk_hn, text='Xem ảnh', font=(fontTypeApp, 14), fg='white', bg='green',
                            width=10, height=1, command=btn_xemAnh_ddhn)
            btn_xemAnh_ddhn.place(x=650, y=60)
            btn_recog_ddhn= Button(tk_hn, text='Xóa', font=(fontTypeApp, 14), fg='white', bg='green',
                            width=10, height=1, command=btn_xoa_ddhn)
            btn_recog_ddhn.place(x=770, y=60)
        def btn_ExToExcel():
            msnv, hotennv, list_day, list_gio = QuerySql.exportHistoryAttendance()
            file_name = 'export_execl/attendance_today.xls'
            Export.excel(msnv,hotennv,list_day,list_gio,file_name)
            messagebox.showinfo('TB','Export đến file exel thành công')

        btn_ExToExcel= Button(tk_hn, text='Export to excel', font=(fontTypeApp, 14), fg='white', bg='green',
                            width=15, height=1, command=btn_ExToExcel)
        btn_ExToExcel.place(x=350, y=480)
        
        tvhn.bind('<Button-1>', selectItem)