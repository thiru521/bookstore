import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql

class book():
    def __init__(self, root):
        self.root = root
        self.root.title("Book Store")

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        title = tk.Label(self.root, text="Book store Management", bd=4, relief="groove", bg="gray", fg="cyan", font=["Elephant", 45, "italic"])
        title.pack(side="top", fill="x")

        #AddFrame

        addFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(100,140,240))
        addFrame.place(width=self.width/3, height=self.height-180, x=70, y=100)

        nameLbl = tk.Label(addFrame, text="Book_Name:", bg=self.clr(100,140,240), font=("Arial", 15, "bold"))
        nameLbl.grid(row=0, column=0, padx=20, pady=30)
        self.name = tk.Entry(addFrame, bd=2, width=18, font=("Ariel",20))
        self.name.grid(row=0, column=1, padx=10, pady=30)
        
        ediLbl = tk.Label(addFrame, text="Edition:", bg=self.clr(100,140,240), font=("Arial", 15, "bold"))
        ediLbl.grid(row=1, column=0, padx=20, pady=30)
        self.edition = tk.Entry(addFrame, bd=2, width=18, font=("Arial", 20))
        self.edition.grid(row=1, column=1, padx=10, pady=30)

        priceLb1 = tk.Label(addFrame, text="Price:", bg=self.clr(100,140,240), font=("Arial", 15, "bold"))
        priceLb1.grid(row=2, column=0, padx=20, pady=30)
        self.price = tk.Entry(addFrame, bd=2, width=18, font=("Arial", 20))
        self.price.grid(row=2, column=1, padx=10, pady=30)

        quantLbl = tk.Label(addFrame, text="Quantity:", bg=self.clr(100,140,240), font=("Arial", 15, "bold"))
        quantLbl.grid(row=3, column=0, padx=20, pady=30)
        self.quantity = tk.Entry(addFrame, bd=2, width=18, font=("Arial", 20))
        self.quantity.grid(row=3, column=1, padx=10, pady=30)

        addBtn = tk.Button(addFrame, command=self.insertFun,  text="Add_Book", width=20, bd=3, relief="raised", font=("Arial", 20, "bold"))
        addBtn.grid(row=4, column=0, padx=30, pady=40, columnspan=2)


        #detail Frame

        self.detFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(100,240,140))
        self.detFrame.place(width=self.width/2, height=self.height-180, x=self.width/3+140, y=100)

        nameLbl = tk.Label(self.detFrame, text="Book_Name:", bg=self.clr(100,240,140), font=("Arial", 15, "bold"))
        nameLbl.grid(row=0, column=0, padx=10, pady=20)
        self.name2 = tk.Entry(self.detFrame, bd=2, width=16, font=("Arial", 15))
        self.name2.grid(row=0, column=1, padx=5, pady=20)

        optLbl = tk.Label(self.detFrame, text="Edition:", bg=self.clr(100,240,140), font=("Arial", 15, "bold"))
        optLbl.grid(row=0, column=3, padx=10, pady=20)
        self.options = ttk.Combobox(self.detFrame, width=20, font=("Arial", 15), values=("First", "Second", "Third"))
        self.options.set("select Edition")
        self.options.grid(row=0, column=4, padx=5, pady=20)

        btnFrame = tk.Frame(self.detFrame, bd=3, relief="ridge", bg=self.clr(140, 210, 120))
        btnFrame.place(width=self.width/2-20, height=70, x=8, y=60)

        srchBtn = tk.Button(btnFrame, command=self.srchFun, text="Search", width=10, bd=3, relief="raised", font=("Arial", 15, "bold"))
        srchBtn.grid(row=0, column=0, padx=25, pady=10)
        
        allBtn = tk.Button(btnFrame, command=self.showAllFun, text="Show_All", width=10, bd=3, relief="raised", font=("Arial", 15, "bold"))
        allBtn.grid(row=0, column=1, padx=25, pady=10)

        purBtn = tk.Button(btnFrame, command=self.purFun, text="Purchase", width=10, bd=3, relief="raised", font=("Arial", 15, "bold"))
        purBtn.grid(row=0, column=2, padx=25, pady=10)
        
        delBtn = tk.Button(btnFrame, command=self.delFun, text="Remove", width=10, bd=3, relief="raised", font=("Arial", 15, "bold"))
        delBtn.grid(row=0, column=3, padx=25, pady=10)

        self.tabFun()

    def tabFun(self):
        tabFrame = tk.Frame(self.detFrame, bd=4, relief="sunken", bg="cyan")
        tabFrame.place(width=self.width/2-40, height=self.height-350, x=17, y=150) 

        x_scrol = tk.Scrollbar(tabFrame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol = tk.Scrollbar(tabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")  

        self.table= ttk.Treeview(tabFrame, xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set, columns=("name", "edi", "price", "quant"))

        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)

        self.table.heading("name", text="book")
        self.table.heading("edi", text="Edition")
        self.table.heading("price", text="price")
        self.table.heading("quant", text="Quantity")
        self.table["show"]= "headings"

        self.table.pack(fill="both", expand=1)

    def insertFun(self):
        name = self.name.get() 
        edi = self.edition.get()
        pri = self.price.get()
        qu = self.quantity.get()  

        if name and edi and pri and qu:
            price = int(pri)
            quantity = int(qu)

            try:
               self.dbFun()
               self.cur.execute("insert into books(name, edition, price, quant) values(%s,%s,%s,%s)",(name,edi,price,quantity))
               self.con.commit()
               tk.messagebox.showinfo("Success", f"Book.{name} is Added Successfully in Store!")

               self.cur.execute("select * from books where name=%s",name)
               row = self.cur.fetchone()

               self.table.delete(*self.table.get_children())
               self.table.insert('',tk.END,values=row)
                
               self.name.delete(0, tk.END) 
               self.edition.delete(0, tk.END)
               self.price.delete(0, tk.END)
               self.quantity.delete(0, tk.END)

               self.con.close()

            except Exception as e:   
                tk.messagebox.showerror("Error", f"Error: {e}") 

        else:
            tk.messagebox.showwarning("warning", "Please Fill All Input Fields!")

    def srchFun(self):
        name = self.name2.get()        
        opt = self.options.get()

        try:
           self.dbFun()
           self.cur.execute("select * from books where name=%s and edition=%s", (name,opt))
           row = self.cur.fetchone()
           if row:
              self.table.delete(*self.table.get_children())
              self.table.insert('',tk.END,values=row)

              self.con.close()
           else:
               tk.messagebox.showerror("Error",f"Book.{name} or Edition.{opt} is invalid")    

        except Exception as e:   
                tk.messagebox.showerror("Error", f"Error: {e}")  

    def showAllFun(self):
        try:
             self.dbFun()
             self.cur.execute("Select * from books")
             data = self.cur.fetchall()
             self.table.delete(*self.table.get_children())

             for i in data:
                self.table.insert('',tk.END,values=i)

             self.con.close()   
                  
        except Exception as e:   
                tk.messagebox.showerror("Error", f"Error: {e}")

    def purFun(self):
        name = self.name2.get()
        opt = self.options.get()
        try:
            self.dbFun()
            self.cur.execute("select price,quant from books where name=%s and edition=%s",(name,opt))
            row = self.cur.fetchone()

            if row[1] > 0:
               upd = row[1]-1
               self.cur.execute("update books set quant=%s where name=%s and edition=%s",(upd,name,opt))                 
               self.con.commit()
               tk.messagebox.showinfo("Success", f"You Have Purchased Book.{name} of {opt} Edition\nYou Have To Pay.{row[0]}$")

               self.cur.execute("select * from books where name=%s and edition=%s",(name,opt)) 
               row = self.cur.fetchone()

               self.table.delete(*self.table.get_children())
               self.table.insert('',tk.END,values=row)

               self.con.close() 

            else:
                tk.messagebox.showwarning("Warning",f"sorry book.{name} of {opt} edition is no more available!")   

        except Exception as e:   
           tk.messagebox.showerror("Error", f"Error: {e}") 

    def delFun(self):
        name = self.name2.get()
        opt = self.options.get()

        try:
            self.dbFun()
            self.cur.execute("delete from books where name=%s and edition=%s",(name,opt)) 
            self.con.commit() 

            self.table.delete(*self.table.get_children())
            tk.messagebox.showinfo("Success",f"Book.{name} of {opt} edition removed from stored") 

            self.con.close()
          
        except Exception as e:   
           tk.messagebox.showerror("Error", f"Error: {e}") 

    def dbFun(self):
            self.con = pymysql.connect(host="localhost", user="root", password="root", database="books")  
            self.cur = self.con.cursor()



    def clr(self,r,g,b):
        return f"#{r:02x}{g:02x}{b:02x}"

root = tk.Tk()
obj = book(root)
root.mainloop()