import tkinter as tk
from datetime import date
from tkcalendar import DateEntry
from tkinter import ttk
import transaction
import homepage
import customer
import sqlite3


def reports():
    connection = sqlite3.connect('japaeng.db')
    cursor = connection.cursor()

    def switch_to_transaction():
        reports_root.destroy()
        transaction.transaction_view()

    def home_view():
        reports_root.destroy()
        homepage.homepage_view()

    def switch_to_customer():
        reports_root.destroy()
        customer.customer_view()

    def generate_report():
        connection = sqlite3.connect('japaeng.db')
        cursor = connection.cursor()

        cust_name = customer_label_entry.get()

        cursor.execute(
            "SELECT customer_id FROM CUSTOMER WHERE customer_fname || ' ' || customer_mname || ' ' || customer_lname = ?",
            (customer_label_entry.get(),))
        customer_id_row = cursor.fetchone()

        query = '''
                SELECT t.transaction_id, c.customer_fname || ' ' || c.customer_mname || ' ' || c.customer_lname AS customer_name,
                    t.transaction_total_amount, t.transaction_status
                FROM LAUNDRY_TRANSACTION t
                JOIN CUSTOMER c ON t.customer_id = c.customer_id
                WHERE t.customer_id = ? AND t.transaction_date = ? AND t.transaction_status = ?
        '''

        cursor.execute(query, (customer_id_row[0], date_label.get(), status_label_entry.get()))

        rows = cursor.fetchall()

        # Clear the existing data in the data table
        data_table.delete(*data_table.get_children())

        # Insert new data into the data table
        for row in rows:
            data_table.insert("", "end", values=row)

    # Create the main application window
    reports_root = tk.Tk()
    reports_root.title("Home Page")
    reports_root.geometry("{width}x{height}+0+0".format(width=reports_root.winfo_screenwidth(),
                                                        height=reports_root.winfo_screenheight()))
    reports_root.configure(bg="gray")

    # Top Panel
    # Top Panel
    top_panel = tk.Frame(reports_root, bg="black", height=50)
    top_panel.pack(fill=tk.X)

    # Change font, size, and color for "Japaeng" label
    label_title = tk.Label(top_panel, text="Japaeng", fg="white", bg="black", font=("Arial", 24, "bold"), padx=10)
    label_title.pack(side=tk.LEFT)

    # Change button color to blend with the background
    logout_button = tk.Button(top_panel, text="Log Out", fg="white", bg="black", command="", relief=tk.FLAT)
    logout_button.pack(side=tk.RIGHT, padx=10)

    # Left Panel for Welcome Message, Date, and Buttons
    left_panel = tk.Frame(reports_root, bg="black", width=150)  # Adjust the width here (originally 200)
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
        buttons_panel, text="Reports", command="", width=30, height=5,
        bg=button_bg_color, fg="white", font=("Helvetica", 12)
    )

    home_button.pack(side=tk.TOP, padx=10, pady=5)
    transaction_button.pack(side=tk.TOP, padx=10, pady=5)
    customer_button.pack(side=tk.TOP, padx=10, pady=5)
    report_button.pack(side=tk.TOP, padx=10, pady=5)

    # Content Panel
    content_panel = tk.Frame(reports_root, bg="white")
    content_panel.pack(fill=tk.BOTH, expand=True)

    # Add a black frame inside the white content_panel
    frame_inside_content = tk.Frame(content_panel, bg="black", padx=15, pady=15)  # Adjust padding here (originally 20)
    frame_inside_content.pack(padx=50, pady=50, fill=tk.BOTH, expand=True)  # Adjust fill settings

    # Create another panel inside the black frame with white interior
    inner_panel = tk.Frame(frame_inside_content, bg="white")
    inner_panel.pack(fill=tk.BOTH, expand=True)  # Adjust fill settings to occupy the entire black frame

    # Create Transaction Form inside the inner_panel
    create_transaction_label = tk.Label(inner_panel, text="Reports", bg="white", fg="black",
                                        font=("Helvetica", 16, "bold"))
    create_transaction_label.grid(row=0, column=1, pady=(50, 50), columnspan=4)  # Span four columns to center it

    # Set column and row weights to make the form centered
    inner_panel.columnconfigure(0, weight=1)
    inner_panel.columnconfigure(5, weight=1)
    inner_panel.rowconfigure(5, weight=1)

    cursor.execute('''
        SELECT customer_id, customer_fname || ' ' || customer_mname || ' ' || customer_lname AS full_name
        FROM CUSTOMER;
    ''')

    rows = cursor.fetchall()

    customer_names = [row[1] for row in rows]

    customer_label = tk.Label(inner_panel, text="Customer", bg="white", fg="black", font=("Helvetica", 14))
    customer_label.grid(row=1, column=0, padx=20, pady=20, sticky="e")  # Adjust sticky to the right
    customer_label_entry = ttk.Combobox(inner_panel, values=customer_names,
                                        font=("Helvetica", 12))
    customer_label_entry.grid(row=1, column=1, padx=20, pady=5, sticky="w")

    status_label = tk.Label(inner_panel, text="Status", bg="white", fg="black", font=("Helvetica", 14))
    status_label.grid(row=2, column=0, padx=20, pady=20, sticky="e")  # Adjust sticky to the right
    status_label_entry = ttk.Combobox(inner_panel, values=['Completed', 'Processing'],
                                      font=("Helvetica", 12))
    status_label_entry.grid(row=2, column=1, padx=20, pady=5, sticky="w")

    date_label = tk.Label(inner_panel, text="Date", bg="white", fg="black", font=("Helvetica", 14))
    date_label.grid(row=3, column=0, padx=20, pady=20, sticky="e")  # Adjust sticky to the right
    date_label = DateEntry(inner_panel, selectmode='day', font=("Helvetica", 12))
    date_label.grid(row=3, column=1, padx=20, pady=5, sticky="w")

    create_button = tk.Button(inner_panel, text="Filter", bg="#87CEEB", fg="black", font=("Helvetica", 12),
                              command=generate_report)
    create_button.grid(row=4, column=0, padx=(50, 0), pady=10, sticky="w")  # Span two columns to center it

    # Create the report panel under the "Create" button
    report_panel = tk.Frame(inner_panel, bg="white", bd=3, relief=tk.SOLID)
    report_panel.grid(row=5, column=0, padx=50, pady=(10, 0), columnspan=10, sticky="ew")

    # Add a data table using ttk.Treeview
    data_table = ttk.Treeview(report_panel,
                              columns=("Date", "Description", "Amount", "Status"))

    # Define column headings
    data_table.heading("#1", text="Transaction ID")
    data_table.heading("#2", text="Name")
    data_table.heading("#3", text="Total Amount")
    data_table.heading("#4", text="Status")

    # Set column widths
    data_table.column("#1", width=100)
    data_table.column("#2", width=300)
    data_table.column("#3", width=100)
    data_table.column("#4", width=100)

    data_table.pack(fill=tk.BOTH, expand=True)

    # Adjust column weight to center the report_panel
    inner_panel.columnconfigure(1, weight=0)
    inner_panel.columnconfigure(1, weight=100)
    report_panel.columnconfigure(40, weight=0)  # Add this line to center the report panel

    # Start the main event loop
    reports_root.mainloop()
