"""
RetailManagementSystem
this would used in grocery stores and small business owners who want to manage following
*inventory
*sales
*dealers
*customers

this is the main file used to operate multiple functionalities
"""

import mod.warehouse as wharehouse
import mod.transaction as transaction
import mod.customer as customer
import mod.dumpDB as dumpDB
import mod.coupon as coupon
import mod.dealer as dealer
import mod.alert as alert
import mod.bill as bill
import mysql.connector


def sqlLogin(dbName):
    """ Login Procedure """
    global uName
    global uPass
    while True:
        uName = input('Enter Username-->')
        uPass = input('Enter Password-->')
        a = ' ' * (len(uPass) + 17) + '\n'  # count number of char. in pass
        print("\033[F" + a, end="", flush=True)  # \033[F is ANSI to the cursor one line up and added spaces to remove password

        sqlConnector = mysql.connector.connect(host='localhost', username=uName, password=uPass, database=dbName)
        if sqlConnector.is_connected():
            print('connected')
            return sqlConnector
        else:
            print('Error in connecting. Please try again.')
            continue


# Database selection/insrtallation procedure
dpDB = input('Do you want to install test Database? (y/n)')

if dpDB.lower() == 'y':
    dbName = 'Retail_test_db'
    sqlConnector = sqlLogin(dbName)  # function call to mysql login
    sqlCursor = sqlConnector.cursor()
    dumpDB.initialiseDB(sqlCursor, dbName)
    dumpDB.jamData(sqlConnector, dbName)

elif dpDB.lower() == 'n':
    print('No Database will be installed.')
    dbName = input('Enter database name-->')
    sqlConnector = sqlLogin(dbName)  # function call to mysql login
    sqlCursor = sqlConnector.cursor()

else:
    getch = input('Wrong Input. Run program again')


while True:
    print('\nEnter q on completion.')
    print('\
        1. Create new Bill\n\
        2. View a Bill\n\
        3. Alter a Bill\n\n\
        4. New Transaction\n\
        5. View Transaction\n\n\
        6. New Product\n\
        7. Edit Product\n\
        8. View Product\n\n\
        9. Add Customer\n\
        10. View Customer\n\n\
        11. Add Dealer\n\
        12. View Dealer\n\n\
        13. Coupon Management\n\n\
        14. Check Alerts')

    selection = input('\nEnter number from the following-->')
    if selection == '1':
        bill.createBill(sqlConnector)
    elif selection == '2':
        s_id = input('Enter Sales ID-->')
        bill.viewBill(s_id)
    elif selection == '3':
        s_id = input('Enter Sales ID-->')
        bill.alterBill(s_id, sqlCursor)
    elif selection == '4':
        transaction.newtransaction(sqlConnector)
    elif selection == '5':
        transaction.viewTransaction(sqlCursor)
    elif selection == '6':
        wharehouse.newProduct(sqlConnector)
    elif selection == '7':
        wharehouse.editProduct(sqlConnector)
    elif selection == '8':
        p_id = input('Enter Product ID-->')
        wharehouse.viewProduct(sqlConnector, p_id)
    elif selection == '9':
        customer.newCustomer(sqlConnector)
    elif selection == '10':
        c_id = input('Enter all to view all.\nEnter Customer ID-->')
        customer.viewCustomer(sqlConnector, c_id)
    elif selection == '11':
        dealer.newDealer(sqlConnector)
    elif selection == '12':
        d_id = input('Enter Dealer ID-->')
        dealer.viewDealer(sqlConnector, d_id)
    elif selection == '13':
        print('\
        1. New Coupon\n\
        2. Edit Coupon\n\
        3. Delete Coupon\n\
        4. View Coupon\n')
        sel = input('Enter number from the following-->')
        if sel == '1':
            coupon.newCoupon(sqlConnector)
        elif sel == '2':
            coupon.editCoupon(sqlConnector)
        elif sel == '3':
            coupon.deleteCoupon(sqlConnector)
        elif sel == '4':
            coupon.viewCoupon(sqlConnector)
        else:
            print('Wrong Input.')
            continue
    elif selection == '14':
        alert.alertSystem(sqlConnector)
    elif selection.lower() == 'q':
        break
    else:
        print('Wrong Input. Try again.')
    getch = input('Press Enter to continue.')

sqlConnector.commit()
sqlConnector.close()
getch = input()
