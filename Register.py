import sqlite3
import tkinter as tk
from tkinter import *
from PIL import ImageTk,Image
import main as main
from User import User
import tkinter.messagebox

class Register(tk.Frame):
    def __init__(self, master):
        global background_image
        frame = tk.Frame.__init__(self, master)
        background_image = ImageTk.PhotoImage(Image.open('pictures/reg3.png ').resize((3200,1100), Image.Resampling.LANCZOS))
        Canvas1 = tk.Canvas(self)
        Canvas1.create_image(300, 340, image=background_image)
        Canvas1.config(bg="white", width=700, height=800)
        Canvas1.pack(expand=True, fill='both')
        Label(self, text="Registration")
        Label(self,text="login").place(relx=0.15, rely=0.3, relwidth=0.15, relheight=0.1)
        Label(self, text="password").place(relx=0.15, rely=0.4, relwidth=0.15, relheight=0.1)
        Label(self, text="confirm password").place(relx=0.15, rely=0.5, relwidth=0.15, relheight=0.1)
        login = Entry(self,width=30)
        login.place(relx=0.28,rely=0.30, relwidth=0.45,relheight=0.1)
        password = Entry(self,width=30,show='*')
        password.place(relx=0.28,rely=0.4, relwidth=0.45,relheight=0.1)
        password_confirmation = Entry(self, width=30, show='*')
        password_confirmation.place(relx=0.28, rely=0.5, relwidth=0.45, relheight=0.1)
        Button(self, text="Return to start page", command=lambda: master.switch_frame(main.StartPage)).place(relx=0.60,rely=0.85, relwidth=0.15, relheight=0.1)

        def RegisterUser(event = None):
            event = event
            Password = password.get()
            self.correctionOftext(login.get())
            self.correctionOftext(Password)
            if Password == password_confirmation.get():
                connection = sqlite3.connect('Library_dataBase.db')
                coursor = connection.cursor()
                coursor.execute("SELECT * FROM users")
                logins = coursor.fetchall()
                UserExists = False
                for userData in logins:
                    if userData[0] == login.get():
                        UserExists = True
                if UserExists:
                    tk.messagebox.showinfo('Info', 'User with this login alredy exist!! Try Again')
                else:
                    coursor.execute("INSERT INTO users VALUES (:login,:password,:ReadedBooks)",
                                {
                                    'login': login.get(),
                                    'password': password.get(),
                                    'ReadedBooks': ''
                                }
                                )
                    RegistredUser = User(login.get(), password.get())
                    tk.messagebox.showinfo('Info', 'Registration completed')
                login.delete(0, END)
                password.delete(0, END)
                password_confirmation.delete(0, END)
                connection.commit()
                connection.close()
            else:
                tk.messagebox.showinfo('Info', 'Passwords are diffrent')

        Button(self, text= "Register", command=RegisterUser).place(relx=0.15,rely=0.85, relwidth=0.15,relheight=0.1)

    def correctionOftext(self,txt):
        if txt.isprintable():
            for i in txt:
                if i.isspace():
                    tk.messagebox.showinfo('Info', 'Wrong input')
            self.text = txt
        else:
            tk.messagebox.showinfo('Info', 'Wrong input')
