
def alertSystem(sqlConnector):
    sqlCursor = sqlConnector.cursor()

    # Low quantity products output
    print("Low quantity Alerts")
    sqlCursor.execute("SELECT p_id, p_name, p_quantity, p_price FROM stock WHERE p_quantity<=7")  # Receiving p_id and p_name for selection
    retrieveSet = sqlCursor.fetchall()
    if retrieveSet:
        displaySet(retrieveSet)

    # Expired product alert
    print('Expired Products')
    sqlCursor.execute("SELECT p_id, p_name, p_quantity, p_price FROM stock WHERE p_expire<=CURDATE()")
    retrieveSet = sqlCursor.fetchall()
    displaySet(retrieveSet)


def displaySet(retrieveSet):
    print('Product ID'.ljust(14), 'Product Name'.ljust(33), 'Quantity Available', sep='')  # Displaying hedings
    for p_id, p_name, p_quantity, p_price in retrieveSet:
        print(p_id.rjust(10) + '    ', p_name.ljust(33), p_quantity, sep='')  # displaying the ID Names and Quantities
