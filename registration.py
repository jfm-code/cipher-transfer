from libraries import *
from encrypt import *
import login

def user_register():
    print("-- Begin User Registration --")
    fullname = input("Enter Full Name: ")
    email = input("Enter Email Address: ")

    # Check if the user already exists - preven duplicates
    file_size = os.path.getsize("client_info.json")
    if file_size != 0:
        with open("client_info.json", "r") as json_file:
            existing_data = json.load(json_file)
        for user in existing_data:
            if (user["email"] == email):
                print("There is already an account with this email. Please login instead.")
                login.user_login(delay_number)
                return

    password = pwinput.pwinput("Enter Password: ")
    # validate the security of the password
    while password_validate(password) is False:
        print("Your password needs to have at least 1 uppercase letter, 1 lowercase letter, 1 digit, 1 special symbol.")
        password = pwinput.pwinput("Please choose another password. Enter -1 to quit: ")
        if password == '-1':
            print("Exiting Secure Drop...")
            exit()
    
    user_salt = genSalt(SALT_SIZE)
    password = hashing(password, user_salt)
    contact_list = []
    if IP_port_list is not None:
        user_port = IP_port_list[-1]
        IP_port_list.pop() #delete the last element of the list
        user_IP = IP_port_list[-1]
        IP_port_list.pop()

    new_user = {
        "fullname": fullname,
        "email": email,
        "IP": user_IP,
        "port": user_port,
        "salt": user_salt,
        "password": password,
        "contacts": contact_list
    }
    # check if the file is empty or not first
    file_size = os.path.getsize("client_info.json")
    if file_size != 0:
        with open("client_info.json", "r") as json_file:
            existing_data = json.load(json_file)
    else:
        existing_data = []
    # update the user list
    existing_data.append(new_user)
    with open("client_info.json", "w") as json_file:
        json.dump(existing_data, json_file, indent=4)
    print("User Registration Complete.")
    reg_more = input("Do you want to register another account? (y/n): ")
    if (reg_more == 'y'):
        user_register()

#######################################################
def password_validate(user_password):
    if len(user_password) < 12:
        return False
    upper_found = False
    lower_found = False
    digit_found = False
    symbol_found = False
    for c in user_password:
        if c.isupper():
            upper_found = True
        elif c.islower():
            lower_found = True
        elif c.isdigit():
            digit_found = True
        elif (c == '!' or c == '@' or c == '#' or c == '$' or c == '%' or c == '&' or c == '*'):
            symbol_found = True
    if (upper_found == True and lower_found == True and digit_found == True and symbol_found == True):
        return True
    else:
        return False
