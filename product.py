from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import heapq  # for min-heap

class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+310+195")
        self.root.title("Inventory Management System")
        self.root.config(bg="#faf4e9")
        self.root.focus_force()

        # ============================= VARIABLES ============================
        self.var_cat = StringVar()
        self.var_sup = StringVar()
        self.cat_list = []
        self.sup_list = []
        self.fetch_sup_cat()
        self.var_pid = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        # ============================= HEAPS ================================
        self.low_stock_heap = []  # min-heap for low stock alerts

        # ============================= FRAME ============================
        product_Frame = Frame(self.root, bd=3, relief=RIDGE, bg="#faf4e9")
        product_Frame.place(x=10, y=10, width=450, height=480)

        title = Label(product_Frame, text="Manage Product Details",
                      font=("poppin", 20, "bold"), bg="#6C4F4F", fg="#faf4e9")
        title.pack(side=TOP, fill=X)

        lbl_category = Label(product_Frame, text="Category", font=("poppin", 18), bg="#faf4e9")
        lbl_category.place(x=30, y=70)
        lbl_supplier = Label(product_Frame, text="Supplier", font=("poppin", 18), bg="#faf4e9")
        lbl_supplier.place(x=30, y=120)
        lbl_name = Label(product_Frame, text="Name", font=("poppin", 18), bg="#faf4e9")
        lbl_name.place(x=30, y=170)
        lbl_price = Label(product_Frame, text="Price", font=("poppin", 18), bg="#faf4e9")
        lbl_price.place(x=30, y=220)
        lbl_qty = Label(product_Frame, text="Quantity", font=("poppin", 18), bg="#faf4e9")
        lbl_qty.place(x=30, y=270)
        lbl_status = Label(product_Frame, text="Status", font=("poppin", 18), bg="#faf4e9")
        lbl_status.place(x=30, y=320)

        cmb_cat = ttk.Combobox(product_Frame, textvariable=self.var_cat,
                               values=self.cat_list, state='readonly', justify=CENTER, font=("poppin", 15))
        cmb_cat.place(x=180, y=70, width=250)
        cmb_cat.current(0)

        cmb_sup = ttk.Combobox(product_Frame, textvariable=self.var_sup,
                               values=self.sup_list, state='readonly', justify=CENTER, font=("poppin", 15))
        cmb_sup.place(x=180, y=120, width=250)
        cmb_sup.current(0)

        txt_name = Entry(product_Frame, textvariable=self.var_name, font=("poppin", 15), bg='#d3d8cc')
        txt_name.place(x=180, y=170, width=250)
        txt_price = Entry(product_Frame, textvariable=self.var_price, font=("poppin", 15), bg='#d3d8cc')
        txt_price.place(x=180, y=220, width=250)
        txt_qty = Entry(product_Frame, textvariable=self.var_qty, font=("poppin", 15), bg='#d3d8cc')
        txt_qty.place(x=180, y=270, width=250)

        cmb_status = ttk.Combobox(product_Frame, textvariable=self.var_status,
                                  values=("Active", "Inactive"), state='readonly',
                                  justify=CENTER, font=("poppin", 15))
        cmb_status.place(x=180, y=320, width=250)
        cmb_status.current(0)

        # ============================= BUTTONS ============================
        btn_frame = Frame(product_Frame, bg="#faf4e9")
        btn_frame.place(x=30, y=390, width=400, height=60)

        Button(btn_frame, text="Save", font=("poppin", 15), command=self.add, bg="#6CB1AA", fg="#faf4e9", cursor="hand2").place(x=0, y=10, width=90, height=35)
        Button(btn_frame, text="Update", font=("poppin", 15), command=self.update, bg="#898561", fg="#faf4e9", cursor="hand2").place(x=100, y=10, width=90, height=35)
        Button(btn_frame, text="Delete", font=("poppin", 15), command=self.delete, bg="#AF5B51", fg="#faf4e9", cursor="hand2").place(x=200, y=10, width=90, height=35)
        Button(btn_frame, text="Clear", font=("poppin", 15), command=self.clear, bg="#C17C45", fg="#faf4e9", cursor="hand2").place(x=300, y=10, width=90, height=35)

        # ============================= Search & Table ============================
        SearchFrame = LabelFrame(self.root, text="Search Product", font=("poppin", 12, "bold"), bd=2, relief=RIDGE, bg="#faf4e9")
        SearchFrame.place(x=480, y=10, width=600, height=80)

        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby,
                                  values=("Select", "Category", "Supplier", "Name"), state="readonly",
                                  justify=CENTER, font=("poppin", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("poppin", 15), bg="#d3d8cc").place(x=200, y=10)
        btn_search = Button(SearchFrame, text="Search", command=self.search, font=("poppin", 15), bg="#6E8E8B", fg="#faf4e9", cursor="hand2").place(x=435, y=8, height=30, width=150)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#faf4e9", foreground="black", rowheight=25, fieldbackground="#faf4e9")
        style.configure("Treeview.Heading", background="#faf4e9", foreground="black", font=("Poppins", 11, "bold"))
        style.map("Treeview", background=[("selected", "#faf4e9")], foreground=[("selected", "#3C3C3C")])

        p_frame = Frame(self.root, bd=3, relief=RIDGE)
        p_frame.place(x=480, y=100, width=600, height=390)

        scrolly = Scrollbar(p_frame, orient=VERTICAL)
        scrollx = Scrollbar(p_frame, orient=HORIZONTAL)

        self.productTable = ttk.Treeview(p_frame, columns=("pid", "Supplier", "Category", "name", "price", "qty", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.productTable.xview)
        scrolly.config(command=self.productTable.yview)

        self.productTable.heading("pid", text="PID")
        self.productTable.heading("Category", text="Category")
        self.productTable.heading("Supplier", text="Supplier")
        self.productTable.heading("name", text="Name")
        self.productTable.heading("price", text="Price")
        self.productTable.heading("qty", text="Quantity")
        self.productTable.heading("status", text="Status")
        self.productTable["show"] = "headings"
        self.productTable.pack(fill=BOTH, expand=1)

        self.productTable.column("pid", width=50)
        self.productTable.column("Category", width=100)
        self.productTable.column("Supplier", width=100)
        self.productTable.column("name", width=150)
        self.productTable.column("price", width=100)
        self.productTable.column("qty", width=100)
        self.productTable.column("status", width=100)
        self.productTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # ============================= SUPPORT FUNCTIONS ============================
    def fetch_sup_cat(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM category")
            cat = cur.fetchall()
            self.cat_list.clear()
            self.cat_list.append("Select")
            for i in cat:
                self.cat_list.append(i[0])

            cur.execute("SELECT name FROM Supplier")
            sup = cur.fetchall()
            self.sup_list.clear()
            self.sup_list.append("Select")
            for i in sup:
                self.sup_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    # ============================= ADD / UPDATE / DELETE ============================
    def add(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            if self.var_cat.get() == "Select" or self.var_sup.get() == "Select" or self.var_name.get() == "":
                messagebox.showerror("Error", "All fields are Required", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This Product Already present, Try a Different One", parent=self.root)
                else:
                    cur.execute("INSERT INTO product(Category, Supplier,  name,  price,  qty,  status) VALUES (?,?,?,?,?,?)", (
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def update(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Kindly select product from the list", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Product", parent=self.root)
                else:
                    cur.execute("UPDATE product SET Category=?, Supplier=?, name=?, price=?, qty=?, status=? WHERE pid=?", (
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                        self.var_pid.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Product Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Kindly Select the product from the list", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid product", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Are you sure you want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("DELETE from product WHERE pid=?", (self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Product Deleted Successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_pid.set('')
        self.var_cat.set('')
        self.var_sup.set('')
        self.var_name.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.var_status.set('')
        self.show()

    # ============================= SHOW FUNCTION WITH LOW STOCK ALERT ============================
    def show(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()
            self.productTable.delete(*self.productTable.get_children())
            self.low_stock_heap.clear()  # clear heap before rebuild
            for row in rows:
                self.productTable.insert('', END, values=row)
                # push qty into min-heap
                heapq.heappush(self.low_stock_heap, (int(row[5]), row[3]))  # (qty, name)

            # Check for low stock products
            while self.low_stock_heap and self.low_stock_heap[0][0] <= 5:
                qty, name = heapq.heappop(self.low_stock_heap)
                messagebox.showwarning("Low Stock Alert", f"Product '{name}' is about to go out of stock! Only {qty} left.")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    # ============================= SEARCH FUNCTION ============================
    def search(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select Search by option.", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search input is required.", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE " + self.var_searchby.get() + " LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.productTable.delete(*self.productTable.get_children())
                    for row in rows:
                        self.productTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No Record Found!", parent=self.root)
        except Exception as ex:   # <- This is the except block
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.productTable.focus()
        content = (self.productTable.item(f))
        row = content["values"]
        self.var_pid.set(row[0])
        self.var_cat.set(row[2])
        self.var_sup.set(row[1])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_status.set(row[6])


# ============================= MAIN ============================
if __name__ == "__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()
