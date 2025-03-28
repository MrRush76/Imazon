import sqlite3
class Database():
    databaseRef: str

    def __init__(self, givenDatabaseRef: str):
        self.databaseRef = givenDatabaseRef

    def readAll(self, tableName: str):
        db = sqlite3.connect(self.databaseRef)
        data = db.execute("SELECT * FROM " + tableName)
        result = data.fetchall()
        db.close()
        return result

    def insertIntoTable(self, tableName: str, data: list) -> bool:
        db = sqlite3.connect(self.databaseRef)
        placeholders = ", ".join(["?"] * len(data))
        try:
            db.execute("INSERT INTO " + tableName + " VALUES (" + placeholders + ")", data)
            db.commit()
        except sqlite3.IntegrityError:
            db.close()
            return False
        db.close()
        return True


def create_tables(db):
    db.execute("CREATE TABLE IF NOT EXISTS Product ( Product_ID INTEGER PRIMARY KEY, PName TEXT NOT NULL, PDescription TEXT NOT NULL, PPrice TEXT NOT NULL)")
    db.execute("CREATE TABLE IF NOT EXISTS Basket ( Product_ID INTEGER, User_ID INTEGER, Quantity INTEGER,    FOREIGN KEY(Product_ID) REFERENCES Basket(Product_ID), FOREIGN KEY(User_ID) REFERENCES Customer(User_ID), PRIMARY KEY(Product_ID, User_ID))")
    db.execute("CREATE TABLE IF NOT EXISTS Customer ( User_ID INTEGER PRIMARY KEY, Username TEXT , Password TEXT NOT NULL, Email_Address TEXT NOT NULL, Contact_Number TEXT NOT NULL, FOREIGN KEY(Username) REFERENCES Basket(Username))")

class ImazonDatabase(Database):
    def __init__(self, db_path):
        super().__init__(db_path)
        self.create_tables()

    def create_tables(self):
        db = sqlite3.connect(self.databaseRef)
        create_tables(db)
        db.close()

    def insert_product(self, name, description, price):
        db = sqlite3.connect(self.databaseRef)
        data = db.execute("SELECT MAX(Product_ID) FROM Product")
        result = data.fetchone()[0]
        if result is not None:
            product_id = result + 1
        else:
            product_id = 1
        db.execute("INSERT INTO Product (Product_ID, PName, PDescription, PPrice) VALUES (?, ?, ?, ?)", (product_id, name, description, price))
        db.commit()
        db.close()

    def add_customer(self, username, password, email, contact_number):
        db = sqlite3.connect(self.databaseRef)
        data = db.execute("SELECT MAX(User_ID) FROM Customer")
        result = data.fetchone()[0]
        if result is not None:
            user_id = result + 1
        else:
            user_id = 1
        db.execute("INSERT INTO Customer (user_id, Username, Password, Email_Address, Contact_Number) VALUES (?, ?, ?, ?,?)", (user_id, username, password, email, contact_number))
        db.commit()
        db.close()

    def add_to_basket(self, product_id, user_id):
        db = sqlite3.connect(self.databaseRef)
        db.execute("INSERT INTO Basket (Product_ID, user_id) VALUES (?, ?)", (product_id, user_id))
        db.commit()
        db.close()

    def check_account(self, username, password):
        db = sqlite3.connect(self.databaseRef)
        data = db.execute("SELECT * FROM Customer WHERE Username = ? AND Password = ?", (username, password))
        result = data.fetchall()
        db.close()
        if result:
            return True
        return False

    def check_user_basket(self, username):
        db = sqlite3.connect(self.databaseRef)
        data = db.execute("SELECT DISTINCT User_ID FROM Basket")
        cIds = data.fetchall()
        for cId in cIds:
            data = db.execute("SELECT PName FROM Product INNER JOIN Basket ON Product.Product_ID = Basket.Product_ID WHERE Basket.User_ID = ?", (username,))
            result = data.fetchall()
            if result:
                break
        result = data.fetchall()
        db.close()
        return result

# Sample products
db = ImazonDatabase("./Imazon.db")
db.insert_product("Laptop", "A high-performance laptop", 999.99)
db.insert_product("Smartphone", "A latest model smartphone", 699.99)
db.insert_product("Headphones", "Noise-cancelling headphones", 199.99)
db.insert_product("Tablet", "A lightweight tablet", 299.99)
db.insert_product("Smartwatch", "A smartwatch with various features", 199.99)
db.insert_product("Camera", "A digital camera with high resolution", 499.99)
db.insert_product("Printer", "A wireless printer", 149.99)
db.insert_product("Monitor", "A 24-inch monitor", 179.99)
db.insert_product("Keyboard", "A mechanical keyboard", 99.99)
db.insert_product("Mouse", "A wireless mouse", 49.99)


def menu():
    db = ImazonDatabase("./Imazon.db")
    print("Welcome to Imazon!")
    print("1. Add Product")
    print("2. Add Customer")
    print("3. Add to Basket")
    print("4. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        product_id = input("Enter Product ID: ") # autogen
        name = input("Enter Product Name: ")
        description = input("Enter Product Description: ")
        price = float(input("Enter Product Price: "))
        db.insert_product(product_id, name, description, price)
        print("Product added successfully.")
        menu()
    elif choice == "2":
        # autogen something
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        email = input("Enter Email Address: ")
        contact_number = input("Enter Contact Number: ")
        db.add_customer(username, password, email, contact_number)
        print("Customer added successfully.")
        menu()
    elif choice == "3":
        product_id = input("Enter Product ID: ")
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        if not db.check_account(username, password):
            print("Invalid username or password.")
            menu()
            return
        db.add_to_basket(product_id, username)
        print("Product added to basket.")
        menu()
    elif choice == "4":
        username = input("Enter Username: ")
        check = db.check_user_basket(username)
        if check:
            print("Products in your basket:")
            for product in check:
                print(product[0])
        else:
            print("Your basket is empty.")
    elif choice == "5":
        print("Exiting...")
        exit()

    else:
        print("Invalid choice, please try again.")
        menu()

if __name__ == "__main__":
    menu()

