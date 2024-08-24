from libraries import *
from contact import *
import socket 
import sys 
import os 
import ssl

def prep_send(userEmail, userName):
    # Check if we can actually send file to this user or not
    print("Before being able to send the file. We will list all the contacts that you can send file to.")
    valid_contacts = list_contact(userEmail, userName)

    print("-- Start Sending File --")
    receiver = input("Please enter the name/email of the person you want to send the file to: ")
    if (receiver in valid_contacts):
        file_path = input("Please enter the path to the file: ")
        while (not os.path.exists(file_path)):
            print("File not found.\n")
            file_path = input("Please enter the path to the file: ")
        send_file("127.0.0.1", PORT, file_path)
    else:
        print("The contact name/email is not valid. Cannot send file. Please choose another option.")

#######################################################
def send_file(server_ip, server_port, file_path):
        # Ensure that the given file exists
        # Create a client socket using IPv4 and TCP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set up the SSL context
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        # Wrap the socket to secure it using TLS
        secureConnection = context.wrap_socket(client_socket, server_hostname=server_ip)
        try:
            secureConnection.connect((server_ip, server_port))
            print(f"Connected to server at {server_ip}:{server_port}")

            # Extract file name from path
            file_name = file_path.split('/')[-1]
            
            # Send the length of the file name to the server
            secureConnection.send(len(file_name.encode()).to_bytes(4, byteorder='big'))
            
            # Send the actual file name
            secureConnection.send(file_name.encode())
            
            # Open and send file
            with open(file_path, 'rb') as file:
                while True:
                    data = file.read(1024)
                    if not data:
                        break
                    secureConnection.send(data)

            print("File sent successfully.")

        except Exception as e:
            print(f"Error: {e}")
            
        finally:
            secureConnection.close()
            print(f"Connection to {server_ip}:{server_port} closed.")

#######################################################
def start_listening(host, port):
    # Create the server socket using IPv4 and TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)  # Listen with a backlog of 5 connections
    

    # Set up the SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

    print(f"Server listening on port {port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Wrap the socket to secure it using TLS
        secureConnection = context.wrap_socket(client_socket, server_side=True)

        # First, receive the 4-byte file name length
        file_name_length = int.from_bytes(secureConnection.recv(4), byteorder='big')

        try:
            # Now, receive the actual file name
            file_name = secureConnection.recv(file_name_length).decode()
            print(f"Receiving file named: {file_name}\n" + "*" * 80)

            # Receive the file content and save it
            folder_path = r'/home/jessicavu04/CollegeSpring2024/CompSecurity/SecureDrop/downloads'
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'wb') as file:
                while True:
                    data = secureConnection.recv(1024)
                    if not data:
                        break
                    file.write(data)
                    
            print(f"Received file {file_name}")

        except Exception as e:
            print(f"Error: {e}")

        secureConnection.close()
        print(f"Connection with {client_address} closed.")