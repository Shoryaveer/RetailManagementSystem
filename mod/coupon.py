import random


def newCoupon(sqlConnector):
    min_prod = int(input("Enter the minimum product-->"))
    percentage = int(input("Enter discount percentage-->"))
    expire_date = input("Enter the expiry date (yyyy-mm-dd)-->")

    cursor = sqlConnector.cursor()

    # Generating co_id
    cursor.execute('SELECT co_id FROM coupons')
    retrieveSet = cursor.fetchall()
    coidArray = [x[0] for x in retrieveSet]
    while True:
        co_id = str(random.randint(10000000, 99999999))
        if co_id in coidArray:
            continue
        else:
            break

    query = f"INSERT INTO coupons(co_id,expire_date,min_prod,percentage) VALUES('{co_id}',{expire_date},{min_prod},{percentage})"
    cursor.execute(query)
    sqlConnector.commit()
    print('New coupon added.')
    viewCoupon(sqlConnector)


def editCoupon(sqlConnector):
    cursor = sqlConnector.cursor()
    coidInput = input("Enter the co_id you want to edit-->")
    expiry_date = input("Enter the expiry date (yyyy-mm-dd)-->")
    min_prod = int(input("Enter the minimum product-->"))
    percentage = int(input("Enter discount percentage-->"))

    query = f"UPDATE coupons SET expiry_date={expiry_date}, min_prod={min_prod}, percentage={percentage} WHERE co_id={coidInput}"
    cursor.execute(query)
    sqlConnector.commit()
    viewCoupon(sqlConnector)


def deleteCoupon(sqlConnector):
    cursor = sqlConnector.cursor()
    viewCoupon(sqlConnector)
    coidInput = input("Enter the Coupon ID to delete-->")
    cursor.execute(f"DELETE FROM coupons WHERE co_id={coidInput}")
    sqlConnector.commit()
    viewCoupon(sqlConnector)


def viewCoupon(sqlConnector):
    cursor = sqlConnector.cursor()
    cursor.execute("select * from coupons")
    retrieveSet = cursor.fetchall()
    print('Coupon ID', 'Expire Date', 'Minimum Product', 'Percentage', sep='')  # Displaying hedings
    for co_id, expire_date, min_prod, percentage in retrieveSet:
        print(co_id.ljust(10), expire_date, str(min_prod).ljust(15), str(percentage), sep='')  # displaying the ID Names and Quantities
