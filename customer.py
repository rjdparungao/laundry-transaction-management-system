import re
import tkinter as tk
from datetime import date
from tkinter import ttk, messagebox, simpledialog
import transaction
import homepage
import reports
import create_customer
import sqlite3


def customer_view():
    connection = sqlite3.connect('japaeng.db')
    cursor = connection.cursor()

    def switch_to_transaction():
        customer_root.destroy()
        transaction.transaction_view()

    def switch_to_reports():
        customer_root.destroy()
        reports.reports()

    def home_view():
        customer_root.destroy()
        homepage.homepage_view()

    def create_a_customer():
        customer_root.destroy()
        create_customer.create_customer()

    def fetch_and_display_data(table):
        connection = sqlite3.connect('japaeng.db')
        cursor = connection.cursor()
        # Clear the existing data in the data table
        data_table.delete(*data_table.get_children())

        # Fetch data from the database and insert it into the data table
        cursor.execute("SELECT * FROM CUSTOMER")
        rows = cursor.fetchall()
        for row in rows:
            data_table.insert("", "end", values=row)

        # Close the database connection
        connection.close()

    def update_button_state(event):

        def delete_customer():
            selected_item = data_table.focus()
            if selected_item:
                selected_row = data_table.item(selected_item)
                cust_id = selected_row["values"][0]
                try:
                    connection = sqlite3.connect('japaeng.db')
                    cursor = connection.cursor()

                    cursor.execute("DELETE FROM CUSTOMER WHERE customer_id = ?", (cust_id,))
                    connection.commit()
                    connection.close()
                    customer_root.update()
                    messagebox.showinfo("Delete Customer", "Customer Deleted Successfully!")
                    fetch_and_display_data(data_table)  # Refresh the data table with the latest data
                except:
                    messagebox.showwarning("Error Deleting Customer!", "There seems to be a problem deleting customer.")
            else:
                messagebox.showwarning("Warning", "Please select a row first.")

        def commit_update():

            def validate_name(name):
                # Check if the name contains only letters and period
                return bool(re.match(r'^[A-Za-z. ]+$', name))

            def validate_contact_number(contact_number):
                # Check if the contact number contains only numbers
                return bool(re.match(r'^\d+$', contact_number))

            def validate_fields():
                # Get the values from the entry fields
                fname = fname_text.get()
                mname = mname_text.get()
                lname = lname_text.get()
                contact_number = contact_no_entry.get()
                address = address_entry.get()

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

            try:
                if not validate_fields():
                    return

                connection = sqlite3.connect('japaeng.db')
                cursor = connection.cursor()

                cursor.execute('''
                                  UPDATE CUSTOMER
                                  SET customer_fname = ?,
                                      customer_mname = ?,
                                      customer_lname = ?,
                                      customer_contactNo = ?,
                                      customer_address = ?
                                  WHERE customer_id = ?
                              ''', (fname_text.get(), mname_text.get(), lname_text.get(), contact_no_entry.get(),
                                    address_entry.get(), cust_id))
                connection.commit()
                connection.close()
                messagebox.showinfo("Update Customer", "Customer Updated Successfully!")
                edit_root.withdraw()
                fetch_and_display_data(data_table)
            except sqlite3.Error as e:
                # Handle any exceptions that occur during the execution of the SQL query
                messagebox.showerror("Error", f"An error occurred: {e}")

        selected_item = data_table.focus()

        if selected_item:
            selected_row = data_table.item(selected_item)
            edit_root = tk.Tk()
            edit_root.title("Edit Customer")
            edit_root.geometry("400x500")
            edit_root.configure(bg="white")

            edit_panel = tk.Frame(edit_root, bg="white", height=50)
            edit_panel.pack(fill=tk.BOTH, expand=True)

            fname_label = tk.Label(edit_panel, bg="white", text="First Name", font=("Helvetica", 12))
            fname_label.grid(row=0, column=0, padx=20, pady=5, sticky='w')
            fname_text = tk.Entry(edit_panel, font=("Helvetica", 12))
            fname_text.grid(row=0, column=1, padx=20, pady=5, sticky='w')

            fname_text.insert(0, selected_row["values"][1])

            mname_label = tk.Label(edit_panel, bg="white", text="Middle Name", font=("Helvetica", 12))
            mname_label.grid(row=1, column=0, padx=20, pady=5, sticky='w')
            mname_text = tk.Entry(edit_panel, font=("Helvetica", 12))
            mname_text.grid(row=1, column=1, padx=20, pady=5, sticky='w')

            mname_text.insert(0, selected_row["values"][2])

            lname_label = tk.Label(edit_panel, bg="white", text="Last Name", font=("Helvetica", 12))
            lname_label.grid(row=2, column=0, padx=20, pady=5, sticky='w')
            lname_text = tk.Entry(edit_panel, font=("Helvetica", 12))
            lname_text.grid(row=2, column=1, padx=20, pady=5, sticky='w')

            lname_text.insert(0, selected_row["values"][3])

            contact_no_label = tk.Label(edit_panel, bg="white", text="Contact No.", font=("Helvetica", 12))
            contact_no_label.grid(row=3, column=0, padx=20, pady=5, sticky='w')
            contact_no_entry = tk.Entry(edit_panel, font=("Helvetica", 12))
            contact_no_entry.grid(row=3, column=1, padx=20, pady=5, sticky='w')

            contact_no_entry.insert(0, selected_row["values"][4])

            address_label = tk.Label(edit_panel, bg="white", text="Address", font=("Helvetica", 12))
            address_label.grid(row=4, column=0, padx=20, pady=5, sticky='w')
            address_entry = tk.Entry(edit_panel, font=("Helvetica", 12))
            address_entry.grid(row=4, column=1, padx=20, pady=5, sticky='w')

            address_entry.insert(0, selected_row["values"][5])

            cust_id = selected_row["values"][0]

            update_button = tk.Button(edit_panel, text="Update", bg="#87CEEB", font=("Helvetica", 12),
                                      command=commit_update)
            update_button.grid(row=7, column=0, padx=20, pady=10, sticky="w")

            del_button = tk.Button(edit_panel, text="Delete", bg="red", font=("Helvetica", 12),
                                   command=delete_customer)
            del_button.grid(row=7, column=1, padx=20, pady=10, sticky="w")
        else:
            messagebox.showinfo("Info", "Please select a row to update.")

    # Create the main application window
    customer_root = tk.Tk()
    customer_root.title("Home Page")
    customer_root.geometry("{width}x{height}+0+0".format(width=customer_root.winfo_screenwidth(),
                                                         height=customer_root.winfo_screenheight()))
    customer_root.configure(bg="gray")

    # Top Panel
    # Top Panel
    top_panel = tk.Frame(customer_root, bg="black", height=50)
    top_panel.pack(fill=tk.X)

    # Change font, size, and color for "Japaeng" label
    label_title = tk.Label(top_panel, text="Japaeng", fg="white", bg="black", font=("Arial", 24, "bold"), padx=10)
    label_title.pack(side=tk.LEFT)

    # Change button color to blend with the background
    logout_button = tk.Button(top_panel, text="Log Out", fg="white", bg="black", command="", relief=tk.FLAT)
    logout_button.pack(side=tk.RIGHT, padx=10)

    # Left Panel for Welcome Message, Date, and Buttons
    left_panel = tk.Frame(customer_root, bg="black", width=150)  # Adjust the width here (originally 200)
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
        buttons_panel, text="Customers", command="", width=30, height=5,
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
    content_panel = tk.Frame(customer_root, bg="white")
    content_panel.pack(fill=tk.BOTH, expand=True)

    # Add a black frame inside the white content_panel
    frame_inside_content = tk.Frame(content_panel, bg="black", padx=15, pady=15)  # Adjust padding here (originally 20)
    frame_inside_content.pack(padx=50, pady=50, fill=tk.BOTH, expand=True)  # Adjust fill settings

    # Create another panel inside the black frame with white interior
    inner_panel = tk.Frame(frame_inside_content, bg="white")
    inner_panel.pack(fill=tk.BOTH, expand=True)  # Adjust fill settings to occupy the entire black frame

    heading_label = tk.Label(inner_panel, text="CUSTOMER", bg="white", font=("Helvetica", 16, "bold"))
    heading_label.pack(pady=(20, 20))

    # Labels inside the inner_panel
    data_table = ttk.Treeview(inner_panel,
                              columns=(
                                  "Customer ID", "First Name", "Middle Name", "Last Name", "Contact No.", "Address"))

    # Define column headings
    data_table.heading("#1", text="Customer ID")
    data_table.heading("#2", text="First Name")
    data_table.heading("#3", text="Middle Name")
    data_table.heading("#4", text="Last Name")
    data_table.heading("#5", text="Contact No.")
    data_table.heading("#6", text="Address")

    # Set column widths
    data_table.column("#1", width=100)
    data_table.column("#2", width=100)
    data_table.column("#3", width=100)
    data_table.column("#4", width=100)
    data_table.column("#5", width=100)
    data_table.column("#6", width=200)

    fetch_and_display_data(data_table)
    data_table.bind("<<TreeviewSelect>>", update_button_state)

    data_table.pack(fill=tk.BOTH, expand=True)

    # Create a new frame for the buttons below the data table
    buttons_frame = tk.Frame(inner_panel, bg="white")
    buttons_frame.pack(side=tk.BOTTOM, pady=(0, 10))

    # Create a new frame for the "Create New Customer" button
    create_frame = tk.Frame(inner_panel, bg="white")
    create_frame.pack(side=tk.BOTTOM, pady=(20, 60))

    # Create New Transaction button inside the create_frame
    create_new_button = tk.Button(create_frame, command=create_a_customer, text="Create New Customer", bg="#87CEEB",
                                  fg="black",
                                  font=("Helvetica", 14))
    create_new_button.pack(ipadx=40, ipady=15)

    customer_root.mainloop()
