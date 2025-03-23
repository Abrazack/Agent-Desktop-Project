import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from tkinter.constants import BOTH, YES
import os
import json
from datetime import datetime
import hashlib
import random
import string
import pandas as pd

# File paths
USER_FILE = "users.json"
LOG_FILE = "log.txt"
INVENTORY_FILE = "inventory.json"
SALES_FILE = "sales.json"
SUPPLIERS_FILE = "suppliers.json"

# Brand colors
COLOR_BG = "#f3ddb3"
COLOR_PRIMARY = "#f3a157"
COLOR_SECONDARY = "#2f7366"
COLOR_ACCENT = "#0261d9"
COLOR_ERROR = "#d87487"

# Gradient colors for 3D effect
GRADIENT_BG = "#f3ddb3"
GRADIENT_PRIMARY = "#f3a157"
GRADIENT_SECONDARY = "#2f7366"
GRADIENT_ACCENT = "#0261d9"

def log_activity(message):
    max_log_size = 10 * 1024 * 1024  # 10 MB
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > max_log_size:
        with open(LOG_FILE, "w") as log:
            log.write("")  # Clear the log file
    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.now()} - {message}\n")

def load_data(file):
    try:
        if not os.path.exists(file):
            return {}
        with open(file, "r") as f:
            return json.load(f)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")
        return {}

def save_data(data, file):
    try:
        with open(file, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {e}")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    return hashlib.sha256(password.encode()).hexdigest() == hashed_password

def generate_username(first_name, last_name, users):
    base_username = (first_name[0] + last_name).lower()
    username = base_username
    count = 1
    while username in users:
        username = f"{base_username}{count}"
        count += 1
    return username

def generate_strong_password():
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    symbols = string.punctuation
    password = [
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(digits),
        random.choice(symbols),
    ]
    for _ in range(6):
        password.append(random.choice(uppercase + lowercase + digits + symbols))
    random.shuffle(password)
    return "".join(password)

class RoleSelectionWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Select Role")
        self.root.geometry("400x300")
        self.root.configure(bg=GRADIENT_BG)
        
        main_frame = tk.Frame(root, bg=GRADIENT_BG, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="Select Your Role", font=("Helvetica", 18, "bold"), 
                bg=GRADIENT_BG, fg=GRADIENT_SECONDARY).pack(pady=20)
        
        tk.Button(main_frame, text="Login as Admin", command=lambda: self.open_login("admin"), 
                width=20, height=2, bg=GRADIENT_PRIMARY, fg="white", font=("Helvetica", 12, "bold"), 
                relief=tk.RAISED, bd=3).pack(pady=10)
        
        tk.Button(main_frame, text="Login as Employee", command=lambda: self.open_login("employee"), 
                width=20, height=2, bg=GRADIENT_ACCENT, fg="white", font=("Helvetica", 12, "bold"), 
                relief=tk.RAISED, bd=3).pack(pady=10)

    def open_login(self, role):
        print(f"Opening login window for {role}")  # Debugging
        self.root.withdraw()  # Hide role selection window
        LoginWindow(self.root, role)

class LoginWindow:
    def __init__(self, master, role):
        self.master = master
        self.role = role
        
        self.window = tk.Toplevel(master)
        self.window.title("Login")
        self.window.geometry("400x300")
        self.window.configure(bg=GRADIENT_BG)
        
        main_frame = tk.Frame(self.window, bg=GRADIENT_BG, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text=f"Login as {role.capitalize()}", font=("Helvetica", 18, "bold"), 
                bg=GRADIENT_BG, fg=GRADIENT_SECONDARY).pack(pady=20)
        
        tk.Label(main_frame, text="Username:", bg=GRADIENT_BG, fg=GRADIENT_SECONDARY, 
                font=("Helvetica", 12)).pack(pady=5)
        self.username_entry = tk.Entry(main_frame, width=20, font=("Helvetica", 12))
        self.username_entry.pack()
        
        tk.Label(main_frame, text="Password:", bg=GRADIENT_BG, fg=GRADIENT_SECONDARY, 
                font=("Helvetica", 12)).pack(pady=5)
        self.password_entry = tk.Entry(main_frame, width=20, show="*", font=("Helvetica", 12))
        self.password_entry.pack()
        
        tk.Button(main_frame, text="Login", command=self.login, 
                width=15, bg=GRADIENT_PRIMARY, fg="white", font=("Helvetica", 12, "bold"), 
                relief=tk.RAISED, bd=3).pack(pady=20)
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.users = load_data(USER_FILE)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        stored_user = self.users.get(username)
        
        if stored_user and verify_password(password, stored_user["password"]) and stored_user["role"] == self.role:
            log_activity(f"{username} ({self.role}) logged in successfully.")
            self.window.destroy()
            self.master.destroy()  # Close all windows
            main_app(username, self.role)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials", parent=self.window)
            log_activity(f"Failed login attempt for {username} as {self.role}.")

    def on_close(self):
        print("Closing login window")  # Debugging
        self.window.destroy()
        self.master.deiconify()  # Show role selection window again

class AgentDesktop:
    def __init__(self, root, username, role):
        self.root = root
        self.root.title("Agent Desktop")
        self.root.geometry("1000x600")
        self.root.configure(bg=GRADIENT_BG)
        self.username = username
        self.role = role
        
        main_frame = tk.Frame(root, bg=GRADIENT_BG, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text=f"Welcome, {username} ({role})", font=("Helvetica", 18, "bold"), 
                bg=GRADIENT_BG, fg=GRADIENT_SECONDARY).pack(pady=20)
        
        if role == "admin":
            self.create_admin_interface(main_frame)
        else:
            self.create_employee_interface(main_frame)
            
        tk.Button(main_frame, text="Exit", command=root.quit, width=20, height=2, 
                bg=COLOR_ERROR, fg="white", font=("Helvetica", 12, "bold"), 
                relief=tk.RAISED, bd=3).pack(pady=20)

    def create_admin_interface(self, parent):
        tk.Button(parent, text="Manage Employees", command=self.manage_employees, width=20, height=2, 
                bg=GRADIENT_PRIMARY, fg="white", font=("Helvetica", 12, "bold"), 
                relief=tk.RAISED, bd=3).pack(pady=10)
        tk.Button(parent, text="Manage Inventory", command=self.manage_inventory, width=20, height=2, 
                bg=GRADIENT_ACCENT, fg="white", font=("Helvetica", 12, "bold"), 
                relief=tk.RAISED, bd=3).pack(pady=10)
        tk.Button(parent, text="Manage Suppliers", command=self.manage_suppliers, width=20, height=2, 
                bg=GRADIENT_SECONDARY, fg="white", font=("Helvetica", 12, "bold"), 
                relief=tk.RAISED, bd=3).pack(pady=10)
        tk.Button(parent, text="View Sales", command=self.view_sales, width=20, height=2, 
                bg=GRADIENT_SECONDARY, fg="white", font=("Helvetica", 12, "bold"), 
                relief=tk.RAISED, bd=3).pack(pady=10)

    def create_employee_interface(self, parent):
        tk.Button(parent, text="View Inventory", command=self.view_inventory, width=20, height=2, 
                bg=GRADIENT_ACCENT, fg="white", font=("Helvetica", 12, "bold"), 
                relief=tk.RAISED, bd=3).pack(pady=10)
        tk.Button(parent, text="View Profile", command=self.view_profile, width=20, height=2, 
                bg=GRADIENT_SECONDARY, fg="white", font=("Helvetica", 12, "bold"), 
                relief=tk.RAISED, bd=3).pack(pady=10)

    def manage_employees(self):
        messagebox.showinfo("Manage Employees", "Employee management functionality will be implemented here.")

    def manage_inventory(self):
        messagebox.showinfo("Manage Inventory", "Inventory management functionality will be implemented here.")

    def manage_suppliers(self):
        messagebox.showinfo("Manage Suppliers", "Supplier management functionality will be implemented here.")

    def view_sales(self):
        messagebox.showinfo("View Sales", "Sales viewing functionality will be implemented here.")

    def view_inventory(self):
        messagebox.showinfo("View Inventory", "Inventory viewing functionality will be implemented here.")

    def view_profile(self):
        messagebox.showinfo("View Profile", "Profile viewing functionality will be implemented here.")

def main_app(username, role):
    root = tk.Tk()
    app = AgentDesktop(root, username, role)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = RoleSelectionWindow(root)
    root.mainloop()
