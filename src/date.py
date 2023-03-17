from tkinter import messagebox
from datetime import datetime, time

class SearchDate:
    @classmethod
    def formatDate(cls, searchkey):
        format = "%d-%m-%Y"
        isCheck = True
        try:
            isCheck = bool(datetime.strptime(searchkey, format))
        except ValueError:
            isCheck = False
        if(isCheck == False):
            messagebox.showinfo("message", "Enter date by format: 20-09-2020")
        return searchkey

class CurrentDate:
    @staticmethod
    def dateHourTimeAttendance():
        current = datetime.now()
        date = date.today()
        time = current.time()
        startMorning = time(hour = 7, minute = 30, second = 1)
        endMorning = time(hour = 8, minute = 45, second = 56)
        startAfternoon = time(hour = 4, minute = 25, second = 56)
        endAfternoon= time(hour = 5, minute = 50, second = 56)
        return date, time, startMorning, endMorning, startAfternoon, endAfternoon

    @staticmethod
    def setupHourAutoExport():
        startExport = time(hour = 13, minute = 40, second = 10)
        endExport = time(hour = 17, minute = 40, second = 10)
        return startExport, endExport
