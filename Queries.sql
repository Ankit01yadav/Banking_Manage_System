create database BANK_MANAGEMENT;
use BANK_MANAGEMENT;
CREATE TABLE account (
    name VARCHAR(255),
    account_no VARCHAR(10) PRIMARY KEY,
    dob DATE,
    address VARCHAR(255),
    contact_no VARCHAR(10),
    opening_balance INT,
    account_type VARCHAR(50)
);
CREATE TABLE amount (
    account_no VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255),
    balance INT,
    FOREIGN KEY (account_no) REFERENCES account(account_no)
);
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_no VARCHAR(10),
    transaction_type VARCHAR(50),
    amount INT,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_no) REFERENCES account(account_no)
);
show tables;
Select * from account;

