import random


def newProduct(sqlConnector):
    prod_name = input("Product Name-->")
    prod_quantity = int(input("Quantity-->"))
    dealer_id = input("Dealer id-->")
    prod_price = float(input("Selling Price-->"))
    prod_expiry = input("Expire Date(yyyy-mm-dd)-->")
    cursor = sqlConnector.cursor()

    # Generating prod_id
    cursor.execute('SELECT p_id FROM stock')
    retrieveSet = cursor.fetchall()
    prodidArray = [x[0] for x in retrieveSet]
    while True:
        prod_id = str(random.randint(10, 99))
        if prod_id in prodidArray:
            continue
        else:
            break

    query = f"INSERT INTO stock(p_id,p_name,p_quantity,d_id,p_price,p_expiry) VALUES\
        ('{prod_id}', '{prod_name}', {prod_quantity}, '{dealer_id}', {prod_price}, {prod_expire})"
    cursor.execute(query)
    sqlConnector.commit()


def editProduct(sqlConnector):
    cursor = sqlConnector.cursor()

    viewProduct(sqlConnector, 'all')
    p_id = input("Enter the Product ID you want to edit-->")

    prod_name = input("Product Name-->")
    prod_quantity = int(input("Quantity-->"))
    dealer_id = input("Dealer ID -->")
    prod_price = float(input("Price-->"))
    prod_expiry = input("Expire Date(yyyy-mm-dd)-->")

    query = f"UPDATE stock SET \
        d_id='{dealer_id}', p_name='{prod_name}', p_quantity={prod_quantity}, p_price={prod_price}, p_expire='{prod_expiry}' \
        WHERE p_id='{p_id}'"
    cursor.execute(query)
    sqlConnector.commit()


def viewProduct(sqlConnector, p_id_):
    sqlCursor = sqlConnector.cursor()
    sqlCursor.execute("SELECT p_id, p_name, p_quantity, p_price FROM stock")  # Receiving p_id and p_name for selection
    retrieveSet = sqlCursor.fetchall()
    print('Product ID'.ljust(14), 'Product Name'.ljust(33), 'Quantity Available', sep='')  # Displaying hedings
    for p_id, p_name, p_quantity, p_price in retrieveSet:
        if p_id == 'all':
            print(p_id.rjust(10) + '    ', p_name.ljust(33), p_quantity, sep='')  # displaying the ID Names and Quantities
        elif p_id == p_id_:
            print(p_id.rjust(10) + '    ', p_name.ljust(33), p_quantity, sep='')
