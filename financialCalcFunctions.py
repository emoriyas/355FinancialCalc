# Filename: financialCalcFunctions.py
# Author: Eric Moriyasu
# Description: Includes functions to be called by main.py

import sqlite3
from math import floor
import re

# Function maint
# Parameter cmd (array) : Commands separated by spaces
# Parameter c : Database connection
#
# Description: Either reads the conversion rate between two currencies or create a new currency
#				calls either the maintRead function or the maintWrite function
def maint(cmd, c):
	if(len(cmd) < 2):
		inputCmd = input("Would you like to read or write? : ")
		if(inputCmd == "read"):
			cmd.append("read")
			inputCmd = input("Pleaes input two currency codes (example: USD EUR): ")
			inputCmd = inputCmd.split(" ")
			if(len(inputCmd) == 2):
				cmd.extend(inputCmd)
				maintRead(cmd, c)
			else:
				print("Invalid input, please type in two currency codes")
		elif(inputCmd == "write"):
			cmd.append("write")
			print("Pleaes input curency name, 3-letter currency code, and the dollar value of the currency")
			inputCmd = input("Example (Euro EUR 1.18): ")
			#print(inputCmd)
			inputCmd = inputCmd.split(" ")
			if(len(inputCmd) == 3):
				cmd.extend(inputCmd)
				maintWrite(cmd, c)
			else:
				print("Invalid input")
		else:
			print("Invalid Input, please type in \"read\" or \"write\"")
		#maint(cmd)
	else:
		if(cmd[1] == "read"):
			maintRead(cmd, c)
		elif(cmd[1] == "write"):
			maintWrite(cmd, c)
		else:
			print("Invalid parameters")

# Function maintRead
# Parameter cmd (array) : Commands separated by spaces
# Parameter c : Database connection
#
# Description: Rreads the conversion rate between two currencies
def maintRead(cmd, c):
	if(len(cmd) < 4):
		print("Missing data")
	else:
		query = "SELECT ca.cname, ca.dollarVal, cb.cname, cb.dollarVal FROM currency as ca "
		query = query + "LEFT JOIN currency as cb ON ca.ccode=\"" + cmd[2] + "\" AND cb.ccode=\"" + cmd[3] + "\" "
		query = query + "WHERE ca.ccode=\"" + cmd[2] + "\""
		#print(query)
		c.execute(query);
		stkdata = c.fetchall();

		if(len(stkdata) < 1):
			print("Currencies not found")
			return()

		row = stkdata[0]

		if(len(row) < 4):
			print("Currencies not found")
			return()
		elif(row[1] == None or row[3] == None):
			print("Currencies not found")
			return()

		arr = [1, cmd[2], cmd[3]]
		conv = conversion(arr, c)
		print("Conversion rate between " + row[0] + " and " + row[2] + " is " + str(conv))

# Function maintWrite
# Parameter cmd (array) : Commands separated by spaces
# Parameter c : Database connection
#
# Description: Creates a new currency
def maintWrite(cmd, c):
	#print(cmd)
	if(len(cmd) < 5):
		print("Invalid Input")
	elif(len(cmd[3]) != 3):
		print("Currency code must be three letter")
	else:
		query = "SELECT cid FROM currency WHERE ccode=\"" + cmd[3] +"\""
		c.execute(query);
		stkdata = c.fetchall();
		if(len(stkdata) > 0):
			print("Currency already exists")
		else:
			try:
				a = float(cmd[4])
				if (a <= 0):
					print("PLease input a positive float greater than 0")
					return()
			except:
				print("Please input a valid float value")
				return()
			try:
				query = "INSERT INTO currency(cname, ccode, dollarVal) VALUES (\"" + cmd[2] + "\", \"" + cmd[3] + "\", " + cmd[4] + ")"
				#print(query)
				c.execute(query);
			except:
				print("Invalid input")

# Function currencyList
# Parameter c : Database connection
#
# Description: prints a list of all currencies
def currencyList(c):
	query = "SELECT cname, ccode, dollarVal FROM currency"
	c.execute(query);
	stkdata = c.fetchall();
	print("------------------------------")
	print("Currency Name | Currency Code | Value in Dollar\n")
	for row in stkdata:
		print(row[0] + " | " + row[1] + " | " + str(row[2]))
	print("------------------------------")

# Function userList
# Parameter c : Database connection
#
# Description: prints a list of all users
def userList(c):
	query = "SELECT username, balance FROM users"
	c.execute(query);
	stkdata = c.fetchall();
	print("------------------------------")
	for row in stkdata:
		print("user " + row[0] + " has $" + str(row[1]) + " in account")
	print("------------------------------")

# Function transaction
# Parameter cmd (array) : Commands separated by spaces
# Parameter c : Database connection
#
# Description: Can increase or decrease the balance of a specified user. If currency is not given, assumes dollar
def transaction(cmd, c):
	query = ""
	num = 0;

	if(len(cmd) < 3):
		print("Invalid input")
		return "a"
	elif(len(cmd) == 3):
		cmd.append("USD")

#	try:
#		num = re.sub(r'[^0-9.]', '', cmd[2])
#		num = float(num)
#		conv = [num, cmd[3] , "USD"]
#		if(num == 0):
#			print("Invalid currency")
#			return()
		#num = float(cmd[2])
#	except:
#		print("Invalid input, please input a number")
#		return "a"

	num = re.sub(r'[^0-9.-]', '', cmd[2])
	try:
		num = float(num)
	except:
		print("Please input float value")
		return()
	conv = [num, cmd[3] , "USD"]
	num = conversion(conv, c)
	#if(num == 0):
	#	return()

	query = "SELECT uid, balance FROM users WHERE username = \"" + cmd[1] + "\""
	c.execute(query);
	stkdata = c.fetchall();
	if(len(stkdata) != 1):
		print("No user found")
	else:
		userData = stkdata[0]
		newBalance = userData[1] + num
		print("user " + cmd[1] + " now has $" + str(newBalance) + " in balance")
		query = "UPDATE users SET balance = " + str(newBalance) + " WHERE uid = " + str(userData[0])
		c.execute(query);


# Function conversion
# Parameter cmd (array) : Commands separated by spaces
# Parameter c : Database connection
#
# return conv (float) : converted value
#
# Description: converts currencies
def conversion(cmd, c):
	if(len(cmd) < 3):
		print("Missing data")
	else:
		query = "SELECT ca.cname, ca.dollarVal, cb.cname, cb.dollarVal FROM currency as ca "
		query = query + "LEFT JOIN currency as cb ON ca.ccode=\"" + cmd[1] + "\" AND cb.ccode=\"" + cmd[2] + "\" "
		query = query + "WHERE ca.ccode=\"" + cmd[1] + "\""
		#print(query)
		c.execute(query);
		stkdata = c.fetchall();

		if(len(stkdata) < 1):
			print("Currencies not found")
			return(-1)

		row = stkdata[0]

		if(len(row) < 4):
			print("Currencies not found")
			return(-1)
		elif(row[1] == None or row[3] == None):
			print("Currencies not found")
			return(-1)

		try:
			conv = (cmd[0] * row[1]) / row[3]
			conv = round(conv, 2)
		except:
			print("non-float value inserted")
			conv = 0;
		return(float(conv))


# Function add
# Parameter cmd (array) : Commands separated by spaces
# Parameter userData (array) : Holds user credentials
# Parameter c : Database connection
#
# Description: Adds a specified amount to the user's balance.
def add(cmd, userData, c): #ADD 5 USD
	query = ""
	num = 0;
	uid = userData[0]
	currBalance = 0;

	if(len(cmd) < 2):
		print("Invalid input")
		return "a"
	elif(len(cmd) == 2):
		cmd.append("USD")

	num = re.sub(r'[^0-9.]', '', cmd[1])

	try:
		num = float(num)
	except:
		print("Please input float value")
		return()
	conv = [num, cmd[2] , "USD"]
	num = conversion(conv, c)
	#if(num == 0):
	#	return()

	#get userbalance
	query = "SELECT uid, balance FROM users WHERE uid=" + str(userData[0])
	c.execute(query);
	stkdata = c.fetchall();
	if(len(stkdata) != 1):
		print("User not found")
		return()
	else:
		row = stkdata[0]
		currBalance = row[1]


	#userData = stkdata[0]
	newBalance = currBalance + num
	newBalance = round(newBalance, 2)
	userData[3] = newBalance
	print("You now have $" + str(newBalance) + " in balance") #Gives balance in dollar due to gold standard implimentation
	query = "UPDATE users SET balance = " + str(newBalance) + " WHERE uid = " + str(uid)
	c.execute(query);

# Function subtract
# Parameter cmd (array) : Commands separated by spaces
# Parameter userData (array) : Holds user credentials
# Parameter c : Database connection
#
# Description: Subtracts a specified amount from the user's balance.
def subtract(cmd, userData, c): #SUB 5 USD
	query = ""
	num = 0;
	uid = userData[0]
	currBalance = 0;

	if(len(cmd) < 2):
		print("Invalid input")
		return "a"
	elif(len(cmd) == 2):
		cmd.append("USD")

	num = re.sub(r'[^0-9.]', '', cmd[1])

	try:
		num = float(num)
	except:
		print("Please input float value")
		return()
	conv = [num, cmd[2] , "USD"]
	num = conversion(conv, c) #converts
	#if(num == 0):
	#	return()

	#get userbalance
	query = "SELECT uid, balance FROM users WHERE uid=" + str(userData[0])
	c.execute(query);
	stkdata = c.fetchall();
	if(len(stkdata) != 1):
		print("User not found")
		return()
	else:
		row = stkdata[0]
		currBalance = row[1]

	#userData = stkdata[0]
	newBalance = currBalance - num
	newBalance = round(newBalance, 2)
	userData[3] = newBalance
	print("You now have $" + str(newBalance) + " in balance") #Gives balance in dollar due to gold standard implimentation
	query = "UPDATE users SET balance =" + str(newBalance) + " WHERE uid = " + str(uid)
	c.execute(query);


# Function wire
# Parameter cmd (array) : Commands separated by spaces
# Parameter c : Database connection
#
# Description: Transfers funds from one user to another
# WIRE user1 user2 amt currency
def wire(cmd, c):
	#print(cmd)
	query = ""
	num = 0;
	user1 = cmd[1]
	uid1 = -1
	user1Balance = 0.0
	user2 = cmd[2]
	uid2 = -1
	user2Balance = 0.0

	if(len(cmd) < 4):
		print("Invalid input")
		return "a"
	elif(len(cmd) == 4):
		cmd.append("USD")

	num = re.sub(r'[^0-9.-]', '', cmd[3])
	try:
		num = float(num)
	except:
		print("Please input float value")
	conv = [num, cmd[4] , "USD"]
	num = conversion(conv, c)
	if(num == 0):
		return()

#look bottom
	query = "SELECT uid, balance FROM users WHERE username = \"" + str(cmd[1]) + "\""
	c.execute(query);
	stkdata = c.fetchall();
	if(len(stkdata) != 1):
		print("User not found")
		return()
	else:
		row = stkdata[0]
		uid1 = row[0]
		user1Balance = row[1]

	query = "SELECT uid, balance FROM users WHERE username = \"" + str(cmd[2]) + "\""
	c.execute(query);
	stkdata = c.fetchall();
	if(len(stkdata) != 1):
		print("User not found")
		return()
	else:
		row = stkdata[0]
		uid2 = row[0]
		user2Balance = row[1]
		#newBalance = userData[1] + num
		#print("user " + cmd[1] + " now has $" + str(newBalance) + " in balance")
		#query = "UPDATE users SET balance = " + str(newBalance) + " WHERE uid = " + str(userData[0])
		#c.execute(query);

	user1Balance = user1Balance - num
	user1Balance = round(user1Balance, 2)
	user2Balance = user2Balance + num
	user2Balance = round(user2Balance, 2)
	print("user " + user1 + " now has $" + str(user1Balance) + " in balance") #Gives balance in dollar due to gold standard implimentation
	print("user " + user2 + " now has $" + str(user2Balance) + " in balance") #Gives balance in dollar due to gold standard implimentation

	query = "UPDATE users SET balance = " + str(user1Balance) + " WHERE uid = " + str(uid1)
	c.execute(query);
	query = "UPDATE users SET balance = " + str(user2Balance) + " WHERE uid = " + str(uid2)
	c.execute(query);
