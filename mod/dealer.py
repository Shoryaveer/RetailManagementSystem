import random


def newDealer(sqlConnector):
    """ Creates a new customer entry in database. """
    # obtaining required fields
    dName = input('Enter Name-->')
    dAddress = input('Enter Address-->')
    dMobile = input('Enter Mobile number-->')

    # Generating d_id
    sqlCursor = sqlConnector.cursor()
    sqlCursor.execute('SELECT d_id FROM dealer_data')
    retrieveSet = sqlCursor.fetchall()
    didArray = [x[0] for x in retrieveSet]
    while True:
        d_id = str(random.randint(100, 999))
        if d_id in didArray:
            continue
        else:
            break

    sqlCursor.execute(f"INSERT INTO dealer_data(d_id, d_name, d_address, d_mobile) \
                      VALUES('{d_id}', '{dName}', '{dAddress}', '{dMobile}')")
    sqlConnector.commit()
    viewDealer(sqlConnector, d_id)
    print('Dealer added.')


def viewDealer(sqlConnector, d_id):
    """ gets all the details of customer linked to d_id.
    if d_id is 'all' then prints all the dealer and their data."""

    sqlCursor = sqlConnector.cursor()
    sqlCursor.execute('SELECT d_id, d_name, d_address, d_mobile FROM dealer_data')
    retrieveSet = sqlCursor.fetchall()

    print('Dealer ID ', 'Name'.ljust(30), 'Address'.ljust(40), 'Mobile')
    for d_id_, dName, dAddress, dMobile in retrieveSet:
        if d_id.lower() == 'all':
            print(d_id_.ljust(10), dName.ljust(30), dAddress.ljust(40), dMobile)
        elif d_id == d_id_:
            print(d_id_.ljust(10), dName.ljust(30), dAddress.ljust(40), dMobile)


if __name__ == '__main__':
    import mysql.connector
    myconn = mysql.connector.connect(host="localhost", user='root', password='admin', database='tt')
    # newtransaction(myconn)
    # newDealer(myconn)
    viewDealer(myconn, 'all')
