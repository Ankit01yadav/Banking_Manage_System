import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import time  # Import time module

mydb = mysql.connector.connect(host='localhost', user='root', passwd='Ankit@2541', database='BANK_MANAGEMENT')

def validate_account_number(ac):
    return ac.isalnum() and len(ac) == 10

def validate_contact_number(cn):
    return cn.isdigit() and len(cn) == 10

def open_acc():
    def submit():
        n = name_entry.get()
        ac = ac_entry.get()
        db = dob_entry.get()
        add = addr_entry.get()
        cn = contact_entry.get()
        atype = acc_type_entry.get()
        ob = int(balance_entry.get())
        if validate_account_number(ac) and validate_contact_number(cn):
            data1 = (n, ac, db, add, cn, ob, atype)
            data2 = (ac, n, ob)
            sql1 = 'INSERT INTO account (name, account_no, dob, address, contact_no, opening_balance, account_type) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            sql2 = 'INSERT INTO amount (account_no, name, balance) VALUES (%s, %s, %s)'
            x = mydb.cursor()
            
            start_time = time.time()
            x.execute(sql1, data1)
            x.execute(sql2, data2)
            mydb.commit()
            end_time = time.time()
            
            response_time = end_time - start_time
            print(f"Time taken for account creation: {response_time:.4f} seconds")
            
            messagebox.showinfo("Success", f"Account Created Successfully\nTime taken: {response_time:.4f} seconds")
            new_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid Account Number or Contact Number")

    new_window = tk.Toplevel(root)
    new_window.title("Open New Account")
    
    labels = ["Name", "Account No", "Date Of Birth (YYYY-MM-DD)", "Address", "Contact No", "Account Type", "Opening Balance"]
    entries = [tk.Entry(new_window) for _ in labels]
    name_entry, ac_entry, dob_entry, addr_entry, contact_entry, acc_type_entry, balance_entry = entries

    for i, (label, entry) in enumerate(zip(labels, entries)):
        tk.Label(new_window, text=label).grid(row=i, column=0, padx=10, pady=5)
        entry.grid(row=i, column=1, padx=10, pady=5)
    
    tk.Button(new_window, text="Submit", command=submit).grid(row=len(labels), column=1, pady=10)

def depo_amount():
    def submit():
        amount = int(amount_entry.get())
        ac = ac_entry.get()
        if validate_account_number(ac):
            a = 'SELECT balance FROM amount WHERE account_no=%s'
            data = (ac,)
            x = mydb.cursor()
            
            start_time = time.time()
            x.execute(a, data)
            result = x.fetchone()
            end_time = time.time()
            
            response_time = end_time - start_time
            print(f"Time taken for balance check: {response_time:.4f} seconds")
            
            if result:
                t = result[0] + amount
                sql = 'UPDATE amount SET balance=%s WHERE account_no=%s'
                d = (t, ac)
                
                start_time = time.time()
                x.execute(sql, d)
                sql_tr = 'INSERT INTO transactions (account_no, transaction_type, amount) VALUES (%s, %s, %s)'
                data_tr = (ac, 'Deposit', amount)
                x.execute(sql_tr, data_tr)
                mydb.commit()
                end_time = time.time()
                
                response_time = end_time - start_time
                print(f"Time taken for deposit operation: {response_time:.4f} seconds")
                
                messagebox.showinfo("Success", f"Amount Deposited Successfully\nTime taken: {response_time:.4f} seconds")
                new_window.destroy()
            else:
                messagebox.showerror("Error", "Account Not Found")
        else:
            messagebox.showerror("Error", "Invalid Account Number")

    new_window = tk.Toplevel(root)
    new_window.title("Deposit Amount")
    
    tk.Label(new_window, text="Account No").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(new_window, text="Amount").grid(row=1, column=0, padx=10, pady=5)
    
    ac_entry = tk.Entry(new_window)
    amount_entry = tk.Entry(new_window)
    
    ac_entry.grid(row=0, column=1, padx=10, pady=5)
    amount_entry.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Button(new_window, text="Submit", command=submit).grid(row=2, column=1, pady=10)

def withdraw_amount():
    def submit():
        amount = int(amount_entry.get())
        ac = ac_entry.get()
        if validate_account_number(ac):
            a = 'SELECT balance FROM amount WHERE account_no=%s'
            data = (ac,)
            x = mydb.cursor()
            
            start_time = time.time()
            x.execute(a, data)
            result = x.fetchone()
            end_time = time.time()
            
            response_time = end_time - start_time
            print(f"Time taken for balance check: {response_time:.4f} seconds")
            
            if result and result[0] >= amount:
                t = result[0] - amount
                sql = 'UPDATE amount SET balance=%s WHERE account_no=%s'
                d = (t, ac)
                
                start_time = time.time()
                x.execute(sql, d)
                sql_tr = 'INSERT INTO transactions (account_no, transaction_type, amount) VALUES (%s, %s, %s)'
                data_tr = (ac, 'Withdraw', amount)
                x.execute(sql_tr, data_tr)
                mydb.commit()
                end_time = time.time()
                
                response_time = end_time - start_time
                print(f"Time taken for withdrawal operation: {response_time:.4f} seconds")
                
                messagebox.showinfo("Success", f"Amount Withdrawn Successfully\nTime taken: {response_time:.4f} seconds")
                new_window.destroy()
            else:
                messagebox.showerror("Error", "Insufficient Balance or Account Not Found")
        else:
            messagebox.showerror("Error", "Invalid Account Number")

    new_window = tk.Toplevel(root)
    new_window.title("Withdraw Amount")
    
    tk.Label(new_window, text="Account No").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(new_window, text="Amount").grid(row=1, column=0, padx=10, pady=5)
    
    ac_entry = tk.Entry(new_window)
    amount_entry = tk.Entry(new_window)
    
    ac_entry.grid(row=0, column=1, padx=10, pady=5)
    amount_entry.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Button(new_window, text="Submit", command=submit).grid(row=2, column=1, pady=10)

def balance_enquiry():
    def submit():
        ac = ac_entry.get()
        if validate_account_number(ac):
            a = 'SELECT balance FROM amount WHERE account_no=%s'
            data = (ac,)
            x = mydb.cursor()
            
            start_time = time.time()
            x.execute(a, data)
            result = x.fetchone()
            end_time = time.time()
            
            response_time = end_time - start_time
            print(f"Time taken for balance enquiry: {response_time:.4f} seconds")
            
            if result:
                messagebox.showinfo("Balance", f"Balance for account {ac} is {result[0]}\nTime taken: {response_time:.4f} seconds")
                new_window.destroy()
            else:
                messagebox.showerror("Error", "Account Not Found")
        else:
            messagebox.showerror("Error", "Invalid Account Number")

    new_window = tk.Toplevel(root)
    new_window.title("Balance Enquiry")
    
    tk.Label(new_window, text="Account No").grid(row=0, column=0, padx=10, pady=5)
    
    ac_entry = tk.Entry(new_window)
    
    ac_entry.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Button(new_window, text="Submit", command=submit).grid(row=1, column=1, pady=10)

def display_details():
    def submit():
        ac = ac_entry.get()
        if validate_account_number(ac):
            a = '''
            SELECT account.name, account.account_no, account.dob, account.address, account.contact_no, 
                   account.opening_balance, account.account_type, amount.balance
            FROM account
            JOIN amount ON account.account_no = amount.account_no
            WHERE account.account_no = %s
            '''
            data = (ac,)
            x = mydb.cursor()
            
            start_time = time.time()
            x.execute(a, data)
            result = x.fetchone()
            end_time = time.time()
            
            response_time = end_time - start_time
            print(f"Time taken for display details: {response_time:.4f} seconds")
            
            if result:
                details = f"Name: {result[0]}\nAccount No: {result[1]}\nDOB: {result[2]}\nAddress: {result[3]}\nContact No: {result[4]}\nOpening Balance: {result[5]}\nAccount Type: {result[6]}\nCurrent Balance: {result[7]}"
                messagebox.showinfo("Customer Details", f"{details}\nTime taken: {response_time:.4f} seconds")
                new_window.destroy()
            else:
                messagebox.showerror("Error", "Account Not Found")
        else:
            messagebox.showerror("Error", "Invalid Account Number")

    new_window = tk.Toplevel(root)
    new_window.title("Display Customer Details")
    
    tk.Label(new_window, text="Account No").grid(row=0, column=0, padx=10, pady=5)
    
    ac_entry = tk.Entry(new_window)
    
    ac_entry.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Button(new_window, text="Submit", command=submit).grid(row=1, column=1, pady=10)

def close_acc():
    def submit():
        ac = ac_entry.get()
        if validate_account_number(ac):
            sql1 = 'DELETE FROM account WHERE account_no=%s'
            sql2 = 'DELETE FROM amount WHERE account_no=%s'
            sql3 = 'DELETE FROM transactions WHERE account_no=%s'
            data = (ac,)
            x = mydb.cursor()
            
            start_time = time.time()
            x.execute(sql1, data)
            x.execute(sql2, data)
            x.execute(sql3, data)
            mydb.commit()
            end_time = time.time()
            
            response_time = end_time - start_time
            print(f"Time taken for account closure: {response_time:.4f} seconds")
            
            messagebox.showinfo("Success", f"Account Closed Successfully\nTime taken: {response_time:.4f} seconds")
            new_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid Account Number")

    new_window = tk.Toplevel(root)
    new_window.title("Close Account")
    
    tk.Label(new_window, text="Account No").grid(row=0, column=0, padx=10, pady=5)
    
    ac_entry = tk.Entry(new_window)
    
    ac_entry.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Button(new_window, text="Submit", command=submit).grid(row=1, column=1, pady=10)

def view_transactions():
    def submit():
        ac = ac_entry.get()
        if validate_account_number(ac):
            a = 'SELECT transaction_id, transaction_type, amount, transaction_date FROM transactions WHERE account_no=%s'
            data = (ac,)
            x = mydb.cursor()
            
            start_time = time.time()
            x.execute(a, data)
            results = x.fetchall()
            end_time = time.time()
            
            response_time = end_time - start_time
            print(f"Time taken for viewing transactions: {response_time:.4f} seconds")
            
            if results:
                transactions = "\n".join([f"Transaction ID: {row[0]}, Type: {row[1]}, Amount: {row[2]}, Date: {row[3]}" for row in results])
                messagebox.showinfo("Transactions", f"{transactions}\nTime taken: {response_time:.4f} seconds")
                new_window.destroy()
            else:
                messagebox.showerror("Error", "No Transactions Found")
        else:
            messagebox.showerror("Error", "Invalid Account Number")

    new_window = tk.Toplevel(root)
    new_window.title("View Transactions")
    
    tk.Label(new_window, text="Account No").grid(row=0, column=0, padx=10, pady=5)
    
    ac_entry = tk.Entry(new_window)
    
    ac_entry.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Button(new_window, text="Submit", command=submit).grid(row=1, column=1, pady=10)

root = tk.Tk()
root.title("Bank Management System")

# Use ttk.Style to customize button styles
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12), padding=10, background='lightblue')

buttons = [
    ("Open New Account", open_acc),
    ("Deposit Amount", depo_amount),
    ("Withdraw Amount", withdraw_amount),
    ("Balance Enquiry", balance_enquiry),
    ("Display Customer Details", display_details),
    ("Close Account", close_acc),
    ("View Transactions", view_transactions)
]

for i, (text, command) in enumerate(buttons):
    ttk.Button(root, text=text, command=command, style='TButton').grid(row=i, column=0, padx=20, pady=10, sticky="ew")

root.mainloop()
