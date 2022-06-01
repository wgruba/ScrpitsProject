import random
import sqlite3
import tkinter as tk
from tkinter import *
from PIL import ImageTk,Image
import main as main
from Book import Book
from User import User


class UserActions(tk.Frame):
    book = None
    User = None
    def __init__(self, master):
        global background_image,bookImage1,bookImage2,bookImage3
        frame = tk.Frame.__init__(self, master)
        background_image = ImageTk.PhotoImage(Image.open('pictures/lib.jpg').resize((1600, 800), Image.Resampling.LANCZOS))
        Canvas1 = tk.Canvas(frame)
        Canvas1.create_image(300, 340, image=background_image)
        Canvas1.config(bg="white", width=700, height=800)
        Canvas1.pack(expand=True, fill='both')
        Button(frame, text="Return to start page",bg='black', fg='white' ,command=lambda: master.switch_frame(main.StartPage)).place(relx=0.28,rely=0.8, relwidth=0.45,relheight=0.1)
        Button(frame, text="Add some books",bg='black', fg='white', command=self.addSomeBooks).place(relx=0.28,rely=0.7, relwidth=0.45,relheight=0.1)
        BookNameBut = Entry(frame, width=30)
        BookNameBut.place(relx=0.25,rely=0.05, relwidth=0.50,relheight=0.05)
        self.LoadUser()

        #books shown to user in user Page
        Label(frame, text="Some of your books: ", bg='black', fg='white', font=('Courier', 15)).place(relx=0.2,rely=0.15,relwidth=0.30,relheight=0.07)
        book1 = list(self.User.ReadedBooks.values())
        ran = random.randrange(0,len(book1))
        bookImage1 = ImageTk.PhotoImage(Image.open(book1[ran][0].coverPage).resize((200,180),Image.Resampling.LANCZOS))
        Label(frame, image=bookImage1, bg='black', fg='white', font=('Courier', 15)).place(relx=0.05, rely=0.25, relwidth=0.25,relheight=0.30)
        Label(frame, text=book1[ran][0].name, bg='black', fg='white', font=('Courier', 15)).place(relx=0.05, rely=0.55,relwidth=0.15,relheight=0.05)
        ran = random.randrange(0, len(book1))
        bookImage2 = ImageTk.PhotoImage(Image.open(book1[ran][0].coverPage).resize((200,180),Image.Resampling.LANCZOS))
        Label(frame, image= bookImage2, bg='black', fg='white', font=('Courier', 15)).place(relx=0.37,rely=0.25,relwidth=0.25,relheight=0.30)
        Label(frame, text=book1[ran][0].name, bg='black', fg='white', font=('Courier', 15)).place(relx=0.37, rely=0.55,relwidth=0.25,relheight=0.05)
        ran = random.randrange(0, len(book1))
        bookImage3 = ImageTk.PhotoImage(Image.open(book1[ran][0].coverPage).resize((200,180),Image.Resampling.LANCZOS))
        Label(frame, image=bookImage3, bg='black', fg='white', font=('Courier', 15)).place(relx=0.7,rely=0.25,relwidth=0.25,relheight=0.30)
        Label(frame, text=book1[ran][0].name, bg='black', fg='white', font=('Courier', 15)).place(relx=0.7, rely=0.55,relwidth=0.25,relheight=0.05)
        def SearchBook():
            global bookImage
            bookName = BookNameBut.get()
            connection = sqlite3.connect('Library_dataBase.db')
            coursor = connection.cursor()
            coursor.execute("SELECT * FROM books")
            books = coursor.fetchall()
            for bookData in books:
                if bookData[0] == bookName:
                    self.book = Book(bookData[0],bookData[1],bookData[2],bookData[3],bookData[4],bookData[5])
            if self.book is not None:
                top = tk.Toplevel()
                bookImage = ImageTk.PhotoImage(Image.open(self.book.coverPage))
                image = Label(top,image=bookImage).grid(row=2,column=1)
                Label(top,text=self.book.name).grid(row=1,column=1)
                Label(top,text=self.book.author).grid(row=3,column=1)
                Label(top, text="" + str(self.book.nrPages)+"str.").grid(row=4,column=1)
                Label(top, text="Readed: " + str(self.book.readed) + " times").grid(row=5, column=1)
                Label(top, text="Rating: " + str(self.book.rating)).grid(row=6, column=1)
                Button(top, text="Set as Readed", command= self.SetAsReaded).grid(row=7,column=1)
                Button(top, text="Add to Your Books", command=self.AddToUserBooks).grid(row=7, column=2)
                Button(top, text="Rate", command=self.rateBook).grid(row=7, column=3)
                Button(top, text="Exit", command=top.destroy).grid(row=7, column=4)
            else:
                tk.messagebox.showinfo('Info', 'There is no book with that title')
            connection.commit()
            connection.close()
        Button(frame, text="Search", bg='black', fg='white',command=SearchBook).place(relx=0.60,rely=0.1, relwidth=0.15,relheight=0.03)

    def SetAsReaded(self):
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

    def AddToUserBooks(self):
        if self.book.name != None and self.book.name not in self.User.ReadedBooks.keys():
            self.User.ReadedBooks[self.book.name] = (self.book,False)
            tk.messagebox.showinfo('Info', 'succesfully added ' + self.User.ReadedBooks[self.book.name][0].name + ' to your readed list')
            self.User.updateUser()
        else:
            tk.messagebox.showinfo('Info', 'cannot add to Account')

    def rateBook(self):
        top2 = tk.Toplevel()
        Label(top2, text="How do you rate these book? (1-10)").grid(row=1, column=3)
        ratingEn = Entry(top2,width=30)
        ratingEn.grid(row=2,column=3)
        def inside():
            rate = int(ratingEn.get())
            if rate > 1 and rate < 10:
                self.book.rating += rate/10
                self.book.UpdateBook()
            else:
                tk.messagebox.showinfo('Info', 'wrong rating')
        Button(top2, text="Rate", command=inside).grid(row=3, column=1)
        Button(top2, text="Exit", command=top2.destroy).grid(row=3, column=4)


    def addSomeBooks(self):
        book1 = Book('Cień i kość','Leigh Bardugo',288,'pictures/cień_i_kość.jpg')
        book2 = Book('Krew i miód', 'Shelby Mahurin', 512, 'pictures/krew_i_miód.png')
        book3 = Book('Mentalista', 'Henrik Fexeus', 680, 'pictures/mentalista.png')
        book4 = Book('Pan Tadeusz', 'Adam Mickiewicz', 344, 'pictures/pan_tadeusz.png')

        connection = sqlite3.connect('Library_dataBase.db')
        coursor = connection.cursor()
        coursor.execute("SELECT * FROM books")
        adds = coursor.fetchall()
        UserExists = False
        for userData in adds:
            if userData[0] == book1.name:
                UserExists = True
        if UserExists:
            tk.messagebox.showinfo('Info', 'These books exist!! Try Again')
        else:
            book1.SaveBook()
            book2.SaveBook()
            book3.SaveBook()
            book4.SaveBook()

    def LoadUser(self):
        connection = sqlite3.connect('Library_dataBase.db')
        coursor = connection.cursor()
        f = open("LogedUser.txt", "r")
        userlogin = f.readline()
        coursor.execute("SELECT *  FROM users ")
        usersData = coursor.fetchall()
        for user in usersData:
            if user[0] == userlogin:
                self.User = User(user[0],user[1],user[2])
        connection.commit()
        connection.close()
