import socket, sys, os, ssl
import pwinput
import json
import stat
import time
import math
import random
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import base64
from multiprocessing import Process

# Global variables
PORT = 60000
MAX_ATTEMPT = 3
MAX_CONTACT = 3
DELAY_TIME = 300 # at first it is 300s = 5mins
SALT_SIZE = 20
IP_port_list = ["127.0.0.1", 20, "127.0.0.1", 22, "127.0.0.1", 25, "172.18.69.219", 80]
delay_number = 0
alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']