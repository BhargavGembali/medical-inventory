import sqlite3

def connect_db():
    return sqlite3.connect("medical_store.db")

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            quantity INTEGER,
            price REAL,
            expiry_date TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_id INTEGER,
            quantity_sold INTEGER,
            sale_date TEXT,
            FOREIGN KEY(medicine_id) REFERENCES medicines(id)
        )
    """)
    
    conn.commit()
    conn.close()
