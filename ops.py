import sqlite3
import tkinter as tk
import tkinter.ttk as tkk
from tkinter import messagebox

#CRUD
class ConnectDB:
    def __init__(self):
        self.conn = sqlite3.connect('db.sqlite3')
        self.cur = self.conn.cursor()
        self.create_table()
        
    def create_table(self):
        try:
            self.cur.execute('''CREATE TABLE IF NOT EXISTS products (
                name TEXT,
                price INT,
                valid TEXT
            )''')
            
        except Exception as error:
            print('\nUnable to create\n', error)
        else:
            print('\nTable created\n')
    
    def insertRecord(self, name, price, valid):
        try:
            self.cur.execute('''INSERT INTO products VALUES (?,?,?)''', (name, price, valid))
        except Exception as error:
            print('\nUnable to insert\n', error)
        else:
            self.conn.commit()
            print('Record inserted')
#Read all    
    def readRecord(self):
        return self.cur.execute('SELECT rowid, * FROM products').fetchall()
#Read last row id     
    def readLastRec(self):
        return self.cur.execute('SELECT MAX(rowid) FROM products').fetchone()
    
    '''def updateRecord(self,rowid):
        try:
            self.cur.execute("UPDATE products SET name=?, price=?, valid=? WHERE rowid=?",(rowid,))
        except Exception as error:
            print('\nUnable to update\n', error)        
        else:
            self.conn.commit()
            print('\nRecord Updated\n')'''

    def updateRecord(self, name, price, valid, rowid):
        try:
            self.cur.execute("UPDATE products SET name=?, price=?, valid=? WHERE rowid=?", (name, price, valid, rowid))
        except Exception as error:
            print('\nUnable to update\n', error)
        else:
            self.conn.commit()
            print('\nRecord Updated\n')
          
    def deleteRecord(self, rowid):
        try:
            self.cur.execute("DELETE FROM products WHERE rowid=?", (rowid,))
        except Exception as error:
            print('\nUnable to delete\n', error)
        else:
            self.conn.commit()            
            print('\nRecord deleted\n')

#GUI             
class Window(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        #Collecting info according to monitor
        m_width = round(self.winfo_screenwidth()/2)
        m_height = round(self.winfo_screenheight()/2)
        m_size = ('%sx%s' % (m_width,m_height))
        master.title('Products')
        master.geometry(m_size)
        #Instace of DB
        self.dbApp = ConnectDB()
        self.pack()
        #Calling widgets
        self.create_widgets()
        
    def create_widgets(self):
        #Containers
        frame1 = tk.Frame(self)
        frame1.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)

        frame2 = tk.Frame(self)
        frame2.pack(fill=tk.BOTH, expand=True)

        frame3 = tk.Frame(self)
        frame3.pack(side=tk.BOTTOM, padx=5)

        # Labels.
        lblCode = tk.Label(frame1, text='Name')
        lblCode.grid(row=0, column=0)

        lblName = tk.Label(frame1, text='Price')
        lblName.grid(row=0, column=1)

        lblPrice = tk.Label(frame1, text='Valid')
        lblPrice.grid(row=0, column=2)
        
        #Entries
        self.txtName=tk.Entry(frame1)
        self.txtName.grid(row=1, column=0)
        
        self.txtPrice=tk.Entry(frame1)
        self.txtPrice.grid(row=1, column=1, padx=10)
        
        self.txtValid=tk.Entry(frame1)
        self.txtValid.grid(row=1, column=2)
        
        #Buttons
        btnInsert=tk.Button(frame1, text=' Add ', bg='green', fg='white')
        btnInsert['command']=self.insertProduct
        btnInsert.grid(row=0, column=3, rowspan=2, padx=10)
        
        btnClear=tk.Button(frame1, text='Clear', bg='blue', fg='white')
        btnClear['command']=self.clearScrn
        btnClear.grid(row=0, column=4, rowspan=2, padx=10)
        
        btnUpdate=tk.Button(frame3, text=' Alter ',bg='blue', fg='white')
        btnUpdate['command']=self.updateProduct
        btnUpdate.pack(pady=25)
        
        btnDelete=tk.Button(frame3, text='Remove',bg='red', fg='white')
        btnDelete['command']=self.deleteProduct
        btnDelete.pack(pady=35)
        
        #Treeview
        self.treeView = tkk.Treeview(frame2, columns=('Name','Price','Valid'))
        self.treeView.heading('#0', text='Code')
        self.treeView.heading('#1', text='Name')
        self.treeView.heading('#2', text='Price')
        self.treeView.heading('#3', text='Valid')
        
        #To see data from base on treeview
        for row in self.dbApp.readRecord():
            self.treeView.insert('', 'end', text=row[0], values=(row[1], row[2], row[3]))
            
            self.treeView.pack(fill=tk.BOTH, expand=True)
            
        self.treeView.bind('<<TreeviewSelect>>', self.showSelectedRecord)
            

    #Treeview operations
    def showSelectedRecord(self, event):
        self.clearScrn()
        for selection in self.treeView.selection():
            item=self.treeView.item(selection)
            name, price, valid = item['values'] [0:3]
            self.txtName.insert(0, name)
            self.txtPrice.insert(0, price)
            self.txtValid.insert(0, valid)    
        
    def insertProduct(self):       
        name = self.txtName.get()
        price = self.txtPrice.get()
        valid = self.txtValid.get()
        #Inserting typed data on db
        self.dbApp.insertRecord(name=name, price=price, valid=valid)
        #Collecting last row id inserted 
        rowid=self.dbApp.readLastRec()[0]
        #Adding new data on treeview 
        self.treeView.insert('', 'end', text=rowid, values=(name, price, valid))
                   
    def updateProduct(self):
        #Get the selected item from the treeview
        selected_item = self.treeView.selection()
        
        if selected_item:
            #Get the values of the selected item
            values = self.treeView.item(selected_item)['values']
            
            #Get the rowid of the selected item
            rowid = self.treeView.item(selected_item)['text']
            
            #Get the updated values from the entries
            name = self.txtName.get()
            price = self.txtPrice.get()
            valid = self.txtValid.get()
            
            #Check if all fields are filled
            if name and price and valid:
                #Update the record in the database
                self.dbApp.updateRecord(name, price, valid, rowid)
                
                #Update the selected item in the treeview
                self.treeView.item(selected_item, text=rowid, values=(name, price, valid))
            else:
                messagebox.showerror('Error', 'All fields are required.')
        else:
            messagebox.showerror('Error', 'Please select a product to update.')
            
                       
    def deleteProduct(self):
        #Checking if item is selected
        if not self.treeView.focus():
            messagebox.showerror('Fail', 'No item selected!')
        else:
            selected_i = self.treeView.focus()    
            rowid = self.treeView.item(selected_i)
            #Removing it from db
            self.dbApp.deleteRecord(rowid['text'])
            #Removing it from tree
            self.treeView.delete(selected_i) 
            
    
    def clearScrn(self):
        self.txtName.delete(0, tk.END)
        self.txtPrice.delete(0, tk.END)
        self.txtValid.delete(0, tk.END)
            
root = tk.Tk()
app = Window(master=root)
app.mainloop()   
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            