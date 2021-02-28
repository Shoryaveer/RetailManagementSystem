import random


def newCustomer(sqlConnector):
    """ Creates a new customer entry in database. """
    # obtaining required fields
    cName = input('Enter Name-->')
    cAddress = input('Enter Address-->')
    cMobile = input('Enter Mobile number-->')

    # Generating c_id
    sqlCursor = sqlConnector.cursor()
    sqlCursor.execute('SELECT c_id FROM c_data')
    retrieveSet = sqlCursor.fetchall()
    cidArray = [x[0] for x in retrieveSet]
    while True:
        c_id = str(random.randint(10000, 99999))
        if c_id in cidArray:
            continue
        else:
            break

    sqlCursor.execute(f"INSERT INTO c_data(c_id, c_name, c_address, c_mobile) \
                      VALUES('{c_id}', '{cName}', '{cAddress}', '{cMobile}')")
    sqlConnector.commit()


def viewCustomer(sqlConnector, c_id):
    """ gets all the details of customer linked to c_id.
    if c_id is 'all' then prints all the customers and their data."""

    sqlCursor = sqlConnector.cursor()
    sqlCursor.execute('SELECT c_id, c_name, c_address, c_mobile FROM c_data')
    retrieveSet = sqlCursor.fetchall()

    print('Customer ID ', 'Name'.ljust(30), 'Address'.ljust(40), 'Mobile')
    for c_id_, cName, cAddress, cMobile in retrieveSet:
        if c_id.lower() == 'all':
            print(c_id_.rjust(11), '  ', cName.ljust(31), cAddress.ljust(41), cMobile, sep='')
        elif c_id == c_id_:
            print(c_id_.rjust(11), '  ', cName.ljust(31), cAddress.ljust(41), cMobile, sep='')
