import re
import tkinter as tk
from datetime import date
from tkinter import ttk, messagebox

from tkcalendar import DateEntry

import homepage
import customer
import transaction
import reports
import sqlite3


def add_transaction():
    connection = sqlite3.connect('japaeng.db')
    cursor = connection.cursor()

    def validate_not_empty(value):
        return value and value.strip() != ""

    def validate_name(name):
        # Check if the name contains only letters and period
        return bool(re.match(r'^[A-Za-z. ]+$', name))

    def validate_qty_wt(num):
        # Check if the contact number contains only numbers
        return bool(re.match(r'^\d+$', num))

    def validate_fields():
        # Get the values from the entry fields
        customer = customer_label_entry.get()
        date = date_dropdown.get()
        service = service_dropdown.get()
        qty_wt = qty_wt_entry.get()

        # Validate fields
        if not all((customer, date, service, qty_wt)):
            messagebox.showerror("Error", "All fields are required.")
            return False
        if not validate_not_empty(customer):
            messagebox.showerror("Error", "Select customer.")
            return False
        if not validate_qty_wt(qty_wt):
            messagebox.showerror("Error", "Invalid quantity/weight.")
            return False

        return True

    def fetch_customer_names():
        connection = sqlite3.connect('japaeng.db')
        cursor = connection.cursor()

        cursor.execute("SELECT customer_id, customer_fname, customer_lname FROM CUSTOMER")
        rows = cursor.fetchall()

        # Combine first name and last name to get the full name
        customer_names = [f"{row[1]} {row[2]}" for row in rows]

        connection.close()
        return customer_names

    def fetch_customer_id_by_name(customer_name):
        connection = sqlite3.connect('japaeng.db')
        cursor = connection.cursor()

        # Use parameterized query to prevent SQL injection
        cursor.execute("SELECT customer_id FROM CUSTOMER WHERE customer_fname || ' ' || customer_lname = ?",
                       (customer_name,))
        row = cursor.fetchone()

        connection.close()

        if row:
            return row[0]
        else:
            return None

    def home_view():
        add_transaction_root.destroy()
        homepage.homepage_view()

    def switch_to_reports():
        add_transaction_root.destroy()
        reports.reports()

    def switch_to_transaction():
        add_transaction_root.destroy()
        transaction.transaction_view()

    def switch_to_customer():
        add_transaction_root.destroy()
        customer.customer_view()

    def create_a_transaction():
        global service_price, service_id

        if not validate_fields():
            return

        transaction_date = date_dropdown.get()
        transaction_status = status.get()

        customer_name = customer_label_entry.get()
        customer_id = fetch_customer_id_by_name(customer_name)

        cursor.execute("SELECT service_id, service_price FROM SERVICE WHERE service_category = ?", (service_dropdown.get(),))
        result = cursor.fetchone()

        weight = qty_wt_entry.get()

        total_amount = float(weight) * result[1]

        try:
            cursor.execute('''
                        INSERT INTO LAUNDRY_TRANSACTION (transaction_total_amount, transaction_date, transaction_status, 
                        customer_id, services_id)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (total_amount, transaction_date, transaction_status, customer_id, result[0]))

            transaction_id = cursor.lastrowid  # need sa laundry

            connection.commit()

            cursor.execute('''
                        INSERT INTO LAUNDRY (laundry_category, laundry_quantity, laundry_weight, transaction_id, 
                        service_id)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (laundry_category.get(), qty_wt_entry.get(), qty_wt_entry.get(), transaction_id, result[0]))

            connection.commit()

            # Show the messagebox after successful execution
            messagebox.showinfo("Create Transaction", "Transaction has been added successfully!")

            switch_to_transaction()

        except sqlite3.Error as e:
            # Handle any exceptions that occur during the execution of the SQL query
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Create the main application window
    add_transaction_root = tk.Tk()
    add_transaction_root.title("Home Page")
    add_transaction_root.geometry("{width}x{height}+0+0".format(width=add_transaction_root.winfo_screenwidth(),
                                                                height=add_transaction_root.winfo_screenheight()))
    add_transaction_root.configure(bg="gray")

    # Top Panel
    # Top Panel
    top_panel = tk.Frame(add_transaction_root, bg="black", height=50)
    top_panel.pack(fill=tk.X)

    # Change font, size, and color for "Japaeng" label
    label_title = tk.Label(top_panel, text="Japaeng", fg="white", bg="black", font=("Arial", 24, "bold"), padx=10)
    label_title.pack(side=tk.LEFT)

    # Change button color to blend with the background
    logout_button = tk.Button(top_panel, text="Log Out", fg="white", bg="black", command="", relief=tk.FLAT)
    logout_button.pack(side=tk.RIGHT, padx=10)

    # Left Panel for Welcome Message, Date, and Buttons
    left_panel = tk.Frame(add_transaction_root, bg="black", width=150)  # Adjust the width here (originally 200)
    left_panel.pack(side=tk.LEFT, fill=tk.Y)

    # Create a sub-frame for the Welcome and Date labels
    welcome_date_frame = tk.Frame(left_panel, bg="black")
    welcome_date_frame.pack(side=tk.TOP, fill=tk.X)

    welcome_label = tk.Label(welcome_date_frame, text="Welcome admin!", bg="black", fg="white", font=("Helvetica", 20))
    welcome_label.pack(pady=10, padx=10, anchor="w")

    current_date = date.today().strftime("%B %d, %Y")
    date_label = tk.Label(welcome_date_frame, text="Date: " + current_date, bg="black", fg="white",
                          font=("Helvetica", 12))
    date_label.pack(pady=0, padx=10, anchor="w")

    # Buttons Panel
    buttons_panel = tk.Frame(left_panel, bg="black")
    buttons_panel.pack(pady=20)

    # Buttons for "Transactions," "Customers," "Reports," and "Home" with modified appearance to blend with the
    # background
    button_bg_color = "black"  # Change this color to match your desired background color

    home_button = tk.Button(
        buttons_panel, text="Home", command=home_view, width=30, height=5,
        bg=button_bg_color, fg="white", font=("Helvetica", 12)
    )
    transaction_button = tk.Button(
        buttons_panel, text="Transactions", command=switch_to_transaction, width=30, height=5,
        bg=button_bg_color, fg="white", font=("Helvetica", 12)
    )
    customer_button = tk.Button(
        buttons_panel, text="Customers", command=switch_to_customer, width=30, height=5,
        bg=button_bg_color, fg="white", font=("Helvetica", 12)
    )
    report_button = tk.Button(
        buttons_panel, text="Reports", command=switch_to_reports, width=30, height=5,
        bg=button_bg_color, fg="white", font=("Helvetica", 12)
    )

    home_button.pack(side=tk.TOP, padx=10, pady=5)
    transaction_button.pack(side=tk.TOP, padx=10, pady=5)
    customer_button.pack(side=tk.TOP, padx=10, pady=5)
    report_button.pack(side=tk.TOP, padx=10, pady=5)

    # Content Panel
    content_panel = tk.Frame(add_transaction_root, bg="white")
    content_panel.pack(fill=tk.BOTH, expand=True)

    # Add a black frame inside the white content_panel
    frame_inside_content = tk.Frame(content_panel, bg="black", padx=15, pady=15)  # Adjust padding here (originally 20)
    frame_inside_content.pack(padx=50, pady=50, fill=tk.BOTH, expand=True)  # Adjust fill settings

    # Create another panel inside the black frame with white interior
    inner_panel = tk.Frame(frame_inside_content, bg="white")
    inner_panel.pack(fill=tk.BOTH, expand=True)  # Adjust fill settings to occupy the entire black frame

    # Create Transaction Form inside the inner_panel
    create_transaction_label = tk.Label(inner_panel, text="Create Transaction", bg="white", fg="black",
                                        font=("Helvetica", 16, "bold"))
    create_transaction_label.grid(row=0, column=1, pady=(50, 50), columnspan=4)  # Span four columns to center it

    # Set column and row weights to make the form centered
    inner_panel.columnconfigure(0, weight=1)
    inner_panel.columnconfigure(5, weight=1)
    inner_panel.rowconfigure(5, weight=1)

    customer_names = fetch_customer_names()

    customer_label = tk.Label(inner_panel, text="Customer", bg="white", fg="black", font=("Helvetica", 14))
    customer_label.grid(row=1, column=0, padx=20, pady=20, sticky="e")  # Adjust sticky to the right
    customer_label_entry = ttk.Combobox(inner_panel, values=customer_names,
                                        font=("Helvetica", 12))
    customer_label_entry.grid(row=1, column=1, padx=20, pady=5, sticky="w")

    date_label = tk.Label(inner_panel, text="Date", bg="white", fg="black", font=("Helvetica", 14))
    date_label.grid(row=1, column=2, padx=20, pady=20, sticky="w")
    date_dropdown = DateEntry(inner_panel, selectmode='day', font=("Helvetica", 12))
    date_dropdown.grid(row=1, column=3, padx=20, pady=5, sticky="w")

    cursor.execute("SELECT service_id, service_category, service_price FROM SERVICE")
    services = cursor.fetchall()

    service_names = [f"{service[1]}" for service in services]

    service_label = tk.Label(inner_panel, text="Service", bg="white", fg="black", font=("Helvetica", 14))
    service_label.grid(row=2, column=0, padx=20, pady=20, sticky="e")  # Adjust sticky to the right
    service_dropdown = ttk.Combobox(inner_panel, values=service_names,
                                    font=("Helvetica", 12))
    service_dropdown.grid(row=2, column=1, padx=20, pady=5, sticky="w")

    status_label = tk.Label(inner_panel, text="Status", bg="white", fg="black",
                            font=("Helvetica", 14))
    status_label.grid(row=2, column=2, padx=20, pady=20, sticky="e")
    status = ttk.Combobox(inner_panel, values=["Processing", "Completed"],
                          font=("Helvetica", 12))
    status.grid(row=2, column=3, padx=20, pady=5, sticky="e")

    qty_wt_label = tk.Label(inner_panel, text="Qty/Wt", bg="white", fg="black", font=("Helvetica", 14))
    qty_wt_label.grid(row=4, column=0, padx=20, pady=20, sticky="e")
    qty_wt_entry = tk.Entry(inner_panel, font=("Helvetica", 12))
    qty_wt_entry.grid(row=4, column=1, padx=20, pady=5, sticky="e")

    laundry_category_label = tk.Label(inner_panel, text="Laundry Category", bg="white", fg="black",
                                      font=("Helvetica", 14))
    laundry_category_label.grid(row=3, column=0, padx=20, pady=20, sticky="e")
    laundry_category = ttk.Combobox(inner_panel, values=["Clothes", "Bed Sheets"],
                                    font=("Helvetica", 12))
    laundry_category.grid(row=3, column=1, padx=20, pady=5, sticky="e")

    create_button = tk.Button(inner_panel, text="Create", bg="#87CEEB", fg="black", font=("Helvetica", 12),
                              command=create_a_transaction)
    create_button.grid(row=5, column=2, padx=20, pady=10, sticky="w")  # Span two columns to center it

    # Start the main event loop
    add_transaction_root.mainloop()
