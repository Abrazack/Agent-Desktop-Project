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

# Brand colors
COLOR_BG = "#f3ddb3"
COLOR_PRIMARY = "#f3a157"
COLOR_SECONDARY = "#2f7366"
COLOR_ACCENT = "#0261d9"
COLOR_ERROR = "#d87487"

def log_activity(message):
    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.now()} - {message}\n")

def load_users():
    if not os.path.exists(USER_FILE):
        return {"admin": {"password": hash_password("admin123"), "role": "admin"}}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        return {}
    with open(INVENTORY_FILE, "r") as f:
        return json.load(f)

def save_inventory(inventory):
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

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
        self.root.configure(bg=COLOR_BG)
        
        main_frame = tk.Frame(root, bg=COLOR_BG, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="Select Your Role", font=("Helvetica", 18, "bold"), 
                bg=COLOR_BG, fg=COLOR_SECONDARY).pack(pady=20)
        
        tk.Button(main_frame, text="Login as Admin", command=lambda: self.open_login("admin"), 
                width=20, height=2, bg=COLOR_PRIMARY, fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)
        
        tk.Button(main_frame, text="Login as Employee", command=lambda: self.open_login("employee"), 
                width=20, height=2, bg=COLOR_ACCENT, fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)

    def open_login(self, role):
        self.root.withdraw()  # Hide role selection window
        LoginWindow(self.root, role)

class LoginWindow:
    def __init__(self, master, role):
        self.master = master
        self.role = role
        
        self.window = tk.Toplevel(master)
        self.window.title("Login")
        self.window.geometry("400x300")
        self.window.configure(bg=COLOR_BG)
        
        main_frame = tk.Frame(self.window, bg=COLOR_BG, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text=f"Login as {role.capitalize()}", font=("Helvetica", 18, "bold"), 
                bg=COLOR_BG, fg=COLOR_SECONDARY).pack(pady=20)
        
        tk.Label(main_frame, text="Username:", bg=COLOR_BG, fg=COLOR_SECONDARY, 
                font=("Helvetica", 12)).pack(pady=5)
        self.username_entry = tk.Entry(main_frame, width=20, font=("Helvetica", 12))
        self.username_entry.pack()
        
        tk.Label(main_frame, text="Password:", bg=COLOR_BG, fg=COLOR_SECONDARY, 
                font=("Helvetica", 12)).pack(pady=5)
        self.password_entry = tk.Entry(main_frame, width=20, show="*", font=("Helvetica", 12))
        self.password_entry.pack()
        
        tk.Button(main_frame, text="Login", command=self.login, 
                width=15, bg=COLOR_PRIMARY, fg="white", font=("Helvetica", 12, "bold")).pack(pady=20)
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.users = load_users()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        stored_user = self.users.get(username)
        
        if stored_user and stored_user["password"] == hash_password(password) and stored_user["role"] == self.role:
            log_activity(f"{username} ({self.role}) logged in successfully.")
            self.window.destroy()
            self.master.destroy()  # Close all windows
            main_app(username, self.role)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials", parent=self.window)
            log_activity(f"Failed login attempt for {username} as {self.role}.")

    def on_close(self):
        self.window.destroy()
        self.master.deiconify()  # Show role selection window again

class AgentDesktop:
    def __init__(self, root, username, role):
        self.root = root
        self.root.title("Agent Desktop")
        self.root.geometry("1000x600")
        self.root.configure(bg=COLOR_BG)
        self.username = username
        self.role = role
        
        main_frame = tk.Frame(root, bg=COLOR_BG, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text=f"Welcome, {username} ({role})", font=("Helvetica", 18, "bold"), 
                bg=COLOR_BG, fg=COLOR_SECONDARY).pack(pady=20)
        
        if role == "admin":
            self.create_admin_interface(main_frame)
        else:
            self.create_employee_interface(main_frame)
            
        tk.Button(main_frame, text="Exit", command=root.quit, width=20, height=2, 
                bg=COLOR_ERROR, fg="white", font=("Helvetica", 12, "bold")).pack(pady=20)

    def create_admin_interface(self, parent):
        tk.Button(parent, text="Manage Employees", command=self.manage_employees, width=20, height=2, 
                bg=COLOR_PRIMARY, fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)
        tk.Button(parent, text="Manage Inventory", command=self.manage_inventory, width=20, height=2, 
                bg=COLOR_ACCENT, fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)
        tk.Button(parent, text="View System Logs", command=self.view_logs, width=20, height=2, 
                bg=COLOR_SECONDARY, fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)

    def create_employee_interface(self, parent):
        tk.Button(parent, text="View Inventory", command=self.view_inventory, width=20, height=2, 
                bg=COLOR_ACCENT, fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)
        tk.Button(parent, text="View Profile", command=self.view_profile, width=20, height=2, 
                bg=COLOR_SECONDARY, fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)

    def manage_employees(self):
        emp_window = tk.Toplevel(self.root)
        emp_window.title("Manage Employees")
        emp_window.geometry("1000x600")
        emp_window.configure(bg=COLOR_BG)

        # Buttons
        button_frame = tk.Frame(emp_window, bg=COLOR_BG)
        button_frame.pack(fill=tk.X, pady=10)

        tk.Button(button_frame, text="Add Employee", command=self.add_employee, width=20, height=2, 
                bg=COLOR_PRIMARY, fg="white", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Edit Employee", command=self.edit_employee, width=20, height=2, 
                bg=COLOR_ACCENT, fg="white", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Reset Password", command=self.reset_password, width=20, height=2, 
                bg=COLOR_SECONDARY, fg="white", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Export to Excel", command=self.export_employees_to_excel, width=20, height=2, 
                bg=COLOR_SECONDARY, fg="white", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Back", command=emp_window.destroy, width=20, height=2, 
                bg=COLOR_ERROR, fg="white", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=5)

        # Employee table
        self.employee_table = ttk.Treeview(emp_window, columns=("Username", "Full Name", "Email", "Phone", "Department", "Job Title"), show="headings")
        self.employee_table.heading("Username", text="Username")
        self.employee_table.heading("Full Name", text="Full Name")
        self.employee_table.heading("Email", text="Email")
        self.employee_table.heading("Phone", text="Phone")
        self.employee_table.heading("Department", text="Department")
        self.employee_table.heading("Job Title", text="Job Title")
        self.employee_table.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Load employee data
        self.load_employee_table()

    def load_employee_table(self):
        # Clear existing data
        for row in self.employee_table.get_children():
            self.employee_table.delete(row)

        # Load data from users.json
        users = load_users()
        for username, details in users.items():
            if details["role"] == "employee":
                self.employee_table.insert("", "end", values=(
                    username,
                    details.get("full_name", "N/A"),
                    details.get("email", "N/A"),
                    details.get("phone", "N/A"),
                    details.get("department", "N/A"),
                    details.get("job_title", "N/A")
                ))

    def add_employee(self):
        first_name = simpledialog.askstring("Add Employee", "Enter first name:")
        last_name = simpledialog.askstring("Add Employee", "Enter last name:")
        users = load_users()
        username = generate_username(first_name, last_name, users)

        # Generate a strong password
        password = generate_strong_password()
        messagebox.showinfo("Generated Password", f"Generated password for {username}: {password}")

        email = simpledialog.askstring("Add Employee", "Enter email:")
        phone = simpledialog.askstring("Add Employee", "Enter phone number:")
        department = simpledialog.askstring("Add Employee", "Enter department:")
        job_title = simpledialog.askstring("Add Employee", "Enter job title:")

        if username and password:
            users[username] = {"password": hash_password(password), "role": "employee", "full_name": f"{first_name} {last_name}", "email": email, "phone": phone, "department": department, "job_title": job_title}
            save_users(users)
            log_activity(f"Employee {username} added with system-generated password.")
            messagebox.showinfo("Success", f"Employee added successfully. Username: {username}")
            self.load_employee_table()

    def edit_employee(self):
        selected_item = self.employee_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an employee to edit.")
            return

        username = self.employee_table.item(selected_item, "values")[0]
        users = load_users()
        if username in users:
            new_password = simpledialog.askstring("Edit Employee", "Enter new password (leave blank to keep current):")
            new_email = simpledialog.askstring("Edit Employee", "Enter new email (leave blank to keep current):")
            new_phone = simpledialog.askstring("Edit Employee", "Enter new phone number (leave blank to keep current):")
            new_department = simpledialog.askstring("Edit Employee", "Enter new department (leave blank to keep current):")
            new_job_title = simpledialog.askstring("Edit Employee", "Enter new job title (leave blank to keep current):")

            if new_password:
                users[username]["password"] = hash_password(new_password)
            if new_email:
                users[username]["email"] = new_email
            if new_phone:
                users[username]["phone"] = new_phone
            if new_department:
                users[username]["department"] = new_department
            if new_job_title:
                users[username]["job_title"] = new_job_title

            save_users(users)
            log_activity(f"Employee {username} edited.")
            messagebox.showinfo("Success", f"Employee {username} updated successfully.")
            self.load_employee_table()
        else:
            messagebox.showerror("Error", "Employee not found.")

    def reset_password(self):
        selected_item = self.employee_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an employee to reset password.")
            return

        username = self.employee_table.item(selected_item, "values")[0]
        users = load_users()
        if username in users:
            # Generate a strong password
            new_password = generate_strong_password()
            users[username]["password"] = hash_password(new_password)
            save_users(users)
            log_activity(f"Password reset for {username}.")
            messagebox.showinfo("Password Reset", f"Password reset successfully. New password: {new_password}")
        else:
            messagebox.showerror("Error", "Employee not found.")

    def export_employees_to_excel(self):
        users = load_users()
        employee_data = []
        for username, details in users.items():
            if details["role"] == "employee":
                employee_data.append([
                    username,
                    details.get("full_name", "N/A"),
                    details.get("email", "N/A"),
                    details.get("phone", "N/A"),
                    details.get("department", "N/A"),
                    details.get("job_title", "N/A")
                ])

        # Create a DataFrame
        df = pd.DataFrame(employee_data, columns=["Username", "Full Name", "Email", "Phone", "Department", "Job Title"])

        # Save to Excel
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Success", f"Employee data exported to {file_path}")

    def manage_inventory(self):
        inv_window = tk.Toplevel(self.root)
        inv_window.title("Manage Inventory")
        inv_window.geometry("1000x600")
        inv_window.configure(bg=COLOR_BG)

        # Buttons
        button_frame = tk.Frame(inv_window, bg=COLOR_BG)
        button_frame.pack(fill=tk.X, pady=10)

        tk.Button(button_frame, text="Add Item", command=self.add_inventory_item, width=20, height=2, 
                bg=COLOR_PRIMARY, fg="white", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Edit Item", command=self.edit_inventory_item, width=20, height=2, 
                bg=COLOR_ACCENT, fg="white", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Remove Item", command=self.remove_inventory_item, width=20, height=2, 
                bg=COLOR_ERROR, fg="white", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Export to Excel", command=self.export_inventory_to_excel, width=20, height=2, 
                bg=COLOR_SECONDARY, fg="white", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Back", command=inv_window.destroy, width=20, height=2, 
                bg=COLOR_SECONDARY, fg="white", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=5)

        # Inventory table
        self.inventory_table = ttk.Treeview(inv_window, columns=("Item", "Quantity", "Price"), show="headings")
        self.inventory_table.heading("Item", text="Item")
        self.inventory_table.heading("Quantity", text="Quantity")
        self.inventory_table.heading("Price", text="Price")
        self.inventory_table.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Load inventory data
        self.load_inventory_table()

    def load_inventory_table(self):
        # Clear existing data
        for row in self.inventory_table.get_children():
            self.inventory_table.delete(row)

        # Load data from inventory.json
        inventory = load_inventory()
        for item, details in inventory.items():
            self.inventory_table.insert("", "end", values=(
                item,
                details.get("quantity", "N/A"),
                details.get("price", "N/A")
            ))

    def add_inventory_item(self):
        item_name = simpledialog.askstring("Add Item", "Enter item name:")
        quantity = simpledialog.askinteger("Add Item", "Enter quantity:")
        price = simpledialog.askfloat("Add Item", "Enter price:")

        if item_name and quantity and price:
            inventory = load_inventory()
            inventory[item_name] = {"quantity": quantity, "price": price}
            save_inventory(inventory)
            log_activity(f"Inventory item {item_name} added.")
            messagebox.showinfo("Success", f"Inventory item {item_name} added successfully.")
            self.load_inventory_table()

    def edit_inventory_item(self):
        selected_item = self.inventory_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an item to edit.")
            return

        item_name = self.inventory_table.item(selected_item, "values")[0]
        inventory = load_inventory()
        if item_name in inventory:
            new_quantity = simpledialog.askinteger("Edit Item", "Enter new quantity (leave blank to keep current):")
            new_price = simpledialog.askfloat("Edit Item", "Enter new price (leave blank to keep current):")

            if new_quantity:
                inventory[item_name]["quantity"] = new_quantity
            if new_price:
                inventory[item_name]["price"] = new_price

            save_inventory(inventory)
            log_activity(f"Inventory item {item_name} edited.")
            messagebox.showinfo("Success", f"Inventory item {item_name} updated successfully.")
            self.load_inventory_table()
        else:
            messagebox.showerror("Error", "Item not found.")

    def remove_inventory_item(self):
        selected_item = self.inventory_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an item to remove.")
            return

        item_name = self.inventory_table.item(selected_item, "values")[0]
        inventory = load_inventory()
        if item_name in inventory:
            del inventory[item_name]
            save_inventory(inventory)
            log_activity(f"Inventory item {item_name} removed.")
            messagebox.showinfo("Success", f"Inventory item {item_name} removed successfully.")
            self.load_inventory_table()
        else:
            messagebox.showerror("Error", "Item not found.")

    def export_inventory_to_excel(self):
        inventory = load_inventory()
        inventory_data = []
        for item, details in inventory.items():
            inventory_data.append([
                item,
                details.get("quantity", "N/A"),
                details.get("price", "N/A")
            ])

        # Create a DataFrame
        df = pd.DataFrame(inventory_data, columns=["Item", "Quantity", "Price"])

        # Save to Excel
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Success", f"Inventory data exported to {file_path}")

    def view_profile(self):
        users = load_users()
        user = users.get(self.username)
        if user:
            profile_info = f"Username: {self.username}\nFull Name: {user.get('full_name', 'N/A')}\nEmail: {user.get('email', 'N/A')}\nPhone: {user.get('phone', 'N/A')}\nDepartment: {user.get('department', 'N/A')}\nJob Title: {user.get('job_title', 'N/A')}"
            messagebox.showinfo("Your Profile", profile_info)
        else:
            messagebox.showerror("Error", "User not found.")

    def view_logs(self):
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as log:
                logs = log.read()
            messagebox.showinfo("System Logs", logs if logs else "No logs found.")
        else:
            messagebox.showerror("Error", "Log file not found.")

def main_app(username, role):
    root = tk.Tk()
    app = AgentDesktop(root, username, role)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    RoleSelectionWindow(root)
    root.mainloop()
