import tkinter as tk
from tkinter import messagebox
import mysql.connector

mydb = mysql.connector.connect(host='localhost', user='root', passwd='Ankit@2541', database='BANK_MANAGEMENT')

def validate_account_number(ac):
    return ac.isdigit() and len(ac) == 10

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
            x.execute(sql1, data1)
            x.execute(sql2, data2)
            mydb.commit()
            messagebox.showinfo("Success", "Account Created Successfully")
            new_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid Account Number or Contact Number")

    new_window = tk.Toplevel(root)
    new_window.title("Open New Account")
    
    tk.Label(new_window, text="Name").grid(row=0, column=0)
    tk.Label(new_window, text="Account No").grid(row=1, column=0)
    tk.Label(new_window, text="Date Of Birth (YYYY-MM-DD)").grid(row=2, column=0)
    tk.Label(new_window, text="Address").grid(row=3, column=0)
    tk.Label(new_window, text="Contact No").grid(row=4, column=0)
    tk.Label(new_window, text="Account Type").grid(row=5, column=0)
    tk.Label(new_window, text="Opening Balance").grid(row=6, column=0)
    
    name_entry = tk.Entry(new_window)
    ac_entry = tk.Entry(new_window)
    dob_entry = tk.Entry(new_window)
    addr_entry = tk.Entry(new_window)
    contact_entry = tk.Entry(new_window)
    acc_type_entry = tk.Entry(new_window)
    balance_entry = tk.Entry(new_window)
    
    name_entry.grid(row=0, column=1)
    ac_entry.grid(row=1, column=1)
    dob_entry.grid(row=2, column=1)
    addr_entry.grid(row=3, column=1)
    contact_entry.grid(row=4, column=1)
    acc_type_entry.grid(row=5, column=1)
    balance_entry.grid(row=6, column=1)
    
    tk.Button(new_window, text="Submit", command=submit).grid(row=7, column=1)
    
def depo_amount():
    def submit():
        amount = int(amount_entry.get())
        ac = ac_entry.get()
        if validate_account_number(ac):
            a = 'SELECT balance FROM amount WHERE account_no=%s'
            data = (ac,)
            x = mydb.cursor()
            x.execute(a, data)
            result = x.fetchone()
            if result:
                t = result[0] + amount
                sql = 'UPDATE amount SET balance=%s WHERE account_no=%s'
                d = (t, ac)
                x.execute(sql, d)
                sql_tr = 'INSERT INTO transactions (account_no, transaction_type, amount) VALUES (%s, %s, %s)'
                data_tr = (ac, 'Deposit', amount)
                x.execute(sql_tr, data_tr)
                mydb.commit()
                messagebox.showinfo("Success", "Amount Deposited Successfully")
                new_window.destroy()
            else:
                messagebox.showerror("Error", "Account Not Found")
        else:
            messagebox.showerror("Error", "Invalid Account Number")

    new_window = tk.Toplevel(root)
    new_window.title("Deposit Amount")
    
    tk.Label(new_window, text="Account No").grid(row=0, column=0)
    tk.Label(new_window, text="Amount").grid(row=1, column=0)
    
    ac_entry = tk.Entry(new_window)
    amount_entry = tk.Entry(new_window)
    
    ac_entry.grid(row=0, column=1)
    amount_entry.grid(row=1, column=1)
    
    tk.Button(new_window, text="Submit", command=submit).grid(row=2, column=1)

def withdraw_amount():
    def submit():
        amount = int(amount_entry.get())
        ac = ac_entry.get()
        if validate_account_number(ac):
            a = 'SELECT balance FROM amount WHERE account_no=%s'
            data = (ac,)
            x = mydb.cursor()
            x.execute(a, data)
            result = x.fetchone()
            if result and result[0] >= amount:
                t = result[0] - amount
                sql = 'UPDATE amount SET balance=%s WHERE account_no=%s'
                d = (t, ac)
                x.execute(sql, d)
                sql_tr = 'INSERT INTO transactions (account_no, transaction_type, amount) VALUES (%s, %s, %s)'
                data_tr = (ac, 'Withdraw', amount)
                x.execute(sql_tr, data_tr)
                mydb.commit()
                messagebox.showinfo("Success", "Amount Withdrawn Successfully")
                new_window.destroy()
            else:
                messagebox.showerror("Error", "Insufficient Balance or Account Not Found")
        else:
            messagebox.showerror("Error", "Invalid Account Number")

    new_window = tk.Toplevel(root)
    new_window.title("Withdraw Amount")
    
    tk.Label(new_window, text="Account No").grid(row=0, column=0)
    tk.Label(new_window, text="Amount").grid(row=1, column=0)
    
    ac_entry = tk.Entry(new_window)
    amount_entry = tk.Entry(new_window)
    
    ac_entry.grid(row=0, column=1)
    amount_entry.grid(row=1, column=1)
    
    tk.Button(new_window, text="Submit", command=submit).grid(row=2, column=1)

def balance_enquiry():
    def submit():
        ac = ac_entry.get()
        if validate_account_number(ac):
            a = 'SELECT balance FROM amount WHERE account_no=%s'
            data = (ac,)
            x = mydb.cursor()
            x.execute(a, data)
            result = x.fetchone()
            if result:
                messagebox.showinfo("Balance", f"Balance for account {ac} is {result[0]}")
                new_window.destroy()
            else:
                messagebox.showerror("Error", "Account Not Found")
        else:
            messagebox.showerror("Error", "Invalid Account Number")

    new_window = tk.Toplevel(root)
    new_window.title("Balance Enquiry")
    
    tk.Label(new_window, text="Account No").grid(row=0, column=0)
    
    ac_entry = tk.Entry(new_window)
    
    ac_entry.grid(row=0, column=1)
    
    tk.Button(new_window, text="Submit", command=submit).grid(row=1, column=1)

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
            x.execute(a, data)
            result = x.fetchone()
            if result:
                details = f"Name: {result[0]}\nAccount No: {result[1]}\nDOB: {result[2]}\nAddress: {result[3]}\nContact No: {result[4]}\nOpening Balance: {result[5]}\nAccount Type: {result[6]}\nCurrent Balance: {result[7]}"
                messagebox.showinfo("Customer Details", details)
                new_window.destroy()
            else:
                messagebox.showerror("Error", "Account Not Found")
        else:
            messagebox.showerror("Error", "Invalid Account Number")

    new_window = tk.Toplevel(root)
    new_window.title("Display Customer Details")
    
    tk.Label(new_window, text="Account No").grid(row=0, column=0)
    
    ac_entry = tk.Entry(new_window)
    
    ac_entry.grid(row=0, column=1)
    
    tk.Button(new_window, text="Submit", command=submit).grid(row=1, column=1)

def close_acc():
    def submit():
        ac = ac_entry.get()
        if validate_account_number(ac):
            sql1 = 'DELETE FROM account WHERE account_no=%s'
            sql2 = 'DELETE FROM amount WHERE account_no=%s'
            sql3 = 'DELETE FROM transactions WHERE account_no=%s'
            data = (ac,)
            x = mydb.cursor()
            x.execute(sql1, data)
            x.execute(sql2, data)
            x.execute(sql3, data)
            mydb.commit()
            messagebox.showinfo("Success", "Account Closed Successfully")
            new_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid Account Number")

    new_window = tk.Toplevel(root)
    new_window.title("Close Account")
    
    tk.Label(new_window, text="Account No").grid(row=0, column=0)
    
    ac_entry = tk.Entry(new_window)
    
    ac_entry.grid(row=0, column=1)
    
    tk.Button(new_window, text="Submit", command=submit).grid(row=1, column=1)

def view_transactions():
    def submit():
        ac = ac_entry.get()
        if validate_account_number(ac):
            a = 'SELECT transaction_id, transaction_type, amount, transaction_date FROM transactions WHERE account_no=%s'
            data = (ac,)
            x = mydb.cursor()
            x.execute(a, data)
            results = x.fetchall()
            if results:
                transactions = "\n".join([f"Transaction ID: {row[0]}, Type: {row[1]}, Amount: {row[2]}, Date: {row[3]}" for row in results])
                messagebox.showinfo("Transactions", transactions)
                new_window.destroy()
            else:
                messagebox.showerror("Error", "No Transactions Found")
        else:
            messagebox.showerror("Error", "Invalid Account Number")

    new_window = tk.Toplevel(root)
    new_window.title("View Transactions")
    
    tk.Label(new_window, text="Account No").grid(row=0, column=0)
    
    ac_entry = tk.Entry(new_window)
    
    ac_entry.grid(row=0, column=1)
    
    tk.Button(new_window, text="Submit", command=submit).grid(row=1, column=1)

root = tk.Tk()
root.title("Bank Management System")

tk.Button(root, text="Open New Account", command=open_acc).grid(row=0, column=0)
tk.Button(root, text="Deposit Amount", command=depo_amount).grid(row=1, column=0)
tk.Button(root, text="Withdraw Amount", command=withdraw_amount).grid(row=2, column=0)
tk.Button(root, text="Balance Enquiry", command=balance_enquiry).grid(row=3, column=0)
tk.Button(root, text="Display Customer Details", command=display_details).grid(row=4, column=0)
tk.Button(root, text="Close Account", command=close_acc).grid(row=5, column=0)
tk.Button(root, text="View Transactions", command=view_transactions).grid(row=6, column=0)

root.mainloop()
