from tkinter import messagebox
from datetime import datetime, date, time

class SearchDate:
    @classmethod
    def formatDate(cls, searchkey):
        format = "%Y-%m-%d"
        isCheck = True
        try:
            isCheck = bool(datetime.strptime(searchkey, format))
        except:
            isCheck = False
        if(isCheck == False):
            messagebox.showinfo("message", "Enter date by format: 2023-03-18")
        return searchkey

class CurrentDate:
    @staticmethod
    def dateHourTimeAttendance():
        current = datetime.now()
        today = date.today()
        currentTime = current.time()
        startMorning = time(hour = 7, minute = 30, second = 1)
        endMorning = time(hour = 10, minute = 45, second = 56)
        startAfternoon = time(hour = 13, minute = 25, second = 56)
        endAfternoon = time(hour = 22, minute = 50, second = 56)
        return today, currentTime, startMorning, endMorning, startAfternoon, endAfternoon

    @staticmethod
    def setupHourAutoExport():
        startExport = time(hour = 13, minute = 40, second = 10)
        endExport = time(hour = 17, minute = 40, second = 10)
        return startExport, endExport
