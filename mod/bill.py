""" This module helps manage bill for user. """
import pickle
import random
import os
import mysql.connector


class Bill:
    """ Contains bill creation and modification methods """

    def __init__(self, sqlConnector):
        self.productQueue = {}
        self.c_id = 'NULL'
        self.s_id = None
        self.sqlConnector = sqlConnector
        self.sqlCursor = sqlConnector.cursor()

    def getProductQueue(self):

        # checking database connection
        if not self.sqlConnector.is_connected():
            print('No Connection.')
            return

        self.sqlCursor.execute("SELECT p_id, p_name, p_quantity, p_price FROM stock")  # Receiving p_id and p_name for selection
        retrieveSet = self.sqlCursor.fetchall()

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
        if not productQueue:
            print('No bill created')
            productQueue = -1
        self.productQueue = productQueue

    def viewBill(self, showID='n'):
        """ This will show the bill for the required sales ID. """

        # checking database connection
        if not self.sqlConnector.is_connected():
            print('No Connection.')
            return

        if not self.s_id:
            print('Sales ID does not exist.')
            return

        print('\nSales ID : ', self.s_id, '\nCustomer ID : ', self.c_id)

        totalPrice = 0
        for productKeys in self.productQueue.keys():
            p_quantity, p_price, p_name = self.productQueue[productKeys]
            if showID == 'y':
                print('Product ID    ', 'Product Name'.ljust(33), 'Product Quantity   ', 'Total Price', sep='')
                print(productKeys.rjust(10) + '    ', p_name.ljust(33), str(p_quantity).ljust(19), p_quantity * p_price, sep='')
            else:
                print('Product Name'.ljust(33), 'Product Quantity   ', 'Total Price', sep='')
                print(p_name.ljust(33), str(p_quantity).ljust(19), p_quantity * p_price, sep='')
        if showID == 'y':
            totalPrice += p_quantity * p_price
            print('Grand Total : '.rjust(66), totalPrice, sep='')
        else:
            totalPrice += p_quantity * p_price
            print('Grand Total : '.rjust(52), totalPrice, sep='')

    def alterBill(self, display='d'):
        """ This is used to alter bill which exist in file. """

        # checking database connection
        if not self.sqlConnector.is_connected():
            print('No Connection.')
            return

        # displaying the bill
        if display == 'nd':
            pass
        else:
            self.viewBill('y')

        # taking input for the product ID and edit it
        print('Enter q on completion.')
        while True:
            idInput = input('Enter Product ID to edit-->')
            if idInput == 'q':
                break
            elif idInput not in self.productQueue.keys():
                print('Key error no further changes will made.')
                break
            else:
                print('\n1. Delete\n2. Edit All\n3. Edit Customer ID')
                alterChoice = input('Select a no. from above list-->')
                if alterChoice == '1':
                    billIn = open(r'.\obj\bill.obj', 'rb')
                    billOut = open(r'.\obj\temp', 'wb')
                    try:
                        billIn.seek(0)
                        while True:
                            billObj = pickle.load(billIn)
                            if billObj.s_id == self.s_id:
                                billObj.productQueue.pop(idInput)
                            pickle.dump(billObj, billOut)

                    except EOFError:
                        billIn.close()
                        billOut.close()
                        os.remove(r'.\obj\bill.obj')
                        os.rename(r'.\obj\temp', r'.\obj\bill.obj')
                        print(f'Product ID {idInput} deleted successfully.')

                elif alterChoice == '2':
                    billIn = open(r'.\obj\bill.obj', 'rb')
                    billOut = open(r'.\obj\temp', 'wb')
                    try:
                        billIn.seek(0)
                        while True:
                            billObj = pickle.load(billIn)
                            if billObj.s_id == self.s_id:
                                billObj.productQueue.update(self.productQueue)
                            pickle.dump(billObj, billOut)

                    except EOFError:
                        billIn.close()
                        billOut.close()
                        os.remove(r'.\obj\bill.obj')
                        os.rename(r'.\obj\temp', r'.\obj\bill.obj')
                        print('Product list updated successfully.')

                elif alterChoice == '3':
                    self.sqlCursor.execute('SELECT c_id FROM c_data')
                    retrieveSet = self.sqlCursor.fetchall()
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
                            billObj = pickle.load(billIn)
                            if billObj.s_id == self.s_id:
                                billObj.c_id = cidInput
                            pickle.dump(billObj, billOut)

                    except EOFError:
                        billIn.close()
                        billOut.close()
                        os.remove(r'.\obj\bill.obj')
                        os.rename(r'.\obj\temp', r'.\obj\bill.obj')
                        print('Product list updated successfully.')

    def createBill(self):
        self.getProductQueue()
        if self.productQueue == -1:
            return

        # Attaining c_id
        self.sqlCursor.execute('SELECT c_id FROM c_data')
        retrieveSet = self.sqlCursor.fetchall()
        cidArray = [x[0] for x in retrieveSet]
        while True:
            cidInput = input('\nEnter customer ID if any-->')
            if cidInput in cidArray:
                self.c_id = cidInput
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

        # Generating s_id
        self.sqlCursor.execute('SELECT s_id FROM sales')
        retrieveSet = self.sqlCursor.fetchall()
        sidArray = [x[0] for x in retrieveSet]
        while True:
            s_id = str(random.randint(10000, 99999))
            if s_id in sidArray:
                continue
            else:
                break
        self.s_id = s_id

        # Storing Bill in file and making entry in DB
        billOut = open(r'.\obj\bill.obj', 'ab+')
        print(type(self))
        pickle.dump(self, billOut)
        billOut.close()
        return
        self.sqlCursor.execute(f"INSERT INTO sales(c_id, s_id) VALUES('{self.c_id}', '{self.s_id}')")
        self.sqlConnector.commit()

        self.viewBill()

        # Bill finalisation and alteration
        alterCheck = input('\nDo you want to change bill(y/n)-->')
        if alterCheck.lower() == 'y':
            self.alterBill('nd')  # nd stands for no display of bill
        elif alterCheck.lower() == 'n':
            print('\nNo alterations made. Bill will be saved')
        else:
            print('\nWrong input. Bill will be saved.')


def getBillObj(s_id):
    billIn = open(r'.\obj\bill.obj', 'rb')
    billIn.seek(0)
    while True:
        billObj = pickle.load(billIn)
        if billObj.s_id == s_id:
            return billObj
    billIn.close()
    return
