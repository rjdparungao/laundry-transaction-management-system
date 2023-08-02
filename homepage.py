import tkinter as tk
from tkinter import ttk
from datetime import date
import sqlite3
import transaction
import customer
import reports


def homepage_view():

    connection = sqlite3.connect('japaeng.db')

    cursor = connection.cursor()

    def fetch_and_display_data(table):
        connection = sqlite3.connect('japaeng.db')
        cursor = connection.cursor()
        # Clear the existing data in the data table
        data_table.delete(*data_table.get_children())

        # Fetch data from the database and insert it into the data table
        cursor.execute('''
            SELECT t.transaction_id, t.transaction_total_amount, t.transaction_date, t.transaction_status, 
            c.customer_fname || ' ' || c.customer_mname || ' ' || c.customer_lname AS customer_name, 
            s.service_category
            FROM LAUNDRY_TRANSACTION t
            JOIN CUSTOMER c ON t.customer_id = c.customer_id
            JOIN SERVICE s ON t.services_id = s.service_id;
        ''')
        rows = cursor.fetchall()

        for row in rows:
            data_table.insert("", "end", values=row)

        # Close the database connection
        connection.close()

    def switch_to_transaction():
        homepage_root.destroy()
        transaction.transaction_view()

    def switch_to_reports():
        homepage_root.destroy()
        reports.reports()

    def switch_to_customer():
        homepage_root.destroy()
        customer.customer_view()

    def count_transactions():
        connection = sqlite3.connect('japaeng.db')
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM LAUNDRY_TRANSACTION")
        count = cursor.fetchone()[0]

        connection.close()
        return count

    homepage_root = tk.Tk()
    homepage_root.geometry("{width}x{height}+0+0".format(width=homepage_root.winfo_screenwidth(),
                                                         height=homepage_root.winfo_screenheight()))
    homepage_root.title("Laundry Management System")
    homepage_root.configure(bg="black")

    # Configure colors
    bg_color = "#F2F2F2"
    header_bg_color = "#222222"
    header_fg_color = "white"
    button_bg_color = "#007BFF"
    button_fg_color = "white"

    # Top Panel
    top_panel = tk.Frame(homepage_root, bg="black", height=50)
    top_panel.pack(fill=tk.X)

    # Change font, size, and color for "Japaeng" label
    label_title = tk.Label(top_panel, text="Japaeng", fg="white", bg="black", font=("Arial", 24, "bold"), padx=10)
    label_title.pack(side=tk.LEFT)

    # Change button color to blend with the background
    logout_button = tk.Button(top_panel, text="Log Out", fg="white", bg="black", command="", relief=tk.FLAT)
    logout_button.pack(side=tk.RIGHT, padx=10)

    # Left Panel for Welcome Message, Date, and Buttons
    left_panel = tk.Frame(homepage_root, bg="black", width=150)  # Adjust the width here (originally 200)
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
        buttons_panel, text="Home", width=30, height=5,
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
    content_panel = tk.Frame(homepage_root, bg="white")
    content_panel.pack(fill=tk.BOTH, expand=True)

    # Add a black frame inside the white content_panel
    frame_inside_content = tk.Frame(content_panel, bg="black", padx=15, pady=15)  # Adjust padding here (originally 20)
    frame_inside_content.pack(padx=50, pady=50, fill=tk.BOTH, expand=True)  # Adjust fill settings

    # Create another panel inside the black frame with white interior
    inner_panel = tk.Frame(frame_inside_content, bg="white")
    inner_panel.pack(fill=tk.BOTH, expand=True)  # Adjust fill settings to occupy the entire black frame

    # Labels inside the inner_panel

    dashboard_label = tk.Label(inner_panel, text="Dashboard", bg="white", fg="black", font=("Helvetica", 16, "bold"))
    dashboard_label.pack(side=tk.TOP, padx=10, pady=10)

    # Create a Treeview widget for the data table
    data_table = ttk.Treeview(inner_panel,
                              columns=("Transaction ID", "Customer Name", "Transaction Status", "Date", "Total Amount"))

    # Define column headings
    data_table.heading("#1", text="Transaction ID")
    data_table.heading("#2", text="Customer Name")
    data_table.heading("#3", text="Transaction Status")
    data_table.heading("#4", text="Date")
    data_table.heading("#5", text="Total Amount")

    # Set column widths
    data_table.column("#1", width=100)
    data_table.column("#2", width=150)
    data_table.column("#3", width=150)
    data_table.column("#4", width=100)
    data_table.column("#5", width=100)

    cursor.execute("SELECT COUNT(*) FROM LAUNDRY_TRANSACTION")
    count = cursor.fetchone()[0]

    count_of_transactions = tk.Label(inner_panel, text="Total Number of transactions: {  }")
    count_of_transactions.pack(side=tk.BOTTOM, padx=10, pady=10)

    count = count_transactions()
    count_of_transactions.config(text=f"Total Transactions: {count}")

    fetch_and_display_data(data_table)
    data_table.pack(fill=tk.BOTH, expand=True)

    # Center the data table in the inner_panel
    data_table.bind("<Configure>", lambda e: data_table.column("#0", width=0))  # Hide the first column
    data_table.pack_configure(anchor=tk.CENTER)

    # Start the main event loop
    homepage_root.mainloop()
