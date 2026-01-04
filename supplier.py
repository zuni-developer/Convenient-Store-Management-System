from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

# ===================== Linked List Classes ===================== #
class SupplierNode:
    """Node class for a single supplier in the linked list"""
    def __init__(self, invoice, name, contact, description):
        self.invoice = invoice
        self.name = name
        self.contact = contact
        self.description = description
        self.next = None

class SupplierLinkedList:
    """Singly linked list to store suppliers"""
    def __init__(self):
        self.head = None

    def add_supplier(self, invoice, name, contact, description):
        """Add supplier at the end of the linked list"""
        new_node = SupplierNode(invoice, name, contact, description)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def update_supplier(self, invoice, name, contact, description):
        """Update a supplier in the list by invoice"""
        current = self.head
        while current:
            if current.invoice == invoice:
                current.name = name
                current.contact = contact
                current.description = description
                return True
            current = current.next
        return False

    def delete_supplier(self, invoice):
        """Delete a supplier node by invoice"""
        current = self.head
        prev = None
        while current:
            if current.invoice == invoice:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next
        return False

    def find_supplier(self, invoice):
        """Find and return a supplier node by invoice"""
        current = self.head
        while current:
            if current.invoice == invoice:
                return current
            current = current.next
        return None

    def get_all_suppliers(self):
        """Return all suppliers as a list of tuples"""
        suppliers = []
        current = self.head
        while current:
            suppliers.append((current.invoice, current.name, current.contact, current.description))
            current = current.next
        return suppliers


# ===================== Supplier GUI Class ===================== #
class supplierclass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+310+195")
        self.root.title("Inventory Management System | Developed by Xeven")
        self.root.config(bg="#faf4e9")
        self.root.focus_force()

        # =================== Linked List =================== #
        self.supplier_list = SupplierLinkedList()  # Our in-memory linked list

        # ===================== Create Table if not exists ====================#
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Supplier(
                invoice TEXT PRIMARY KEY,
                name TEXT,
                contact TEXT,
                description TEXT
            )
        """)
        con.commit()
        con.close()

        #==================== All Variables ====================#
        self.var_searchtxt = StringVar()
        self.var_Supp_Invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()

        #==================== GUI Elements ====================#
        lbl_search = Label(self.root,text="Invoice No.",bg="#faf4e9", font=("poppin", 15))
        lbl_search.place(x=680, y=80)

        txt_search = Entry(self.root,textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="#d3d8cc").place(x=790, y=80,width=160)
        btn_search = Button(self.root, text="Search",command=self.search, font=("poppin", 15,"bold"), bg="#6E8E8B", fg="#faf4e9", cursor="hand2").place(x=960, y=76, height=30, width=110)

        title = Label(self.root, text="Supplier Details", font=("poppin", 20,"bold"), bg="#456578", fg="#faf4e9").place(x=50, y=10,height=40, width=1020)

        lbl_Supplier_Invoice = Label(self.root, text="Invoice No", font=("poppin", 15), bg="#faf4e9").place(x=50, y=120)
        txt_Supplier_Invoice = Entry(self.root, textvariable=self.var_Supp_Invoice, font=("poppin", 15), bg="#d3d8cc").place(x=180, y=120, width=150)

        lbl_name = Label(self.root, text="Name", font=("poppin", 15), bg="#faf4e9").place(x=50, y=170)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("poppin", 15), bg="#d3d8cc").place(x=180, y=170, width=180)

        lbl_contact = Label(self.root, text="Contact", font=("poppin", 15), bg="#faf4e9").place(x=50, y=220)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("poppin", 15), bg="#d3d8cc").place(x=180, y=220, width=180)

        lbl_description = Label(self.root, text="Description", font=("poppin", 15), bg="#faf4e9").place(x=50, y=270)
        self.txt_description = Text(self.root, font=("poppin", 15), bg="#d3d8cc")
        self.txt_description.place(x=180, y=270, width=400, height=70)

        # Buttons
        Button(self.root, text="Save", command=self.add, font=("poppin", 15,"bold"), bg="#6CB1AA", fg="#faf4e9", cursor="hand2").place(x=180, y=380, width=110, height=32)
        Button(self.root, text="Update", command=self.update, font=("poppin", 15 ,"bold"), bg="#898561", fg="#faf4e9", cursor="hand2").place(x=300, y=380, width=110, height=32)
        Button(self.root, text="Delete", command=self.delete, font=("poppin", 15 ,"bold" ), bg="#AF5B51", fg="#faf4e9", cursor="hand2").place(x=420, y=380, width=100, height=32)
        Button(self.root, text="Clear", command=self.clear,  font=("poppin", 15 ,"bold"), bg="#C17C45", fg="#faf4e9", cursor="hand2").place(x=530, y=380, width=110, height=32)

        # Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#faf4e9", foreground="black", rowheight=25, fieldbackground="#faf4e9")
        style.configure("Treeview.Heading", background="#faf4e9", foreground="black", font=("Poppins", 11, "bold"))
        style.map("Treeview", background=[("selected", "#faf4e9")], foreground=[("selected", "#3C3C3C")])
        
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=680, y=120, width=390, height=350)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.supplierTable = ttk.Treeview(emp_frame, columns=("invoice","name",  "contact", "description"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)

        self.supplierTable.heading("invoice", text="Invoice No")
        self.supplierTable.heading("name", text="Name")
        self.supplierTable.heading("contact", text="Contact")
        self.supplierTable.heading("description", text="Description")
        self.supplierTable["show"] = "headings"
        self.supplierTable.pack(fill=BOTH, expand=1)
        self.supplierTable.column("invoice", width=100)
        self.supplierTable.column("name", width=150)
        self.supplierTable.column("contact", width=100)
        self.supplierTable.column("description", width=280)

        self.supplierTable.bind("<ButtonRelease-1>", self.get_data)

        # Load existing suppliers from DB into linked list
        self.load_suppliers_from_db()
        self.show()

    # ================== Load DB into Linked List ================== #
    def load_suppliers_from_db(self):
        """Load all suppliers from the database into the linked list"""
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM Supplier")
            rows = cur.fetchall()
            for row in rows:
                self.supplier_list.add_supplier(row[0], row[1], row[2], row[3])
        except Exception as ex:
            messagebox.showerror("Error", f"Error loading suppliers: {str(ex)}", parent=self.root)
        finally:
            con.close()

    # ================== Add Supplier ================== #
    def add(self):   
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            if self.var_Supp_Invoice.get() == "":
                messagebox.showerror("Error", "Invoice Must Be Required", parent=self.root)
                return

            # Add to DB
            cur.execute("SELECT * FROM Supplier WHERE invoice =?", (self.var_Supp_Invoice.get(),))
            if cur.fetchone() is not None:
                messagebox.showerror("Error", "Invoice Already Exists", parent=self.root)
                return

            cur.execute("INSERT INTO Supplier(invoice, name, contact, description) VALUES (?,?,?,?)", (
                self.var_Supp_Invoice.get(),
                self.var_name.get(),
                self.var_contact.get(),
                self.txt_description.get('1.0', END),
            ))
            con.commit()

            # ================== Add to Linked List ================== #
            self.supplier_list.add_supplier(
                self.var_Supp_Invoice.get(),
                self.var_name.get(),
                self.var_contact.get(),
                self.txt_description.get('1.0', END)
            )

            messagebox.showinfo("Success", "Supplier Added Successfully", parent=self.root)
            self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    # ================== Show Suppliers ================== #
    def show(self):
        """Show all suppliers from linked list in Treeview"""
        self.supplierTable.delete(*self.supplierTable.get_children())
        for row in self.supplier_list.get_all_suppliers():
            self.supplierTable.insert('', END, values=row)

    # ================== Get Data from Treeview ================== #
    def get_data(self, ev):
        f = self.supplierTable.focus()
        content = self.supplierTable.item(f)
        row = content["values"]
        if row:
            self.var_Supp_Invoice.set(row[0])
            self.var_name.set(row[1])
            self.var_contact.set(row[2])
            self.txt_description.delete('1.0', END)
            self.txt_description.insert(END, row[3])

    # ================== Update Supplier ================== #
    def update(self):   
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            if self.var_Supp_Invoice.get() == "":
                messagebox.showerror("Error", "Invoice Must Be Required", parent=self.root)
                return

            cur.execute("UPDATE Supplier SET name=?, contact=?, description=? WHERE invoice=?", (
                self.var_name.get(),
                self.var_contact.get(),
                self.txt_description.get('1.0', END),
                self.var_Supp_Invoice.get(),
            ))
            con.commit()

            # Update linked list
            self.supplier_list.update_supplier(
                self.var_Supp_Invoice.get(),
                self.var_name.get(),
                self.var_contact.get(),
                self.txt_description.get('1.0', END)
            )

            messagebox.showinfo("Success", "Supplier Updated Successfully", parent=self.root)
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    # ================== Delete Supplier ================== #
    def delete(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            if self.var_Supp_Invoice.get() == "":
                messagebox.showerror("Error", "Invoice Must Be Required", parent=self.root)
                return

            cur.execute("DELETE FROM Supplier WHERE invoice=?", (self.var_Supp_Invoice.get(),))
            con.commit()

            # Delete from linked list
            self.supplier_list.delete_supplier(self.var_Supp_Invoice.get())

            messagebox.showinfo("Success", "Supplier Deleted Successfully", parent=self.root)
            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    # ================== Clear Fields ================== #
    def clear(self):
        self.var_Supp_Invoice.set('')
        self.var_name.set('')
        self.var_contact.set('')
        self.txt_description.delete('1.0', END)
        self.var_searchtxt.set('')
        self.show()

    # ================== Search Supplier ================== #
    def search(self):
        invoice = self.var_searchtxt.get().strip()
        if invoice == "":
            messagebox.showerror("Error", "Invoice should be required.", parent=self.root)
            return

        # Ensure linked list is synced with database
        if self.supplier_list.head is None:
            self.load_suppliers_from_db()

        node = self.supplier_list.find_supplier(invoice)
        if node:
            self.supplierTable.delete(*self.supplierTable.get_children())
            self.supplierTable.insert('', END, values=(
                node.invoice.strip(),
                node.name.strip(),
                node.contact.strip(),
                node.description.strip()
            ))
        else:
            # Double-check in DB (in case linked list wasn’t updated)
            con = sqlite3.connect(database='ims.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM Supplier WHERE invoice=?", (invoice,))
            row = cur.fetchone()
            con.close()

            if row:
                self.supplierTable.delete(*self.supplierTable.get_children())
                self.supplierTable.insert('', END, values=row)
            else:
                messagebox.showerror("Error", "No Record Found!", parent=self.root)



# ===================== Main ===================== #
if __name__ == "__main__":
    root = Tk()
    obj = supplierclass(root)
    root.mainloop()
