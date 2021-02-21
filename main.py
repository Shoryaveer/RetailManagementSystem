"""RetailManagementSystem
this would used in grocery stores and small business owners who want to manage following
*inventory
*sales
*dealers
*customers

this is the main file used to operate multiple functionalities """

import mod.dumpDB
import mysql.connector


def sqlLogin():
    """ Login Procedure """
    global uName
    global uPass
    uName = input('Enter Username-->')
    uPass = input('Enter Password-->')
    a = ' ' * (len(uPass) + 17) + '\n'  # count number of char. in pass
    print("\033[F" + a, end="", flush=True)  # \033[F is ANSI to the cursor one line up and added spaces to remove password


sqlLogin()  # function call to mysql login

# Database selection/insrtallation procedure
dpDB = input('Do you want to install test Database? (y/n)')

if dpDB.lower() == 'y':

    pass

elif dpDB.lower() == 'n':
    print('No Database will be installed.')
    dbName = input('Enter database name-->')

SQLconnector = mysql.connector.connect(host='localhost', username=uName, password=uPass, database=dbName)

if SQLconnector.is_connected():
    print('connected')
else:
    print('Error in connecting. Please try again.')
    sqlLogin()
