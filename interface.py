import sqlite3
import tkinter as tk
from main import ImazonDatabase


class cancelButton(tk.Button):

    def __init__(self, frameRef: tk.Frame):
        super().__init__(frameRef, text="Cancel", font=["Century Gothic", 20], command=self.closeWindow)

    def closeWindow(self):
        self.winfo_toplevel().destroy()

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
        tk.Label(self, text="Username:", font=["Century Gothic", 20]).grid(row=0, column=0)
        tk.Label(self, text="Password:", font=["Century Gothic", 20]).grid(row=1, column=0)
        tk.Label(self,text="Email Adress", font=["Century Gothic", 20]).grid(row=2, column=0)
        tk.Label(self,text="Phone Number", font=["Century Gothic", 20]).grid(row=3, column=0)

        self.usernameEntry = tk.Entry(self)
        self.usernameEntry.grid(row=0, column=1, columnspan=2)

        self.passwordEntry = tk.Entry(self)
        self.passwordEntry.grid(row=1, column=1, columnspan=2)

        self.emailEntry = tk.Entry(self)
        self.emailEntry.grid(row=2, column=1, columnspan=2)

        self.phoneNumEntry = tk.Entry(self)
        self.phoneNumEntry.grid(row=3, column=1, columnspan=2)

        cancelButton(self).grid(row=4, column=0)
        tk.Button(self, text="Register", font=["Century Gothic", 20], command=lambda: self.SubmitButtonClick()).grid(row=4, column=2)

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


class BasketFrame(tk.Frame):
    
    
    def __init__(self, windowRef: tk.Tk, givenUser : int, oldFrame: tk.Frame = None):
        if oldFrame is not None:
            oldFrame.destroy()
        super().__init__(windowRef)
        self.User = int(givenUser)
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
        db = ImazonDatabase("./Imazon.db")
        items = db.check_user_basket(self.User)
        items = [list(item) for item in items]
        tk.Label(self, text ="Items In Your Basket", font=["Century Gothic", 20]).grid(row=1, column=0)
        tk.Button(self, text= "Return", command= lambda: ShoppingFrame(self.master, self.User, self), font=["Century Gothic", 20]).grid(row=1, column=1)
        item_labels = []
        def add_item_and_increment(item_id, idx):
            db.add_to_basket(item_id, self.User)
            items[idx][3] += 1
            print(items[idx][3])
            item_labels[idx].config(text=f"{items[idx][1]} - {items[idx][2]} - {items[idx][3]}")
        def remove_and_decrease(item_id, idx):
            db.remove_from_basket(item_id, self.User)
            items[idx][3] -= 1
            print(items[idx][3])
            if items[idx][3] < 1:
                items[idx][3] = 0
            item_labels[idx].config(text=f"{items[idx][1]} - {items[idx][2]} - {items[idx][3]}")
        for i in range(len(items)):
            item_id = items[i][0]
            label = tk.Label(self, text=f"{items[i][1]} - {items[i][2]} - {items[i][3]}", font=["Century Gothic", 20])
            label.grid(row=i + 2, column=0)
            item_labels.append(label)
            tk.Button(self, text="+", font=["Century Gothic", 20],
                  command=lambda id=item_id, idx=i: add_item_and_increment(id, idx)).grid(row=i+2, column=1)
            tk.Button(self, text="-", font=["Century Gothic", 20],
                  command=lambda id=item_id, idx=i: remove_and_decrease(id, idx)).grid(row=i+2, column=2)
        


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
        tk.Label(self, text="Username:", font=["Century Gothic", 20]).grid(row=0, column=0)
        tk.Label(self, text="Password:", font=["Century Gothic", 20]).grid(row=1, column=0)

        self.usernameEntry = tk.Entry(self)
        self.usernameEntry.grid(row=0, column=1, columnspan=2)

        self.passwordEntry = tk.Entry(self)
        self.passwordEntry.grid(row=1, column=1, columnspan=2)

        cancelButton(self).grid(row=2, column=0)
        tk.Button(self, text="Login", font=["Century Gothic", 20], command=lambda: self.SubmitButtonClick()).grid(row=2, column=2)

    def SubmitButtonClick(self):
        username: str = self.usernameEntry.get()
        password: str = self.passwordEntry.get()

        print(username)
        print(password)
        db = ImazonDatabase("./Imazon.db")
        user_exists = db.check_account(username, password)
        if user_exists:
            ShoppingFrame(self.master,user_exists, self )
        else:
            label = tk.Label(self, text="Incorrect Username or Password", font=["Century Gothic", 20])
            label.grid(row=3, column=1, columnspan=3)
            self.after(1000, label.destroy)
        # valid = true

class ShoppingFrame(tk.Frame):

    itemSearch: tk.Entry

    def __init__(self, windowRef: tk.Tk, givenUser : int, oldFrame: tk.Frame = None):
        if oldFrame is not None:
            oldFrame.destroy()
        super().__init__(windowRef)
        self.User = int(givenUser)
        self.SetupLayout()
        self.pack(fill="both", expand=True)

    def view_Basket(self):
        BasketFrame(self.master,self.User,self)
    

    def SetupLayout(self):
        self.columnconfigure(6,weight=1)
        tk.Label(self, text ="Search:", font=["Century Gothic", 20]).grid(row=0, column=0)
        self.itemSearch = tk.Entry(self)
        self.itemSearch.grid(row=0, column=1, columnspan=2)
        tk.Button(self, text="Go", font=["Century Gothic", 20], command= lambda: self.SubmitButtonClick()).grid(row=0, column=3)
        tk.Button(self, text="Basket", font=["Century Gothic", 20], command= lambda: self.view_Basket()).grid(row=0, column=5)


    def SubmitButtonClick(self):
        tk.Button(self, text="Reset Search", font=["Century Gothic", 20], command=lambda: ShoppingFrame(self.master,self.User,self)).grid(row=0, column=6)
        db = ImazonDatabase("./Imazon.db")
        item: str = self.itemSearch.get().lower()
        data = db.execute("SELECT Product_ID, PName, PDescription, PPrice  FROM Product WHERE PName LIKE ?" , (item,))
        result = data.fetchall()
        print(result)
        print(self.User)
        tk.Label(self, text ="Items Found:", font=["Century Gothic", 20]).grid(row=1, column=0)
        for item in result:
            print(item[0])
            quantity = [0]
            item_id = item[0]
            label = tk.Label(self, text=f"{item[1]} - {item[2]} - {item[3]} - Added: {quantity[0]}", font=["Century Gothic", 20])
            label.grid(row=result.index(item) + 2, column=0)
            def add_and_increment(item_id=item_id, quantity=quantity, label=label):
                db.add_to_basket(item_id, self.User)
                quantity[0] += 1
                label.config(text=f"{item[1]} - {item[2]} - {item[3]} - Added: {quantity[0]}")
            def remove_and_increment(item_id=item_id, quantity=quantity, label=label):
                db.remove_from_basket(item_id, self.User)
                quantity[0] = max(quantity[0] - 1, 0)
                label.config(text=f"{item[1]} - {item[2]} - {item[3]} - Added: {quantity[0]}")
            tk.Button(self, text="+", font=["Century Gothic", 20], command=add_and_increment).grid(row=result.index(item)+2, column=1)
            tk.Button(self, text="-", font=["Century Gothic", 20], command=remove_and_increment).grid(row=result.index(item)+2, column=2)


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


