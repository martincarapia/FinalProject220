# Python code for a Tkinter GUI with SQLite database

import sqlite3
import tkinter as tk
from tkinter import messagebox
import databaselink as database

class TimeTrackingApp:
    """
    A class to represent the Time Tracking application GUI.
    """

    def __init__(self, root):
        """
        Initialize the TimeTrackingApp instance with the root window and setup the GUI.

        Args:
            root (tk.Tk): The root window of the Tkinter application.
        """
        self.root = root
        self.root.title("Time Tracking")

        # Setup the database
        database.setup_database()

        # GUI elements
        self.label_username = tk.Label(root, text="Username")
        self.label_username.pack()
        self.entry_username = tk.Entry(root)
        self.entry_username.pack()

        self.label_password = tk.Label(root, text="Password")
        self.label_password.pack()
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack()

        self.button_register = tk.Button(root, text="Register", command=self.register_user)
        self.button_register.pack()

    def register_user(self):
        """
        Register a new user by getting the username and password from the entry fields.
        If the username and password are valid, add the user to the database.
        Display appropriate messages for success or error.

        Raises:
            sqlite3.IntegrityError: If the username already exists in the database.
        """
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username and password:
            try:
                database.add_user(username, password)
                messagebox.showinfo("Success", "User registered successfully!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists!")
        else:
            messagebox.showerror("Error", "Please enter both username and password.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackingApp(root)
    root.mainloop()