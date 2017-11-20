# Filename: financialCalcUserFunctions.py
# Author: Eric Moriyasu
# Description: Includes functions to be called by main.py

import hashlib
import sqlite3
import random
import string
import financialCalcFunctions as func

# Function createSalt
# Parameter length (int) : Length of the salt
#
# Description: Creates a random string of a specified length to be used as password salt
def createSalt(length):
	salt = "";
	for i in range (length):
		salt = salt + random.choice(string.ascii_letters + string.digits)
	#print("salt = " + salt)
	return(salt)

# Function login
# Parameter username (string) : username
# Parameter password (string) : password
# Parameter c : Database connection
#
# return ret (array) : user credentials.
#
# Description: Validates login. If validated returns user credentials in an array
def login(username, password, c):
	success = 0
	ret = [-1, -1, "", -1] #[uid, permissions, username, balance]
	salt = ""
	storedHash = "" #The hashed password stored in db
	hasher = hashlib.sha256()

	query = "SELECT uid, permissions, username, password, salt, balance FROM users WHERE username =\"" + username + "\""
	c.execute(query)
	stkdata = c.fetchall()

	if(len(stkdata) == 1):
		row = stkdata[0]
		salt = row[4]
		storedHash = row[3]
		password = password + salt
		password = password.encode("utf-8")
		hasher.update(password)
		password = hasher.hexdigest()
		#print("input:  " + password)
		#print("stored: " + storedHash)
		if(password == storedHash):
			print("Login successful")
			success = 1
			ret[0] = row[0]
			ret[1] = row[1]
			ret[2] = row[2]
			ret[3] = row[5]
	if(success == 0):
		print("Username/Password combination does not match")
	return(ret)



# Function addUser
# Parameter cmd (array) : Commands separated by spaces
# Parameter c : Database connection
#
# Description: Creates a user. Assume balance is 0 if balance is not given

#ADDUSER username, password, permission, balance
def addUser(cmd, c):
	#check if user exist (check uname and/or UID?)
	#ERROR If user already exists
	#create if user does not exist
	username = "";
	password = "";
	permission = 1;
	#balance = cmd[4];
	#print(len(cmd))

	if(len(cmd) < 4):
		print("Invalid Input")
		return()
	elif(len(cmd) == 4):
		balance = 0;
	elif(len(cmd) == 5):
		try:
			balance = float(cmd[4])
		except:
			print("Please input a float value for the user balance")
			return()
	else:
		print("Invalid Input");
		return()

	username = cmd[1]
	password = cmd[2]

	try:
		permission = int(cmd[3])
	except:
		"Please input an integer for user permission"

	query = "SELECT uid, username FROM users"
	c.execute(query)
	stkdata = c.fetchall()
	for row in stkdata:
		if(row[1] == username):
			print("username \"" + username + "\" already exists")
			return()
	salt = createSalt(10)
	password = password + salt
	sha256Hash = hashlib.sha256()
	password = password.encode("utf-8")
	sha256Hash.update(password)
	hashedPassword = sha256Hash.hexdigest()

	#INSERT INTO users VALUES(0, 7, "admin", "1234", "salt" 1337);
	query = "INSERT INTO users (username, password, permissions, salt, balance) "
	query = query + "VALUES ( \"" + str(username) + "\", \"" + hashedPassword + "\", " + str(permission) + ", \"" + salt + "\", " + str(balance) + ")"
	#print(query)
	c.execute(query)
	print("User added")

# Function deleteUser
# Parameter cmd (array) : Commands separated by spaces
# Parameter c : Database connection
#
# Description: Deletes a user
#DELUSER UID
def deleteUser(cmd, c):
	#check if user exists
	#ERROR if user exists
	if(len(cmd) < 2):
		print("Missing Data")
	else:
		uid = cmd[1]
		#query = "SELECT uid, username, balance FROM users WHERE uid =" + str(uid)
		query = "SELECT uid, username, balance, permissions FROM users WHERE username = \"" + str(uid) + "\""
		c.execute(query)
		stkdata = c.fetchall();
		#print(len(stkdata))
		if(len(stkdata) < 1): #if there are no user with the specified UID
			print("User not found")
			return()
		elif(len(stkdata) > 1): #if two users somehow share the same UID
			print("ERROR! DUPLICATE USERS")
			return()
		elif(stkdata[0][3] == 7):
			print("cannot remove administrators")
			return()
		else: #iff only one user is found
			row = stkdata[0]
			print("User Found!")
			print("Delete User UID: " + str(row[0]) + ", username: " + str(row[1]) + ", balance: " + str(row[2]) + "?")
			inputCmd = input("confirm? (y/n): ")
			if(inputCmd == "y" or inputCmd == "yes"):
				#query = "DELETE FROM users WHERE uid=" + str(uid)
				query = "DELETE FROM users WHERE username=\"" + str(uid) + "\""
				c.execute(query)
				print("User deleted")
			else:
				print("User delete canceled")

# Function getBalance
# Parameter cmd (array) : Commands separated by spaces
# Parameter userData (array) : Holds user credentials
# Parameter c : Database connection
#
# Description: Prints user balance. Assume USD if curency is not specified
def getBalance(cmd, userData, c): #BALANCE VAL currencyCode
	query = ""
	num = 0;
	uid = userData[0]
	currBalance = 0;

	if(len(cmd) < 1):
		print("Invalid input")
		return "a"
	elif(len(cmd) == 1):
		cmd.append("USD")

	#get userbalance
	query = "SELECT balance FROM users WHERE uid=" + str(userData[0])
	c.execute(query);
	stkdata = c.fetchall();
	if(len(stkdata) != 1):
		print("User not found")
		return()
	else:
		row = stkdata[0]
		balance = row[0]
		conv = [balance, "USD" , cmd[1]]
		balance = func.conversion(conv, c)
		if(balance != - 1):
			print("Your balance is " + str(balance) + " " + cmd[1])