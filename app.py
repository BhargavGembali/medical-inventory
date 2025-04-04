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

refresh_inventory()
root.mainloop()
