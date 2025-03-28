import tkinter as tk
from main import ImazonDatabase
import time


class cancelButton(tk.Button):

    def __init__(self, window: tk.Tk):
        super().__init__(window, text="Cancel", command=lambda: window.destroy())


class LoginPage(tk.Tk):

    usernameEntry: tk.Entry
    passwordEntry: tk.Entry

    def __init__(self):
        super().__init__()
        self.title("Login Page")
        self.create_Widgets()

        self.mainloop()

    def create_Widgets(self):

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
            self.destroy()
            y: ShoppingPage = ShoppingPage()
        else:
            label = tk.Label(self, text="Incorrect Username or Password")
            label.grid(row=3, column=1, columnspan=3)
            self.after(1000, label.destroy)
        # valid = true

class ShoppingPage(tk.Tk):

    itemSearch: tk.Entry

    def __init__(self):
        super().__init__()
        self.title("Shopping Page")
        self.create_Widgets()

        self.mainloop()

    def create_Widgets(self):

        tk.Label(self, text ="Search:").grid(row=0, column=0)
        self.itemSearch = tk.Entry(self)
        self.itemSearch.grid(row=0, column=1, columnspan=2)
        tk.Button(self, text="Go", command= lambda: self.SubmitButtonClick()).grid(row=0, column=3)



        cancelButton(self).grid(row=2, column=0)


    def SubmitButtonClick(self):
        db = ImazonDatabase("./Imazon.db")
        item: str = self.itemSearch.get().lower()
        data = db.execute("SELECT PName, PDescription , Price FROM Products WHERE PName = ?" , (item))
        result = data.fectchall()
        tk.Label =




x: LoginPage = LoginPage()


