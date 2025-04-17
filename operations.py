from database import connect_db
from prettytable import PrettyTable
import datetime

def add_medicine(name, category, quantity, price, expiry_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO medicines (name, category, quantity, price, expiry_date) VALUES (?, ?, ?, ?, ?)",
                   (name, category, quantity, price, expiry_date))
    conn.commit()
    conn.close()

def view_inventory():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines")
    rows = cursor.fetchall()
    table = PrettyTable(["ID", "Name", "Category", "Qty", "Price", "Expiry"])
    for row in rows:
        table.add_row(row)
    print(table)
    conn.close()

def update_medicine_stock(med_id, quantity):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE medicines SET quantity = ? WHERE id = ?", (quantity, med_id))
    conn.commit()
    conn.close()

def sell_medicine(med_id, quantity_sold):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT quantity FROM medicines WHERE id = ?", (med_id,))
    result = cursor.fetchone()

    if result and result[0] >= quantity_sold:
        new_quantity = result[0] - quantity_sold
        update_medicine_stock(med_id, new_quantity)

        sale_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO sales (medicine_id, quantity_sold, sale_date) VALUES (?, ?, ?)",
                       (med_id, quantity_sold, sale_date))
        conn.commit()
        print("Sale recorded successfully.")
    else:
        print("Insufficient stock!")
    
    conn.close()

def low_stock_alert(threshold=5):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines WHERE quantity <= ?", (threshold,))
    rows = cursor.fetchall()
    print("\n🔔 Low Stock Alerts:")
    if rows:
        for row in rows:
            print(f"{row[1]} (ID: {row[0]}) - Quantity: {row[3]}")
    else:
        print("No low stock alerts.")
    conn.close()


def view_inventory():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines")
    rows = cursor.fetchall()
    conn.close()
    return rows

def low_stock_alert(threshold=5):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines WHERE quantity <= ?", (threshold,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_medicine(med_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medicines WHERE id = ?", (med_id,))
    conn.commit()
    conn.close()

def modify_quantity(med_id, new_quantity):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE medicines SET quantity = ? WHERE id = ?", (new_quantity, med_id))
    conn.commit()
    conn.close()

def low_stock_alert(threshold=5):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines WHERE quantity <= ? ORDER BY id DESC", (threshold,))
    rows = cursor.fetchall()
    conn.close()
    return rows
