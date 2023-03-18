import hashlib
from tkinter import*
from tkinter import messagebox
from connect_db import QuerySql

fontTypeApp = 'Times New Roman'

class ChangeInfoAdmin:
      def show():
        changeInfoAdminScreen = Tk()
        changeInfoAdminScreen.geometry('550x150')
        changeInfoAdminScreen.resizable(False, False)
        changeInfoAdminScreen.configure(bg = 'CornflowerBlue')

        def changeInfoFunc():
            newUsername = inputUsernameAdmin.get()
            newPassword = inputNewPasswordAdmin.get()
            if((newUsername == '' and newPassword == '') or newUsername == '' or newPassword==''):
                messagebox.showinfo('message', 'Please, enter value into fiels.')
            elif(len(newPassword) < 6 and len(newPassword)>10):
                messagebox.showinfo('message', 'Length password from 6 to 10 character')
            else:
                md = hashlib.md5()
                md.update(newPassword.encode())
                newPassword = md.hexdigest()
                QuerySql.updateAdmin(newUsername, newPassword)
                messagebox.showinfo('message', 'Change info admin success.')
                changeInfoAdminScreen.destroy()

        lableNewUsernameAdmin = Label(changeInfoAdminScreen, text = 'username', bd = 4, fg = 'white', font = (fontTypeApp, 16), width = 10, bg = 'green')
        lableNewUsernameAdmin.place(x = 15, y = 10)
        inputUsernameAdmin = Entry(changeInfoAdminScreen, width = 35, bd = 5, font = (fontTypeApp, 14))
        inputUsernameAdmin.place(x = 200, y = 10)
        lableNewPasswordAdmin = Label(changeInfoAdminScreen, text = 'password', bd = 4, fg = 'white', font = (fontTypeApp, 16), width = 10, bg = 'green')
        lableNewPasswordAdmin.place(x = 15, y = 50)
        inputNewPasswordAdmin = Entry(changeInfoAdminScreen, width = 35, bd = 5, font = (fontTypeApp, 14), show = '*')
        inputNewPasswordAdmin.place(x= 200, y= 50)
        buttonChangeInfo = Button(changeInfoAdminScreen, text = 'Change Admin', font = (fontTypeApp, 14), fg = 'white', bg = 'red',
            width = 15, height = 1, command = changeInfoFunc)
        buttonChangeInfo.place(x = 250, y = 90)