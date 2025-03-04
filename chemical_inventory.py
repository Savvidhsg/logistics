import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # For table view

# 🛢 Initialize Database 
def init_db():
    conn = sqlite3.connect('chemicals.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chemicals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity REAL NOT NULL,
        unit TEXT NOT NULL,
        description TEXT,
        hazard_classification TEXT,
        storage_temperature TEXT,
        expiry_date TEXT
    )
    ''')
    conn.commit()
    conn.close()

init_db()  # Run DB setup

# 🟢 Add Chemical
def add_chemical():
    name = name_entry.get()
    quantity = quantity_entry.get()
    unit = unit_entry.get()
    description = desc_entry.get()
    hazard_class = hazard_entry.get()
    storage_temp = storage_entry.get()
    expiry_date = expiry_entry.get()

    if name and quantity and unit and expiry_date:
        try:
            quantity = float(quantity)  # Ensure it's a number
            conn = sqlite3.connect('chemicals.db')
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO chemicals (name, quantity, unit, description, hazard_classification, storage_temperature, expiry_date) 
                VALUES (?, ?, ?, ?, ?, ?, ?)""", 
                (name, quantity, unit, description, hazard_class, storage_temp, expiry_date))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Added {name} ({quantity} {unit})")
            clear_entries()
            show_chemicals()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Warning", "Please fill all required fields.")

# 🔍 View Chemicals
def show_chemicals():
    conn = sqlite3.connect('chemicals.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, quantity, unit, description, hazard_classification, storage_temperature, expiry_date FROM chemicals')
    rows = cursor.fetchall()
    conn.close()

    tree.delete(*tree.get_children())  # Clear previous data
    for row in rows:
        tree.insert("", "end", values=row)

# 🗑 Delete Chemical
def delete_chemical():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a chemical to delete.")
        return
    
    chem_id = tree.item(selected_item, "values")[0]  # Get selected row ID
    conn = sqlite3.connect('chemicals.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chemicals WHERE id = ?", (chem_id,))
    conn.commit()
    conn.close()

    tree.delete(selected_item)  # Remove from UI
    messagebox.showinfo("Deleted", "Chemical deleted successfully.")

# 📝 Update Chemical
def update_chemical():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a chemical to update.")
        return

    chem_id = tree.item(selected_item, "values")[0]
    name = name_entry.get()
    quantity = quantity_entry.get()
    unit = unit_entry.get()
    description = desc_entry.get()
    hazard_class = hazard_entry.get()
    storage_temp = storage_entry.get()
    expiry_date = expiry_entry.get()

    if name and quantity and unit and expiry_date:
        try:
            quantity = float(quantity)
            conn = sqlite3.connect('chemicals.db')
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE chemicals 
                SET name=?, quantity=?, unit=?, description=?, hazard_classification=?, storage_temperature=?, expiry_date=? 
                WHERE id=?""",
                (name, quantity, unit, description, hazard_class, storage_temp, expiry_date, chem_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Updated {name}")
            show_chemicals()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Warning", "Please fill all fields.")

# 🧹 Clear Input Fields
def clear_entries():
    name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    unit_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    hazard_entry.delete(0, tk.END)
    storage_entry.delete(0, tk.END)
    expiry_entry.delete(0, tk.END)

# Initialize Tkinter window
root = tk.Tk()
root.title("Chemical Inventory Management")
root.geometry("800x500")

# 📌 Labels and Entry Fields (INPUT BOXES)
tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
name_entry = tk.Entry(root, width=30)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Quantity:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
quantity_entry = tk.Entry(root, width=30)
quantity_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Unit:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
unit_entry = tk.Entry(root, width=30)
unit_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Description:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
desc_entry = tk.Entry(root, width=30)
desc_entry.grid(row=3, column=1, padx=10, pady=5)

# 📌 New UI Fields for Safety & Hazard Information
tk.Label(root, text="Hazard Classification:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
hazard_entry = tk.Entry(root, width=30)
hazard_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Storage Temperature:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
storage_entry = tk.Entry(root, width=30)
storage_entry.grid(row=5, column=1, padx=10, pady=5)

# 📌 Expiry Date Field
tk.Label(root, text="Expiry Date (YYYY-MM-DD):").grid(row=6, column=0, padx=10, pady=5, sticky="w")
expiry_entry = tk.Entry(root, width=30)
expiry_entry.grid(row=6, column=1, padx=10, pady=5)

# 📌 Buttons
tk.Button(root, text="Add Chemical", command=add_chemical).grid(row=7, column=0, columnspan=2, padx=10, pady=5)
tk.Button(root, text="Delete Chemical", command=delete_chemical).grid(row=8, column=0, columnspan=2, padx=10, pady=5)
tk.Button(root, text="Update Chemical", command=update_chemical).grid(row=9, column=0, columnspan=2, padx=10, pady=5)

# 📌 Table (Treeview)
columns = ("ID", "Name", "Quantity", "Unit", "Description", "Hazard Classification", "Storage Temperature", "Expiry Date")
tree = ttk.Treeview(root, columns=columns, show="headings")

# Set column headers
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)  # Adjust width

tree.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

# Load data on startup
show_chemicals()

# Start Tkinter loop
root.mainloop()
