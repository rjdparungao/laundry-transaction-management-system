import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("800x500")
root.title("Laundry Management System")

# Configure colors
bg_color = "#F2F2F2"
header_bg_color = "#222222"
header_fg_color = "white"
button_bg_color = "#007BFF"
button_fg_color = "white"

# Create the header frame
header_frame = tk.Frame(root, bg=header_bg_color)
header_frame.pack(fill=tk.X)

# Create the navigation buttons
japaeng_button = tk.Button(header_frame, text="JaPaeng", font=("Arial", 12, "bold"), width=10, bg=header_bg_color, fg=header_fg_color, relief=tk.FLAT, borderwidth=0, highlightthickness=0)
japaeng_button.pack(side=tk.LEFT, padx=10, pady=10)

home_button = tk.Button(header_frame, text="Home", font=("Arial", 12), width=10, bg=header_bg_color, fg=header_fg_color, relief=tk.FLAT, borderwidth=0, highlightthickness=0)
home_button.pack(side=tk.LEFT, padx=10, pady=10)

transaction_button = tk.Button(header_frame, text="Transactions", font=("Arial", 12), width=12, bg=header_bg_color, fg=header_fg_color, relief=tk.FLAT, borderwidth=0, highlightthickness=0)
transaction_button.pack(side=tk.LEFT, padx=10, pady=10)

daily_report_button = tk.Button(header_frame, text="Daily Report", font=("Arial", 12), width=12, bg=header_bg_color, fg=header_fg_color, relief=tk.FLAT, borderwidth=0, highlightthickness=0)
daily_report_button.pack(side=tk.LEFT, padx=10, pady=10)


# Create the greeting and logout button

login_button = tk.Button(header_frame, text="Login", font=("Arial", 12), bg=header_bg_color, fg=header_fg_color)
login_button.pack(side=tk.RIGHT, padx=10, pady=10)

signin_button = tk.Button(header_frame, text="Signin", font=("Arial", 12), bg=header_bg_color, fg=header_fg_color)
signin_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Create the main content area
content_frame = tk.Frame(root, bg=bg_color)
content_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=30)

# Create the welcome message
welcome_label = tk.Label(content_frame, text="Welcome To Our LaundryShop!", font=("Arial", 26, "bold"))
welcome_label.pack()





root.mainloop()
