import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

# Function to connect to MySQL database
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="python"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error connecting to database: {err}")
        return None

# Function to execute SQL queries
def execute_query(query, conn):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error executing query: {err}")

# Function to insert data into the database
def insert_data(user_id, name, email, conn):
    query = f"INSERT INTO users (id, name, email) VALUES ({user_id}, '{name}', '{email}')"
    execute_query(query, conn)
    messagebox.showinfo("Success", "User added successfully!")

# Function to delete data from the database
def delete_data(user_id, conn):
    query = f"DELETE FROM users WHERE id={user_id}"
    execute_query(query, conn)
    messagebox.showinfo("Success", "User deleted successfully!")

# Function to update data in the database
def update_data(user_id, name, email, conn):
    query = f"UPDATE users SET name='{name}', email='{email}' WHERE id={user_id}"
    execute_query(query, conn)
    messagebox.showinfo("Success", "User updated successfully!")

# Function to retrieve data from the database
def retrieve_data(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error retrieving data: {err}")
        return []

# Function to handle the 'Add' button click event
def add_user():
    user_id = int(user_id_entry.get())
    name = name_entry.get()
    email = email_entry.get()
    if user_id and name and email:
        insert_data(user_id, name, email, conn)
        refresh_table()
    else:
        messagebox.showwarning("Warning", "Please enter user ID, name, and email!")

def delete_user():
    selected_item = user_table.selection()
    if selected_item:
        user_id = user_table.item(selected_item, "values")[0]  # Extract user ID from the selected item
        delete_data(user_id, conn)
        refresh_table()
        clear_fields()
    else:
        messagebox.showwarning("Warning", "Please select a user!")

def update_user():
    selected_item = user_table.selection()
    if selected_item:
        user_id = user_table.item(selected_item, "values")[0]  # Extract user ID from the selected item
        name = name_entry.get()
        email = email_entry.get()
        update_data(user_id, name, email, conn)
        refresh_table()
    else:
        messagebox.showwarning("Warning", "Please select a user!")

def fill_fields(event):
    selected_item = user_table.selection()
    if selected_item:
        values = user_table.item(selected_item, "values")
        user_id_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        user_id_entry.insert(0, values[0])
        name_entry.insert(0, values[1])
        email_entry.insert(0, values[2])

def clear_fields():
    user_id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

def refresh_table():
    user_table.delete(*user_table.get_children())
    for row in retrieve_data(conn):
        user_table.insert('', 'end', values=row)
        
# Main application window
root = tk.Tk()
root.title("CRUD Application")

# Database connection
conn = connect_to_db()

# GUI elements
tk.Label(root, text="User ID:").grid(row=0, column=0, padx=5, pady=5)
user_id_entry = tk.Entry(root)
user_id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Name:").grid(row=1, column=0, padx=5, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Email:").grid(row=2, column=0, padx=5, pady=5)
email_entry = tk.Entry(root)
email_entry.grid(row=2, column=1, padx=5, pady=5)

add_button = tk.Button(root, text="Add", command=add_user)
add_button.grid(row=3, column=0, padx=5, pady=5, sticky="we")

update_button = tk.Button(root, text="Update", command=update_user)
update_button.grid(row=3, column=1, padx=5, pady=5, sticky="we")

delete_button = tk.Button(root, text="Delete", command=delete_user)
delete_button.grid(row=3, column=2, padx=5, pady=5, sticky="we")

clear_button = tk.Button(root, text="Clear", command=clear_fields)
clear_button.grid(row=4, column=1, padx=5, pady=5, sticky="we")

user_table = ttk.Treeview(root, columns=("ID", "Name", "Email"), show="headings")
user_table.heading("ID", text="ID")
user_table.heading("Name", text="Name")
user_table.heading("Email", text="Email")
user_table.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

# Populate the table initially
refresh_table()

# Bind the treeview selection event to the fill_fields function
user_table.bind("<<TreeviewSelect>>", fill_fields)

root.mainloop()
