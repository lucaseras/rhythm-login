"""
Lucas Eras Paiva, Zach Mines
COMP360, Professor Sebastian Zimmeck
Wesleyan University
Required file: users.txt (same folder, should be initially empty)
Summary: this code, written with python 3.0, is a login system that takes into consideration the rhythm of password input when authenticating the user. This rhythm is the interval between every letter inputted in the password. The user information is saved in the file users.txt in the form "username password intervals" per line. 
This code is not concerned with making sure that information is safely kept hidden. Rather, the goal with this file is to show how these typing intervals can be an extra layer of the security of login authentication.
"""


import sys
# installing readchar is required to run this code
# in terminal: pip3 install readchar
import readchar
import time
import platform

#*****#
# Main (initial) function
#*****#

def main():
	print("\n*****\nMain Menu\n*****")
	print("1: Create user account")
	print("2: Login")
	print("3: List accounts in memory")
	print("4: Quit")
	user_input = input()


	if user_input == "4":
		sys.exit()
	elif user_input == "1":
		create_user()
	elif user_input == "2":
		login()
	elif user_input == "3":
		listAccounts()
	else:
		print("Enter a valid number")
		main()

#*****#
# Helper functions
#*****#

### Checks if two given rhythms are similar enough (according to the errorMargin value)
def authenticaterhythms(l1, l2):

	errorMargin = 0.15

	i = 0
	while i < len(l1):
		if not ((l1[i] - errorMargin < l2[i]) and (l2[i] < l1[i] + errorMargin)):
			return False
		i += 1
	return True

"""
Helper function that gets the password being inputted as well as the time in-between keystrokes,
returning a tuple (intervals, inputString) where intervals is a float list of the keystroke intervals
and inputString is the final password
"""
def getIntervals():
	intervals = []
	inputString = ""
	input_key = ""

	while input_key != readchar.key.ENTER:
		# Getting time between key presses
		startingTime = time.time()
		if platform.system() == 'Darwin':
			input_key = readchar.readchar()
		elif platform.system() == 'Windows':
			input_key = readchar.readkey()
		print("*", sep=' ', end='', flush=True) #flush=true makes the print unbuffered, so that the print occurs despite the buffer from readchar
		#print(input_key)

		# Checking for exceptional inputs
		if input_key == "\x7f":
			print("\nBackspace is not allowed. Try to write continuously")
			print("\nEnter your password: ")
			return getIntervals()

		if input_key == "\x20":
			print("\nSpaces are not allowed")
			print("\nEnter your password: ")
			return getIntervals()

		
		if input_key == "\x1b":
			raise Exception("Esc")

		# There are multiple other keyboard keys that should be included. Better would be to whitelist only the characters that are allowed — not in the scope of this code.


		endTime = time.time()
		# print(input_key, end = '')
		inputString += input_key
		elapsedtime =  endTime - startingTime
		intervals.append(elapsedtime)
	intervals = intervals[1:-1]
	inputString = inputString[:-1].replace(" ", "")
	return (intervals, inputString)


#*****#
# User class (used to create a new user, including the rhythm calculation)
#*****#

class User:
	def __init__(self, username = "", password = "", rhythm = []):
		if username == "":
			print("Enter your username: ")
			self.username = str(input())
			print("Enter your password: ")
			self.rhythm = []

			try:
				(intervals, inputString) = getIntervals()
				self.rhythm = intervals
				self.password = inputString
			except:
				raise Exception("User could not be created")

		else:
			self.username, self.password, self.rhythm = username, password, rhythm


	def __str__(self):
		rhythmString = ""
		for index in range(len(self.password)-1):
			rhythmString += (str(self.password[index]) + " -> " + str(self.password[index + 1])+": " + str(self.rhythm[index]) + "\n")


		return ("\nUsername: " + str(self.username) + " \npassword: " + 
			str(self.password) + "\nrhythm: \n" + rhythmString + "\nTotal password time: " + str(sum(self.rhythm)))

#*****#
# Create user (i.e., where input is written in the users.txt file in string form (users divided by lines))
#*****#

def create_user():
	try:
		print("\nYou are creating an account. Do not forget to type your password with proper hand posture and speed. If necessary, practice typing your password before creating your account.\n")
		new_user = User()
	except:
		print("\nReturning to main menu\n")
		main()
	else:

		if len(new_user.password) < 6:
			print("\nError: please, enter a password with at least 6 characters\n")
			del new_user
			return create_user()

		if "\b" in new_user.password:
			print("\nYou have pressed an invalid key. Please try again\n")
			return create_user()

		print("")
		print(new_user)

		usersFile = open("users.txt", "r+")
		for line in usersFile:
			if line.split()[0] == new_user.username:
				print("\n***This username already exists***")
				return main()


		listAsString = str(new_user.rhythm)
		new_user_string = new_user.username + " " + new_user.password + " " + listAsString.replace(' ','')
		new_user_string = new_user_string.replace('\n', ' ').replace('\r', '')
		usersFile.write(new_user_string + "\n")
		print("\n***Account created successfully***\n")


#*****#
# Authenticate user
#*****#

def login():
	try:
		# Recall that creating an instance of the User() will generate a User object that has username, password and rhythm
		inputUser = User()
	except:
		print("\nReturning to main menu\n")
		main()
	else:
		readUser = ""
		usersFile = open("users.txt", "r")
		usernameExists = False
		standardLogin = False

		for line in usersFile:
			lineInput = line.split()
			linerhythm = list(map(float, lineInput[2].strip('][').split(',')))
			readUser = User(lineInput[0], lineInput[1], linerhythm)

			if readUser.username == inputUser.username:
				usernameExists = True

				if readUser.password == inputUser.password:
					standardLogin = True
					break
				else:
					print("")
					print("\n***Incorrect password***\n")


		# standardLogin mimicks a standard login system that only verifies if the username and password data matches
		if standardLogin:
			print("\n***You have inserted the correct username and password***\n")
			print("Calculating typing rhythm authentication...")

			rhythmLogin = authenticaterhythms(readUser.rhythm, inputUser.rhythm)

			# rhythmLogin is added layer of security that verifies if the user's password input has a valid rhythm
			if rhythmLogin:
				print("\n***Your typing rhythm matched***\nYou are logged in\n")

			else:
				print("\n***Your typing rhythm did not match***\n")

			print("***Extra information***\n")
			print("The account stored in memory contains the following data: ")
			print(readUser)
			print("\n ————————— \nThe input: ")
			print(inputUser)

			readUserTotalTime = sum(readUser.rhythm)
			inputUserTotalTime = sum(inputUser.rhythm)

			if inputUserTotalTime > readUserTotalTime:
				print("\nYou have taken " + str(inputUserTotalTime - readUserTotalTime) + " seconds longer than the initial instance of your account\n")

			else:
				print("\n You were " + str(readUserTotalTime - inputUserTotalTime) + " seconds faster than the initial instance of your account\n")

		if usernameExists == False:
			print("This username doesn't exist")


#*****#
# Listing accounts in memory
#*****#
	
def listAccounts():
	usersFile = open("users.txt", "r")
	print("\nList of all accounts: \n")
	for line in usersFile:
		lineInput = line.split()
		print("Username: " + lineInput[0])
		print("Password: " + lineInput[1] + "\n")

while True:
	main()