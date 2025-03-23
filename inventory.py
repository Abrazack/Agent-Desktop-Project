import tkinter as tk
from tkinter import messagebox

# Inventory Data (Dictionary Format)
inventory = {}

# Add Item to Inventory
def add_item():
    item = item_entry.get()
    quantity = quantity_entry.get()

    if item and quantity.isdigit():
        inventory[item] = inventory.get(item, 0) + int(quantity)
        update_display()
        item_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Enter valid item and quantity!")

# Remove Item from Inventory
def remove_item():
    item = item_entry.get()

    if item in inventory:
        del inventory[item]
        update_display()
        item_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Item not found!")

# Display Inventory
def update_display():
    inventory_display.delete(1.0, tk.END)
    for item, quantity in inventory.items():
        inventory_display.insert(tk.END, f"{item}: {quantity} pcs\n")

# GUI Setup
root = tk.Tk()
root.title("Inventory System")
root.geometry("400x400")

# Labels
tk.Label(root, text="Item Name:").pack()
item_entry = tk.Entry(root)
item_entry.pack()

tk.Label(root, text="Quantity:").pack()
quantity_entry = tk.Entry(root)
quantity_entry.pack()

# Buttons
tk.Button(root, text="Add Item", command=add_item).pack(pady=5)
tk.Button(root, text="Remove Item", command=remove_item).pack(pady=5)

# Inventory Display
inventory_display = tk.Text(root, height=10, width=40)
inventory_display.pack()

# Run the App
root.mainloop()
