'''RetailManagementSystem
this would used in grocery stores and small business owners who want to manage following
*inventory
*sales
*dealers
*customers '''

''' this is the main file used to operate multiple functionalities '''

import mod.dumpDB
import mysql.connector

dpDB = input('Do you want to install test Database? (y/n)')

uName = input('Enter Username-->')
uPass = input('Enter Password-->')
print('\b')



if dpDB.lower() == 'y':
    
    pass

elif dpDB.lower() == 'n':
    print('No Database will be installed.')

