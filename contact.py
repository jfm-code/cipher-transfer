from libraries import *
from encrypt import passCheck, AES_encrypt, AES_decrypt

def add_contact(userEmail, userName):
    # check if exceed maximum number of contact or not
    with open("client_info.json", "r") as json_file:
        existing_data = json.load(json_file)

    for user in existing_data:
        if (user["email"] == userEmail):
            if (len(user["contacts"]) > MAX_CONTACT):
                print("You have reached the maximum contact. Cannot add more contact.")
                exit()

    print("-- Start Adding Contact --")
    fullname = input("Enter Contact Name: ")
    while (fullname == userName):
        print("Invalid name. You can't add yourself as your contact.")
        fullname = input("Please Enter Contact Name Again: ")
    email = input("Enter Contact Email: ")
    while (email == userEmail):
        print("Invalid email. You can't add yourself as your contact.")
        email= input("Please Enter Contact Email Again: ")
    new_contact = {
        "contact_name": fullname,
        "contact_email": email
    }

    with open("client_info.json", "r") as json_file:
        existing_data = json.load(json_file)

    for user in existing_data:
        if (user["email"] == userEmail):
            #if the contact already exists then do not add it - prevent duplicates
            for current in user["contacts"]:
                if (AES_decrypt(user["password"], current["contact_email"]) == email):
                    print("This contact already exists in the user's contact list.")
                    choice = input("Do you want to add another contact? (y/n): ")
                    if (choice == 'y' or choice == "yes"):
                        add_contact(userEmail, userName)
                    else:
                        return

            #if no duplicates then encrypt the new_contact with AES before put that in json file
            new_contact["contact_name"] = AES_encrypt(user["password"], fullname)
            new_contact["contact_email"] = AES_encrypt(user["password"], email)
            user["contacts"].append(new_contact)

    with open("client_info.json", "w") as json_file:
        json.dump(existing_data, json_file, indent=4)

    choice = input("Do you want to add another contact? (y/n): ")
    if (choice == 'y' or choice == "yes"):
        add_contact(userEmail, userName)
    else:
        print("Adding new contact completed.")

def list_contact(userEmail, userName):
    #prevent the case when the attacker has access to the user's account
    #attacker won't be able to see the contact because he doesn't know the password
    entered_password = pwinput.pwinput("Please enter your password again to see the list of contact: ")

    with open("client_info.json", "r") as json_file:
        existing_data = json.load(json_file)

    contact_list = []

    #get the list of contacts from user account first
    for user in existing_data:
        if (user["email"] == userEmail):
            if (passCheck(entered_password, user["salt"], user["password"])):
                print("Correct password. Printing the contact list...")
                for contact in user["contacts"]:
                    #decrypt before append it in the contact_list
                    contact_list.append(AES_decrypt(user["password"], contact["contact_name"]))
                    contact_list.append(AES_decrypt(user["password"], contact["contact_email"]))
            else:
                print("Incorrect password.")
                return #simply exit the function

    #check if contact exist/registered or not
    #contact_list[:] is a shallow copy of contact_list
    #if we dont use a copy of the list, when we remove an element, the rest will be pushed forward
    #and therefore causing the next element (the one right after the deleted one) being skipped in the loop
    for contact in contact_list[:]:  
        contact_exist = False
        for user in existing_data:
            if (contact == user["fullname"] or contact == user["email"]):
                contact_exist = True
        if (contact_exist == False):
            contact_list.remove(contact)

    #if contact exists, check if contact has user as his contact or not
    for user_contact in existing_data:
        if (user_contact["fullname"] in contact_list):
            found_user = False
            for contact_of_contact in user_contact["contacts"]:
                if (AES_decrypt(user_contact["password"], contact_of_contact["contact_email"]) == userEmail):
                    found_user = True
            if (found_user == False):
                contact_list.remove(user_contact["fullname"])
                contact_list.remove(user_contact["email"])

    print(contact_list)
    return contact_list