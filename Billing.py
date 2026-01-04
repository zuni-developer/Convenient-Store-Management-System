from tkinter import *
import winsound
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import time
import os
import tempfile
from tkinter import filedialog

class BillClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x720+100+30")
        self.root.title("Inventory Management System | Developed by Xeven")
        self.root.config(bg="#faf4e9")
        self.cartList = []
        self.printCheck=0

        # ===== Title Bar =====
        img = Image.open("image/logo.png")
        img = img.resize((50, 50), Image.LANCZOS)  # width=50, height=50

        self.icon_title = ImageTk.PhotoImage(img)
        title = Label(self.root, text="Convenient Store Management System",image=self.icon_title,compound=LEFT, font=("poppins", 30, "bold"),
                      bg="#575C49", fg="#faf4e9", padx=20,pady=15, justify=CENTER, )
        title.pack(side = TOP, fill = X)



        # ===== Clock Bar =====
        self.lbl_clock = Label(
            self.root,
            text="Welcome to Convenient Store Management System\t\tDate: DD-MM-YYYY\t\tTime: HH:MM:SS",
            font=("Poppins", 15),
            bg="#6B858C",
            fg="#faf4e9"
        )
        self.lbl_clock.place(x=0, y=84, relwidth=1, height=40)

        self.update_clock()

        #====== Product Frame ======
        self.searchVar = StringVar()
        ProductFrame1 = Frame(self.root, bd= 4, relief= RIDGE, bg ="#faf4e9")
        ProductFrame1.place( x = 6, y = 130, width = 410, height = 550)

        pTitle = Label(ProductFrame1, text = "All Products", font = ("poppin", 18, "bold"),bg="#456578",fg="#faf4e9").pack(side=TOP, fill=X)

        ProductFrame2 = Frame(ProductFrame1,relief= RIDGE, bg ="#faf4e9")
        ProductFrame2.place( x = 2, y = 42, width = 398, height = 90)

        lbl_search = Label(ProductFrame2, text="Search Product | By Name", font=("poppin", 15, "bold"), bg="#faf4e9", fg= "green").place(x=2, y=5)
        lbl_pname = Label(ProductFrame2, text="Product Name", font=("poppin", 13, "bold"), bg="#faf4e9").place(x=2, y=45)
        entry_search = Entry(ProductFrame2, textvariable= self.searchVar, font=("poppin", 13), bg="#d3d8cc").place(x=126, y=47, width=150, height=22)
        btn_search = Button(ProductFrame2, text="Search",command=self.search,cursor="hand2", font=("poppin", 13), bg="#6CB1AA", fg="#faf4e9").place(x= 284, y= 45, width=100, height=25 )
        btn_show_all = Button(ProductFrame2, text="Show All",command=self.show,cursor="hand2", font=("poppin", 13), bg="#C17C45", fg="#faf4e9").place(x= 284, y= 10, width=100, height=25 )

        style = ttk.Style()
        style.theme_use("default")

        # Change table background colors
        style.configure(
            "Treeview",
            background="#faf4e9",       # background of rows
            foreground="black",
            rowheight=25,
            fieldbackground="#faf4e9"   # background of empty area
        )

        # Change header color
        style.configure(
            "Treeview.Heading",
            background="#faf4e9",       # header background
            foreground="black",
            font=("Poppins", 11, "bold")
        )

        # Change selected row color
        style.map(
            "Treeview",
            background=[("selected", "#faf4e9")],
            foreground=[("selected", "#3C3C3C")]
        )
        
        ProductFrame3 = Frame(ProductFrame1, bd= 3, relief= RIDGE)
        ProductFrame3.place(x=2, y=140, width= 398, height= 380)

        scrolly = Scrollbar(ProductFrame3, orient=VERTICAL)
        scrollx = Scrollbar(ProductFrame3, orient=HORIZONTAL)

        self.productTable = ttk.Treeview(ProductFrame3, columns=("pid","name", "price", "qty", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.productTable.xview)
        scrolly.config(command=self.productTable.yview)

        self.productTable.heading("pid", text="PID")
        self.productTable.heading("name", text="Name")
        self.productTable.heading("price", text="Price")
        self.productTable.heading("qty", text="Quantity")
        self.productTable.heading("status", text="Status")
        self.productTable["show"] = "headings"

        self.productTable.column("pid", width=50)
        self.productTable.column("name", width=100)
        self.productTable.column("price", width=100)
        self.productTable.column("qty", width=70)
        self.productTable.column("status", width=100)
        self.productTable.pack(fill=BOTH, expand=1)
        self.productTable.bind("<ButtonRelease-1>", self.get_data)

        lbl_note = Label(ProductFrame1, text="NOTE: Enter 0 quantity to remove item from cart", font=("poppin", 12), bg= "#faf4e9", fg="red").pack(side=BOTTOM, fill=X)

        #====== Customer Frame ======
        self.cnameVar = StringVar()
        self.contactVar = StringVar()

        CustomerFrame = Frame(self.root, bd= 4, relief= RIDGE, bg ="#faf4e9")
        CustomerFrame.place( x = 420, y = 130, width = 530, height = 70)

        cTitle = Label(CustomerFrame, text = "Customer Details", font = ("poppin", 13),bg="lightgray").pack(side=TOP, fill=X)

        lbl_cname = Label(CustomerFrame, text="Name", font=("poppin", 13), bg="#faf4e9").place(x=5, y=35)
        entry_cname = Entry(CustomerFrame, textvariable= self.cnameVar, font=("poppin", 13), bg="#d3d8cc").place(x=80, y=35, width=180)

        lbl_contact = Label(CustomerFrame, text="Contact", font=("poppin", 13), bg="#faf4e9").place(x=270, y=35)
        entry_contact = Entry(CustomerFrame, textvariable= self.contactVar, font=("poppin", 13), bg="#d3d8cc").place(x=350, y=34, width=140)

        #====== Calculator and Cart Frame ======
        Cal_Cart_frame = Frame(self.root, bd= 2, relief= RIDGE, bg ="#faf4e9")
        Cal_Cart_frame.place( x = 420, y = 205, width = 530, height = 360)


        #========= Calculator Frame ============
        self.calInputVar = StringVar()

        CalFrame = Frame(Cal_Cart_frame, bd= 9, relief= RIDGE, bg ="#faf4e9")
        CalFrame.place( x = 5, y = 10, width = 268, height = 340)

        cal_input = Entry(CalFrame, textvariable = self.calInputVar, font=("arial", 15, "bold"), width= 21, bd=10, relief=GROOVE, state="readonly", justify= RIGHT)
        cal_input.grid(row=0, columnspan=4)

        btn_7 = Button(CalFrame, text='7', font=("arial", 15, "bold"),command=lambda: self.get_cal_input(7), width= 4, bd=5, pady=12, cursor="hand2").grid(row=1, column=0)
        btn_8 = Button(CalFrame, text='8', font=("arial", 15, "bold"),command=lambda: self.get_cal_input(8), width= 4, bd=5, pady=12, cursor="hand2").grid(row=1, column=1)
        btn_9 = Button(CalFrame, text='9', font=("arial", 15, "bold"),command=lambda: self.get_cal_input(9), width= 4, bd=5, pady=12, cursor="hand2").grid(row=1, column=2)
        btn_plus = Button(CalFrame, text='+', font=("arial", 15, "bold"),command=lambda: self.get_cal_input('+'), width= 4, bd=5, pady=12, cursor="hand2").grid(row=1, column=3)

        btn_4 = Button(CalFrame, text='4', font=("arial", 15, "bold"),command=lambda: self.get_cal_input(4), width= 4, bd=5, pady=12, cursor="hand2").grid(row=2, column=0)
        btn_5 = Button(CalFrame, text='5', font=("arial", 15, "bold"),command=lambda: self.get_cal_input(5), width= 4, bd=5, pady=12, cursor="hand2").grid(row=2, column=1)
        btn_6 = Button(CalFrame, text='6', font=("arial", 15, "bold"),command=lambda: self.get_cal_input(6), width= 4, bd=5, pady=12, cursor="hand2").grid(row=2, column=2)
        btn_minus = Button(CalFrame, text='-', font=("arial", 15, "bold"),command=lambda: self.get_cal_input('-'), width= 4, bd=5, pady=12, cursor="hand2").grid(row=2, column=3)

        btn_1 = Button(CalFrame, text='1', font=("arial", 15, "bold"),command=lambda: self.get_cal_input(1), width= 4, bd=5, pady=12, cursor="hand2").grid(row=3, column=0)
        btn_2 = Button(CalFrame, text='2', font=("arial", 15, "bold"),command=lambda: self.get_cal_input(2), width= 4, bd=5, pady=12, cursor="hand2").grid(row=3, column=1)
        btn_3 = Button(CalFrame, text='3', font=("arial", 15, "bold"),command=lambda: self.get_cal_input(3), width= 4, bd=5, pady=12, cursor="hand2").grid(row=3, column=2)
        btn_mul = Button(CalFrame, text='x', font=("arial", 15, "bold"),command=lambda: self.get_cal_input('*'), width= 4, bd=5, pady=12, cursor="hand2").grid(row=3, column=3)

        btn_0 = Button(CalFrame, text='0', font=("arial", 15, "bold"),command=lambda: self.get_cal_input(0), width= 4, bd=5, pady=12, cursor="hand2").grid(row=4, column=0)
        btn_c = Button(CalFrame, text='C', font=("arial", 15, "bold"),command=lambda: self.clear_cal_input(), width= 4, bd=5, pady=12, cursor="hand2").grid(row=4, column=1)
        btn_eq = Button(CalFrame, text='=', font=("arial", 15, "bold"),command=lambda: self.perform_cal(), width= 4, bd=5, pady=12, cursor="hand2").grid(row=4, column=2)
        btn_div = Button(CalFrame, text='/', font=("arial", 15, "bold"),command=lambda: self.get_cal_input('/'), width= 4, bd=5, pady=12, cursor="hand2").grid(row=4, column=3)

        # cart frame copy
        CartFrame = Frame(Cal_Cart_frame, bd= 3, relief= RIDGE)
        CartFrame.place(x=280, y=8, width= 245, height= 342)
        self.cartTitle = Label(CartFrame, text = "Cart \t Total Product: [0]", font = ("poppin", 13),bg="lightgray")
        self.cartTitle.pack(side=TOP, fill=X)

        scrolly = Scrollbar(CartFrame, orient=VERTICAL)
        scrollx = Scrollbar(CartFrame, orient=HORIZONTAL)

        self.cartTable = ttk.Treeview(CartFrame, columns=("pid","name", "price", "qty"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.cartTable.xview)
        scrolly.config(command=self.cartTable.yview)

        self.cartTable.heading("pid", text="PID")
        self.cartTable.heading("name", text="Name")
        self.cartTable.heading("price", text="Price")
        self.cartTable.heading("qty", text="Qty")
        self.cartTable["show"] = "headings"

        self.cartTable.column("pid", width=40)
        self.cartTable.column("name", width=90)
        self.cartTable.column("price", width=90)
        self.cartTable.column("qty", width=40)
        self.cartTable.pack(fill=BOTH, expand=1)
        self.cartTable.bind("<ButtonRelease-1>", self.get_data_cart)
        

        #======== Add Cart Frame =========
        self.idVar = StringVar()
        self.pnameVar = StringVar()
        self.qtyVar = StringVar()
        self.priceVar = StringVar()
        self.stockVar = StringVar()

        AddCartFrame = Frame(self.root, bd= 2, relief= RIDGE, bg ="#faf4e9")
        AddCartFrame.place( x = 420, y = 570, width = 530, height = 110)

        pName = Label(AddCartFrame, text="Product Name", font=("poppin", 13), bg="#faf4e9").place(x=10, y=5)
        add_pname = Entry(AddCartFrame, textvariable= self.pnameVar, font=("poppin", 13), bg="#DEC7B6", state="readonly").place(x=12, y=35, width=190, height=22)

        pPrice = Label(AddCartFrame, text="Price per Quantity", font=("poppin", 13), bg="#faf4e9").place(x=220, y=5)
        add_pprice = Entry(AddCartFrame, textvariable= self.priceVar, font=("poppin", 13), bg="#DEC7B6", state="readonly").place(x=220, y=35, width=150, height=22)

        pQty = Label(AddCartFrame, text="Quantity", font=("poppin", 13), bg="#faf4e9").place(x=390, y=5)
        add_pqty = Entry(AddCartFrame, textvariable= self.qtyVar, font=("poppin", 13), bg="#d3d8cc").place(x=390, y=35, width=100, height=22)

        self.lbl_inStock = Label(AddCartFrame, text="In Stock", font=("poppin", 13), bg="#faf4e9")
        self.lbl_inStock.place(x=10, y=70)

        btn_clear = Button(AddCartFrame, text="Clear", font=("poppin", 13,"bold"), bg="#AF5B51", cursor="hand2", fg="#faf4e9").place(x=150, y=67, width=150, height=30)
        btn_addCart = Button(AddCartFrame, text="Add | Update",command=self.add_cart, font=("poppin", 13,"bold"), bg="#898561", cursor="hand2", fg="#faf4e9").place(x=320, y=67, width=180, height=30)

        #========== Billing frame ========

        billFrame = Frame(self.root,bd= 2, relief= RIDGE, bg ="#faf4e9" )
        billFrame.place(x= 953, y= 130, width=390, height=410)

        bTitle = Label(billFrame, text = "Customer Billing Area", font = ("poppin", 15, "bold"),bg="#6C4F4F",fg="#faf4e9").pack(side=TOP, fill=X)

        scrolly = Scrollbar(billFrame, orient = VERTICAL)
        scrolly.pack(side=RIGHT, fill= Y)

        self.txt_bill_area = Text(billFrame, yscrollcommand= scrolly.set, bg= "#faf4e9")
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview )

        #========== Bill Buttons frame ========

        billButtons = Frame(self.root,bd= 2, relief= RIDGE, bg ="#faf4e9" )
        billButtons.place(x= 953, y= 540, width=390, height=140)

        self.lbl_amount = Label(billButtons, text='Total Amount\n[0]', font=('poppin', 13, 'bold'), fg= '#faf4e9', bg="#538B85")
        self.lbl_amount.place(x =4, y=5, width= 130, height=70)

        self.lbl_dis = Label(billButtons, text='Discount\n[5%]', font=('poppin', 13, 'bold'), fg= '#faf4e9', bg="#898561")
        self.lbl_dis.place(x =137, y=5, width= 120, height=70)

        self.lbl_pay = Label(billButtons, text='Net Pay\n[0]', font=('poppin', 13, 'bold'), fg= '#faf4e9', bg="#C17C45")
        self.lbl_pay.place(x =260, y=5, width= 120, height=70)

        btn_print = Button(billButtons, command=self.print_bill, text='Print Bill', font=('poppin', 13, 'bold'),cursor="hand2", fg= '#faf4e9', bg="#AF5B51")
        btn_print.place(x =4, y=80, width= 130, height=50)

        btn_clear = Button(billButtons, text='Clear',command=self.clear_all, font=('poppin', 13, 'bold'),cursor="hand2", fg= '#faf4e9', bg="#95676c")
        btn_clear.place(x =137, y=80, width= 120, height=50)

        btn_generate = Button(billButtons, text='Generate', command=self.generate_bill, font=('poppin', 13, 'bold'), cursor="hand2",fg= '#faf4e9', bg="#456578")
        btn_generate.place(x =260, y=80, width= 120, height=50)

        #=============Footer==============
        footer = Label(self.root, text="Atika Lodhi | Manal Mubashir | Zona Zaib | Summaiya Khurram", font=("poppin", 10), bg="#4d6363", fg="#faf4e9").pack(side=BOTTOM, fill=X)

        self.show()
        #=========================All Functions====================================

    def get_cal_input(self, num):
        xnum = self.calInputVar.get() + str(num)
        self.calInputVar.set(xnum)
    
    def clear_cal_input(self):
        self.calInputVar.set('')
   
    def perform_cal(self):
        result = self.calInputVar.get()
        self.calInputVar.set(eval(result))
           
    def show(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT pid, name, price, qty, status FROM product WHERE status = 'Active'")
            rows=cur.fetchall()
            #======SQLITE WALA Employee Table k bat hori h========#
            self.productTable.delete(*self.productTable.get_children())
            #====rows blue hoga sqloite table related===#
            for row in rows:
                self.productTable.insert('',END,values=row)
        
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def search(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            if self.searchVar.get() == "":
                messagebox.showerror("Error", "Search input is required.", parent = self.root)
            else:
                cur.execute("SELECT pid, name, price, qty, status FROM product WHERE name LIKE '%"+self.searchVar.get()+"%'")
                rows=cur.fetchall()
                if len(rows) != 0:
                    self.productTable.delete(*self.productTable.get_children())
                    for row in rows:
                        self.productTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error", "No Record Found!", parent = self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self,ev):
        f = self.productTable.focus()
        content = (self.productTable.item(f))
        row = content["values"]
        self.idVar.set(row[0])
        self.pnameVar.set(row[1])
        self.priceVar.set(row[2])
        self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
        self.stockVar.set(row[3])
        self.qtyVar.set('1')

    def get_data_cart(self,ev):
        f = self.cartTable.focus()
        content = (self.cartTable.item(f))
        row = content["values"]
        self.idVar.set(row[0])
        self.pnameVar.set(row[1])
        self.priceVar.set(row[2])
        self.qtyVar.set(row[3])
        self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
        self.stockVar.set(row[4])

    def add_cart(self):
        if self.qtyVar.get() == "":
            messagebox.showerror("Error", "Quantity is required!", parent=self.root)
        elif self.idVar.get() == "":
            messagebox.showerror("Error", "Select the product from list first.", parent=self.root)
        elif int(self.qtyVar.get()) > int(self.stockVar.get()):
            messagebox.showerror("Error", "Invalid Quantity.", parent=self.root)
        else:
            unit_price = float(self.priceVar.get())
            qty = int(self.qtyVar.get())
            total_price = unit_price * qty
            total_price = float("{:.2f}".format(total_price))  # 2 decimal places

            # Store cart data: [pid, name, total_price, quantity, stock]
            cartData = [self.idVar.get(), self.pnameVar.get(), total_price, self.qtyVar.get(), self.stockVar.get()]

            present = 'no'
            index = 0
            for row in self.cartList:
                if self.idVar.get() == row[0]:
                    present = 'yes'
                    break
                index += 1

            if present == 'yes':
                op = messagebox.askyesno(
                    "Confirm",
                    "Product is already present.\nDo you want to Update or Remove it from the cart?",
                    parent=self.root
                )
                if op:
                    if self.qtyVar.get() == '0':
                        self.cartList.pop(index)
                    else:
                        # Update quantity and recalculate total price
                        new_qty = int(self.qtyVar.get())
                        new_total = float("{:.2f}".format(unit_price * new_qty))
                        self.cartList[index][2] = new_total
                        self.cartList[index][3] = self.qtyVar.get()
            else:
                self.cartList.append(cartData)

            self.show_cart()
            self.bill_updates()

    def show_cart(self):
        try:
            self.cartTable.delete(*self.cartTable.get_children())
            for row in self.cartList:
                self.cartTable.insert('',END,values=row)
        
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def generate_bill(self):
        if self.cnameVar.get() == "" or self.contactVar.get() == "":
            messagebox.showerror("Error", f"Customer details are required", parent=self.root)  
        elif len (self.cartList)==0:
            messagebox.showerror("Error", f"Kindly add Products First", parent=self.root)
        else:
            #=======Bill Top=======
            self.bill_top()
            #=======Bill Middle====
            self.bill_middle()
            #=======Bill Bottom====
            self.bill_bottom()

            fp=open(f"bill/{str(self.invoice)}.txt","w")
            fp.write(self.txt_bill_area.get("1.0",END))
            fp.close()
            messagebox.showinfo("Saved","Bill has been Generated successfully in Backend!", parent = self.root)

            self.printCheck = 1

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%y"))
        bill_top_temp = f"""
\t\tXYZ-Inventory
 Phone No. 98725***** , Scotland-125001
{str("="*45)}
 Customer Name: {self.cnameVar.get()}
 Ph no. :{self.contactVar.get()}
 Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d%m%y"))}
{str("="*45)}
 Product Name\t\t\tQTY\tPrice
{str("="*45)}
"""
        self.txt_bill_area.delete("1.0",END)
        self.txt_bill_area.insert("1.0",bill_top_temp)
    
    def bill_bottom(self):
        bill_bottom_temp = f"""
{str("="*45)}
 Bill Amount\t\t\t\tRs.{self.bill_amt:.2f}
 Discount\t\t\t\tRs.{self.discount:.2f}
 Net Pay\t\t\t\tRs.{self.net_pay:.2f}
{str("="*45)}\n
"""
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def bill_middle(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()

        try:
            for row in self.cartList:
                pid = row[0]
                name = row[1]
                qty = int(row[4]) - int(row[3])

                # Determine status based on remaining quantity
                if int(row[3]) == int(row[4]):
                    status = "Inactive"
                else:
                    status = "Active"

                # Calculate price and format to 2 decimal places
                price = float(row[2]) * int(row[3])
                price_str = "{:.2f}".format(price)  # <-- 2 decimal formatting

                # Insert into bill area
                self.txt_bill_area.insert(END, f"\n {name}\t\t\t{row[3]}\tRs.{price_str}")

                # Update product quantity in database
                cur.execute("UPDATE product SET qty=?, status=? WHERE pid=?", (
                    qty,
                    status,
                    pid
                ))
                con.commit()

            con.close()
            self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
          
    def clear_cart(self):
        self.idVar.set("")
        self.pnameVar.set("")
        self.priceVar.set("")
        self.qtyVar.set("")
        self.lbl_inStock.config(text=f"In Stock")
        self.stockVar.set("")         

    def clear_all(self):
        del self.cartList[:]
        self.cnameVar.set("")
        self.contactVar.set("")
        self.txt_bill_area.delete("0.1", END)
        self.cartTitle.config(text=f"Cart \t Total Product: [0]")
        self.searchVar.set("") 
        self.clear_cart() 
        self.show()
        self.show_cart()  
        self.printCheck=0
      
    def bill_updates(self):
        self.bill_amt = 0
        self.net_pay = 0
        self.discount = 0

        for row in self.cartList:
            # row[2] is total price already, row[3] is quantity
            self.bill_amt += float(row[2])  # if row[2] is already total price, no need to multiply by qty

        self.bill_amt = float("{:.2f}".format(self.bill_amt))
        self.discount = float("{:.2f}".format((self.bill_amt * 5) / 100))
        self.net_pay = float("{:.2f}".format(self.bill_amt - self.discount))

        self.lbl_amount.config(text=f"Total Amount\n[{self.bill_amt}]")
        self.lbl_pay.config(text=f"Net Pay\n[{self.net_pay}]")
        self.cartTitle.config(text=f"Cart \t Total Product: [{len(self.cartList)}]")

    def print_bill(self):
        try:
            # Open file dialog to choose location and name
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt")],
                initialfile=f"{int(time.strftime('%H%M%S')) + int(time.strftime('%d%m%y'))}.txt",
                title="Save Bill As"
            )

            # If user cancels, file_path will be empty
            if not file_path:
                return

            # Write the bill to chosen location
            with open(file_path, "w") as f:
                f.write(self.txt_bill_area.get('1.0', END))

            messagebox.showinfo(
                "Saved",
                f"Bill saved successfully!\n\nLocation:\n{os.path.abspath(file_path)}",
                parent=self.root
            )

        except Exception as ex:
            messagebox.showerror("Error", f"Error while saving bill: {str(ex)}", parent=self.root)

    def update_clock(self):
        current_time = time.strftime("%I:%M:%S %p")  # 12-hour format with AM/PM
        current_date = time.strftime("%d-%m-%Y")

        # Update label text
        self.lbl_clock.config(
            text=f"Welcome to Convenient Store Management System\t\tDate: {current_date}\t\tTime: {current_time}"
        )

        # Recall this function every 1000ms (1 second)
        self.lbl_clock.after(1000, self.update_clock)

if __name__ == "__main__":
    root = Tk()
    obj = BillClass(root)
    root.mainloop()