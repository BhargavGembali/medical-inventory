import tkinter as tk
from tkinter import messagebox, ttk
from database import create_tables
from operations import *

create_tables()

root = tk.Tk()
root.title("Medical Store Inventory")
root.geometry("800x500")

# --------- Helper Functions ---------

def refresh_inventory():
    for row in tree.get_children():
        tree.delete(row)
    data = view_inventory()
    for row in data:
        tree.insert('', tk.END, values=row)

def add_medicine_popup():
    popup = tk.Toplevel(root)
    popup.title("Add Medicine")
    popup.geometry("300x300")

    labels = ["Name", "Category", "Quantity", "Price", "Expiry (YYYY-MM-DD)"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(popup, text=label).pack()
        entry = tk.Entry(popup)
        entry.pack()
        entries.append(entry)

    def submit():
        try:
            name = entries[0].get()
            category = entries[1].get()
            quantity = int(entries[2].get())
            price = float(entries[3].get())
            expiry = entries[4].get()

            add_medicine(name, category, quantity, price, expiry)
            messagebox.showinfo("Success", "Medicine added!")
            popup.destroy()
            refresh_inventory()
        except:
            messagebox.showerror("Error", "Invalid input!")

    tk.Button(popup, text="Add", command=submit).pack(pady=10)

def sell_medicine_popup():
    popup = tk.Toplevel(root)
    popup.title("Sell Medicine")
    popup.geometry("250x200")

    tk.Label(popup, text="Medicine ID").pack()
    id_entry = tk.Entry(popup)
    id_entry.pack()

    tk.Label(popup, text="Quantity to sell").pack()
    qty_entry = tk.Entry(popup)
    qty_entry.pack()

    def sell():
        try:
            med_id = int(id_entry.get())
            qty = int(qty_entry.get())
            sell_medicine(med_id, qty)
            popup.destroy()
            refresh_inventory()
        except:
            messagebox.showerror("Error", "Invalid input or stock too low.")

    tk.Button(popup, text="Sell", command=sell).pack(pady=10)

def show_low_stock():
    low_stock = low_stock_alert()
    msg = "\n".join([f"{row[1]} (ID: {row[0]}, Qty: {row[3]})" for row in low_stock])
    if msg:
        messagebox.showwarning("Low Stock Alert", msg)
    else:
        messagebox.showinfo("All Good", "No low stock items!")

def delete_medicine_popup():
    popup = tk.Toplevel(root)
    popup.title("Delete Medicine")
    popup.geometry("250x150")

    tk.Label(popup, text="Enter Medicine ID to delete").pack(pady=5)
    id_entry = tk.Entry(popup)
    id_entry.pack()

    def delete():
        try:
            med_id = int(id_entry.get())
            delete_medicine(med_id)
            popup.destroy()
            refresh_inventory()
            messagebox.showinfo("Deleted", "Medicine deleted.")
        except:
            messagebox.showerror("Error", "Invalid ID!")

    tk.Button(popup, text="Delete", command=delete).pack(pady=10)


def modify_quantity_popup():
    popup = tk.Toplevel(root)
    popup.title("Modify Quantity")
    popup.geometry("250x200")

    tk.Label(popup, text="Medicine ID").pack()
    id_entry = tk.Entry(popup)
    id_entry.pack()

    tk.Label(popup, text="New Quantity").pack()
    qty_entry = tk.Entry(popup)
    qty_entry.pack()

    def modify():
        try:
            med_id = int(id_entry.get())
            qty = int(qty_entry.get())
            modify_quantity(med_id, qty)
            popup.destroy()
            refresh_inventory()
            messagebox.showinfo("Updated", "Quantity updated.")
        except:
            messagebox.showerror("Error", "Invalid input!")

    tk.Button(popup, text="Update", command=modify).pack(pady=10)


def show_low_stock():
    low_stock = low_stock_alert()
    if not low_stock:
        messagebox.showinfo("All Good", "No low stock items!")
        return

    popup = tk.Toplevel(root)
    popup.title("Low Stock Items")
    popup.geometry("600x300")

    cols = ("ID", "Name", "Category", "Quantity", "Price", "Expiry")
    stock_tree = ttk.Treeview(popup, columns=cols, show='headings')
    for col in cols:
        stock_tree.heading(col, text=col)
        stock_tree.column(col, width=100)
    stock_tree.pack(fill="both", expand=True)

    for row in low_stock:
        stock_tree.insert('', tk.END, values=row)


def show_sales():
    sales = view_sales()
    if not sales:
        messagebox.showinfo("No Sales", "No sales recorded yet!")
        return

    popup = tk.Toplevel(root)
    popup.title("Sales Records")
    popup.geometry("600x300")

    cols = ("Sale ID", "Medicine Name", "Quantity Sold", "Sale Date")
    sales_tree = ttk.Treeview(popup, columns=cols, show='headings')
    for col in cols:
        sales_tree.heading(col, text=col)
        sales_tree.column(col, width=150)
    sales_tree.pack(fill="both", expand=True)

    for row in sales:
        sales_tree.insert('', tk.END, values=row)




# --------- Treeview (Inventory Table) ---------

columns = ("ID", "Name", "Category", "Quantity", "Price", "Expiry")
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack(pady=20, fill="x")

# --------- Buttons ---------

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Medicine", width=15, command=add_medicine_popup).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Sell Medicine", width=15, command=sell_medicine_popup).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Low Stock Alert", width=15, command=show_low_stock).grid(row=0, column=2, padx=10)
tk.Button(btn_frame, text="Refresh", width=15, command=refresh_inventory).grid(row=0, column=3, padx=10)
tk.Button(btn_frame, text="Delete Medicine", width=15, command=delete_medicine_popup).grid(row=1, column=0, padx=10, pady=5)
tk.Button(btn_frame, text="Modify Quantity", width=15, command=modify_quantity_popup).grid(row=1, column=1, padx=10, pady=5)
tk.Button(btn_frame, text="📊 View Sales", width=15, command=show_sales).grid(row=1, column=2, padx=10, pady=5)


refresh_inventory()
root.mainloop()
