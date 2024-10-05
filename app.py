import tkinter as tk
from tkinter import messagebox
import sqlite3

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Item Name").grid(row=0, column=0)
        self.item_name_entry = tk.Entry(self.root)
        self.item_name_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Quantity").grid(row=1, column=0)
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Price").grid(row=2, column=0)
        self.price_entry = tk.Entry(self.root)
        self.price_entry.grid(row=2, column=1)

        tk.Button(self.root, text="Add Item", command=self.add_item).grid(row=3, column=0)
        tk.Button(self.root, text="View Inventory", command=self.view_inventory).grid(row=3, column=1)

        self.inventory_listbox = tk.Listbox(self.root, width=50)
        self.inventory_listbox.grid(row=4, column=0, columnspan=2)

    def add_item(self):
        item_name = self.item_name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        if not item_name or not quantity or not price:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO inventory (item_name, quantity, price) VALUES (?, ?, ?)",
                       (item_name, quantity, price))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Added {item_name} to inventory.")
        self.item_name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

    def view_inventory(self):
        self.inventory_listbox.delete(0, tk.END)

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory")
        items = cursor.fetchall()

        for item in items:
            self.inventory_listbox.insert(tk.END, f"ID: {item[0]}, Name: {item[1]}, Quantity: {item[2]}, Price: {item[3]}")

        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
