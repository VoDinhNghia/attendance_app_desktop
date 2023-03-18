import tkinter
from tkinter import*
from tkinter import ttk, messagebox
from connect_db import QuerySql
from view_image import ViewImage
from date import SearchDate

fontTypeApp = 'Times New Roman'
path = 'image_trainning_model'

class FrameSearchByDate:
    def __init__(self, searchKey):
        self.searchKey = searchKey

    def show(self):
        global searchDate
        searchDate = SearchDate.formatDate(self.searchKey)
        resultAttendanceByDate = QuerySql.queryHistoryByDate(searchDate)
        searchByDateScreen = Tk()
        searchByDateScreen.title('attendance list')
        searchByDateScreen.geometry('950x550')
        searchByDateScreen.resizable(False,False)
        searchByDateScreen.configure(bg='CornflowerBlue')
        lableTitleSearch = Label(searchByDateScreen, text = 'attendance list by date '+str(searchDate), font = (fontTypeApp, 18),fg='green')
        lableTitleSearch.place(x = 200, y = 10)
        showNumberIdOnClickRow = Label(searchByDateScreen, text = '', font = (fontTypeApp, 14))
        showNumberIdOnClickRow.place(x = 10, y = 60)
        showNameOnClickRow = Label(searchByDateScreen, text = '', font = (fontTypeApp, 14))
        showNameOnClickRow.place(x = 80, y = 60)
        showDateOnClickRow = Label(searchByDateScreen, text = '', font = (fontTypeApp, 14))
        showDateOnClickRow.place(x = 300, y = 60)
        showTimeOnClickRow = Label(searchByDateScreen, text = '', font = (fontTypeApp, 14))
        showTimeOnClickRow.place(x = 500, y = 60)
        frameResultSearch = Frame(searchByDateScreen)
        frameResultSearch.pack(side = tkinter.LEFT, padx = 50)
        treeViewSearch = ttk.Treeview(frameResultSearch, columns = (1,2,3,4), show = 'headings', height = '15', padding = 'Centimeters')
        treeViewSearch.pack(side = 'right')
        verscrlbarSearch = ttk.Scrollbar(searchByDateScreen, orient = 'vertical', command = treeViewSearch.yview)
        verscrlbarSearch.pack(side ='right', fill ='x') 
        treeViewSearch.configure(xscrollcommand = verscrlbarSearch.set)
        treeViewSearch.heading(1, text = 'Number Id')
        treeViewSearch.heading(2, text = 'Name')
        treeViewSearch.heading(3, text = 'Date attendance')
        treeViewSearch.heading(4, text = 'Time attendance')
        for i in resultAttendanceByDate:
            treeViewSearch.insert('', 'end', values = i)
        
        def selectItemSearch(event):
            cursorItem = treeViewSearch.focus()
            getValueOnClick = treeViewSearch.item(cursorItem)
            valuesOnRow = getValueOnClick['values']
            values = []
            for i in valuesOnRow:
                values.append(i)
            try:
                showNumberIdOnClickRow.configure(text = values[0])
                showNameOnClickRow.configure(text = values[1])
                showDateOnClickRow.configure(text = values[2])
                showTimeOnClickRow.configure(text = values[3])
            except:
                print('error exception')
            def deleteAttendanceSearchFunc():
                try:
                    rowDeleteSearch = treeViewSearch.selection()[0]
                    idSearch = int(values[0])
                    timeSearch = values[3]
                except:
                    print('error exception')
                treeViewSearch.delete(rowDeleteSearch)
                QuerySql.deleteHistoryAttendance(idSearch, timeSearch)
                messagebox.showinfo('message', 'Delete row success.')
            def viewImageSearchFunc():
                pathImgCorrectSearch = 'image_correct'
                ViewImage(pathImgCorrectSearch, int(values[0])).view()

            buttonViewImageSearch = Button(searchByDateScreen, text = 'View image', font = (fontTypeApp, 14), fg = 'white', bg = 'green',
                width = 10, height = 1, command = viewImageSearchFunc)
            buttonViewImageSearch.place(x = 650, y = 60)
            buttonDeleteAttendanceSearch = Button(searchByDateScreen, text = 'Delete', font=(fontTypeApp, 14), fg = 'white', bg = 'green',
                width = 10, height = 1, command = deleteAttendanceSearchFunc)
            buttonDeleteAttendanceSearch.place(x=770, y=60)
        def statictisSearchFunc():
            lableListSearch, attendanceListSearch, notYetAttendanceSearch = QuerySql.statictisHistoryByDate(searchDate)
            statictisSearchScreen = Tk()
            statictisSearchScreen.title('List staff not yet attendance')
            statictisSearchScreen.geometry('600x550')
            statictisSearchScreen.resizable(False, False)
            statictisSearchScreen.configure(bg='CornflowerBlue')
            lableTitleNotYetAttendanceSearch = Label(statictisSearchScreen, text = 'List staff not yet attendance', font = (fontTypeApp, 18),fg = 'green')
            lableTitleNotYetAttendanceSearch.place(x = 50, y = 10)

            frameStatictisSearch = Frame(statictisSearchScreen)
            frameStatictisSearch.pack(side = tkinter.LEFT, padx = 30)
            treeViewStatictisSearch = ttk.Treeview(frameStatictisSearch, columns = (1,2), show = 'headings', height = '15', padding='Centimeters')
            treeViewStatictisSearch.pack(side = 'right')
            verscrlbarStatictisSearch = ttk.Scrollbar(statictisSearchScreen, orient = 'vertical', command = treeViewStatictisSearch.yview)
            verscrlbarStatictisSearch.pack(side ='right', fill = 'x') 
            treeViewStatictisSearch.configure(xscrollcommand = verscrlbarStatictisSearch.set)
            treeViewStatictisSearch.heading(1, text = 'Number Id')
            treeViewStatictisSearch.heading(2, text = 'name')
            
            lableStatictisSearchNotYet = Label(statictisSearchScreen, text='Not yet: ', font = (fontTypeApp, 16), fg = 'red')
            lableStatictisSearchNotYet.place(x = 100, y = 60)
            lableStatictisSearchNotYetValue = Label(statictisSearchScreen, text = ' ', font = (fontTypeApp, 16), fg = 'red')
            lableStatictisSearchNotYetValue.place(x = 300, y = 60)
            lableStatictisSearchAlready = Label(statictisSearchScreen, text = 'Already: ', font = (fontTypeApp, 16), fg = 'red')
            lableStatictisSearchAlready.place(x = 400, y = 60)
            lblTitleStatictisSearchAlreadyValue = Label(statictisSearchScreen, text = ' ', font = (fontTypeApp, 16), fg = 'red')
            lblTitleStatictisSearchAlreadyValue.place(x = 550, y = 60)
            if(len(attendanceListSearch) == 0):
                for y in lableListSearch:
                    treeViewStatictisSearch.insert('', 'end', values = (y[0], y[1]))
                lableStatictisSearchNotYetValue.configure(text = len(lableListSearch))
                lblTitleStatictisSearchAlreadyValue.configure(text = len(attendanceListSearch))
            elif(len(attendanceListSearch) == len(lableListSearch)):
                for i in notYetAttendanceSearch:
                    treeViewStatictisSearch.insert('', 'end', values = '')
                lableStatictisSearchNotYetValue.configure(text = 0)
                lblTitleStatictisSearchAlreadyValue.configure(text = len(attendanceListSearch))
            else:
                for i in notYetAttendanceSearch:
                    treeViewStatictisSearch.insert('', 'end', values = (i[0], i[1]))
                lableStatictisSearchNotYetValue.configure(text = len(notYetAttendanceSearch))
                lblTitleStatictisSearchAlreadyValue.configure(text = len(attendanceListSearch))

        buttonStatictisSearch = Button(searchByDateScreen, text = 'Statictis', font = (fontTypeApp, 14), fg = 'white', bg = 'green',
            width = 10, height = 1, command = statictisSearchFunc)
        buttonStatictisSearch.place(x = 350, y = 480)
        
        treeViewSearch.bind('<Button-1>', selectItemSearch)