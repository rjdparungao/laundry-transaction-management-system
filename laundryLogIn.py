import tkinter as tk


def login():
    username = entry_login.get()  # Get the value from the login entry widget
    password = entry_password.get()  # Get the value from the password entry widget

    # Perform login validation or processing logic here
    # For example, you can check if the username and password are valid

    # Display a message based on the login result
    if username == "admin" and password == "password":
        result_label.config(text="Login successful!")
    else:
        result_label.config(text="Invalid login credentials!", fg="red")


root = tk.Tk()

root.geometry("1280x960")

# Create a big title label above the login fields
title_label = tk.Label(root, text="Laundry Service Transaction Management System", font=("Arial", 24, "bold"))
title_label.pack(pady=300)  # Add vertical padding

input_frame = tk.Frame(root)
input_frame.pack(pady=100)  # Add padding around the frame

entry_login = tk.Entry(input_frame, font=("Arial", 18), width=30)  # Increased font size and width
entry_login.pack(pady=10)

entry_password = tk.Entry(input_frame, font=("Arial", 18), width=30, show="*")  # Increased font size and width
entry_password.pack(pady=10)

input_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

login_button = tk.Button(root, text="Login", command=login, font=("Arial", 16))  # Increased font size
login_button.pack(pady=10)
login_button.configure(bg="#007BFF", fg="white")

result_label = tk.Label(root, text="")
result_label.pack()

result_label.place(relx=0.5, rely=0.57, anchor=tk.CENTER)
login_button.place(relx=0.5, rely=0.61, anchor=tk.CENTER)

root.mainloop()
