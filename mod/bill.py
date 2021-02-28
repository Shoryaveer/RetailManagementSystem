""" This module helps manage bill for user. """
import random
import pickle
import os
# move bin to database folder


def createBill(sqlConnector):
    """ Bill Creation procedure """

    sqlCursor = sqlConnector.cursor()

    productQueue = getProductQueue(sqlCursor)
    # productQueue = {'c_id': '', 's_id': '', 'co': percentage, 'p_id': [p_quantity, p_price, p_name]...}

    # Attaining other information
    sqlCursor.execute('SELECT c_id FROM c_data')
    retrieveSet = sqlCursor.fetchall()
    cidArray = [x[0] for x in retrieveSet]
    while True:
        cidInput = input('\nEnter customer ID if any-->')
        if cidInput in cidArray:
            productQueue['c_id'] = cidInput
            break
        elif not cidInput:
            print('Proceeding without customer ID.')
            productQueue['c_id'] = 'NULL'
            break
        else:
            cidCheck = input('Entered customer ID is not valid.\nEnter r to try again-->')
            if cidCheck == 'r':
                continue
            else:
                print('Proceeding without customer ID.')
                productQueue['c_id'] = 'NULL'
                break

    # Generating s_id
    sqlCursor.execute('SELECT s_id FROM sales')
    retrieveSet = sqlCursor.fetchall()
    sidArray = [x[0] for x in retrieveSet]
    while True:
        s_id = str(random.randint(10000, 99999))
        if s_id in sidArray:
            continue
        else:
            break

    # Adding s_id, c_id to productQueue
    productQueue['s_id'] = s_id

    # Adding coupons to bill
    sqlCursor.execute(f"SELECT percentage FROM coupons \
        WHERE expire_date>CURDATE() AND min_prod<={len(productQueue) - 2}")
    retrieveSet = sqlCursor.fetchall()
    if retrieveSet:
        coCheck = input('Coupon available do you want to apply coupon(y/n)-->')
        if coCheck.lower() == 'y':
            productQueue['co'] = max(retrieveSet[0])
        else:
            print('No coupons added.')
            productQueue['co'] = 0
    else:
        print('No coupons available.')
        productQueue['co'] = 0

    # Storing Bill in file and making entry in DB
    billOut = open(r'.\obj\bill.obj', 'ab+')
    pickle.dump(productQueue, billOut)
    sqlCursor.execute(f"INSERT INTO sales(c_id, s_id) VALUES('{productQueue['c_id']}', '{s_id}')")
    sqlConnector.commit()

    # Closing open files
    billOut.close()

    # Bill summary
    viewBill(s_id)

    # Bill finalisation and alteration
    alterCheck = input('\nDo you want to change bill(y/n)-->')
    if alterCheck.lower() == 'y':
        alterBill(s_id, sqlCursor, 'nd')  # nd stands for no display of bill
    elif alterCheck.lower() == 'n':
        print('\nNo alterations made. Bill will be saved')
    else:
        print('\nWrong input. Bill will be saved.')

    # Reducing stock quantities
    for p_id in productQueue:
        if p_id != 'c_id' and p_id != 's_id' and p_id != 'co':
            sqlCursor.execute(f"UPDATE stock SET p_quantity = p_quantity - {productQueue[p_id][0]} WHERE p_id = {p_id}")
            sqlConnector.commit()


def viewBill(s_id, showID='n'):
    """ This will show the bill for the required sales ID. """

    productQueue = getBill(s_id)
    if not productQueue:
        print('Sales ID does not exist.')
        return

    print('\nSales ID : ', s_id, '\nCustomer ID : ', productQueue['c_id'])

    totalPrice = 0
    n = 0
    for productKeys in productQueue.keys():
        if productKeys != 's_id' and productKeys != 'c_id' and productKeys != 'co':
            p_quantity, p_price, p_name = productQueue[productKeys]
            if n == 0:
                if showID == 'y':
                    print('Product ID    ', 'Product Name'.ljust(33), 'Product Quantity   ', 'Total Price', sep='')
                    print(productKeys.rjust(10) + '    ', p_name.ljust(33), str(p_quantity).ljust(19), p_quantity * p_price, sep='')
                    n = 1
                else:
                    print('Product Name'.ljust(33), 'Product Quantity   ', 'Total Price', sep='')
                    print(p_name.ljust(33), str(p_quantity).ljust(19), p_quantity * p_price, sep='')
                    n = 1
            else:
                if showID == 'y':
                    print(productKeys.rjust(10) + '    ', p_name.ljust(33), str(p_quantity).ljust(19), p_quantity * p_price, sep='')
                else:
                    print(p_name.ljust(33), str(p_quantity).ljust(19), p_quantity * p_price, sep='')
            totalPrice += p_quantity * p_price

    if productQueue['co']:
        totalPrice -= totalPrice * (productQueue['co'] * 0.01)
    if showID == 'y':
        print('Coupon Less : '.rjust(66), productQueue['co'], sep='')
        print('Grand Total : '.rjust(66), totalPrice, sep='')
    else:
        print('Coupon Less : '.rjust(52), productQueue['co'], sep='')
        print('Grand Total : '.rjust(52), totalPrice, sep='')


def getBill(s_id):
    billIn = open(r'.\obj\bill.obj', 'rb')

    # Impoting all sales dictionaries from file
    salesList = []
    saleIDs = []
    try:
        billIn.seek(0)
        while True:
            productDict = pickle.load(billIn)
            salesList.append(productDict)
            saleIDs.append(productDict['s_id'])

    except EOFError:
        billIn.close()

    if s_id in saleIDs:
        for productQueue in salesList:
            if productQueue['s_id'] == s_id:
                return productQueue
    else:
        return


def alterBill(s_id, sqlCursor, display='d'):
    """ This is used to alter bill which exist in file. """

    productQueue = getBill(s_id)
    if not productQueue:
        print(f'Sales id {s_id} does not exist.')
        return

    if display == 'nd':
        pass
    else:
        viewBill(s_id, 'y')

    print('Enter q on completion.')
    while True:
        idInput = input('Enter Product ID to edit-->')
        if idInput == 'q':
            break
        elif idInput not in productQueue.keys():
            print('Key error no further changes will made.')
            break
        else:
            print('\n1. Delete\n2. Edit\n3. Edit Customer ID')
            alterChoice = input('Select a no. from above list-->')
            if alterChoice == '1':
                billIn = open(r'.\obj\bill.obj', 'rb')
                billOut = open(r'.\obj\temp', 'wb')
                try:
                    billIn.seek(0)
                    while True:
                        productDict = pickle.load(billIn)
                        if productDict['s_id'] == s_id:
                            productDict.pop(idInput)
                        pickle.dump(productDict, billOut)

                except EOFError:
                    billIn.close()
                    billOut.close()
                    os.remove(r'.\obj\bill.obj')
                    os.rename(r'.\obj\temp', r'.\obj\bill.obj')
                    print(f'Product ID {idInput} deleted successfully.')

            elif alterChoice == '2':
                productQueue = getProductQueue(sqlCursor)
                billIn = open(r'.\obj\bill.obj', 'rb')
                billOut = open(r'.\obj\temp', 'wb')
                try:
                    billIn.seek(0)
                    while True:
                        productDict = pickle.load(billIn)
                        if productDict['s_id'] == s_id:
                            productDict.update(productQueue)
                        pickle.dump(productDict, billOut)

                except EOFError:
                    billIn.close()
                    billOut.close()
                    os.remove(r'.\obj\bill.obj')
                    os.rename(r'.\obj\temp', r'.\obj\bill.obj')
                    print('Product list updated successfully.')

            elif alterChoice == '3':
                sqlCursor.execute('SELECT c_id FROM c_data')
                retrieveSet = sqlCursor.fetchall()
                cidArray = [x[0] for x in retrieveSet]
                while True:
                    cidInput = input('\nEnter customer ID if any-->')
                    if cidInput in cidArray:
                        break
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

                billIn = open(r'.\obj\bill.obj', 'rb')
                billOut = open(r'.\obj\temp', 'wb')
                try:
                    billIn.seek(0)
                    while True:
                        productDict = pickle.load(billIn)
                        if productDict['s_id'] == s_id:
                            productDict['c_id'] = cidInput
                        pickle.dump(productDict, billOut)

                except EOFError:
                    billIn.close()
                    billOut.close()
                    os.remove(r'.\obj\bill.obj')
                    os.rename(r'.\obj\temp', r'.\obj\bill.obj')
                    print('Product list updated successfully.')


def getProductQueue(sqlCursor):
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

    return productQueue
