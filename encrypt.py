from libraries import *

def hashing(string, salt):
        # adds salt
        string += salt
        #generates a random number
        ran = random.randint(0,51)
        #converts int to ascii char, then adds it to string (the pepper)
        string += alph[ran]
        #creates hash object
        hashed = SHA256.new()
        #hashes string
        string = bytes(string, encoding="utf-8")
        hashed.update(string)
        #returns hash, this part can be editted to deposit hash into a file
        return(hashed.hexdigest())
        
############################################################
#Input the size of the salt, outputs a psuedorandom salt of that size
def genSalt(saltSize):
       sample = "!@#$%^&*()}{|:><.,1234567ERTYDFXCV67809BMNmvlaksjdhfgpoqi=-owueyrt}"
       salt = str(''.join(random.choices(sample,k=saltSize)))
       return salt

############################################################
#Inputs password thats stored with the salt, Will check through all peppers then return if its correct or not
def passCheck(password,salt,hashed):
    #adds salt to users password
    password += salt
    #adds peper to the end then compares the hashes
    for x in alph :
            #adds char to password
            password+=x
            #creates a hash with password
            hash = SHA256.new()
            hPass = bytes(password, encoding="utf-8")
            hash.update(hPass)
            #if this hash matches return true
            if(hash.hexdigest()==hashed): return True
            #if it does not match remove the char
            else: password = password[:-1]
    #if it gets through the loop that means incorrect password
    return False

############################################################
def AES_encrypt(hashed_password, info):
        # Generate a salt
        salt = os.urandom(16)

        # Derive a key from the user's password using scrypt
        backend = default_backend()
        kdf = Scrypt(
                salt=salt,
                length=32,
                n=2**14,
                r=8,
                p=1,
                backend=backend
        )
        key = kdf.derive(hashed_password.encode())

        # Initialize AES cipher in CTR mode
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())

        # Encrypt the info of the contact
        encryptor = cipher.encryptor()
        plaintext = str(info).encode()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        # Prepend IV to the ciphertext
        ciphertext_with_iv = iv + ciphertext

        # Append salt to the end of ciphertext_with_iv
        ciphertext_with_salt = ciphertext_with_iv + salt

        # Encode the ciphertext with salt in base64
        ciphertext_with_salt_b64 = base64.b64encode(ciphertext_with_salt)

        return ciphertext_with_salt_b64.decode()

############################################################
def AES_decrypt(hashed_password, ciphertext_with_salt_b64):
    # Convert the base64-encoded string to bytes
    ciphertext_with_salt_bytes = ciphertext_with_salt_b64.encode()

    # Decode the bytes using base64
    ciphertext_with_salt = base64.b64decode(ciphertext_with_salt_bytes)

    # Extract the salt from the end of the ciphertext
    salt = ciphertext_with_salt[-16:]
    ciphertext = ciphertext_with_salt[:-16]

    # Derive a key from the user's password using scrypt
    backend = default_backend()
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
        backend=backend
    )
    key = kdf.derive(hashed_password.encode())

    # Get the IV from the ciphertext
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]

    # Initialize AES cipher in CTR mode
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())

    # Decrypt the ciphertext
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode()
