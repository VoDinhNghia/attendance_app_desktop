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
        resultsFetchData = QuerySql.fetchHistoryAttendanceByCurrentDate()
        attendanceTodayScreen = Tk()
        attendanceTodayScreen.title('List attendance today')
        attendanceTodayScreen.geometry('950x550')
        attendanceTodayScreen.resizable(False, False)
        attendanceTodayScreen.configure(bg ='CornflowerBlue')
        lableTitleAttendanceToday = Label(attendanceTodayScreen, text = 'View list attendance today', font = (fontTypeApp, 18),fg='green')
        lableTitleAttendanceToday.place(x = 200, y = 10)
        showNumberId = Label(attendanceTodayScreen, text = '',font = (fontTypeApp, 14))
        showNumberId.place(x = 10,y = 60)
        showName = Label(attendanceTodayScreen, text = '',font = (fontTypeApp, 14))
        showName.place(x = 80, y = 60)
        showDate = Label(attendanceTodayScreen, text = '',font = (fontTypeApp, 14))
        showDate.place(x = 300, y = 60)
        showTime = Label(attendanceTodayScreen, text = '', font = (fontTypeApp, 14))
        showTime.place(x = 500, y = 60)

        frameAttendanceToday = Frame(attendanceTodayScreen)
        frameAttendanceToday.pack(side = tkinter.LEFT, padx = 50)
        treeviewAttendanceToday = ttk.Treeview(frameAttendanceToday, columns = (1,2,3,4), show ='headings', height = '15', padding='Centimeters')
        treeviewAttendanceToday.pack(side = 'right')
        verscrlbarToday = ttk.Scrollbar(attendanceTodayScreen, orient = 'vertical', command = treeviewAttendanceToday.yview)
        verscrlbarToday.pack(side = 'right', fill = 'x') 
        treeviewAttendanceToday.configure(xscrollcommand = verscrlbarToday.set)
        treeviewAttendanceToday.heading(1, text = 'Number Id')
        treeviewAttendanceToday.heading(2, text = 'Name')
        treeviewAttendanceToday.heading(3, text = 'Date attendance')
        treeviewAttendanceToday.heading(4, text = 'Time attendance')
        for i in resultsFetchData:
            treeviewAttendanceToday.insert('', 'end', values = i)

        def selectItemAttendanceToday(event):
            pathViewToday = 'image_correct'
            cursorItem = treeviewAttendanceToday.focus()
            getValue = treeviewAttendanceToday.item(cursorItem)
            rowData = getValue['values']
            values = []
            for i in rowData:
                values.append(i)
            try:
                showNumberId.configure(text = values[0])
                showName.configure(text = values[1])
                showDate.configure(text =values[2])
                showTime.configure(text = values[3])
            except:
                print('error exception')
            def deleteRowAttendanceTodayFunc():
                try:
                    rowOnclick = treeviewAttendanceToday.selection()[0]
                    idOnclick = int(values[0])
                    timeOnclick = values[3]
                except:
                    print('error exception')
                treeviewAttendanceToday.delete(rowOnclick)
                QuerySql.deleteHistoryAttendance(idOnclick, timeOnclick)
                DeleteFile(pathViewToday, int(values[0])).delete()
                messagebox.showinfo('message', 'Delete row success.')
            def viewImageAttendanceTodayFunc():
                ViewImage(pathViewToday, int(values[0])).view()

            buttonViewImageAttendanceToday = Button(attendanceTodayScreen, text = 'View image', font = (fontTypeApp, 14), fg = 'white', bg = 'green',
                width = 10, height = 1, command = viewImageAttendanceTodayFunc)
            buttonViewImageAttendanceToday.place(x = 650, y = 60)
            buttonDeleteRowAttendanceToday= Button(attendanceTodayScreen, text = 'Delete', font = (fontTypeApp, 14), fg = 'white', bg = 'green',
                width = 10, height = 1, command = deleteRowAttendanceTodayFunc)
            buttonDeleteRowAttendanceToday.place(x = 770, y = 60)
        def exportToExcelAttendanceToday():
            numberIds, names, dateList, timeList = QuerySql.exportHistoryAttendance()
            fileName = 'export_excel/attendance_today.xls'
            Export.excel(numberIds, names, dateList, timeList, fileName)
            messagebox.showinfo('message', 'Export file excel success.')

        buttonExportToExcelAttendanceToday= Button(attendanceTodayScreen, text = 'Export to excel', font = (fontTypeApp, 14), fg = 'white', bg = 'green',
            width = 15, height = 1, command = exportToExcelAttendanceToday)
        buttonExportToExcelAttendanceToday.place(x = 350, y = 480)
        
        treeviewAttendanceToday.bind('<Button-1>', selectItemAttendanceToday)