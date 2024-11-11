'''Modules'''
import FaceAuthenticator
import UserDB
'''Libraries'''
from LibraryImporter import *

un = input("Enter username: ")
pw = input("Enter password: ")

while not (un in UserDB.usernames and pw == UserDB.passwords[un]):
  os.system("cls")
  print("Invalid Username or Password.\n")
  un = input("Enter username: ")
  pw = input("Enter password: ")

role = UserDB.roles[un]
print("\nLogged in successfully.")
FaceAuthenticator.Start(un, role)
