import tkinter as tk
from tkinter import ttk
import crud as crud 
from tkinter import messagebox

class Application(tk.Frame):
    def __init__ (self, master=None):
        
        super().__init__(master)
        widthness = round(self.winfo_screenwidth()/2)
        heightness = round(self.winfo_screenheight()/2)
        sizing = ('%sx%s' % (widthness, heightness))
        
        master.title('Products Table')
        master.geometry(sizing)
        self.objDB = crud.Products()
        
        self.pack()
        
        #Containers
        frame1 = tk.Frame(self)
        frame1.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
        
        frame2 = tk.Frame(self)
        frame2.pack(fill=tk.BOTH, expand=True)
        
        frame3 = tk.Frame(self)
        frame3.pack(side=tk.BOTTOM, padx=5)
        
        #Labels
        lblCode = tk.Label(frame1, text='Code')
        lblCode.grid(row=0, column=0)
        
        lblName = tk.Label(frame1, text='Name')
        lblName.grid(row=0, column=1)
        
        lblPrice = tk.Label(frame1, text='Price')
        lblPrice.grid(row=0, column=2)
        
        #Entries
        self.entry_code = tk.Entry(frame1)
        self.entry_code.grid(row=1, column=0)
        
        self.entry_name = tk.Entry(frame1)
        self.entry_name.grid(row=1, column=1, padx=10)

        self.entry_price = tk.Entry(frame1)
        self.entry_price.grid(row=1, column=2)

        #Insert Button at the top 
        btnInsert = tk.Button(frame1, text='Serach')
        btnInsert['command'] = self.insertProduct
        btnInsert.grid(row=0, column=3, rowspan=2, padx=10)
        
        #Treeview
        self.treeview = ttk.Treeview(frame2, columns=('Code:', 'Name:', 'Price:'))
        self.treeview.heading('#0', text='ROWID')
        self.treeview.heading('#1', text='Code:')
        self.treeview.heading('#2', text='Name:')
        self.treeview.heading('#3', text='Price:')
        
        #See database on treeview
        for row in crud.readProducts():
            self.treeview.insert('', 'end', text=[0], values=(row[1],row[2],row[3]))
            self.treeview.pack(fill=tk.BOTH, expand=True)
            
        #Bottom buttons 
        btnDelete = tk.Button(frame3, text='Delete')
        btnDelete['command']= self.deleteProduct
        btnDelete.pack(side='right')
        
    def insertProduct(self):
        code = self.entry_code.get()
        name = self.entry_name.get()
        price = self.entry_price.get()
        
        rowid = self.objDB = crud.Products()[0]
        self.treeview.insert('', 'end', text=rowid, values=(code, name, price))
    
    def deleteProduct(self):
        if not self.treeview.focus():
            messagebox('Error', 'No selected item')
        else:
            selected_item = self.treeview.focus()
            
            rowid = self.treeview.item(selected_item)
            
            self.objDB = crud.Products(rowid)