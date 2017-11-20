# Filename: main.py
# Author: Eric Moriyasu
# Description: A financial program that tracks of multiple users and currencies
# -Written in Python 3
# -Requires currency.db and financialCalcFunctions.py file in the same directory
import sqlite3
import financialCalcFunctions as func
import financialCalcUserFunctions as userFunc
import os

if not os.path.isfile("currency.db"):
	print("Database not found")
	exit()
conn = sqlite3.connect('currency.db');
c = conn.cursor(); #Connection to sqlite database

#[uid, permissions, username, balance]
userData = [-1, -1, "", -1.1]


running = 1;
#loggedIn = 0;

#Main interface of the program, promts the user for an input. Terminates of the user types "exit"
print("Welcome to Financial Calculator. This program allows you to keep track of multiple users")
print("and change their balance with different currencies")
print("------------------------------")

while(userData[0] == -1):
	print("You must log in to use this program")
	username = input('Enter username: ')
	password = input('Enter password: ')
	userData = userFunc.login(username, password, c)

print("------------------------------")
print("Welcome " + userData[2])
print("------------------------------")
#print(userData)

while(running == 1):
	inputCmd = input('Enter command: ')
	if(inputCmd == "exit"):
		running = 0
	elif(inputCmd == "help"):
		print("------------------------------")
		print("List of commands:\n")
		print("exit - exit the program\n")
		print("help - display list of commands\n")
		print("MAINT - Allow currency conversion data to be entered (or read in)")
		print("parameters: (MAINT read currencyCode1 currencyCode2) OR (MAINT write currencyName currencyCode valueInDollar)")
		print("OR call MAINT by itself\n")
		print("currencyList - display list of currencies\n")
		print("userList - display list of users\n")
		print("transaction - do a transaction")
		print("parameters: transaction userName value currencyCode - Currency Code is optional, will assume dollar if unspecified\n")
		print("ADD - add to balance")
		print("parameters: ammount, currencyCode - Currency Code is optional, will assume dollar if unspecified\n")
		print("SUB - subtract from balance")
		print("parameters: ammount, currencyCode - Currency Code is optional, will assume dollar if unspecified\n")
		print("WIRETO - Do a wire transfer to another user")
		print("parameters: username ammount currencyCode - currency Code is optional, will assume dollar if unspecified\n")

		if(userData[1] == 7):
			print("")
			print("ADDUSER - add a user")
			print("username password permission balance - assume balance is 0 if none is given\n")
			print("DELUSER - remove a user")
			print("username\n")
			print("WIRE - Do a wire transfer from user1 to user2")
			print("parameters: username1 username2 ammount currencyCode - currency Code is optional, will assume dollar if unspecified\n")
			#ADDUSER username, password, permission, balance
		print("------------------------------")
	else:
		cmd = inputCmd.split(" ")
		if(len(cmd) < 1):
			print("Invalid Input")
		elif(cmd[0] == "MAINT"):
			func.maint(cmd, c)
		elif(cmd[0] == "currencyList"):
			func.currencyList(c)
		elif(cmd[0] == "userList"):
			func.userList(c)
		elif(cmd[0] == "transaction"):
			func.transaction(cmd, c)
		elif(cmd[0] == "ADD"):
			func.add(cmd, userData, c)
		elif(cmd[0] == "SUB"):
			func.subtract(cmd, userData, c)
		elif(cmd[0] == "WIRETO"):
			cmd.insert(1, userData[2])
			func.wire(cmd, c)
		elif(cmd[0] == "WIRE" and userData[1] == 7):
			func.wire(cmd, c)
		elif(cmd[0] == "ADDUSER" and userData[1] == 7):
			userFunc.addUser(cmd, c)
		elif(cmd[0] == "DELUSER" and userData[1] == 7):
			userFunc.deleteUser(cmd, c)
		else:
			print("Invalid input, please type \"help\" command to get the list of commands")

conn.commit()