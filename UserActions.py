import os
import random
import sqlite3
import tkinter
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image
import main as main
from Book import Book
from User import User


#Login User Page class
class UserActions(tk.Frame):
    book = None
    User = None
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.parent = master
        self.LoadUser()
        self.CreateStatusBar()
        self.WorkPlace()
        self.CreateBaseMenu()
        self.CreateToolBar()
        self.AddHelpMenu()


    def CreateToolBar(self):
        self.toolbar_images = []
        self.toolbar = tk.Frame(self.parent)
        for image, command,i in (
                ("images/editdelete.gif", self.parent.destroy,0),
                ("images/editadd.gif", self.addSomeBooks,0.05),
                ("images/human.png", self.printUserData,0.1),
                ("images/book.png", self.Mybooks,0.15)):
            image = os.path.join(os.path.dirname(__file__), image)
            try:
                image = tkinter.PhotoImage(file=image)
                self.toolbar_images.append(image)
                button = Button(self.toolbar, image=image,command=command)
                button.place(relx=i,rely = 0,relwidth=0.05,relheight=1)
            except tkinter.TclError as err:
                print(err)
        self.toolbar.place(relx=0,rely=0,relwidth=1,relheight=0.03)

    def CreateStatusBar(self):
        self.statusbar = Label(self.parent, text="on the way…", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        #self.statusbar.after(5000, self.clearStatusBar)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def printUserData(self):
        tk.messagebox.showinfo('Info', f'User \n Login: {self.User.login} \n password: {self.User.password}')

    def CreateBaseMenu(self):
        self.menubar = tk.Menu(self.parent)
        self.parent["menu"] = self.menubar
        fileMenu = tk.Menu(self.menubar)
        for label, command, shortcut_text, shortcut in (
                ("My books ", self.Mybooks, "Ctrl+N", "<Control-n>"),
                ("Delete account", self.deleteAccount, "Ctrl+L", "<Control-l>"),
                ("Logout", self.logout, "Ctrl+S", "<Control-s>"),
                (None, None, None, None),
                ("Quit", self.parent.destroy, "Ctrl+Q", "<Control-q>")):
            if label is None:
                fileMenu.add_separator()
            else:
                fileMenu.add_command(label=label, underline=0,
                                     command=command, accelerator=shortcut_text)
                self.parent.bind(shortcut, command)
        self.menubar.add_cascade(label="File", menu=fileMenu, underline=0)


    #function showing user books
    def Mybooks(self,event = None):
        str = ''
        for book in self.User.ReadedBooks:
            str += '\n' + book
        tk.messagebox.showinfo('Info', 'Yours books: ' + str)

    # function deleting user data from database
    def deleteAccount(self,event= None):
        reply = tkinter.messagebox.askyesnocancel(
            "Deleting account"
            ,
            "Do you want to delete your account?",
            parent=self.parent)
        if reply is None:
            return False
        if reply:
            try:
                connection = sqlite3.connect('Library_dataBase.db')
                coursor = connection.cursor()
                coursor.execute("SELECT * from users")
                coursor.execute(f'DELETE from users WHERE login = "{self.User.login}"')
                connection.commit()
                connection.close()
                tk.messagebox.showinfo('Info', 'Account removed succesfully')
                self.parent.switch_frame(main.StartPage)
            except:
                tk.messagebox.showinfo('Info', 'Something went wrong')
        return True

    def logout(self,event= None):
        self.parent.switch_frame(main.StartPage)

    #function creating interactive user view
    def WorkPlace(self):
        global background_image, bookImage1, bookImage2, bookImage3
        self.frame = tk.Frame(self.parent)
        self.frame.place(relx=0, rely=0.03, relwidth=1, relheight=0.94)
        # adding background image
        background_image = ImageTk.PhotoImage(Image.open('pictures/lib.jpg').resize((3200,1100), Image.Resampling.LANCZOS))
        Canvas1 = tk.Canvas(self.frame)
        Canvas1.create_image(300, 340, image=background_image)
        Canvas1.config(bg="white", width=700, height=800)
        Canvas1.pack(expand=True, fill='both')
        # adding some buttons
        Button(self.frame, text="Return to start page", bg='black', fg='white',command=lambda: self.master.switch_frame(main.StartPage)).place(relx=0.28, rely=0.8, relwidth=0.45,relheight=0.1)
        Button(self.frame, text="Add some books", bg='black', fg='white', command=self.addSomeBooks).place(relx=0.28,rely=0.7,relwidth=0.45,relheight=0.1)
        BookNameBut = Entry(self.frame, width=30)
        BookNameBut.place(relx=0.25, rely=0.05, relwidth=0.50, relheight=0.05)
        Label(self.frame, text="loged as: " + self.User.login, bg='black', fg='white', font=('Courier', 8)).place(relx=0.0,rely=0.0,relwidth=0.2, relheight=0.05)
        Label(self.frame, text="Some of your books: ", bg='black', fg='white', font=('Courier', 15)).place(relx=0.2, rely=0.15,relwidth=0.30,relheight=0.07)
        # books shown to user in user Page
        if self.User.ReadedBooks != {}:
            book1 = list(self.User.ReadedBooks.values())
            ran = random.randrange(0, len(book1))
            bookImage1 = ImageTk.PhotoImage(
                Image.open(book1[ran][0].coverPage).resize((200, 180), Image.Resampling.LANCZOS))
            Label( self.frame, image=bookImage1, bg='black', fg='white', font=('Courier', 15)).place(relx=0.05, rely=0.25,relwidth=0.25,relheight=0.30)
            Label( self.frame, text=book1[ran][0].name, bg='black', fg='white', font=('Courier', 15)).place(relx=0.05,rely=0.55,relwidth=0.25, relheight=0.05)
            ran = random.randrange(0, len(book1))
            bookImage2 = ImageTk.PhotoImage(Image.open(book1[ran][0].coverPage).resize((200, 180), Image.Resampling.LANCZOS))
            Label(self.frame, image=bookImage2, bg='black', fg='white', font=('Courier', 15)).place(relx=0.37, rely=0.25,relwidth=0.25,relheight=0.30)
            Label( self.frame, text=book1[ran][0].name, bg='black', fg='white', font=('Courier', 15)).place(relx=0.37, rely=0.55,relwidth=0.25,relheight=0.05)
            ran = random.randrange(0, len(book1))
            bookImage3 = ImageTk.PhotoImage(
                Image.open(book1[ran][0].coverPage).resize((200, 180), Image.Resampling.LANCZOS))
            Label( self.frame, image=bookImage3, bg='black', fg='white', font=('Courier', 15)).place(relx=0.7, rely=0.25,relwidth=0.25,relheight=0.30)
            Label( self.frame, text=book1[ran][0].name, bg='black', fg='white', font=('Courier', 15)).place(relx=0.7, rely=0.55,relwidth=0.25, relheight=0.05)
        else:
            Label( self.frame, text="Ooops you dont have any book", bg='black', fg='white', font=('Courier', 15)).place( relx=0.30, rely=0.25, relwidth=0.50, relheight=0.1)
        self.setStatusBar("waiting...")
        # inner funkction showing new widow and allowing to look at the book and do some stuff with it
        def SearchBook():
            global bookImage
            self.setStatusBar("looking for book...")
            # importing book from data base
            bookName = BookNameBut.get()
            connection = sqlite3.connect('Library_dataBase.db')
            coursor = connection.cursor()
            coursor.execute("SELECT * FROM books")
            books = coursor.fetchall()
            for bookData in books:
                if bookData[0] == bookName:
                    self.book = Book(bookData[0], bookData[1], bookData[2], bookData[3], bookData[4], bookData[5])
            if self.book is not None:
                # creating window and adding buttons and labes
                top = tk.Toplevel()
                bookImage = ImageTk.PhotoImage(Image.open(self.book.coverPage))
                image = Label(top, image=bookImage).grid(row=2, column=1)
                Label(top, text=self.book.name).grid(row=1, column=1)
                Label(top, text=self.book.author).grid(row=3, column=1)
                Label(top, text="" + str(self.book.nrPages) + "str.").grid(row=4, column=1)
                Label(top, text="Readed: " + str(self.book.readed) + " times").grid(row=5, column=1)
                Label(top, text="Rating: " + str(self.book.rating)).grid(row=6, column=1)
                Button(top, text="Set as Readed", command=self.SetAsReaded).grid(row=7, column=1)
                Button(top, text="Add to Your Books", command=self.AddToUserBooks).grid(row=7, column=2)
                Button(top, text="Rate", command=self.rateBook).grid(row=7, column=3)
                Button(top, text="Exit", command=top.destroy).grid(row=7, column=4)
            else:
                tk.messagebox.showinfo('Info', 'There is no book with that title')
            connection.commit()
            connection.close()

        Button(self.frame, text="Search", bg='black', fg='white', command=SearchBook).place(relx=0.60, rely=0.1,relwidth=0.15, relheight=0.03)


    def setStatusBar(self, txt):
        self.statusbar["text"] = txt

    def clearStatusBar(self):
        self.statusbar["text"] = ""

    def AddHelpMenu(self):
        fileMenu = tk.Menu(self.menubar)
        for label, command, shortcut_text, shortcut in (
                ('Info', self.InfoHelp, "Ctrl+I", "<Control-i>"),
                ("Delete Account?", self.DeleteAccountHelp, "Ctrl+D", "<Control-d>"),
                ("Searching books?", self.SearchingBooks, "Ctrl+W", "<Control-w>"),
                (None, None, None, None),
                ("Quit", self.Quithelp, "Ctrl+H", "<Control-h>")):
            if label is None:
                fileMenu.add_separator()
            else:
                fileMenu.add_command(label=label, underline=0,command=command, accelerator=shortcut_text)
                self.parent.bind(shortcut, command)
        self.menubar.add_cascade(label="Help", menu=fileMenu, underline=0)

    def InfoHelp(self,event = None):
        tk.messagebox.showinfo('Info', 'Hello in our app \n You can search book and read them \n also you can add book to your readed list \n and add your book to our data base')

    def DeleteAccountHelp(self,event= None):
        tk.messagebox.showinfo('Info', 'You can delete all yours data from our app')

    def SearchingBooks(self,event= None):
        tk.messagebox.showinfo('Info', 'You can search books from our data base')

    def Quithelp(self,event= None):
        tk.messagebox.showinfo('Info', 'You are getting out of app')

    #function marking book as readed
    def SetAsReaded(self):
        self.setStatusBar("marking as readed")
        if self.User != None:
            if self.book.name in self.User.ReadedBooks.keys():
                if not self.User.ReadedBooks[self.book.name][1]:
                    self.book.readed += 1
                    self.User.ReadedBooks[self.book.name] = (self.book, True)
                    self.book.UpdateBook()
                    self.User.updateUser()
                else:
                    tk.messagebox.showinfo('Info', 'You have readed this book already')
            else:
                tk.messagebox.showinfo('Info','You don`t have this book')

    # function allowed to adding books to User account
    def AddToUserBooks(self):
        self.setStatusBar("Adding to User books...")
        if self.book.name != None and self.book.name not in self.User.ReadedBooks.keys():
            self.User.ReadedBooks[self.book.name] = (self.book,False)
            tk.messagebox.showinfo('Info', 'succesfully added ' + self.User.ReadedBooks[self.book.name][0].name + ' to your readed list')
            self.User.updateUser()
        else:
            tk.messagebox.showinfo('Info', 'cannot add to Account')

    #function allowed to rating books by user
    def rateBook(self):
        top2 = tk.Toplevel()
        Label(top2, text="How do you rate these book? (1-10)").grid(row=1, column=3)
        ratingEn = Entry(top2,width=30)
        ratingEn.grid(row=2,column=3)
        #rating books
        def inside():
            try:
                rate = int(ratingEn.get())
                if rate > 0 and rate < 11:
                    self.book.rating = round((self.book.rating + (rate/10))/(self.book.readed + 1),2)
                    self.book.UpdateBook()
                    tk.messagebox.showinfo('Info', 'Thank you, for yours rating')
                    top2.destroy()
                else:
                    tk.messagebox.showinfo('Info', 'wrong rating')
            except:
                tk.messagebox.showinfo('Info', 'Wrong Value!! Try again')
        Button(top2, text="Rate", command=inside).grid(row=3, column=1)
        Button(top2, text="Exit", command=top2.destroy).grid(row=3, column=4)

    #non use fuction adding book by user to data base
    def addSomeBooks(self):
        global background_image
        self.setStatusBar("waiting for data...")
        my_filetypes = [('all files', '.*'), ('text files', '.txt')]
        top3 = Frame(self.parent)
        top3.place(relx=0, rely=0.03, relwidth=1, relheight=0.94)
        background_image = ImageTk.PhotoImage(Image.open('pictures/library.png').resize((3200,1100), Image.Resampling.LANCZOS))
        Canvas1 = tk.Canvas(top3)
        Canvas1.create_image(300, 340, image=background_image)
        Canvas1.config(bg="white", width=700, height=800)
        Canvas1.pack(expand=True, fill='both')
        self.path = ''
        book1 = None
        #inner function getting path to image from user
        def getPath():
            answer = filedialog.askopenfilename(parent=top3,initialdir=os.getcwd(),title="Please select a Image:",filetypes=my_filetypes)
            if answer != '':
                self.path = answer
            else:
                tk.messagebox.showinfo('Info', 'Try Again')
        Label(top3,text='What book you want to add? ').place(relx=0.02, rely=0.1, relwidth=0.22, relheight=0.05)
        Label(top3, text='Enter Name of book ').place(relx=0.10, rely=0.25, relwidth=0.22, relheight=0.1)
        Label(top3, text='Enter Author of book ').place(relx=0.10, rely=0.35, relwidth=0.22, relheight=0.1)
        Label(top3, text='Enter number of pages of book ').place(relx=0.10, rely=0.45, relwidth=0.22, relheight=0.1)
        nameEn = Entry(top3,width=30)
        autrorEn = Entry(top3,width=30)
        numofpagesEn = Entry(top3,width=10)
        nameEn.place(relx=0.32, rely=0.25, relwidth=0.50, relheight=0.1)
        autrorEn.place(relx=0.32, rely=0.35, relwidth=0.50, relheight=0.1)
        numofpagesEn.place(relx=0.32, rely=0.45, relwidth=0.50, relheight=0.1)

        #inner function adding books to data base
        def createBook():
            self.setStatusBar("creating book... ")
            name = nameEn.get()
            autror = autrorEn.get()
            numofpages = numofpagesEn.get()
            connection = sqlite3.connect('Library_dataBase.db')
            coursor = connection.cursor()
            coursor.execute("SELECT * FROM books")
            books = coursor.fetchall()
            BookExists = False
            for booksData in books:
                if booksData[0] == name:
                    BookExists = True
            if BookExists:
                tk.messagebox.showinfo('Info', 'These books exist!! Try Again')
            else:
                if name != '' and autror != '' and numofpages != '' and name != ' ' and autror != ' ' and numofpages != ' ' and self.correctionOftext(name) and self.correctionOftext(autror) and self.correctionOftext(numofpages):
                    try:
                        book1 = Book(name, autror, int(numofpages), self.path)
                        tk.messagebox.showinfo('Info', 'Added sucesfully')
                        book1.SaveBook()
                        self.path = ''
                        self.WorkPlace()
                    except:
                        tk.messagebox.showinfo('Info', 'Wrong input')
                        self.setStatusBar("Wrong input")
                else:
                    tk.messagebox.showinfo('Info', 'Wrong input')
        Button(top3, text="Add Book Image", command=getPath).place(relx=0.7, rely=0.60, relwidth=0.1, relheight=0.1)
        Button(top3, text="Back", command=self.WorkPlace).place(relx=0.45, rely=0.60, relwidth=0.15, relheight=0.1)
        Button(top3, text="Add Book", command=createBook).place(relx=0.3, rely=0.60, relwidth=0.1, relheight=0.1)

    # load user from data base
    def LoadUser(self):
        connection = sqlite3.connect('Library_dataBase.db')
        coursor = connection.cursor()
        f = open("LogedUser.txt", "r")
        userlogin = f.readline()
        f.close()
        coursor.execute("SELECT *  FROM users ")
        usersData = coursor.fetchall()
        for user in usersData:
            if user[0] == userlogin:
                self.User = None
                self.User = User(user[0],user[1],user[2])
        connection.commit()
        connection.close()

    #function chcecking corection of input text
    def correctionOftext(self, txt):
        if txt.isprintable():
            for i in txt:
                if i == '_' and i == '%' and i =='#' and i == '@' and i == '^' and i == '~' and i == '*':
                    tk.messagebox.showinfo('Info', 'Wrong input')
                    return False
            return True
        else:
            tk.messagebox.showinfo('Info', 'Wrong input')
            return False