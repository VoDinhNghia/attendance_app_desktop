import pymysql

class ConnectDb:
    @staticmethod
    def connectMysql():
        connect = pymysql.connect(host='localhost', user='root', passwd="root", db='attendance')
        cursor = connect.cursor()
        return connect, cursor

class QuerySql:
    @staticmethod
    def login():
        cur = ConnectDb.connectMysql()[1]
        sql = "SELECT * from users"
        cur.execute(sql)
        return cur.fetchall() 

    @classmethod
    def update_Admin(cls, new_username, new_pass):
        conn, cur = ConnectDb.connectMysql()
        sql = "update users set username = %s, password = %s"
        cur.execute(sql,(new_username,new_pass))
        conn.commit()
    
    @classmethod
    def sql_Labelface(cls, Id):
        conn,cur = ConnectDb.connectMysql()
        cur.execute("select * from label_face where ID=%s", Id)
        conn.commit()
        arr_check_id = cur.fetchall()
        return arr_check_id

    @staticmethod
    def ds_sql_Labelface():
        conn,cur = ConnectDb.connectMysql()
        cur.execute("select * from label_face")
        conn.commit()
        rows = cur.fetchall()
        return rows

    @staticmethod
    def sql_ttdiemdanh_curdate():
        conn,cur = ConnectDb.connectMysql()
        query_tt = "select * from history_attendance where date= curdate()"
        cur.execute(query_tt)
        conn.commit()
        info_tt = cur.fetchall()
        return info_tt

    @classmethod
    def insert_ttdiemdanh(cls, msnv, hoten, ngay, gio):
        conn,cur = ConnectDb.connectMysql()
        sql_tt = "INSERT INTO history_attendance(ID,name,date,time) Values(%s,%s,%s,%s)"
        cur.execute(sql_tt,(msnv,hoten,ngay,gio))
        conn.commit()
    
    @classmethod
    def insert_labelface(cls, Id, Name):
        conn, cur = ConnectDb.connectMysql()
        cmd="INSERT INTO label_face(ID,name) Values(%s,%s)"
        Id = str(Id)
        Name = str(Name)
        cur.execute(cmd,(Id,Name))
        conn.commit()

    @staticmethod
    def ttdiemdanhToExcel():
        conn,cur = ConnectDb.connectMysql()
        cur.execute("select * from history_attendance where date = curdate()")
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
        conn, cur = ConnectDb.connectMysql()
        sql = "select * from history_attendance where date = %s"
        cur.execute(sql, str(x))
        conn.commit()
        rows_ds = cur.fetchall()
        return rows_ds

    @classmethod
    def sql_thongke(cls, x):
        conn, cur = ConnectDb.connectMysql()
        sql_lb = "SELECT * FROM label_face"
        cur.execute(sql_lb)
        arr_lb = cur.fetchall()
        sql_tk = "SELECT ID, Name FROM history_attendance WHERE date= %s"
        cur.execute(sql_tk,str(x))
        conn.commit()
        arr_tt = cur.fetchall()
        arr_chuadd = []
        for i in range(len(arr_lb)):
            for j in arr_tt:
                if(j[0] != arr_lb[i][0]):
                    arr_chuadd.append(arr_lb[i])
                    break
        return arr_lb, arr_tt, arr_chuadd

    @classmethod
    def del_ttdiemdanh(cls, msnv, gio):
        conn, cur = ConnectDb.connectMysql()
        sql_del = "DELETE FROM history_attendance WHERE ID = %s AND time = %s"
        cur.execute(sql_del,(str(msnv),str(gio)))
        conn.commit()

    @classmethod
    def del_labelface(cls, Id):
        conn, cur = ConnectDb.connectMysql()
        sql_del = "DELETE FROM label_face WHERE ID = %s"
        cur.execute(sql_del,str(Id))
        conn.commit()