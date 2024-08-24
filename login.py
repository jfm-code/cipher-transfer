
from libraries import *
from encrypt import *
from contact import *
from send import *


def user_login(delay_number):
    
    print("-- Begin Login --")
    input_email = input("Enter Email Address: ")
    file_size = os.path.getsize("client_info.json")
    if (file_size == 0):
        user_not_exist()
    else:
        found_user = False
        with open("client_info.json", "r") as json_file:
            existing_data = json.load(json_file)
        for user in existing_data:
            if (user["email"] == input_email):
                found_user = True
                saved_password = user["password"]
                saved_salt = user["salt"]
                count_attempt = 0
                while count_attempt < MAX_ATTEMPT:
                    input_password = pwinput.pwinput("Enter Password: ")
                    if (passCheck(input_password, saved_salt, saved_password)):
                        print("-- Login Successfully --")
                        # creates a thread so when logged in you are always listening for files.
                        t1 = Process(target=start_listening, args=("127.0.0.1",PORT))
                        #starts the threads
                        t1.start()
                        #just incase ends the threads
                        show_option(user["email"],user["fullname"])
                        break
                    else:
                        print("Incorrect password. Please try again.")
                        count_attempt+=1
                if (count_attempt == MAX_ATTEMPT):
                    print("Too many attempts. Please wait before you can login again :(")
                    delay_time = calculate_delayTime(delay_number)
                    delay_number+=1
                    start_time = time.time()
                    count_time = 0
                    while time.time() - start_time < delay_time:
                        print("Time remaining (seconds): ", delay_time - count_time) 
                        count_time+=1
                        time.sleep(1)
                    print("You can login again.")
                    count_attempt = 0
                    user_login(delay_number)
        if (found_user == False):
            user_not_exist()

############################################################
def user_not_exist():
    print("This user does not exist. Please register one.")
    response = input("Do you want to register an account? (y/n): ")
    if (response == 'y' or response == 'yes'):
        import main
        main.welcome(delay_number)
    else:
        print("Exiting Secure Drop...")

############################################################
def calculate_delayTime(delay_number):
    return DELAY_TIME * math.pow(3, delay_number)
    #5 min, 15mins, 45mins, 135mins

############################################################
def show_option(userEmail, userName):

    print("Add a new contact        - type \"add\"")
    print("List all online contacts - type \"list\"")
    print("Send file to contact     - type \"send\"")
    print("Exit Secure Drop         - type \"exit\"")

    choice = input("Enter a command:\n")
    if (choice == "add"):
        add_contact(userEmail, userName)
        show_option(userEmail, userName)
    elif (choice == "list"):
        list_contact(userEmail, userName)
        show_option(userEmail, userName)
    elif (choice == "send"):
        prep_send(userEmail,userName)
        show_option(userEmail, userName)
    elif (choice == "exit"):
        print("Exiting Secure Drop...")
        #exit() #This wont stop the thread that is still going on
        os._exit(1)
