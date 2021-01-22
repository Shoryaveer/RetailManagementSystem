""" This module helps manage bill for user. """
import random


def createBill(sqlConnector, dbName):
    """ Bill Creation procedure """

    sqlCursor = sqlConnector.cursor()
    sqlCursor.execute(f'USE {dbName};')

    sqlCursor.execute("SELECT p_id, p_name, p_quantity, p_price FROM stock")  # Receiving p_id and p_name for selection
    retrieveSet = sqlCursor.fetchall()

    idArray = {}  # Dictionary created to store ID(s), quantities and price of product {'p_id': [p_quantity, p_price, p_name]}
    print('Product ID'.ljust(14), 'Product Name'.ljust(33), 'Quantity Available', sep='')  # Displaying hedings
    for p_id, p_name, p_quantity, p_price in retrieveSet:
        print(p_id.rjust(10) + '    ', p_name.ljust(33), p_quantity, sep='')  # displaying the ID Names and Quantities
        idArray[p_id] = [p_quantity, p_price, p_name]  # Storing ID, Quantities and price

    # Attaining product ID and Quantities
    print('\nEnter q on completion')

    productQueue = {}  # Dictionary created to store selected product ID(s) {'p_id': [p_quantity, p_price, p_name]}
    while True:
        idInput = input('\nEnter product ID-->')
        # ID validation block
        if idInput.lower() == 'q':
            break
        elif idInput not in idArray:
            print('Product ID does not exist.')
            continue

        # Quantity validation block
        try:
            quantityInput = int(input('Enter Quantity-->'))
            if quantityInput > idArray[idInput][0]:
                print('Entered Quantity exceeds available stock.')
                continue

        except ValueError:
            print('Wrong char type entered.')
            continue

        # Existing ID verification block
        if idInput in productQueue:
            productQueue[idInput][0] += quantityInput
        else:
            productQueue[idInput] = [quantityInput, idArray[idInput][1], idArray[idInput][2]]

        idArray[idInput][0] -= quantityInput

    # Attaining other information
    sqlCursor.execute('SELECT c_id FROM c_data')
    retrieveSet = sqlCursor.fetchall()
    cidArray = [x[0] for x in retrieveSet]
    while True:
        cidInput = input('\nEnter customer ID if any-->')
        if cidInput in cidArray:
            productQueue['c_id'] = cidInput
        elif not cidInput:
            print('Proceeding without customer ID.')
            break
        else:
            cidCheck = input('Entered customer ID is not valid.\nEnter r to try again-->')
            if cidCheck == 'r':
                continue
            else:
                print('Proceeding without customer ID.')
                break

    # Generating s_id
    while True:
        s_id = str(random.randint(10000, 99999))
        if s_id in cidArray:
            continue
        else:
            break

    # Creating a storage for bill
    # billOut = open(r'.\obj\bill.obj', 'a+')
