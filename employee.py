from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

class employeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+310+195")
        self.root.title("Inventory Management System | Developed by Xeven")
        self.root.config(bg="#faf4e9")
        self.root.focus_force()

        #==================== Create Table if not exists ====================#
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employee(
                eid TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                gender TEXT,
                contact TEXT,
                dob TEXT,
                doj TEXT,
                pass TEXT,
                utype TEXT,
                address TEXT,
                salary TEXT
            )
        """)
        con.commit()
        con.close()

        #==================== All Variables ====================#
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_emp_id = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()

        #==================== Search Frame ====================#
        SearchFrame = LabelFrame(self.root, text="Search Employee", font=("poppin", 12, "bold"), bd=2, relief=RIDGE, bg="#faf4e9")
        SearchFrame.place(x=250, y=20, width=600, height=70)

        cmb_search = ttk.Combobox(SearchFrame,textvariable= self.var_searchby, values=("Select", "Email", "Name", "Contact"), state="readonly", justify=CENTER, font=("poppin", 13))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame,textvariable= self.var_searchtxt, font=("poppin", 13), bg="#d3d8cc").place(x=200, y=10)
        btn_search = Button(SearchFrame, text="Search",command=self.search, font=("poppin", 13), bg="#857164", fg="#faf4e9", cursor="hand2").place(x=410, y=7, height=30, width=150)

        #==================== Title ====================#
        title = Label(self.root, text="Employee Details", font=("poppin", 15), bg="#456578", fg="#faf4e9", pady=5).place(x=50, y=100, width=1000)

        #==================== Content ====================#
        lbl_empid = Label(self.root, text="Emp ID", font=("poppin", 13), bg="#faf4e9").place(x=50, y=150)
        txt_empid = Entry(self.root, textvariable=self.var_emp_id, font=("poppin", 13), bg="#d3d8cc").place(x=150, y=150, width=150)

        lbl_gender = Label(self.root, text="Gender", font=("poppin", 13), bg="#faf4e9").place(x=400, y=150)
        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select", "Male", "Female"), state="readonly", justify=CENTER, font=("poppin", 13))
        cmb_gender.place(x=500, y=150, width=180)
        cmb_gender.current(0)

        lbl_contact = Label(self.root, text="Contact", font=("poppin", 13), bg="#faf4e9").place(x=750, y=150)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("poppin", 13), bg="#d3d8cc").place(x=850, y=150, width=200)

        lbl_name = Label(self.root, text="Name", font=("poppin", 13), bg="#faf4e9").place(x=50, y=190)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("poppin", 13), bg="#d3d8cc").place(x=150, y=190, width=150)

        lbl_dob = Label(self.root, text="D.O.B", font=("poppin", 13), bg="#faf4e9").place(x=400, y=190)
        txt_dob = Entry(self.root, textvariable=self.var_dob, font=("poppin", 13), bg="#d3d8cc").place(x=500, y=190, width=150)

        lbl_doj = Label(self.root, text="D.O.J", font=("poppin", 13), bg="#faf4e9").place(x=750, y=190)
        txt_doj = Entry(self.root, textvariable=self.var_doj, font=("poppin", 13), bg="#d3d8cc").place(x=850, y=190, width=200)

        lbl_email = Label(self.root, text="Email", font=("poppin", 13), bg="#faf4e9").place(x=50, y=230)
        txt_email = Entry(self.root, textvariable=self.var_email, font=("poppin", 13), bg="#d3d8cc").place(x=150, y=230, width=150)

        lbl_pass = Label(self.root, text="Password", font=("poppin", 13), bg="#faf4e9").place(x=400, y=230)
        txt_pass = Entry(self.root, textvariable=self.var_pass, show="*", font=("poppin", 13), bg="#d3d8cc").place(x=500, y=230, width=150)

        lbl_utype = Label(self.root, text="User Type", font=("poppin", 13), bg="#faf4e9").place(x=750, y=230)
        cmb_utype = ttk.Combobox(self.root, textvariable=self.var_utype, values=("Admin", "Staff"), state="readonly", justify=CENTER, font=("poppin", 13))
        cmb_utype.place(x=850, y=230, width=200)
        cmb_utype.current(0)

        lbl_address = Label(self.root, text="Address", font=("poppin", 13), bg="#faf4e9").place(x=50, y=270)
        self.txt_address = Text(self.root, font=("poppin", 13), bg="#d3d8cc")
        self.txt_address.place(x=150, y=270, width=300, height=60)

        lbl_salary = Label(self.root, text="Salary", font=("poppin", 13), bg="#faf4e9").place(x=500, y=270)
        txt_salary = Entry(self.root, textvariable=self.var_salary, font=("poppin", 13), bg="#d3d8cc").place(x=580, y=270, width=150)

        #==================== Buttons ====================#
        btn_save = Button(self.root, text="Save", command=self.add, font=("poppin", 15), bg="#6CB1AA", fg="#faf4e9", cursor="hand2").place(x=500, y=310, width=100, height=30)
        btn_update = Button(self.root, text="Update",command=self.update, font=("poppin", 15), bg="#898561", fg="#faf4e9", cursor="hand2").place(x=610, y=310, width=100, height=30)
        btn_delete = Button(self.root, text="Delete",command=self.delete, font=("poppin", 15), bg="#AF5B51", fg="#faf4e9", cursor="hand2").place(x=720, y=310, width=100, height=30)
        btn_clear = Button(self.root, text="Clear",command=self.clear,  font=("poppin", 15), bg="#C17C45", fg="#faf4e9", cursor="hand2").place(x=830, y=310, width=100, height=30)

        #==================== Frame for Table / List ====================#
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

        emp_frame = Frame(self.root, bd=3, relief=RIDGE, bg= "#faf4e9")
        emp_frame.place(x=0, y=360, relwidth=1, height=140)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.EmployeeTable = ttk.Treeview(emp_frame, columns=("eid","name", "email", "gender", "contact", "dob", "doj", "pass", "utype", "address", "salary"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)

        self.EmployeeTable.heading("eid", text="EMP ID")
        self.EmployeeTable.heading("name", text="Name")
        self.EmployeeTable.heading("email", text="Email")
        self.EmployeeTable.heading("gender", text="Gender")
        self.EmployeeTable.heading("contact", text="Contact")
        self.EmployeeTable.heading("dob", text="D.O.B")
        self.EmployeeTable.heading("doj", text="D.O.J")
        self.EmployeeTable.heading("pass", text="Password")
        self.EmployeeTable.heading("utype", text="User Type")
        self.EmployeeTable.heading("address", text="Address")
        self.EmployeeTable.heading("salary", text="Salary")
        self.EmployeeTable["show"] = "headings"
        self.EmployeeTable.pack(fill=BOTH, expand=1)

        self.EmployeeTable.column("eid", width=80)
        self.EmployeeTable.column("name", width=100)
        self.EmployeeTable.column("email", width=180)
        self.EmployeeTable.column("gender", width=100)
        self.EmployeeTable.column("contact", width=100)
        self.EmployeeTable.column("dob", width=100)
        self.EmployeeTable.column("doj", width=100)
        self.EmployeeTable.column("pass", width=100)
        self.EmployeeTable.column("utype", width=100)
        self.EmployeeTable.column("address", width=210)
        self.EmployeeTable.column("salary", width=100)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

#==========================================================================================================================================#

    def add(self):   
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID Must Be Required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This Employee ID has Already Been Assigned, Try a Different One", parent=self.root)
                else:
                    cur.execute("INSERT INTO employee(eid, name, email, gender, contact, dob, doj, pass, utype, address, salary) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
                        self.var_emp_id.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get('1.0', END).strip(),
                        self.var_salary.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM employee")
            rows = cur.fetchall()

            # ===== Merge Sort Function to Sort by Name =====
            def merge_sort(lst):
                if len(lst) > 1:
                    mid = len(lst) // 2
                    left = lst[:mid]
                    right = lst[mid:]

                    merge_sort(left)
                    merge_sort(right)

                    i = j = k = 0

                    while i < len(left) and j < len(right):
                        if left[i][1].lower() <= right[j][1].lower():
                            lst[k] = left[i]
                            i += 1
                        else:
                            lst[k] = right[j]
                            j += 1
                        k += 1

                    while i < len(left):
                        lst[k] = left[i]
                        i += 1
                        k += 1

                    while j < len(right):
                        lst[k] = right[j]
                        j += 1
                        k += 1

            # Sort the rows by employee name
            merge_sort(rows)

            # ===== Update Treeview =====
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self,ev):
        f = self.EmployeeTable.focus()
        content = (self.EmployeeTable.item(f))
        row = content["values"]
        self.var_emp_id.set(row[0]),
        self.var_name.set(row[1]),
        self.var_email.set(row[2]),
        self.var_gender.set(row[3]),
        self.var_contact.set(row[4]),
        self.var_dob.set(row[5]),
        self.var_doj.set(row[6]),
        self.var_pass.set(row[7]),
        self.var_utype.set(row[8]),
        self.txt_address.delete('1.0', END),
        self.txt_address.insert(END, row[9]),
        self.var_salary.set(row[10]),

    def update(self):   
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID Must Be Required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Emplyee ID", parent=self.root)
                else:
                    cur.execute("UPDATE employee SET name=?, email=?, gender=?, contact=?, dob=?, doj=?, pass=?, utype=?, address=?, salary=? WHERE eid=?", (
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get('1.0', END),
                        self.var_salary.get(),
                        self.var_emp_id.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee Updated Successfully", parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
    
    def delete(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID Must Be Required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Emplyee ID", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Are you sure you want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("DELETE from employee WHERE eid=?",(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Employee Deleted Successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
    
    def clear(self):
        self.var_emp_id.set(''),
        self.var_name.set(''),
        self.var_email.set(''),
        self.var_gender.set('Select'),
        self.var_contact.set(''),
        self.var_dob.set(''),
        self.var_doj.set(''),
        self.var_pass.set(''),
        self.var_utype.set('Admin'),
        self.txt_address.delete('1.0', END),
        self.var_salary.set('')
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()
    
    def search(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            search_by = self.var_searchby.get()
            search_txt = self.var_searchtxt.get().strip()

            if search_by == "Select":
                messagebox.showerror("Error", "Select Search by option.", parent=self.root)
                return
            if search_txt == "":
                messagebox.showerror("Error", "Search input is required.", parent=self.root)
                return

            # Normalize the search text (for consistent comparison)
            search_text = search_txt.lower()

            if search_by == "Name":
                # ===== Binary Search by Name =====
                cur.execute("SELECT * FROM employee")
                rows = cur.fetchall()

                if not rows:
                    messagebox.showerror("Error", "No employees in database.", parent=self.root)
                    return

                rows.sort(key=lambda x: x[1].lower())  # Assuming name is column index 1

                low, high = 0, len(rows) - 1
                result = []
                while low <= high:
                    mid = (low + high) // 2
                    name_mid = rows[mid][1].lower()

                    if name_mid == search_text:
                        # Found — collect duplicates
                        left_idx = mid
                        right_idx = mid
                        while left_idx >= 0 and rows[left_idx][1].lower() == search_text:
                            result.insert(0, rows[left_idx])
                            left_idx -= 1
                        while right_idx < len(rows) and rows[right_idx][1].lower() == search_text:
                            if right_idx != mid:
                                result.append(rows[right_idx])
                            right_idx += 1
                        break
                    elif search_text < name_mid:
                        high = mid - 1
                    else:
                        low = mid + 1

                if result:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in result:
                        self.EmployeeTable.insert('', END, values=row)
                else:
                    messagebox.showinfo("Result", "No Record Found!", parent=self.root)

            else:
                # ===== Linear Search for Email or Contact =====
                # Fix column name mapping to actual DB columns
                column_map = {
                    "Email": "email",
                    "Contact": "contact",
                    "Name": "name"
                }

                col = column_map.get(search_by, search_by.lower())
                cur.execute(f"SELECT * FROM employee WHERE LOWER({col}) LIKE ?", ('%' + search_text + '%',))
                rows = cur.fetchall()

                if rows:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('', END, values=row)
                else:
                    messagebox.showinfo("Result", "No Record Found!", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

#==========================================================================================================================================#

if __name__ == "__main__":
    root = Tk()
    obj = employeClass(root)
    root.mainloop()
