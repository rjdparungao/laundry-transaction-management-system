import tkinter as tk
from tkinter import PhotoImage

root = tk.Tk()
root.geometry("800x500")
root.title("Laundry Management System")

# Configure colors
bg_color = "#F2F2F2"
header_bg_color = "black"
header_fg_color = "white"
button_bg_color = "#007BFF"
button_fg_color = "white"

# Create the header frame
header_frame = tk.Frame(root, bg=header_bg_color)
header_frame.pack(fill=tk.X)

# Create the navigation buttons
home_button = tk.Button(header_frame, text="Home", font=("Arial", 12), width=10, bg=header_bg_color, fg=header_fg_color)
home_button.pack(side=tk.LEFT, padx=10, pady=10)

laundry_type_button = tk.Button(header_frame, text="Laundry Type", font=("Arial", 12), width=12, bg=header_bg_color, fg=header_fg_color)
laundry_type_button.pack(side=tk.LEFT, padx=10, pady=10)

product_list_button = tk.Button(header_frame, text="Product List", font=("Arial", 12), width=12, bg=header_bg_color, fg=header_fg_color)
product_list_button.pack(side=tk.LEFT, padx=10, pady=10)

transaction_button = tk.Button(header_frame, text="Transaction", font=("Arial", 12), width=12, bg=header_bg_color, fg=header_fg_color)
transaction_button.pack(side=tk.LEFT, padx=10, pady=10)

daily_report_button = tk.Button(header_frame, text="Daily Report", font=("Arial", 12), width=12, bg=header_bg_color, fg=header_fg_color)
daily_report_button.pack(side=tk.LEFT, padx=10, pady=10)

users_button = tk.Button(header_frame, text="Users", font=("Arial", 12), width=10, bg=header_bg_color, fg=header_fg_color)
users_button.pack(side=tk.LEFT, padx=10, pady=10)

# Create the greeting and logout button

logout_button = tk.Button(header_frame, text="Logout", font=("Arial", 12), bg=header_bg_color, fg=header_fg_color)
logout_button.pack(side=tk.RIGHT, padx=10, pady=10)

greeting_label = tk.Label(header_frame, text="Hello, User!", font=("Arial", 12), bg=header_bg_color, fg=header_fg_color)
greeting_label.pack(side=tk.RIGHT, padx=10, pady=10)


# Create the main content area
content_frame = tk.Frame(root, bg=bg_color)
content_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=30)

# Create the welcome message
welcome_label = tk.Label(content_frame, text="Welcome, User Administrator!", font=("Arial", 18, "bold"))
welcome_label.pack()

# Create buttons and labels for each section
button_frame = tk.Frame(content_frame, bg=bg_color)
button_frame.pack(pady=30)

laundry_type_button = tk.Button(button_frame, text="Laundry Type", font=("Arial", 16), width=15, bg=button_bg_color, fg=button_fg_color)
laundry_type_button.grid(row=0, column=0, padx=20, pady=10)

laundry_type_label = tk.Label(button_frame, text="Laundry Type Picture", font=("Arial", 12), bg=bg_color)
laundry_type_label.grid(row=1, column=0, padx=20, pady=10)

product_list_button = tk.Button(button_frame, text="Products", font=("Arial", 16), width=15, bg=button_bg_color, fg=button_fg_color)
product_list_button.grid(row=0, column=1, padx=20, pady=10)

product_list_label = tk.Label(button_frame, text="Products Picture", font=("Arial", 12), bg=bg_color)
product_list_label.grid(row=1, column=1, padx=20, pady=10)

transaction_button = tk.Button(button_frame, text="Today's Transactions", font=("Arial", 16), width=15, bg=button_bg_color, fg=button_fg_color)
transaction_button.grid(row=0, column=2, padx=20, pady=10)

transaction_label = tk.Label(button_frame, text="Transactions Picture", font=("Arial", 12), bg=bg_color)
transaction_label.grid(row=1, column=2, padx=20, pady=10)

sales_button = tk.Button(button_frame, text="Today's Sales", font=("Arial", 16), width=15, bg=button_bg_color, fg=button_fg_color)
sales_button.grid(row=0, column=3, padx=20, pady=10)

sales_label = tk.Label(button_frame, text="Sales Picture", font=("Arial", 12), bg=bg_color)
sales_label.grid(row=1, column=3, padx=20, pady=10)

root.mainloop()

# shirt_image = PhotoImage(file="shirt.png")
# laundry_type_label = tk.Label(button_frame, image=shirt_image, bg=bg_color)
# laundry_type_label.grid(row=1, column=0, padx=20, pady=10)
