# Python code for a Tkinter GUI with SQLite database

import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Database setup
conn = sqlite3.connect('time_tracking.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS clock_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    clock_in_time TEXT,
    clock_out_time TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

conn.commit()

# GUI setup
class TimeTrackingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracking App")
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Username").grid(row=0, column=0)
        tk.Label(self.root, text="Password").grid(row=1, column=0)
        
        self.username_entry = tk.Entry(self.root)
        self.password_entry = tk.Entry(self.root, show="*")
        
        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)
        
        tk.Button(self.root, text="Login", command=self.login).grid(row=2, column=0, columnspan=2)
        tk.Button(self.root, text="Register", command=self.create_registration_screen).grid(row=3, column=0, columnspan=2)

    def create_registration_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="New Username").grid(row=0, column=0)
        tk.Label(self.root, text="New Password").grid(row=1, column=0)
        
        self.new_username_entry = tk.Entry(self.root)
        self.new_password_entry = tk.Entry(self.root, show="*")
        
        self.new_username_entry.grid(row=0, column=1)
        self.new_password_entry.grid(row=1, column=1)
        
        tk.Button(self.root, text="Register", command=self.register).grid(row=2, column=0, columnspan=2)
        tk.Button(self.root, text="Back to Login", command=self.create_login_screen).grid(row=3, column=0, columnspan=2)

    def create_main_screen(self):
        self.clear_screen()
        
        # Display the logged-in username
        tk.Label(self.root, text=f"Logged in as: {self.username}").grid(row=0, column=0, columnspan=3)
        
        self.clock_in_button = tk.Button(self.root, text="Clock In", command=self.clock_in)
        self.clock_out_button = tk.Button(self.root, text="Clock Out", command=self.clock_out)
        self.view_hours_button = tk.Button(self.root, text="View Hours", command=self.view_hours)
        
        self.clock_in_button.grid(row=1, column=0)
        self.clock_out_button.grid(row=1, column=1)
        self.view_hours_button.grid(row=1, column=2)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        c.execute('SELECT id FROM users WHERE username=? AND password=?', (username, password))
        user = c.fetchone()
        
        if user:
            self.user_id = user[0]
            self.username = username  # Store the username
            self.create_main_screen()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()
        
        try:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (new_username, new_password))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully")
            self.create_login_screen()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

    def clock_in(self):
        # Check if there is an existing clock-in without a clock-out
        c.execute('SELECT id FROM clock_records WHERE user_id=? AND clock_out_time IS NULL', (self.user_id,))
        if c.fetchone():
            messagebox.showerror("Error", "You must clock out before clocking in again.")
            return
        
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute('INSERT INTO clock_records (user_id, clock_in_time) VALUES (?, ?)', (self.user_id, now))
        conn.commit()
        messagebox.showinfo("Info", "Clocked in at " + now)
        self.update_clock_buttons()

    def clock_out(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute('UPDATE clock_records SET clock_out_time=? WHERE user_id=? AND clock_out_time IS NULL', (now, self.user_id))
        conn.commit()
        messagebox.showinfo("Info", "Clocked out at " + now)
        self.update_clock_buttons()

    def view_hours(self):
        c.execute('SELECT clock_in_time, clock_out_time FROM clock_records WHERE user_id=?', (self.user_id,))
        records = c.fetchall()
        
        total_hours = 0
        for record in records:
            if record[1]:
                clock_in = datetime.strptime(record[0], '%Y-%m-%d %H:%M:%S')
                clock_out = datetime.strptime(record[1], '%Y-%m-%d %H:%M:%S')
                total_hours += (clock_out - clock_in).total_seconds() / 3600
        
        messagebox.showinfo("Total Hours", f"{self.username} worked a total hours: {total_hours:.2f}")

    def update_clock_buttons(self):
        # Check if there is an existing clock-in without a clock-out
        c.execute('SELECT id FROM clock_records WHERE user_id=? AND clock_out_time IS NULL', (self.user_id,))
        if c.fetchone():
            self.clock_in_button.grid_remove()
            self.clock_out_button.grid()
        else:
            self.clock_in_button.grid()
            self.clock_out_button.grid_remove()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackingApp(root)
    root.mainloop()
