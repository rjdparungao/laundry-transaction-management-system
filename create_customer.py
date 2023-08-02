import re
import tkinter as tk
from tkinter import messagebox
from datetime import date
import homepage
import customer
import transaction
import reports
import sqlite3


def create_customer():
    connection = sqlite3.connect('japaeng.db')
    cursor = connection.cursor()

    def validate_name(name):
        # Check if the name contains only letters and period
        return bool(re.match(r'^[A-Za-z. ]+$', name))

    def validate_contact_number(contact_number):
        # Check if the contact number contains only numbers
        return bool(re.match(r'^\d+$', contact_number))

    def validate_fields():
        # Get the values from the entry fields
        fname = customer_label_entry_fname.get()
        mname = customer_label_entry_mname.get()
        lname = customer_label_entry_lname.get()
        contact_number = contact_label_entry.get()
        address = address_textbox.get("1.0", tk.END).strip()

        # Validate fields
        if not all((fname, lname, contact_number, address)):
            messagebox.showerror("Error", "All fields are required.")
            return False
        if not validate_name(fname) or not validate_name(lname) or not validate_name(mname):
            messagebox.showerror("Error", "Invalid name format.")
            return False
        if not validate_contact_number(contact_number):
            messagebox.showerror("Error", "Invalid contact number.")
            return False

        return True

    def create_a_customer():
        if not validate_fields():
            return

        customer_details = [
            customer_label_entry_fname.get(),
            customer_label_entry_mname.get(),
            customer_label_entry_lname.get(),
            contact_label_entry.get(),
            address_textbox.get("1.0", tk.END)
        ]

        try:
            cursor.execute('''
                INSERT INTO CUSTOMER (customer_fname, customer_mname, customer_lname, customer_contactNo, customer_address)
                VALUES (?, ?, ?, ?, ?)
            ''', customer_details)

            # Commit the changes to the database
            connection.commit()

            # Show the messagebox after successful execution
            messagebox.showinfo("Create a Customer", "Customer has been added successfully!")

            # Clear the input fields after successful insertion
            customer_label_entry_fname.delete(0, tk.END)
            customer_label_entry_mname.delete(0, tk.END)
            customer_label_entry_lname.delete(0, tk.END)
            contact_label_entry.delete(0, tk.END)
            address_textbox.delete("1.0", tk.END)

            switch_to_customer()

        except sqlite3.Error as e:
            # Handle any exceptions that occur during the execution of the SQL query
            messagebox.showerror("Error", f"An error occurred: {e}")

    def home_view():
        create_customer_root.destroy()
        homepage.homepage_view()

    def switch_to_reports():
        create_customer_root.destroy()
        reports.reports()

    def switch_to_transaction():
        create_customer_root.destroy()
        transaction.transaction_view()

    def switch_to_customer():
        create_customer_root.destroy()
        customer.customer_view()

    # Create the main application window
    create_customer_root = tk.Tk()
    create_customer_root.title("Create Customer")
    create_customer_root.geometry("{width}x{height}+0+0".format(width=create_customer_root.winfo_screenwidth(),
                                                                height=create_customer_root.winfo_screenheight()))
    create_customer_root.configure(bg="gray")

    # Top Panel
    top_panel = tk.Frame(create_customer_root, bg="black", height=50)
    top_panel.pack(fill=tk.X)

    # Change font, size, and color for "Japaeng" label
    label_title = tk.Label(top_panel, text="Japaeng", fg="white", bg="black", font=("Arial", 24, "bold"), padx=10)
    label_title.pack(side=tk.LEFT)

    # Change button color to blend with the background
    logout_button = tk.Button(top_panel, text="Log Out", fg="white", bg="black", command="", relief=tk.FLAT)
    logout_button.pack(side=tk.RIGHT, padx=10)

    # Left Panel for Welcome Message, Date, and Buttons
    left_panel = tk.Frame(create_customer_root, bg="black", width=150)  # Adjust the width here (originally 200)
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
    content_panel = tk.Frame(create_customer_root, bg="white")
    content_panel.pack(fill=tk.BOTH, expand=True)

    # Add a black frame inside the white content_panel
    frame_inside_content = tk.Frame(content_panel, bg="black", padx=15, pady=15)  # Adjust padding here (originally 20)
    frame_inside_content.pack(padx=50, pady=50, fill=tk.BOTH, expand=True)  # Adjust fill settings

    # Create another panel inside the black frame with white interior
    inner_panel = tk.Frame(frame_inside_content, bg="white")
    inner_panel.pack(fill=tk.BOTH, expand=True)  # Adjust fill settings to occupy the entire black frame

    # Create Transaction Form inside the inner_panel
    create_customer_label = tk.Label(inner_panel, text="Create Customer", bg="white", fg="black",
                                     font=("Helvetica", 16, "bold"))
    create_customer_label.grid(row=0, column=1, pady=(50, 50), columnspan=4)  # Span four columns to center it

    # Set column and row weights to make the form centered
    inner_panel.columnconfigure(0, weight=1)
    inner_panel.columnconfigure(5, weight=1)
    inner_panel.rowconfigure(6, weight=1)

    customer_label = tk.Label(inner_panel, text="First Name", bg="white", fg="black", font=("Helvetica", 14))
    customer_label.grid(row=1, column=0, padx=(20, 0), pady=5, sticky="e")  # Adjust sticky to the right

    customer_label_entry_fname = tk.Entry(inner_panel, font=("Helvetica", 12))
    customer_label_entry_fname.grid(row=1, column=1, padx=(20, 0), pady=5, sticky="w")

    customer_label_mname = tk.Label(inner_panel, text="Middle Name", bg="white", fg="black", font=("Helvetica", 14))
    customer_label_mname.grid(row=2, column=0, padx=(20, 0), pady=5, sticky="e")  # Adjust sticky to the right
    customer_label_entry_mname = tk.Entry(inner_panel, font=("Helvetica", 12))
    customer_label_entry_mname.grid(row=2, column=1, padx=(20, 0), pady=5, sticky="w")

    customer_label_lname = tk.Label(inner_panel, text="Last Name", bg="white", fg="black", font=("Helvetica", 14))
    customer_label_lname.grid(row=3, column=0, padx=(20, 0), pady=5, sticky="e")  # Adjust sticky to the right
    customer_label_entry_lname = tk.Entry(inner_panel, font=("Helvetica", 12))
    customer_label_entry_lname.grid(row=3, column=1, padx=(20, 0), pady=5, sticky="w")

    contact_label = tk.Label(inner_panel, text="Contact No.", bg="white", fg="black", font=("Helvetica", 14))
    contact_label.grid(row=4, column=0, padx=20, pady=20, sticky="e")  # Adjust sticky to the right
    contact_label_entry = tk.Entry(inner_panel, font=("Helvetica", 12))
    contact_label_entry.grid(row=4, column=1, padx=20, pady=5, sticky="w")

    address_label = tk.Label(inner_panel, text="Address", bg="white", fg="black", font=("Helvetica", 14))
    address_label.grid(row=5, column=0, padx=20, pady=20, sticky="e")  # Adjust sticky to the right
    address_textbox = tk.Text(inner_panel, font=("Helvetica", 12), height=5, width=30)
    address_textbox.grid(row=5, column=1, padx=20, pady=5, sticky="w")

    create_button = tk.Button(inner_panel, text="Create", bg="#87CEEB", fg="black", font=("Helvetica", 12),
                              command=create_a_customer)
    create_button.grid(row=6, column=1, padx=20, pady=10, sticky="w")  # Span two columns to center it

    # Start the main event loop
    create_customer_root.mainloop()
