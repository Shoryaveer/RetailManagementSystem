import random


def newtransaction(myconn):

    cursor = myconn.cursor()

    d_id = (input("Enter Dealer id -->"))
    # Generating stock_id or st_id
    cursor.execute('SELECT st_id FROM stocktransac')
    retrieveSet = cursor.fetchall()
    stidArray = [x[0] for x in retrieveSet]
    while True:
        st_id = str(random.randint(1000, 9999))
        if st_id in stidArray:
            continue
        else:
            break

    query = f"INSERT INTO stocktransac(d_id, st_id) VALUES({d_id}, {st_id})"
    cursor.execute(query)
    myconn.commit()

    print('\nEnter product details')
    productDetails = getProductDetails(cursor)
    for p_id in productDetails:
        quantity = productDetails[p_id][0]
        cp = productDetails[p_id][1]
        exp_date = productDetails[p_id][2]
        cursor.execute(f'INSERT INTO stocktransac2(p_id, p_cp, st_id, quantity, exp_date) \
        VALUES({p_id}, {cp}, {st_id}, {quantity}, "{exp_date}")')
        cursor.execute(f"UPDATE stock SET p_quantity=p_quantity+{quantity}, p_expire='{exp_date}' WHERE p_id='{p_id}' ")
    myconn.commit()
    print('New Transaction Created.')


def viewTransaction(sqlCursor):

    sqlCursor.execute('SELECT d_id, st_id, transac_date FROM stocktransac')
    retrieveSet = sqlCursor.fetchall()
    idArray = []
    print('Dealer ID', 'Stock ID', 'Transaction Date', sep=' ')  # Displaying hedings
    for d_id, st_id, transac_date in retrieveSet:
        print(d_id.ljust(10), st_id.ljust(9), transac_date, sep='')
        idArray.append(st_id)
    idInput = input('Enter Stock ID-->')
    sqlCursor.execute(f'SELECT p_id, p_cp, quantity, exp_date FROM stocktransac2 WHERE st_id={idInput}')
    retrieveSet = sqlCursor.fetchall()
    print('Product ID', 'Product CP', 'Quantity', 'Expiry Date', sep=' ')  # Displaying hedings
    for p_id, p_cp, quantity, exp_date in retrieveSet:
        print(p_id.ljust(11), str(p_cp).ljust(11), str(quantity).ljust(9), exp_date, sep='')


def getProductDetails(sqlCursor):
    sqlCursor.execute("SELECT p_id, p_name, p_quantity FROM stock")  # Receiving p_id and p_name for selection
    retrieveSet = sqlCursor.fetchall()
    idArray = {}  # Dictionary created to store ID(s) , names, quantities of product {'p_id': [p_quantity, p_name]}
    print('Product ID'.ljust(14), 'Product Name'.ljust(33), 'Quantity Available', sep='')  # Displaying hedings
    for p_id, p_name, p_quantity in retrieveSet:
        print(p_id.rjust(10) + '    ', p_name.ljust(33), p_quantity, sep='')  # displaying the ID Names and Quantities
        idArray[p_id] = [p_quantity, p_name]  # Storing ID, Quantities and price

    # Attaining product ID and Quantities
    print('\nEnter q on completion')

    productQueue = {}  # Dictionary created to store selected product ID(s) {'p_id': [total quantity, cost price, expire date}
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
            costPrice = float(input('Enter Cost Price-->'))
        except ValueError:
            print('Wrong char type entered.')
            continue

        expire_date = input('Enter Expire Date(yyyy-mm-dd)-->')
        print(type(expire_date))

        # Existing ID verification block
        if idInput in productQueue:
            productQueue[idInput][0] += quantityInput
        else:
            productQueue[idInput] = [quantityInput, costPrice, expire_date]

    return productQueue


if __name__ == '__main__':
    import mysql.connector
    myconn = mysql.connector.connect(host="localhost", user='root', password='admin', database='tt')
    # newtransaction(myconn)
    viewTransaction(myconn.cursor())
