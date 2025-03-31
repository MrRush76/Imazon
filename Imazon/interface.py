import sqlite3
import tkinter as tk
from main import ImazonDatabase
import time


class cancelButton(tk.Button):

    def __init__(self, frameRef:tk.Frame):
        super().__init__(frameRef, text="Cancel", command=lambda: frameRef.destroy())

class RegisterPageFrame(tk.Frame):
    usernameEntry: tk.Entry
    passwordEntry: tk.Entry

    def __init__(self, windowRef: tk.Tk, oldFrame:tk.Frame = None):
        if oldFrame is not None:
            oldFrame.destroy()
        super().__init__(windowRef)
        self.SetupLayout()
        self.pack(fill="both", expand=True)

    def SetupLayout(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        tk.Label(self, text="Username:").grid(row=0, column=0)
        tk.Label(self, text="Password:").grid(row=1, column=0)
        tk.Label(self,text="Email Adress").grid(row=2, column=0)
        tk.Label(self,text="Phone Number").grid(row=3, column=0)

        self.usernameEntry = tk.Entry(self)
        self.usernameEntry.grid(row=0, column=1, columnspan=2)

        self.passwordEntry = tk.Entry(self)
        self.passwordEntry.grid(row=1, column=1, columnspan=2)

        self.emailEntry = tk.Entry(self)
        self.emailEntry.grid(row=2, column=1, columnspan=2)

        self.phoneNumEntry = tk.Entry(self)
        self.phoneNumEntry.grid(row=3, column=1, columnspan=2)

        cancelButton(self).grid(row=4, column=0)
        tk.Button(self, text="Register", command=lambda: self.SubmitButtonClick()).grid(row=4, column=2)

    def SubmitButtonClick(self):
        username: str = self.usernameEntry.get()
        password: str = self.passwordEntry.get()
        email : str = self.emailEntry.get()
        phoneNum: str = self.phoneNumEntry.get()

        print(username)
        print(password)
        db = ImazonDatabase("./Imazon.db")
        try:
            db.add_customer(username,password,email,phoneNum)
            LoginPageFrame(self.master,self)
        except sqlite3.IntegrityError:
            tk.Label(self,text = "Error")

class LoginPageFrame(tk.Frame):

    usernameEntry: tk.Entry
    passwordEntry: tk.Entry

    def __init__(self, windowRef: tk.Tk, oldFrame:tk.Frame = None):
        if oldFrame is not None:
            oldFrame.destroy()
        super().__init__(windowRef)
        self.SetupLayout()
        self.pack(fill="both", expand=True)

    def SetupLayout(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        tk.Label(self, text="Username:").grid(row=0, column=0)
        tk.Label(self, text="Password:").grid(row=1, column=0)

        self.usernameEntry = tk.Entry(self)
        self.usernameEntry.grid(row=0, column=1, columnspan=2)

        self.passwordEntry = tk.Entry(self)
        self.passwordEntry.grid(row=1, column=1, columnspan=2)

        cancelButton(self).grid(row=2, column=0)
        tk.Button(self, text="Login", command=lambda: self.SubmitButtonClick()).grid(row=2, column=2)

    def SubmitButtonClick(self):
        username: str = self.usernameEntry.get()
        password: str = self.passwordEntry.get()

        print(username)
        print(password)
        db = ImazonDatabase("./Imazon.db")
        user_exists = db.check_account(username, password)
        if user_exists:
            ShoppingFrame(self.master,self)
        else:
            label = tk.Label(self, text="Incorrect Username or Password")
            label.grid(row=3, column=1, columnspan=3)
            self.after(1000, label.destroy)
        # valid = true

class ShoppingFrame(tk.Frame):

    itemSearch: tk.Entry

    def __init__(self, windowRef: tk.Tk, oldFrame: tk.Frame = None):
        if oldFrame is not None:
            oldFrame.destroy()
        super().__init__(windowRef)
        self.SetupLayout()
        self.pack(fill="both", expand=True)

    def SetupLayout(self):

        tk.Label(self, text ="Search:").grid(row=0, column=0)
        self.itemSearch = tk.Entry(self)
        self.itemSearch.grid(row=0, column=1, columnspan=2)
        tk.Button(self, text="Go", command= lambda: self.SubmitButtonClick()).grid(row=0, column=3)



        cancelButton(self).grid(row=2, column=0)


    def SubmitButtonClick(self):
        tk.Button(self, text="Reset", command=lambda: ShoppingFrame(self.master,self)).grid(row=0, column=4)
        db = ImazonDatabase("./Imazon.db")
        item: str = self.itemSearch.get().lower()
        data = db.execute("SELECT PName, PDescription , PPrice FROM Product WHERE PName LIKE ?" , (item,))
        result = data.fetchall()
        tk.Label(self, text ="Items Found:").grid(row=1, column=0)
        for i in range(len(result)):
            tk.Label(self,text = result[i]).grid(row=i+2, column=0)



class LoginRegisterFrame(tk.Frame):

    def __init__(self, windowRef: tk.Tk, oldFrame: tk.Frame = None):
        if oldFrame is not None:
            oldFrame.destroy()
        super().__init__(windowRef)
        self.SetupLayout()
        self.pack(fill="both", expand=True)
    def SetupLayout(self):
        # self.configure(bg = "#ff0000")
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        tk.Button(self, text="Login", command=lambda: LoginPageFrame(self.master, self), font=["Century Gothic", 20], width=10).grid(row=2,column=0, padx=(10,5), pady=10)
        tk.Button(self, text="Register", command=lambda: RegisterPageFrame(self.master, self), font=["Century Gothic", 20],width=10).grid(row=2,column=1 , padx=(5,10), pady=10)


class MainPage(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Login Page")
        self.configure(bg="#ff8803")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        LoginRegisterFrame(self)
        self.mainloop()


x: MainPage = MainPage()


