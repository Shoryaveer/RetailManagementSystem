""" this module helps installing test database """

import csv


def initaliseDB(sqlCursor, dbName):
    """ This function is used to create database and tables """

    # Creating rms database
    sqlCursor.execute(f'CREATE DATABASE {dbName};')
    sqlCursor.execute(f'USE {dbName};')

    # Creating customer data table
    sqlCursor.execute(" \
        CREATE TABLE c_data( \
        c_id CHAR(5) PRIMARY KEY, \
        c_name VARCHAR(30), \
        c_address VARCHAR(40), \
        c_mobile CHAR(10) \
        )")

    # Creating sales table
    sqlCursor.execute(" \
        CREATE TABLE sales( \
        s_id CHAR(5) PRIMARY KEY, \
        c_id CHAR(6), \
        issued_on DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP \
        )")

    # Creating stock table
    sqlCursor.execute(" \
        CREATE TABLE stock( \
        p_id CHAR(2) PRIMARY KEY, \
        d_id CHAR(3), \
        p_name VARCHAR(30), \
        p_quantity INT, \
        p_price FLOAT, \
        p_expire DATE \
        )")

    # Creating dealer data table
    sqlCursor.execute(" \
        CREATE TABLE dealer_data( \
        d_id CHAR(3) PRIMARY KEY, \
        d_name VARCHAR(30), \
        d_address VARCHAR(40), \
        d_mobile CHAR(10) \
        )")

    # Creating coupons table
    sqlCursor.execute(" \
        CREATE TABLE coupons( \
        co_id CHAR(8) PRIMARY KEY, \
        expire_date DATE, \
        min_prod INT, \
        percentage INT \
        )")

    # Creating stock transactions
    sqlCursor.execute(" \
        CREATE TABLE stocktransac( \
        d_id CHAR(3), \
        st_id CHAR(4) PRIMARY KEY, \
        transac_date DATETIME DEFAULT CURRENT_TIMESTAMP \
        )")

    # Creating transaction details
    sqlCursor.execute("\
        CREATE TABLE stocktransac2( \
        p_id CHAR(4), \
        p_cp FLOAT, \
        st_id CHAR(4), \
        quantity INT, \
        exp_date DATE \
        )")


def jamData(sqlConnector, dbName):
    """ helps fill data in newly created database """

    sqlCursor = sqlConnector.cursor()
    sqlCursor.execute(f'USE {dbName};')  # Selecting Database

    ##
    # Dumping data in c_data
    insC_Data = open(r'.\database\C_DATA.bin', 'r', newline='\n')  # Relative path opening to data file
    c_dataReader = csv.reader(insC_Data, delimiter='\t')  # Creating CSV databaseect to iter through stored data
    insC_Data.seek(0)  # Moving cursor to the start of file

    for ins in c_dataReader:
        sqlCursor.execute(f" \
        INSERT INTO c_data(c_id, c_name, c_address, c_mobile) \
        VALUES('{ins[0]}', '{ins[1]}', '{ins[2]}', '{ins[3]}') \
        ")
        sqlConnector.commit()
    insC_Data.close()

    ##
    # Dumping data in dealer_data
    insDealer_Data = open(r'.\database\DEALER_DATA.bin', 'r', newline='\n')
    dealer_dataReader = csv.reader(insDealer_Data, delimiter='\t')
    insDealer_Data.seek(0)

    for ins in dealer_dataReader:
        sqlCursor.execute(f" \
        INSERT INTO dealer_data(d_id, d_name, d_address, d_mobile) \
        VALUES('{ins[0]}', '{ins[1]}', '{ins[2]}', '{ins[3]}') \
        ")
        sqlConnector.commit()
    insDealer_Data.close()

    ##
    # Dumping data in coupons
    insCoupons = open(r'.\database\COUPONS.bin', 'r', newline='\n')
    couponsReader = csv.reader(insCoupons, delimiter='\t')
    insCoupons.seek(0)

    for ins in couponsReader:
        sqlCursor.execute(f" \
        INSERT INTO coupons(co_id, expire_date, min_prod, percentage) \
        VALUES('{ins[0]}', '{ins[1]}', {ins[2]}, {ins[3]}) \
        ")
        sqlConnector.commit()
    insCoupons.close()

    ##
    # Dumping data in stock
    insStock = open(r'.\database\STOCK.bin', 'r', newline='\n')
    stockReader = csv.reader(insStock, delimiter='\t')
    insStock.seek(0)

    for ins in stockReader:
        sqlCursor.execute(f" \
        INSERT INTO stock(p_id, d_id, p_name, p_quantity, p_price, p_expire) \
        VALUES('{ins[0]}', '{ins[1]}', '{ins[2]}', {ins[3]}, {ins[4]}, '{ins[5]}') \
        ")
        sqlConnector.commit()
    insStock.close()

    ##
    # Dumping data in sales
    insSales = open(r'.\database\SALES.bin', 'r', newline='\n')
    salesReader = csv.reader(insSales, delimiter='\t')
    insSales.seek(0)

    for ins in salesReader:
        sqlCursor.execute(f" \
        INSERT INTO sales(s_id, c_id, issued_on) \
        VALUES('{ins[0]}', '{ins[1]}', '{ins[2]}') \
        ")
        sqlConnector.commit()
    insSales.close()

    ##
    # Dumping data in stock transaction
    insStockTran = open(r'.\database\STOCKTRAN.bin', 'r', newline='\n')
    stockTranReader = csv.reader(insStockTran, delimiter='\t')
    insStockTran.seek(0)

    for ins in stockTranReader:
        sqlCursor.execute(f" \
        INSERT INTO stocktransac(d_id, st_id, transac_date) \
        VALUES('{ins[0]}', '{ins[1]}', '{ins[2]}') \
        ")
        sqlConnector.commit()
    insStock.close()

    ##
    # Dumping data in transaction details
    insStockTran2 = open(r'.\database\STOCKTRAN2.bin', 'r', newline='\n')
    stockTran2Reader = csv.reader(insStockTran2, delimiter='\t')
    insStockTran2.seek(0)

    for ins in stockTran2Reader:
        sqlCursor.execute(f" \
        INSERT INTO stocktransac2(p_id, p_cp, st_id, quantity, exp_date) \
        VALUES('{ins[0]}', {ins[1]}, '{ins[2]}', {ins[3]}, '{ins[4]}') \
        ")
        sqlConnector.commit()
    insStockTran2.close()
