
import mysql.connector 

mydb = mysql.connector.connect(host='localhost', user='root', passwd='Ankit@2541', database='BANK_MANAGEMENT')

def validate_account_number(ac):
    return ac.isdigit() and len(ac) == 10

def validate_contact_number(cn):
    return cn.isdigit() and len(cn) == 10

def OpenAcc():
    n = input("Enter The Name: ")
    while True:
        ac = input("Enter The Account No: ")
        if validate_account_number(ac):
            break
        else:
            print("Account number must be a 10 digit number. Please try again.")
    db = input("Enter The Date Of Birth: ")
    add = input("Enter The Address: ")
    while True:
        cn = input("Enter The Contact Number: ")
        if validate_contact_number(cn):
            break
        else:
            print("Contact number must be 10 digits long. Please try again.")
    ob = int(input("Enter The Opening Balance: "))
    data1 = (n, ac, db, add, cn, ob)
    data2 = (n, ac, ob)
    sql1 = 'INSERT INTO account VALUES (%s, %s, %s, %s, %s, %s)'
    sql2 = 'INSERT INTO amount VALUES (%s, %s, %s)'
    x = mydb.cursor()
    x.execute(sql1, data1)
    x.execute(sql2, data2)
    mydb.commit()
    print("Data Entered Successfully")

def DepoAmount():
    amount = int(input("Enter the amount you want to deposit: "))
    while True:
        ac = input("Enter The Account No: ")
        if validate_account_number(ac):
            break
        else:
            print("Account number must be a 10 digit number. Please try again.")
    a = 'SELECT balance FROM amount WHERE AccNo=%s'
    data = (ac,)
    x = mydb.cursor()
    x.execute(a, data)
    result = x.fetchone()
    t = result[0] + amount
    sql = 'UPDATE amount SET balance=%s WHERE AccNo=%s'
    d = (t, ac)
    x.execute(sql, d)
    mydb.commit()
    main()

def WithdrawAmount():
    amount = int(input("Enter the amount you want to withdraw: "))
    while True:
        ac = input("Enter The Account No: ")
        if validate_account_number(ac):
            break
        else:
            print("Account number must be a 10 digit number. Please try again.")
    a = 'SELECT balance FROM amount WHERE AccNo=%s'
    data = (ac,)
    x = mydb.cursor()
    x.execute(a, data)
    result = x.fetchone()
    t = result[0] - amount
    sql = 'UPDATE amount SET balance=%s WHERE AccNo=%s'
    d = (t, ac)
    x.execute(sql, d)
    mydb.commit()
    main()

def BalEng():
    while True:
        ac = input("Enter the account no: ")
        if validate_account_number(ac):
            break
        else:
            print("Account number must be a 10 digit number. Please try again.")
    a = 'SELECT * FROM amount WHERE AccNo=%s'
    data = (ac,)
    x = mydb.cursor()
    x.execute(a, data)
    result = x.fetchone()
    print("Balance for account:", ac, "is", result[-1])
    main()

def DisDetails():
    while True:
        ac = input("Enter the account no: ")
        if validate_account_number(ac):
            break
        else:
            print("Account number must be a 10 digit number. Please try again.")
    a = 'SELECT * FROM account WHERE AccNo=%s'
    data = (ac,)
    x = mydb.cursor()
    x.execute(a, data)
    result = x.fetchone()
    for i in result:
        print(i)
    main()

def CloseAcc():
    while True:
        ac = input("Enter the account no: ")
        if validate_account_number(ac):
            break
        else:
            print("Account number must be a 10 digit number. Please try again.")
    sql1 = 'DELETE FROM account WHERE AccNo=%s'
    sql2 = 'DELETE FROM amount WHERE AccNo=%s'
    data = (ac,)
    x = mydb.cursor()
    x.execute(sql1, data)
    x.execute(sql2, data)
    mydb.commit()
    main()

def main():
    print('''1. OPEN NEW ACCOUNT
2. DEPOSIT AMOUNT
3. WITHDRAW AMOUNT
4. BALANCE ENQUIRY
5. DISPLAY CUSTOMER DETAILS
6. CLOSE AN ACCOUNT''')
    choice = input("Enter The Task You Want To Perform: ")
    if choice == '1':
        OpenAcc()
    elif choice == '2':
        DepoAmount()
    elif choice == '3':
        WithdrawAmount()
    elif choice == '4':
        BalEng()
    elif choice == '5':
        DisDetails()
    elif choice == '6':
        CloseAcc()
    else:
        print("Invalid Choice")
        main()

main()
