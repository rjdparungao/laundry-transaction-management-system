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

users_button = tk.Button(header_frame, text="Users", font=("Arial", 12), width=10, bg=header_bg_color, fg=header_fg_color, relief=tk.FLAT, borderwidth=0, highlightthickness=0)
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

# Create the panel in the middle
panel_frame = tk.Frame(content_frame, bg=bg_color)
panel_frame.pack(pady=30)

# Add recent transactions label inside the panel
recent_transactions_label = tk.Label(panel_frame, text="Recent Transactions", font=("Arial", 16), bg=bg_color)
recent_transactions_label.pack(pady=10)

# Create a scrollbar for the panel
scrollbar = ttk.Scrollbar(panel_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a Text widget to display recent transactions
recent_transactions_text = tk.Text(panel_frame, font=("Arial", 12), bg="white", yscrollcommand=scrollbar.set)
recent_transactions_text.pack(expand=True, fill=tk.BOTH)
scrollbar.config(command=recent_transactions_text.yview)


# Create buttons for each section

button_frame = tk.Frame(content_frame, bg=bg_color)
button_frame.pack(pady=20)

create_order_button = tk.Button(button_frame, text="Add", font=("Arial", 12), width=5, bg=button_bg_color, fg=button_fg_color)
create_order_button.grid(row=0, column=0, padx=5, pady=10)

check_orders_button = tk.Button(button_frame, text="Check", font=("Arial", 12), width=5, bg=button_bg_color, fg=button_fg_color)
check_orders_button.grid(row=0, column=1, padx=5, pady=10)

update_orders_button = tk.Button(button_frame, text="Update", font=("Arial", 12), width=5, bg=button_bg_color, fg=button_fg_color)
update_orders_button.grid(row=0, column=2, padx=5, pady=10)

delete_orders_button = tk.Button(button_frame, text="Delete", font=("Arial", 12), width=5, bg=button_bg_color, fg=button_fg_color)
delete_orders_button.grid(row=0, column=3, padx=5, pady=10)




root.mainloop()
