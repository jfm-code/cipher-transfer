# CipherTransfer
CipherTransfer is a secure file transfer system designed to ensure that files are safely transferred between users. The project applies various security principles, including encryption and hashing, to protect user information and files during transfer.

## Project Overview
CipherTransfer provides a series of functionalities for user registration, login validation, contact management, and secure file transfer. It is designed to prevent unauthorized access and ensure that data remains encrypted during all stages of the process.

## Features
### 1. User Registration
Prompt User Information: Collects and stores user details securely.
Duplicate Check: Prevents the registration of duplicate users.
Security Implementations:
Enforces strong password policies (minimum 12 characters, including lowercase, uppercase, numbers, and special symbols).
Hashes passwords using SHA256 with salt and pepper to ensure security.
Passwords are never stored or displayed in plaintext.

### 2. Login Validation
Prompt for Login Information: Securely validates user credentials.
Password Hashing: The entered password is hashed and compared to the stored hash.
Failed Login Attempts: Implements progressive delays (5, 15, 45, 135 minutes) after successive failed login attempts.

### 3. Adding Contact
Contact Information Collection: Gathers and stores contact details securely.
Security Implementations:
Uses AES encryption for storing contact information.
Contacts are encrypted using the user’s password before being saved in the database.

### 4. Listing Contacts
Contact Listing: Displays only the contacts who are mutually registered and added.
Security Implementations:
Prevents unauthorized access to the contact list by requiring the user’s password for decryption.
Contact information remains encrypted in the database.

### 5. Secure File Transfer
File Sending: Allows users to select a contact and securely send files.
Security Implementations:
Utilizes TLS encryption over TCP to secure the file transfer.
Generates TLS private key and public certificate for secure communication.
Files are sent and received between the "files" and "downloads" folders.

## How It Works
### Registration Process
Users are prompted to enter their information.
The system checks for existing users to prevent duplicates.
The password is hashed with SHA256, salted, and peppered before storage.
### Login Process
Users enter their login credentials.
The system checks if the credentials match stored records by hashing the entered password.
If the password is incorrect, progressive delays are introduced after successive failed attempts.
### Contact Management
Adding Contacts: Users can add contacts, which are securely encrypted before being saved.
Listing Contacts: Contacts are only listed if they are mutually added, and the list is decrypted using the user’s password.
### File Transfer
Users select a contact and provide the file path.
The system establishes a secure TLS connection and transfers the file using IPv4 and TCP.

## Authors
Jessica Vu
Noel Taveras
