from tkinter import*
from tkinter import messagebox
from add_new_user import AddNewUser
from add_data_test import AddNewDataTest

fontTypeApp = 'Times New Roman'

class AddNewUserData:
    def __init__(self, latestFrame, lastRet):
        self.latestFrame = latestFrame
        self.lastRet = lastRet

    def show(self):
        addNewUserTrainModelScreen = Tk()
        addNewUserTrainModelScreen.geometry('500x150')
        addNewUserTrainModelScreen.resizable(False, False)
        addNewUserTrainModelScreen.configure(bg = 'CornflowerBlue')
        def addNewUserFunc():
            getValueNumberIdAddNew = inputNewNumberId.get()
            getValueNameAddNew = inputNewNameUser.get()
            if(len(getValueNumberIdAddNew) == 0 or len(getValueNameAddNew) == 0):
                messagebox.showinfo('message', 'Please fill all fields')
            elif getValueNumberIdAddNew.isdecimal:
                AddNewUser(getValueNumberIdAddNew, getValueNameAddNew, self.latestFrame, self.lastRet).add()
            else:
                messagebox.showinfo('message', 'Number Id must is isdecimal.')
            addNewUserTrainModelScreen.destroy()
        
        def addNewDataTestFunc():
            getIdAddTest = inputNewNumberId.get()
            getNameTest = inputNewNameUser.get()
            AddNewDataTest(getIdAddTest, getNameTest , self.latestFrame, self.lastRet).add()
            
        lbl_ID_nguoiMoi = Label(addNewUserTrainModelScreen, text = 'number Id', bd = 4, fg = 'white', font = (fontTypeApp, 16), width = 10, bg = 'green')
        lbl_ID_nguoiMoi.place(x = 15, y = 10)
        inputNewNumberId = Entry(addNewUserTrainModelScreen, bd = 5, width = 35, font = (fontTypeApp, 14))
        inputNewNumberId.place(x = 150, y = 10)
        lbl_Ten_nguoiMoi = Label(addNewUserTrainModelScreen, text='name', bd=4, fg='white', font=(fontTypeApp, 16), width= 10, bg='green')
        lbl_Ten_nguoiMoi.place(x= 15, y= 45)
        inputNewNameUser = Entry(addNewUserTrainModelScreen, width=35, bd=5,font=(fontTypeApp, 14))
        inputNewNameUser.place(x= 150, y= 45)
        buttonAddNewUser = Button(addNewUserTrainModelScreen, text = 'Add new user', font = (fontTypeApp, 14), fg = 'white', bg = 'green',
            width = 15, height = 1, command = addNewUserFunc)
        buttonAddNewUser.place(x = 100, y = 90)
        buttonAddNewDataTest = Button(addNewUserTrainModelScreen, text = 'Add data test', font = (fontTypeApp, 14), fg = 'white', bg = 'green',
            width = 15, height = 1, command = addNewDataTestFunc)
        buttonAddNewDataTest.place(x = 300, y = 90)