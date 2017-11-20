Author: Eric Moriyasu
Description: A financial program that tracks of multiple users and currencies
-Written in Python 3

*Requires all files to be in the same directory
-main.py
-financialCalcFunctions.py
-currency.db

uses sqlite database and uses sqlite3 module, which is part of standard Python library since Python 2.5

To start the program navigate to the directory where all the files are placed and type
"python main.py"

With in the program, commands are:
-exit
-help
-MAINT
-currencyList
-userList
-transaction

details of the functions will be shown with the "help" command.

The program uses the dollar as the gold standard. When using the MAINT function to insert currency
data, the program will ask for the currency in dollar value. When using the userList command to
display list of all users, will show their balance in dollar value

**Some important functions calls are:**
MAINT read currencyCode1 currencyCode2
(ex: MAINT read USD EUR) - this shows the conversion rate between US dollar and the Euro

MAINT write currencyName currencyCode valueInDollar
(ex: MAINT write money MON 2) - this creates a new currency named "money", 1 unit of money is worth $2

transaction transaction userName value currencyCode
(ex: John 5 USD) - adds $5 to John's account
Transaction can also take negative numbers to subtract from the balance.

**example commands:

*MAINT read USD EUR
-"Conversion rate between Dollar and Euro is 0.85"

*MAINT write money MON 1
-adds in a currency named "money" with the code "MON" and its dollar value is 1

*transaction user1 5.1 MON
-"user user1 now has $10.1 in balance"