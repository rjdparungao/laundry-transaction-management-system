import tkinter as tk
from tkinter import messagebox
import homepage


def login_view():
    def switch_view():
        loginRoot.destroy()
        homepage.homepage_view()

    def login():
        username = entry_login.get()
        password = entry_password.get()
        # Login logic goes here

        if username == 'admin' and password == 'pass':
            switch_view()
        else:
            messagebox.showerror("Login Failed", "Invalid Credentials")

    loginRoot = tk.Tk()
    loginRoot.geometry("{width}x{height}+0+0".format(width=loginRoot.winfo_screenwidth(), height=loginRoot.winfo_screenheight()))
    loginRoot.configure(bg="#222222")  # Set background color

    title_label = tk.Label(loginRoot, text="Laundry Service Transaction Management System", font=("Arial", 24, "bold"),
                           fg="#FFFFFF", bg="#222222")
    title_label.pack(pady=100)

    panel_frame = tk.Frame(loginRoot, bg="#333333", padx=20, pady=20)  # Create panel frame
    panel_frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    username_label = tk.Label(panel_frame, text="Username", font=("Arial", 12, "bold"), fg="#FFFFFF", bg="#333333")
    username_label.pack(anchor=tk.W)  # Align to the left

    entry_login = tk.Entry(panel_frame, font=("Arial", 18), width=30, bg="#FFFFFF", fg="#000000")  # Set entry colors
    entry_login.pack(pady=10)

    password_label = tk.Label(panel_frame, text="Password", font=("Arial", 12, "bold"), fg="#FFFFFF", bg="#333333")
    password_label.pack(anchor=tk.W)  # Align to the left

    entry_password = tk.Entry(panel_frame, font=("Arial", 18), width=30, show="*", bg="#FFFFFF",
                              fg="#000000")  # Set entry colors
    entry_password.pack(pady=10)

    login_button = tk.Button(panel_frame, text="Login", command=login, font=("Arial", 16), bg="#007BFF",
                             fg="#FFFFFF")  # Set button colors
    login_button.pack(pady=15)

    loginRoot.mainloop()
