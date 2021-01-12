from tkinter import messagebox
from datetime import datetime, date, time
import numpy as np 

class NgayTim:
    """
    Class handling string parameter day entering for search list attendance.\n
    Class xử lý chuỗi ngày được nhập vào để tìm kiếm danh sách theo ngày
    """
    @classmethod
    def format_ngay(cls, Tim_ngay):
        """
        Return day after string parameter day entering handled.\n
        Trả về ngày sau khi đã được xử lý chuỗi nhập vào.
        """
        ds_dMy = Tim_ngay.split()
        global x
        if(len(ds_dMy)==1  or len(ds_dMy)==0):
            if(len(Tim_ngay)<6 or len(Tim_ngay)>10):
                messagebox.showinfo("Thông báo", "Nhập ngày theo dạng:\n 20/09/2020 or 1-9-2020 or 20 9 2020")
            else:
                if((Tim_ngay[1]=='-' or Tim_ngay[2]=='-') and (Tim_ngay[3]=='-' or Tim_ngay[4]=='-' or Tim_ngay[5]=='-')):
                    n = Tim_ngay.split('-')
                    n = np.array(n,int)
                    a = int(n[2])
                    b = int(n[1])
                    c = int(n[0])
                    x = date(a,b,c)
                elif((Tim_ngay[1]=='/' or Tim_ngay[2]=='/') and (Tim_ngay[3]=='/' or Tim_ngay[4]=='/' or Tim_ngay[5]=='/')):
                    n = Tim_ngay.split('/')
                    n = np.array(n,int)
                    a = int(n[2])
                    b = int(n[1])
                    c = int(n[0])
                    x = date(a,b,c)
                else:
                    messagebox.showinfo("Thông báo", "Nhập ngày theo dạng:\n 20/09/2020 or 1-9-2020 or 20 9 2020")
        
        else:
            if(len(ds_dMy)==2):
                messagebox.showinfo("Thông báo", "Nhập ngày theo dạng:\n 20/09/2020 or 1-9-2020 or 20 9 2020")
            else:
                n = np.array(ds_dMy,int)
                a = int(n[2])
                b = int(n[1])
                c = int(n[0])
                x = date(a,b,c)
        return x

class Ngay_today:
    """
    Class constain return day, hour curent and time about attendance on morning and afternon.\n
    Lớp chứa hàm trả về ngày giờ hiện tại và khoảng thời gian điểm danh vào buổi sáng và chiều
    """
    @staticmethod
    def return_Ngay():
        """
        Function return day, hour current and time about attendance.\n
        Hàm trả về ngày giờ hiện tại và khung giờ điểm danh sáng chiều.
        """
        time1 = datetime.now()
        #ngay1 = date.today()
        Ngay = date.today()
        Gio = time1.time()
        start_dd_sang = time(hour = 8, minute = 1, second = 1)
        end_dd_sang = time(hour = 8, minute = 45, second = 56)
        start_dd_chieu = time(hour = 5, minute = 25, second = 56)
        end_dd_chieu= time(hour = 5, minute = 50, second = 56)
        return Ngay, Gio, start_dd_sang, end_dd_sang, start_dd_chieu, end_dd_chieu

    @staticmethod
    def gioToExcel():
        """
        Return time about to save auto file excel.\n
        trả về khung giờ để tự động lưu vào file excel
        """
        gio_to_excel = time(hour = 13, minute = 40, second = 10)
        gio_end_to_excel = time(hour = 17, minute = 40, second = 10)
        return gio_to_excel,gio_end_to_excel
