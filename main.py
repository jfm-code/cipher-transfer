import login
from libraries import *
from registration import *
from encrypt import *
from contact import *

def welcome(delay_number):
    
    print("Welcome to Secure Drop. What can we help you?")
    print("Register an account        - type \"register\"")
    print("Log in to existing account - type \"login\"")
    print("Exit Secure Drop           - type \"exit\"")

    choice = input("Enter a command: ")
    if (choice == "register"):
        user_register()
    elif (choice == "login"):
        login.user_login(delay_number)
    elif (choice == "exit"):
        print("Exiting Secure Drop...")
    else:
        while(choice != "register" and choice != "login" and choice != "exit"):
            choice = input("Invalid command. Please enter one of the commands above: ")
        if (choice == "register"):
            user_register()
        elif (choice == "login"):
            login.user_login(delay_number)
        elif (choice == "exit"):
            print("Exiting Secure Drop...")

############################################################
# main.c
welcome(delay_number)