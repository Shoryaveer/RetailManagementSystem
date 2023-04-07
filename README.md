# Retail Management System

## Summary

This Retail Management System is a command-line interface-based application designed to manage transactions, products, and dealer information for a retail store. Users can perform various operations, such as creating new transactions, viewing transaction details, generating bills, and more.

- `dumpDB.py`: Imports sample data into the MySQL database.
- `bill.py`: Generates bills for transactions, calculates total costs, and saves the bill information to a file.
- `dealer.py`: Allows users to add, update, and view dealer information.
- `product.py`: Facilitates adding, updating, and viewing product information.
- `transaction.py`: Handles the creation of new transactions and the viewing of transaction details.

## Skills used

- **MySQL connector**: Used for connecting the Python application to a MySQL database, executing SQL queries, and performing database manipulation such as creating, updating, and retrieving records.
- **Command-line interface**: Developed an intuitive command-line interface for users to interact with the system and perform various tasks.
- **Exception handling**: Implemented robust error handling to ensure smooth operation of the system and provide useful feedback to users in case of invalid inputs or unexpected errors.
- **File I/O**: Implemented file reading and writing operations for loading sample data from the `database` folder and storing information in the `bill.obj` file.
- **Database manipulation**: Leveraged SQL skills to perform various database operations such as inserting, updating, and fetching records, as well as managing relationships between tables.

## Features

- **Sample database**: Includes sample data for products, dealers, and transactions to help users get started quickly.
- **Autonomous building of database**: Automatically imports the sample data into the MySQL database upon running the `dumpDB.py` script.
- **Intuitive command-line interface**: Offers an easy-to-use command-line interface for users to interact with the system and perform various operations.
- **Modular design**: Organizes the code into modules for better maintainability and scalability.
