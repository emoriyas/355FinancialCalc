Author: Eric Moriyasu
Description: A financial program that tracks of multiple users and currencies
-Written in Python 3

*Requires all files to be in the same directory
-main.py
-financialCalcFunctions.py
-financialCalcUserFunctions.py
-currency.db

uses sqlite database and uses sqlite3 module, which is part of standard Python library since Python 2.5

To start the program navigate to the directory where all the files are placed and type
"python main.py"

With in the program, commands are:
-exit
-help
-GETBALANCE
-MAINT
-currencyList
-userList
-transaction
-ADD
-SUB
-WIRETO
Admin commands:
ADDUSER
DELUSER
WIRE

details of the functions will be shown with the "help" command.

The program uses the dollar as the gold standard. When using the MAINT function to insert currency
data, the program will ask for the currency in dollar value. When using the userList command to
display list of all users, will show their balance in dollar value

**Some important functions calls are:**
MAINT read currencyCode1 currencyCode2
(ex: MAINT read USD EUR) - this shows the conversion rate between US dollar and the Euro

MAINT write currencyName currencyCode valueInDollar
(ex: MAINT write money MON 2) - this creates a new currency named "money", 1 unit of money is worth $2

transaction userName value currencyCode
(ex: transaction John 5 USD) - adds $5 to John's account
Transaction can also take negative numbers to subtract from the balance.

ADD amount currencyCode
(ex: ADD 5 USD) - adds $5 to your account.
Unlike transaction, ADD cannot take negative numbers

SUB amount currencyCode
(ex: SUB 5 USD) - subtracts $5 from your account.
Unlike transaction, SUB cannot take negative numbers

WIRETO username amount currencyCode
(ex: WIRETO user 5 USD) - sends $5 to user

WIRE user1 user2 amount currency
(ex: WIRE user1 user2 5 USD) - sends $5 from user1's account to user2

ADDUSER username password permission balance
(ex: ADDUSER user1 password 1 0) - creates user1 with password of "password" and permission of 1: an average user with
				   $0 in account

DELUSER username
(ex: DELUSER user1) - removes user1

