from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class CategoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+310+195")
        self.root.title("Inventory Management System")
        self.root.config(bg="#faf4e9")
        self.root.focus_force()

        # ==================== Variables ====================
        self.var_name = StringVar()
        self.var_cat_id = StringVar()

        # ==================== Title ====================
        lbl_title = Label(self.root, text="Product Category",
                          font=("poppin", 20, "bold"),
                          bg="#456578", fg="#faf4e9", relief=RIDGE, pady=5)
        lbl_title.pack(side=TOP, fill=X, padx=30, pady=10)

        # ==================== Input Field ====================
        lbl_name = Label(self.root, text="Enter Category Name",
                         font=("poppin", 20),
                         bg="#faf4e9")
        lbl_name.place(x=40, y=100)

        self.txt_name = Entry(self.root, textvariable=self.var_name,
                              font=("poppin", 18),
                              bg="#d3d8cc")
        self.txt_name.place(x=45, y=170, width=300)

        # ==================== Buttons ====================
        btn_add = Button(self.root, text="Add",
                         font=("poppin", 15),
                         bg="#6CB1AA", fg="#faf4e9", cursor="hand2",
                         command=self.add)
        btn_add.place(x=355, y=170, width=150, height=30)

        btn_delete = Button(self.root, text="Delete",
                            font=("poppin", 15),
                            bg="#AF5B51", fg="#faf4e9", cursor="hand2",
                            command=self.delete)
        btn_delete.place(x=510, y=170, width=150, height=30)

        # ==================== Treeview Frame ====================
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
        
        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=690, y=100, width=380, height=100)

        scrolly = Scrollbar(cat_frame, orient=VERTICAL)
        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)
        self.categoryTable = ttk.Treeview(cat_frame, columns=("cid", "name"),
                                          yscrollcommand=scrolly.set,
                                          xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.categoryTable.xview)
        scrolly.config(command=self.categoryTable.yview)

        self.categoryTable.heading("cid", text="C ID")
        self.categoryTable.heading("name", text="Name")
        self.categoryTable["show"] = "headings"
        self.categoryTable.column("cid", width=10)
        self.categoryTable.column("name", width=200)
        self.categoryTable.pack(fill=BOTH, expand=1)
        self.categoryTable.bind("<ButtonRelease-1>", self.get_data)

        # ==================== Image ====================
        self.im1 = Image.open("image/img2.png")
        self.im1 = self.im1.resize((500, 250), Image.LANCZOS)
        self.im1 = ImageTk.PhotoImage(self.im1)
        self.lbl_im1 = Label(self.root, image=self.im1, bg="#faf4e9")
        self.lbl_im1.place(x=40, y=220)

        self.im2 = Image.open("image/img3.png")
        self.im2 = self.im2.resize((500, 250), Image.LANCZOS)
        self.im2 = ImageTk.PhotoImage(self.im2)
        self.lbl_im2 = Label(self.root, image=self.im2, bg="#faf4e9")
        self.lbl_im2.place(x=560, y=220)


        # ==================== Load Categories ====================
        self.show()

    # ==================== ADD CATEGORY ====================
    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_name.get().strip() == "":
                messagebox.showerror("Error", "Category name is required", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Category already exists", parent=self.root)
                else:
                    cur.execute("INSERT INTO category (name) VALUES(?)", (self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Category added successfully", parent=self.root)
                    self.var_name.set("")
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()
    # ==================== SHOW CATEGORIES ====================
    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM category")
            rows = cur.fetchall()
            self.categoryTable.delete(*self.categoryTable.get_children())
            for row in rows:
                self.categoryTable.insert("", "end", values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self,ev):
        f = self.categoryTable.focus()
        content = (self.categoryTable.item(f))
        row = content["values"]
        self.var_cat_id.set(row[0]),
        self.var_name.set(row[1]),
    # ==================== DELETE CATEGORY ====================
    def delete(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Kindly select Category from the list", parent=self.root)
            else:
                # Check if the category exists
                cur.execute("SELECT * FROM category WHERE cid=?", (self.var_cat_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Category ID", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Are you sure you want to delete?", parent=self.root)
                    if op:
                        # ✅ Delete the category
                        cur.execute("DELETE FROM category WHERE cid=?", (self.var_cat_id.get(),))
                        con.commit()

                        # ✅ Check if table is now empty
                        cur.execute("SELECT COUNT(*) FROM category")
                        count = cur.fetchone()[0]
                        if count == 0:
                            # ✅ Reset the auto-increment counter
                            cur.execute("DELETE FROM sqlite_sequence WHERE name='category'")
                            con.commit()

                        messagebox.showinfo("Delete", "Category Deleted Successfully", parent=self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()



# ==================== MAIN WINDOW ====================
if __name__ == "__main__":
    root = Tk()
    obj = CategoryClass(root)
    root.mainloop()
