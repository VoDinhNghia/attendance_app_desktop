import pymysql

class ConnectDb:
    @staticmethod
    def connectMysql():
        connect = pymysql.connect(host='localhost', user='root', passwd='root', db='attendance')
        cursor = connect.cursor()
        return connect, cursor

class QuerySql:
    @staticmethod
    def login():
        cursor = ConnectDb.connectMysql()[1]
        sql = 'select * from users'
        cursor.execute(sql)
        return cursor.fetchone()

    @classmethod
    def updateAdmin(cls, username, password):
        connect, cursor = ConnectDb.connectMysql()
        sql = 'update users set username = %s, password = %s'
        cursor.execute(sql, (username, password))
        connect.commit()
    
    @classmethod
    def selectLabelfaceById(cls, id):
        connect, cursor = ConnectDb.connectMysql()
        cursor.execute('select * from label_face where ID=%s', id)
        connect.commit()
        results = cursor.fetchall() # fetch one
        return results

    @staticmethod
    def fetchAllLabelface():
        connect, cursor = ConnectDb.connectMysql()
        cursor.execute('select * from label_face')
        connect.commit()
        rows = cursor.fetchall()
        return rows

    @staticmethod
    def fetchHistoryAttendanceByCurrentDate():
        connect, cursor = ConnectDb.connectMysql()
        query = 'select * from history_attendance where date= curdate()'
        cursor.execute(query)
        connect.commit()
        results = cursor.fetchall()
        return results

    @classmethod
    def insertHistoryAttendance(cls, numberId, name, date, time):
        connect, cursor = ConnectDb.connectMysql()
        insertHistory = 'insert into history_attendance(ID,name,date,time) Values(%s,%s,%s,%s)'
        cursor.execute(insertHistory, (numberId, name, date, time))
        connect.commit()
    
    @classmethod
    def insertLabelface(cls, id, name):
        connect, cursor = ConnectDb.connectMysql()
        insertLableFace = 'insert into label_face(ID,name) Values(%s,%s)'
        cursor.execute(insertLableFace, (str(id), str(name)))
        connect.commit()

    @staticmethod
    def exportHistoryAttendance():
        connect, cursor = ConnectDb.connectMysql()
        cursor.execute('select * from history_attendance where date = curdate()')
        connect.commit()
        allHistory = cursor.fetchall()
        numberIds = []
        names = []
        dateList = []
        timeList = []
        for i in allHistory:
            numberIds.append(i[0])
            names.append(i[1])
            dateList.append(str(i[2]))
            timeList.append(str(i[3]))
        
        return numberIds, names, dateList, timeList

    @classmethod
    def queryHistoryByDate(cls, date):
        connect, cursor = ConnectDb.connectMysql()
        queryHistory = 'select * from history_attendance where date = %s'
        cursor.execute(queryHistory, str(date))
        connect.commit()
        resultHistory = cursor.fetchall()
        return resultHistory

    @classmethod
    def statictisHistoryByDate(cls, date):
        lableLists = cls.fetchAllLabelface()
        attendanceList = cls.queryHistoryByDate(date)
        notYetAttendance = []
        for i in range(len(lableLists)):
            for j in attendanceList:
                if(j[0] != lableLists[i][0]):
                    notYetAttendance.append(lableLists[i])
                    break
        return lableLists, attendanceList, notYetAttendance

    @classmethod
    def deleteHistoryAttendance(cls, numberId, time):
        connect, cursor = ConnectDb.connectMysql()
        deleteHistory = 'delete from history_attendance where ID = %s AND time = %s'
        cursor.execute(deleteHistory, (str(numberId),str(time)))
        connect.commit()

    @classmethod
    def deleteLabelface(cls, id):
        connect, cursor = ConnectDb.connectMysql()
        deleteLable = 'delete from label_face where ID = %s'
        cursor.execute(deleteLable, str(id))
        connect.commit()