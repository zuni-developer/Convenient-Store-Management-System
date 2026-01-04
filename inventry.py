from tkinter import *
from PIL import Image, ImageTk
from employee import employeClass   # Import employee in inventory class
from supplier import supplierclass
from product import productClass
from category import CategoryClass
from sales import salesClass
from Billing import BillClass
import sqlite3
from tkinter import messagebox
import os
import time


class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x720+100+30")
        self.root.title("Convenient Store Management System")
        self.root.config(bg="#faf4e9")

        # ===== Data Structures =====
        # Dictionary for dashboard summary
        self.data_summary = {
            "products": 0,
            "suppliers": 0,
            "categories": 0,
            "employees": 0,
            "sales": 0
        }

        # Stack to track window history (LIFO)
        self.window_history = []

        # Queue (list used as FIFO) for recently opened sections
        self.recent_views = []

        # ===== Title Bar =====
        img = Image.open("image/logo.png")
        img = img.resize((50, 50), Image.LANCZOS)
        self.icon_title = ImageTk.PhotoImage(img)

        title = Label(
            self.root, 
            text="Convenient Store Management System", 
            image=self.icon_title, 
            compound=LEFT, 
            font=("poppins", 30, "bold"),
            bg="#575C49", 
            fg="#faf4e9", 
            padx=20,
            anchor="w"
        )
        title.place(x=0, y=2, relwidth=1, height=82)

        billing_button = Button(
            self.root, 
            text="Billing", 
            font=("poppins", 17, "bold"),
            bg="#faf4e9", 
            fg="black", 
            bd=1, 
            cursor="hand2", 
            command=self.bill, 
            padx=24
        ).place(x=1150, y=20)

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

        # ===== Left Menu =====
        self.MenuLogo = Image.open("image/img5.png").resize((200, 190), Image.LANCZOS)
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)

        menu_frame = Frame(self.root, relief=RIDGE, bg="#faf4e9")
        menu_frame.place(x=0, y=123, width=200, height=630)

        lbl_menu = Label(menu_frame, image=self.MenuLogo, compound=TOP,
                         font=("poppins", 20, "bold"), bg="#faf4e9", fg="#faf4e9")
        lbl_menu.pack(side=TOP, fill=X)

        btn_menu = Button(menu_frame, text="Menu", font=("poppins", 19, "bold"),
                          bg="#6B858C", fg="#faf4e9", cursor="hand2").pack(side=TOP, fill=X)

        # ===== Menu Buttons =====
        btn_employee = Button(menu_frame, text="Employee", font=("poppins", 19, "bold"),
                              bg="#faf4e9", fg="black", bd=1, cursor="hand2", command=self.employee)
        btn_employee.pack(fill=X)

        btn_supplier = Button(menu_frame, text="Supplier", command=self.supplier, font=("poppins", 19, "bold"),
                              bg="#faf4e9", fg="black", bd=1, cursor="hand2")
        btn_supplier.pack(fill=X)

        btn_category = Button(menu_frame, text="Category", command=self.category, font=("poppins", 19, "bold"),
                              bg="#faf4e9", fg="black", bd=1, cursor="hand2")
        btn_category.pack(fill=X)

        btn_product = Button(menu_frame, text="Products", command=self.product, font=("poppins", 19, "bold"),
                             bg="#faf4e9", fg="black", bd=1, cursor="hand2")
        btn_product.pack(fill=X)

        btn_sales = Button(menu_frame, text="Sales", command=self.sales, font=("poppins", 19, "bold"),
                           bg="#faf4e9", fg="black", bd=1, cursor="hand2")
        btn_sales.pack(fill=X)

        btn_exit = Button(menu_frame, text="Exit", font=("poppins", 19, "bold"),
                          bg="#faf4e9", fg="black", bd=1, cursor="hand2", command=self.root.destroy)
        btn_exit.pack(fill=X)

        # ==== Dashboard Section ====
        self.lbl_employee = self.create_dashboard_box("Total Employee\n[0]", "image/bg1.png", 270, 150, "#BF9179")
        self.lbl_supplier = self.create_dashboard_box("Total Supplier\n[0]", "image/bg2.png", 620, 150, "#BAB58D")
        self.lbl_category = self.create_dashboard_box("Total Category\n[0]", "image/bg3.png", 970, 150, "#9BBFBC")
        self.lbl_product = self.create_dashboard_box("Total Product\n[0]", "image/bg4.png", 270, 410, "#A6A795")
        self.lbl_sales = self.create_dashboard_box("Total Sales\n[0]", "image/bg5.png", 620, 410, "#B3998C")

        # Optional side image
        self.photo = Image.open("image/img1.png").resize((320, 230), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.photo)
        lbl_image = Label(self.root, image=self.photo, bd=0, bg="#faf4e9")
        lbl_image.place(x=970, y=410)

        # ===== Footer =====
        lbl_footer = Label(
            self.root,
            text="IMS - Inventory Management System | DSA Project\nAtika | Manal | Zona | Summaiya",
            font=("poppins", 12),
            bg="#00264d", fg="#faf4e9"
        )
        lbl_footer.pack(side=BOTTOM, fill=X)

        self.update_content()

    def create_dashboard_box(self, text, image_path, x, y, color):
        frame = Frame(self.root, width=320, height=230, bd=0, bg="#faf4e9")
        frame.place(x=x, y=y)

        bg_image = Image.open(image_path).resize((320, 230))
        bg_photo = ImageTk.PhotoImage(bg_image)
        label_bg = Label(frame, image=bg_photo, bd=0, bg="#faf4e9")
        label_bg.image = bg_photo
        label_bg.place(x=0, y=0)

        label_text = Label(frame, text=text, font=("poppins", 18, "bold"), fg="#51372A", bg=color, justify="center")
        label_text.place(relx=0.5, rely=0.5, anchor="center")

        return label_text

    # ===== Open Employee Window =====
    def employee(self):
        self.window_history.append("Employee")
        self.recent_views.append("Employee")
        if len(self.recent_views) > 3:
            self.recent_views.pop(0)
        print("Window History (Stack):", self.window_history)
        print("Recent Views (Queue):", self.recent_views)
        
        self.new_win = Toplevel(self.root)
        self.new_obj = employeClass(self.new_win)

    def supplier(self):
        self.window_history.append("Supplier")
        self.recent_views.append("Supplier")
        if len(self.recent_views) > 3:
            self.recent_views.pop(0)
        print("Window History (Stack):", self.window_history)
        print("Recent Views (Queue):", self.recent_views)

        self.new_win = Toplevel(self.root)
        self.new_obj = supplierclass(self.new_win)

    def product(self):
        self.window_history.append("Product")
        self.recent_views.append("Product")
        if len(self.recent_views) > 3:
            self.recent_views.pop(0)
        print("Window History (Stack):", self.window_history)
        print("Recent Views (Queue):", self.recent_views)

        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

    def category(self):
        self.window_history.append("Category")
        self.recent_views.append("Category")
        if len(self.recent_views) > 3:
            self.recent_views.pop(0)
        print("Window History (Stack):", self.window_history)
        print("Recent Views (Queue):", self.recent_views)

        self.new_win = Toplevel(self.root)
        self.new_obj = CategoryClass(self.new_win)

    def sales(self):
        self.window_history.append("Sales")
        self.recent_views.append("Sales")
        if len(self.recent_views) > 3:
            self.recent_views.pop(0)
        print("Window History (Stack):", self.window_history)
        print("Recent Views (Queue):", self.recent_views)

        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)

    def bill(self):
        self.window_history.append("Billing")
        self.recent_views.append("Billing")
        if len(self.recent_views) > 3:
            self.recent_views.pop(0)
        print("Window History (Stack):", self.window_history)
        print("Recent Views (Queue):", self.recent_views)

        self.new_win = Toplevel(self.root)
        self.new_obj = BillClass(self.new_win)

    # ===== Clock =====
    def update_clock(self):
        current_time = time.strftime("%I:%M:%S %p")
        current_date = time.strftime("%d-%m-%Y")
        self.lbl_clock.config(
            text=f"Welcome to Convenient Store Management System\t\tDate: {current_date}\t\tTime: {current_time}"
        )
        self.lbl_clock.after(1000, self.update_clock)

    # ===== Dashboard Updates =====
    def update_content(self):
        try:
            con = sqlite3.connect(database='ims.db')
            cur = con.cursor()

            # Fetch counts
            cur.execute("SELECT * FROM product")
            products = cur.fetchall()
            self.data_summary["products"] = len(products)
            self.lbl_product.config(text=f"Total Product\n[{len(products)}]")

            cur.execute("SELECT * FROM supplier")
            suppliers = cur.fetchall()
            self.data_summary["suppliers"] = len(suppliers)
            self.lbl_supplier.config(text=f"Total Supplier\n[{len(suppliers)}]")

            cur.execute("SELECT * FROM category")
            categories = cur.fetchall()
            self.data_summary["categories"] = len(categories)
            self.lbl_category.config(text=f"Total Category\n[{len(categories)}]")

            cur.execute("SELECT * FROM employee")
            employees = cur.fetchall()
            self.data_summary["employees"] = len(employees)
            self.lbl_employee.config(text=f"Total Employee\n[{len(employees)}]")

            # Sales from files
            bills = 0
            if os.path.isdir("bill"):
                bills = len([f for f in os.listdir("bill") if f.lower().endswith(".txt")])
            self.data_summary["sales"] = bills
            self.lbl_sales.config(text=f"Total Sales\n[{bills}]")

            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        # Schedule next refresh
        self.root.after(1000, self.update_content)

if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
