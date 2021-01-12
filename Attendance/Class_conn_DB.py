import pymysql

class connect_DB:
    """
    Class connect to database mysql through Apache Xampp.\n
    Database have three table such as: dangnhap, labelface , ttdiemdanh.
    """
    @staticmethod
    def con_mysql():
        conn = pymysql.connect(host='localhost', user='root', passwd="", db='diemdanh')
        cur = conn.cursor()
        return conn, cur

class sql_DB:
    """
    Class query from database diemdanh on mysql.
    """
    @staticmethod
    def table_DN():
        """
        Function query and return a list login information on table dangnhap.\n
        Hàm truy vấn và trả về danh sách thông tin đăng nhập ở table đăng nhập.
        """
        cur = connect_DB.con_mysql()[1]
        sql = "SELECT * from dangnhap"
        cur.execute(sql)
        return cur.fetchall() 

    @classmethod
    def update_Admin(cls, new_username, new_pass):
        """
        Function use to update table dangnhap.\n
        Hàm dùng để update table dangnhap
        """
        conn, cur = connect_DB.con_mysql()
        sql = "update dangnhap set UserName = %s, PassWord = %s"
        cur.execute(sql,(new_username,new_pass))
        conn.commit()
    
    @classmethod
    def sql_Labelface(cls, Id):
        """
        Function return a list information on table labelface with condition ID = Id.\n
        Hàm trả về danh sách thông tin trong bảng labelface với điều kiện ID=Id truyền vào.
        """
        conn,cur = connect_DB.con_mysql()
        cur.execute("select * from labelface where ID=%s", Id)
        conn.commit()
        arr_check_id = cur.fetchall()
        return arr_check_id

    @staticmethod
    def ds_sql_Labelface():
        """
        Function return a list information on table labelface.\n
        Hàm trả về danh sách thông tin trong bảng labelface.
        """
        conn,cur = connect_DB.con_mysql()
        cur.execute("select * from labelface")
        conn.commit()
        rows = cur.fetchall()
        return rows

    @staticmethod
    def sql_ttdiemdanh_curdate():
        """
        Function return a list current date attendance.\n
        Hàm trả về danh sách điểm danh ngày hiện tại
        """
        conn,cur = connect_DB.con_mysql()
        query_tt = "select * from ttdiemdanh where Ngay= curdate()"
        cur.execute(query_tt)
        conn.commit()
        info_tt = cur.fetchall()
        return info_tt

    @classmethod
    def insert_ttdiemdanh(cls, msnv, hoten, ngay, gio):
        """
        Function insert attendance information to on table ttdiemdanh.\n
        Hàm insert thông tin điểm danh vào table ttdiemdanh
        """
        conn,cur = connect_DB.con_mysql()
        sql_tt = "INSERT INTO ttdiemdanh(ID,Name,Ngay,Gio) Values(%s,%s,%s,%s)"
        cur.execute(sql_tt,(msnv,hoten,ngay,gio))
        conn.commit()
    
    @classmethod
    def insert_labelface(cls, Id, Name):
        """
        Insert addition new people to database (table labelface).\n
        Chèn thêm người mới vào database
        """
        conn, cur = connect_DB.con_mysql()
        cmd="INSERT INTO labelface(ID,Name) Values(%s,%s)"
        Id = str(Id)
        Name = str(Name)
        cur.execute(cmd,(Id,Name))
        conn.commit()

    @staticmethod
    def ttdiemdanhToExcel():
        """
        Return a list information current day attendance to export to excel.\n
        Trả về thông tin danh sách điểm danh ngày hôm nay để export đến excel
        """
        conn,cur = connect_DB.con_mysql()
        cur.execute("select * from ttdiemdanh where Ngay = curdate()")
        conn.commit()
        rows_auto= cur.fetchall()
        msnv = []
        hotennv = []
        list_day = []
        list_gio = []
        for i in rows_auto:
            msnv.append(i[0])
            hotennv.append(i[1])
            list_day.append(str(i[2]))
            list_gio.append(str(i[3]))
        
        return msnv, hotennv, list_day, list_gio

    @classmethod
    def sql_ttdiemdanh_theoNgay(cls, x):
        """
        Function query data on table ttdiemdanh with condition Ngay=x.\n
        Hàm truy vấn dữ liệu trong bảng ttdiemdanh với điều kiện Ngay= ngày truyền vào.
        """
        conn, cur = connect_DB.con_mysql()
        sql = "select * from ttdiemdanh where Ngay = %s"
        cur.execute(sql, str(x))
        conn.commit()
        rows_ds = cur.fetchall()
        return rows_ds

    @classmethod
    def sql_thongke(cls, x):
        """
        Function use to implement feature statistic with parameter such as day (x).\n
        Hàm dùng để thực hiện chức năng thống kê và tham số truyền vào là ngày
        """
        conn, cur = connect_DB.con_mysql()
        sql_lb = "SELECT * FROM labelface"
        cur.execute(sql_lb)
        arr_lb = cur.fetchall()
        #print(arr_lb)
        sql_tk = "SELECT ID, Name FROM ttdiemdanh WHERE Ngay= %s"
        cur.execute(sql_tk,str(x))
        conn.commit()
        arr_tt = cur.fetchall()
        #print(arr_tt)
        arr_chuadd = []
        for i in range(len(arr_lb)):
            for j in arr_tt:
                if(j[0] != arr_lb[i][0]):
                    arr_chuadd.append(arr_lb[i])
                    break
        return arr_lb, arr_tt, arr_chuadd

    @classmethod
    def del_ttdiemdanh(cls, msnv, gio):
        """
        Function delete a line on table ttdiemdanh with two parameter such as msnv and hour attendance.\n
        Hàm xóa một dòng trong table ttdiemdanh với 2 tham số truyền vào là msnv và gio điểm danh.
        """
        conn, cur = connect_DB.con_mysql()
        sql_del = "DELETE FROM ttdiemdanh WHERE ID = %s AND Gio = %s"
        cur.execute(sql_del,(str(msnv),str(gio)))
        conn.commit()

    @classmethod
    def del_labelface(cls, Id):
        """
        Function delete a line on table labelface with parameter such as msnv (ID).\n
        Hàm xóa một dòng trong table labelface với tham số truyền vào là msnv.
        """
        conn, cur = connect_DB.con_mysql()
        sql_del = "DELETE FROM labelface WHERE ID = %s"
        cur.execute(sql_del,str(Id))
        conn.commit()