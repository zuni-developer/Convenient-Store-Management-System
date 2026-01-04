from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import os
import bisect

class salesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+310+195")
        self.root.title("Inventory Management System")
        self.root.config(bg="#faf4e9")
        self.root.focus_force()

        # ======= Variables =======
        self.bill_list = []   # To store invoice numbers
        self.var_invoice = StringVar()

        # ======= Title & Search =======
        lbl_title = Label(self.root, text="View Customer Bills",
                          font=("poppin", 20, "bold"),
                          bg="#456578", fg="#faf4e9", relief=RIDGE)
        lbl_title.pack(side=TOP, fill=X, padx=10, pady=20)

        lnl_invoice = Label(self.root, text="Invoice No.", font=("poppin", 15), bg="#faf4e9")
        lnl_invoice.place(x=50, y=100)
        txt_invoice = Entry(self.root, textvariable=self.var_invoice, font=("poppin", 15), bg="#d3d8cc")
        txt_invoice.place(x=160, y=100, width=250, height=28)
        btn_search = Button(self.root, text="Search", command=self.search, font=("poppin", 15, "bold"),
                            bg="#6CB1AA", fg="#faf4e9", cursor="hand2")
        btn_search.place(x=430, y=100, width=120, height=28)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("poppin", 15, "bold"),
                           bg="#C17C45", fg="#faf4e9", cursor="hand2")
        btn_clear.place(x=570, y=100, width=120, height=28)

        # ======= Bill Listbox =======
        sales_Frame = Frame(self.root, bd=3, relief=RIDGE)
        sales_Frame.place(x=50, y=150, width=200, height=310)
        scrolly = Scrollbar(sales_Frame, orient=VERTICAL)
        self.Sales_List = Listbox(sales_Frame, font=("poppin", 15), bg="#faf4e9", yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH, expand=1)
        self.Sales_List.bind("<ButtonRelease-1>", self.get_data)

        # ======= Bill Display Area =======
        bill_Frame = Frame(self.root, bd=3, relief=RIDGE)
        bill_Frame.place(x=280, y=150, width=410, height=310)
        lbl_title2 = Label(bill_Frame, text="Customer Bill Area",
                           font=("poppin", 20),
                           bg="#A26458", fg="#faf4e9")
        lbl_title2.pack(side=TOP, fill=X)
        scrolly2 = Scrollbar(bill_Frame, orient=VERTICAL)
        self.bill_area = Text(bill_Frame, bg="#EFE7E2", yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH, expand=1)

        # ======= Bill Image =======
        self.bill_photo = Image.open("image/img4.png")
        self.bill_photo = self.bill_photo.resize((350, 380), Image.LANCZOS)
        self.bill_photo = ImageTk.PhotoImage(self.bill_photo)
        lbl_image = Label(self.root, image=self.bill_photo, bd=0, bg="#faf4e9")
        lbl_image.place(x=720, y=90)

        # ======= Load bills =======
        self.show()

    # ====================== Merge Sort and Binary Search Helper ======================
    def merge_sort(self, arr):
        if len(arr) > 1:
            mid = len(arr)//2
            L = arr[:mid]
            R = arr[mid:]
            self.merge_sort(L)
            self.merge_sort(R)

            i = j = k = 0
            while i < len(L) and j < len(R):
                if L[i] < R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1

            while i < len(L):
                arr[k] = L[i]
                i += 1
                k += 1

            while j < len(R):
                arr[k] = R[j]
                j += 1
                k += 1

    # Binary search function
    def binary_search(self, arr, target):
        low = 0
        high = len(arr) - 1

        while low <= high:
            mid = (low + high) // 2
            if arr[mid] == target:
                return mid  # Found the target
            elif arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1

        return -1  # Target not found


    # ====================== Show all bills ======================
    def show(self):
        # Clear previous lists
        del self.bill_list[:]
        self.Sales_List.delete(0, END)

        # Fetch all invoices from 'bill' folder
        for file in os.listdir('bill'):
            if file.endswith('.txt'):
                invoice_no = file.split('.')[0]  # Extract invoice number
                self.bill_list.append(invoice_no)

        # Sort invoices using merge sort
        self.merge_sort(self.bill_list)

        # Display sorted invoices in listbox
        for invoice in self.bill_list:
            self.Sales_List.insert(END, f"{invoice}.txt")

    # ====================== Get data for selected bill ======================
    def get_data(self, ev):
        index_ = self.Sales_List.curselection()
        if not index_:
            return
        file_name = self.Sales_List.get(index_)
        self.bill_area.delete('1.0', END)
        try:
            with open(f'bill/{file_name}', 'r') as fp:
                for line in fp:
                    self.bill_area.insert(END, line)
        except Exception as ex:
            messagebox.showerror("Error", f"Could not read file: {str(ex)}", parent=self.root)

    # ====================== Search invoice ======================
    def search(self):
        if self.var_invoice.get() == "":
            messagebox.showerror("Error", "Invoice no. should be required", parent=self.root)
        else:
            # Sort the bill list first to ensure binary search works correctly
            self.bill_list.sort()
            
            # Use manual binary search
            index = self.binary_search(self.bill_list, self.var_invoice.get())
            if index != -1:
                # Invoice found
                file_name = f'{self.bill_list[index]}.txt'
                self.bill_area.delete('1.0', END)
                with open(f'bill/{file_name}', 'r') as fp:
                    for i in fp:
                        self.bill_area.insert(END, i)
            else:
                messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)


    # ====================== Clear ======================
    def clear(self):
        self.var_invoice.set("")
        self.bill_area.delete('1.0', END)
        self.show()  # Reload and sort invoices

# ====================== Main Window ======================
if __name__ == "__main__":
    root = Tk()
    obj = salesClass(root)
    root.mainloop()
