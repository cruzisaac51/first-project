from sqlite3.dbapi2 import Cursor
from tkinter import Button, PhotoImage, LabelFrame, Label,LEFT,Entry, StringVar, Tk, Toplevel,W,RIGHT,S,CENTER,N,E
from tkinter import ttk
from tkinter.constants import END, X, Y
from PIL import ImageTk, Image
import sqlite3
#create a class 
class product:
    db_name = "databease4P.db"

    def __init__(self,window):
        """this is the main window to open tkinter give the title and the icon for the window"""
        global Title_image
        self.wind = window
        self.wind.title("Isaac's Stores")
        self.wind.iconbitmap('store.ico')


        #frame for initial image 
        imgframe = LabelFrame(self.wind)
        imgframe.grid(row = 0, column = 0, columnspan = 3, pady = 20)
        #logo image
        Title_image = PhotoImage(file= "mainimg.PNG")
        labelimg= Label(imgframe, image = Title_image)
        labelimg.pack()
        
        
        #creating the frame for the products
        frame = LabelFrame(self.wind, text = "new product")
        frame.grid(row = 1, column = 0, columnspan = 3, pady = 20)
        

        #name input
        Label(frame, text = "name").grid(row=2, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=2, column=1)

        #price input
        Label(frame, text = "price:").grid(row=3,column=0)
        self.price = Entry(frame)
        self.price.grid(row=3, column=1)

        #button add product
        ttk.Button(frame, text = "save product", command = self.add_product).grid(row=4,columnspan= 2, sticky = W + E)

        #output messages
        self.message = Label(text = "", fg = "red")
        self.message.grid(row=4, column=0, columnspan=2,sticky = W + E)
        #table product
        self.tree = ttk.Treeview(height= 10, columns = 2)
        self.tree.grid(row=5, column= 0, columnspan=2, padx=15)
        self.tree.heading("#0",text="name",anchor= CENTER)
        self.tree.heading("#1", text="price", anchor = CENTER)
        
        #buttons
        ttk.Button(text="DELETE", command=self.delete_product).grid(row=6, column=0, sticky = W + E)
        ttk.Button(text="EDIT", command=self.edit_product).grid(row=6, column=1, sticky = W + E)

        #filling the row
        self.get_products()

    def run_query(self,query,parameters =()):
        '''function to run the query on database'''
        #open database
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query,parameters)
            conn.commit()
        return result


    def get_products(self):
        '''function to get the products form the table'''
        #cleaning tables
        records= self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        #query products
        query= "select * from product ORDER BY name DESC"
        db_rows = self.run_query(query)
        #filling data
        for row in db_rows:
            self.tree.insert("",0, text = row[1], values = row[2])

    def validate(self):
        return len(self.name.get()) !=0 and len(self.price.get()) !=0


    def add_product(self):
        '''function to add a product '''
        if self.validate():
            query= "INSERT INTO product VALUES(NULL,?,?)"
            parameters = (self.name.get(), self.price.get())
            self.run_query(query,parameters)
            self.message["text"] = "product {} added successfully".format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.message["text"] = "Name and price are required"
        self.get_products()

    def delete_product(self):
        '''function to delete the product from the database'''
        self.message["text"] = ""
        try:
            self.tree.item(self.tree.selection())["text"][0]
        except IndexError as e:
            self.message["text"] ="please select a record"
            return
        self.message["text"] = ""
        name = self.tree.item(self.tree.selection())["text"]
        query = "DELETE FROM product WHERE name=?"
        self.run_query(query, (name, ))
        self.message["text"] = "Record {} deleted successfully".format(name)
        self.get_products()

    def edit_product(self):
        '''fucntion to edit the products and display it  in the table also for the edit button'''
        self.message["text"] = ""
        try:
            self.tree.item(self.tree.selection())["text"][0]
        except IndexError as e:
            self.message["text"] ="please select a record"
            return
        name = self.tree.item(self.tree.selection())["text"]
        old_price = self.tree.item(self.tree.selection())["values"][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = "Edit Product"
        self.edit_wind.iconbitmap('store.ico')

        #frame edit product

        #old_name
        Label(self.edit_wind, text="old name: ").grid(row=0,column=1)
        Entry(self.edit_wind,textvariable= StringVar(self.edit_wind, value = name), state="readonly").grid(row=0,column=2)
        #new_name
        Label(self.edit_wind,text= "new name").grid(row=1,column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1,column=2)

        #old price
        Label(self.edit_wind,text="old price").grid(row=2,column=1)
        Entry(self.edit_wind,textvariable= StringVar(self.edit_wind, value = old_price), state="readonly").grid(row=2,column=2)
        #new price
        Label(self.edit_wind,text="new price").grid(row=3,column=1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row=3,column=2)

        #button save changes
        save_button = Button(self.edit_wind,text="Save Changes", command= lambda: self.edit_records(new_name.get(), name, new_price.get(),old_price))
        save_button.grid(row=4, column=2, sticky = W)

    def edit_records(self,new_name, name, new_price, old_price):
        '''function to edit the products on the database'''
        query = "UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?"
        parameters = (new_name, new_price, name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message["text"] = "Record {} updated successfully".format(name)
        self.get_products()


#call the program to start
if __name__ == "__main__":
    window = Tk()
    application = product(window)
    window.mainloop()
    