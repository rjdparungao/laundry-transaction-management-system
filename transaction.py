import re
import tkinter as tk
from datetime import date
from tkinter import ttk, messagebox

from tkcalendar import DateEntry

import homepage
import create_transaction
import customer
import reports
import sqlite3


def transaction_view():
    connection = sqlite3.connect('japaeng.db')
    cursor = connection.cursor()

    def home_view():
        transaction_root.destroy()
        homepage.homepage_view()

    def switch_to_customer():
        transaction_root.destroy()
        customer.customer_view()

    def switch_to_reports():
        transaction_root.destroy()
        reports.reports()

    def switch_to_add_transaction():
        transaction_root.destroy()
        create_transaction.add_transaction()

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

    def fetch_customer_names():
        connection = sqlite3.connect('japaeng.db')
        cursor = connection.cursor()

        cursor.execute("SELECT customer_id, customer_fname, customer_mname, customer_lname FROM CUSTOMER")
        rows = cursor.fetchall()

        # Combine first name and last name to get the full name
        customer_names = [f"{row[1]} {row[2]} {row[3]}" for row in rows]

        connection.close()
        return customer_names

    def fetch_customer_id_by_name(customer_name):
        connection = sqlite3.connect('japaeng.db')
        cursor = connection.cursor()

        cursor.execute(
            "SELECT customer_id FROM CUSTOMER WHERE customer_fname || ' ' || customer_mname || ' ' "
            "|| customer_lname = ?",
            (customer_name,))
        row = cursor.fetchone()

        connection.close()

        if row:
            return row[0]
        else:
            return None

    def update_button_state(event):
        selected_item = data_table.focus()
        def delete_transaction():
            selected_item = data_table.focus()
            if selected_item:
                selected_row = data_table.item(selected_item)
                trans_id = selected_row["values"][0]
                try:
                    connection = sqlite3.connect('japaeng.db')
                    cursor = connection.cursor()

                    cursor.execute("DELETE FROM LAUNDRY_TRANSACTION WHERE transaction_id = ?", (trans_id,))
                    connection.commit()
                    connection.close()
                    transaction_root.update()
                    messagebox.showinfo("Delete Transaction", "Transaction Deleted Successfully!")
                    fetch_and_display_data(data_table)  # Refresh the data table with the latest data
                except:
                    messagebox.showwarning("Error Transaction Customer!", "There seems to be a problem deleting the "
                                                                          "transaction.")
            else:
                messagebox.showwarning("Warning", "Please select a row first.")

        def commit_update():
            def validate_not_empty(value):
                return value and value.strip() != ""

            def validate_name(name):
                # Check if the name contains only letters and period
                return bool(re.match(r'^[A-Za-z. ]+$', name))

            def validate_qty_wt(num):
                # Check if the contact number contains only numbers
                return bool(re.match(r'^\d+$', num))

            customer_value = customer_label_entry.get()

            date_value = date_dropdown.get()
            service_value = service_dropdown.get()
            transaction_status = status.get()
            laundry_category_value = laundry_category.get()
            qty_wt_entry_value = qty_wt_entry.get()

            def validate_fields():
                # Get the values from the entry fields
                # Validate fields
                if not all((customer_value, date_value, service_value, qty_wt_entry_value)):
                    messagebox.showerror("Error", "All fields are required.")
                    return False
                if not validate_not_empty(customer_value):
                    messagebox.showerror("Error", "Select customer.")
                    return False
                if not validate_qty_wt(qty_wt_entry_value):
                    messagebox.showerror("Error", "Invalid quantity/weight.")
                    return False

                return True

            try:
                if not validate_fields():
                    return

                transac_id = selected_row["values"][0]

                connection = sqlite3.connect('japaeng.db')
                cursor = connection.cursor()

                cursor.execute('''
                    SELECT customer_id
                    FROM CUSTOMER
                    WHERE customer_fname || " " || customer_mname || " " || customer_lname = ?
                ''', (customer_label_entry.get(),))
                new_customer_id = cursor.fetchone()

                customer_id = new_customer_id

                cursor.execute('''
                    SELECT service_id, service_price
                    FROM SERVICE
                    WHERE service_category = ?
                ''', (service_dropdown.get(),))
                record = cursor.fetchone()

                total_amount_value = float(qty_wt_entry.get()) * record[1]

                cursor.execute('''
                    UPDATE LAUNDRY_TRANSACTION
                    SET transaction_total_amount = ?,
                        transaction_date = ?,
                        transaction_status = ?,
                        customer_id = ?,
                        services_id = ?
                    WHERE transaction_id = ?
                ''', (total_amount_value, date_value, transaction_status, customer_id[0],
                      record[0], transac_id))

                connection.commit()
                connection.close()

                connection = sqlite3.connect('japaeng.db')
                cursor = connection.cursor()

                cursor.execute('''
                    UPDATE LAUNDRY
                    SET laundry_category = ?,
                        laundry_quantity = ?,
                        laundry_weight = ?,
                        service_id = ?
                    WHERE transaction_id = ?
                ''', (laundry_category_value, qty_wt_entry_value, qty_wt_entry_value, record[0], transac_id))

                connection.commit()
                connection.close()

                messagebox.showinfo("Update Transaction", "Transaction Updated Successfully!")
                edit_root.withdraw()

                fetch_and_display_data(data_table)
            except sqlite3.Error as e:
                # Handle any exceptions that occur during the execution of the SQL query
                messagebox.showerror("Error", f"An error occurred: {e}")

        if selected_item:
            selected_row = data_table.item(selected_item)
            edit_root = tk.Tk()
            edit_root.title("Edit Customer")
            edit_root.geometry("800x500")
            edit_root.configure(bg="white")

            connection = sqlite3.connect('japaeng.db')
            cursor = connection.cursor()

            transac_id = selected_row["values"][0]

            cursor.execute('''
                SELECT laundry_id, laundry_category, laundry_quantity, laundry_weight, service_id
                FROM LAUNDRY
                WHERE transaction_id = ?
            ''', (transac_id,))

            laundry_rows = cursor.fetchall()

            connection.close()

            edit_panel = tk.Frame(edit_root, bg="white", height=50)
            edit_panel.pack(fill=tk.BOTH, expand=True)

            customer_names = fetch_customer_names()

            customer_label = tk.Label(edit_panel, text="Customer", bg="white", fg="black", font=("Helvetica", 14))
            customer_label.grid(row=1, column=0, padx=20, pady=20, sticky="e")  # Adjust sticky to the right
            customer_label_entry = ttk.Combobox(edit_panel, values=customer_names,
                                                font=("Helvetica", 12))
            customer_label_entry.grid(row=1, column=1, padx=20, pady=5, sticky="w")

            customer_label_entry.set(selected_row["values"][4])

            transac_date_label = tk.Label(edit_panel, text="Date", bg="white", fg="black", font=("Helvetica", 14))
            transac_date_label.grid(row=1, column=2, padx=20, pady=20, sticky="e")
            date_dropdown = DateEntry(edit_panel, selectmode='day', font=("Helvetica", 12))
            date_dropdown.grid(row=1, column=3, padx=20, pady=5, sticky="w")

            date_dropdown.set_date(selected_row["values"][2])

            connection = sqlite3.connect('japaeng.db')
            cursor = connection.cursor()

            cursor.execute("SELECT service_id, service_category, service_price FROM SERVICE")
            services = cursor.fetchall()

            connection.close()

            service_names = [f"{service[1]}" for service in services]

            service_label = tk.Label(edit_panel, text="Service", bg="white", fg="black", font=("Helvetica", 14))
            service_label.grid(row=2, column=0, padx=20, pady=20, sticky="e")  # Adjust sticky to the right
            service_dropdown = ttk.Combobox(edit_panel, values=service_names,
                                            font=("Helvetica", 12))
            service_dropdown.grid(row=2, column=1, padx=20, pady=5, sticky="w")

            connection = sqlite3.connect('japaeng.db')
            cursor = connection.cursor()

            service_dropdown.set(selected_row["values"][5])

            status_label = tk.Label(edit_panel, text="Status", bg="white", fg="black",
                                    font=("Helvetica", 14))
            status_label.grid(row=2, column=2, padx=20, pady=20, sticky="e")
            status = ttk.Combobox(edit_panel, values=["Processing", "Completed"],
                                  font=("Helvetica", 12))
            status.grid(row=2, column=3, padx=20, pady=5, sticky="e")

            status.set(selected_row["values"][3])

            qty_wt_label = tk.Label(edit_panel, text="Qty/Wt", bg="white", fg="black", font=("Helvetica", 14))
            qty_wt_label.grid(row=4, column=0, padx=20, pady=20, sticky="e")
            qty_wt_entry = tk.Entry(edit_panel, font=("Helvetica", 12))
            qty_wt_entry.grid(row=4, column=1, padx=20, pady=5, sticky="e")

            qty_wt_entry.insert(0, laundry_rows[0][2])

            laundry_category_label = tk.Label(edit_panel, text="Laundry Category", bg="white", fg="black",
                                              font=("Helvetica", 14))
            laundry_category_label.grid(row=4, column=2, padx=20, pady=20, sticky="e")
            laundry_category = ttk.Combobox(edit_panel, values=["Clothes", "Bed Sheets"],
                                            font=("Helvetica", 12))
            laundry_category.grid(row=4, column=3, padx=20, pady=5, sticky="e")

            laundry_category.set(laundry_rows[0][1])

            connection = sqlite3.connect('japaeng.db')
            cursor = connection.cursor()

            cursor.execute("SELECT service_id, service_price FROM SERVICE WHERE service_category = ?",
                           (service_dropdown.get(),))
            new_service_category = cursor.fetchone()

            connection.close()

            update_button = tk.Button(edit_panel, text="Update", bg="#87CEEB", font=("Helvetica", 12),
                                      command=commit_update)
            update_button.grid(row=7, column=0, padx=20, pady=10, sticky="w")

            del_button = tk.Button(edit_panel, text="Delete", bg="red", font=("Helvetica", 12),
                                   command=delete_transaction)
            del_button.grid(row=7, column=1, padx=20, pady=10, sticky="w")

    transaction_root = tk.Tk()
    transaction_root.geometry("{width}x{height}+0+0".format(width=transaction_root.winfo_screenwidth(),
                                                            height=transaction_root.winfo_screenheight()))
    transaction_root.title("Laundry Management System")

    # Configure colors
    bg_color = "#F2F2F2"
    header_bg_color = "#222222"
    header_fg_color = "white"
    button_bg_color = "#007BFF"
    button_fg_color = "white"

    # Top Panel
    top_panel = tk.Frame(transaction_root, bg="black", height=50)
    top_panel.pack(fill=tk.X)

    # Change font, size, and color for "Japaeng" label
    label_title = tk.Label(top_panel, text="Japaeng", fg="white", bg="black", font=("Arial", 24, "bold"), padx=10)
    label_title.pack(side=tk.LEFT)

    # Change button color to blend with the background
    logout_button = tk.Button(top_panel, text="Log Out", fg="white", bg="black", command="", relief=tk.FLAT)
    logout_button.pack(side=tk.RIGHT, padx=10)

    # Left Panel for Welcome Message, Date, and Buttons
    left_panel = tk.Frame(transaction_root, bg="black", width=150)  # Adjust the width here (originally 200)
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
        buttons_panel, text="Transactions", command="", width=30, height=5,
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
    content_panel = tk.Frame(transaction_root, bg="white")
    content_panel.pack(fill=tk.BOTH, expand=True)

    # Add a black frame inside the white content_panel
    frame_inside_content = tk.Frame(content_panel, bg="black", padx=15, pady=15)  # Adjust padding here (originally 20)
    frame_inside_content.pack(padx=50, pady=50, fill=tk.BOTH, expand=True)  # Adjust fill settings

    # Create another panel inside the black frame with white interior
    inner_panel = tk.Frame(frame_inside_content, bg="white")
    inner_panel.pack(fill=tk.BOTH, expand=True)  # Adjust fill settings to occupy the entire black frame

    heading_label = tk.Label(inner_panel, text="TRANSACTIONS", bg="white", font=("Helvetica", 16, "bold"))
    heading_label.pack(pady=(20, 20))

    data_table = ttk.Treeview(inner_panel,
                              columns=("Transaction ID", "Total Amount", "Transaction Date", "Status",
                                       "Customer Name", "Service Category"
                                                        ""))

    # Define column headings
    data_table.heading("#1", text="Transaction ID")
    data_table.heading("#2", text="Total Amount")
    data_table.heading("#3", text="Transaction Date")
    data_table.heading("#4", text="Status")
    data_table.heading("#5", text="Customer Name")
    data_table.heading("#6", text="Service Category")

    # Set column widths
    data_table.column("#1", width=100)
    data_table.column("#2", width=100)
    data_table.column("#3", width=100)
    data_table.column("#4", width=100)
    data_table.column("#5", width=100)
    data_table.column("#6", width=100)

    fetch_and_display_data(data_table)
    data_table.bind("<<TreeviewSelect>>", update_button_state)

    data_table.pack(fill=tk.BOTH, expand=True)
    data_table.pack_configure(anchor=tk.CENTER)

    # Create New Transaction button inside the white panel (below the black panel)
    create_new_button = tk.Button(content_panel, text="Create New Transaction", command=switch_to_add_transaction,
                                  bg="#87CEEB", fg="black",
                                  font=("Helvetica", 14))
    create_new_button.pack(pady=(40, 60), ipadx=40, ipady=15)

    transaction_root.mainloop()
