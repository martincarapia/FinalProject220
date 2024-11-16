# Python code for a Tkinter GUI with SQLite database

import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import databaselink as database
from User import User

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
        self.root.title("Time Tracking App")
        self.root.geometry("800x600")  # Set the window size to 800x600 pixels
        self.large_font = ('Helvetica', 20)
        self.create_login_screen()

        database.setup_database()

    def create_login_screen(self):
        """
        Create the login screen with username and password entry fields and login/register buttons.
        """
        self.clear_screen()
        
        tk.Label(self.root, text="Username", font=self.large_font).grid(row=0, column=0)
        tk.Label(self.root, text="Password", font=self.large_font).grid(row=1, column=0)
        
        self.username_entry = tk.Entry(self.root, font=self.large_font)
        self.password_entry = tk.Entry(self.root, show="*", font=self.large_font)
        
        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)
        
        tk.Button(self.root, text="Login", command=self.login, font=self.large_font).grid(row=2, column=0, columnspan=2)
        tk.Button(self.root, text="Register", command=self.create_registration_screen, font=self.large_font).grid(row=3, column=0, columnspan=2)

    def create_registration_screen(self):
        """
        Create the registration screen with new username and password entry fields and register/back buttons.
        """
        self.clear_screen()
        tk.Label(self.root, text="New Username", font=self.large_font).grid(row=0, column=0)
        tk.Label(self.root, text="New Password", font=self.large_font).grid(row=1, column=0)
        
        self.new_username_entry = tk.Entry(self.root, font=self.large_font)
        self.new_password_entry = tk.Entry(self.root, show="*", font=self.large_font)
        
        self.new_username_entry.grid(row=0, column=1)
        self.new_password_entry.grid(row=1, column=1)
        
        tk.Button(self.root, text="Register", command=self.register_user, font=self.large_font).grid(row=2, column=0, columnspan=2)
        tk.Button(self.root, text="Back to Login", command=self.create_login_screen, font=self.large_font).grid(row=3, column=0, columnspan=2)

    def create_main_screen(self):
        """
        Create the main screen with clock in, clock out, view hours, and logout buttons.
        """
        self.clear_screen()
        
        # Display the logged-in username
        tk.Label(self.root, text=f"Logged in as: {self.user.username}", font=self.large_font).grid(row=0, column=0, columnspan=3)
        
        self.clock_in_button = tk.Button(self.root, text="Clock In", command=self.clock_in, font=self.large_font)
        self.clock_out_button = tk.Button(self.root, text="Clock Out", command=self.clock_out, font=self.large_font)
        self.view_hours_button = tk.Button(self.root, text="View Hours", command=self.view_hours, font=self.large_font)
        self.logout_button = tk.Button(self.root, text="Logout", command=self.logout, font=self.large_font)
        
        self.clock_in_button.grid(row=1, column=0)
        self.clock_out_button.grid(row=1, column=1)
        self.view_hours_button.grid(row=1, column=2)
        self.logout_button.grid(row=2, column=0, columnspan=3)
        self.update_clock_buttons()
    def clear_screen(self):
        """
        Clear all widgets from the root window.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        """
        Handle the login process by verifying the username and password.
        If valid, proceed to the main screen.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            user_data = database.get_user(username)
            if user_data and user_data[2] == password:
                self.user = User(user_data[0], user_data[1], user_data[2])
                self.create_main_screen()
                self.update_clock_buttons()
            else:
                messagebox.showerror("Error", "Invalid credentials")
        except sqlite3.OperationalError:
            messagebox.showerror("UserNotFound", "User doesn't exist, please specify a valid user or register a new one")
        except sqlite3.Error:
            messagebox.showerror("Error", "An error occurred while retrieving user information")

    def register_user(self):
        """
        Handle the registration process by adding a new user to the database.
        """
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        try:
            database.add_user(username, password)
            messagebox.showinfo("Success", "User registered successfully")
            self.create_login_screen()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        except sqlite3.Error:
            messagebox.showerror("Error", "An error occurred while registering the user")

    def clock_in(self):
        """
        Handle the clock-in process by recording the current time in the database.
        """
        self.user.clock_in()
        messagebox.showinfo("Info", "Clocked in at " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.update_clock_buttons()

    def clock_out(self):
        """
        Handle the clock-out process by recording the current time in the database.
        """
        self.user.clock_out()
        messagebox.showinfo("Info", "Clocked out at " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.update_clock_buttons()

    def view_hours(self):
        """
        Display the total hours worked by the logged-in user.
        """
        total_hours = self.user.get_total_hours()
        messagebox.showinfo("Total Hours", f"{self.user.username} worked a total of {total_hours:.2f} hours")

    def update_clock_buttons(self):
        """
        Update the visibility of the clock-in and clock-out buttons based on the user's clock-in status.
        """
        if database.has_active_clock_in(self.user.id):
            self.clock_in_button.config(state=tk.DISABLED)
            self.clock_out_button.config(state=tk.NORMAL)
        else:
            self.clock_in_button.config(state=tk.NORMAL)
            self.clock_out_button.config(state=tk.DISABLED)

    def logout(self):
        """
        Handle the logout process by clearing the user session and returning to the login screen.
        """
        self.create_login_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackingApp(root)
    root.mainloop()