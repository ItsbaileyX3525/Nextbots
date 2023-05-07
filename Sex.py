import base64
from cryptography.fernet import Fernet
import os

# Prompt user for input
plaintext = input("Enter the plaintext to be encrypted: ")

# Prompt user for session key
session_key_input = input("Enter a session key (leave blank to generate a new one): ")

if session_key_input:
    # If the user entered a session key, decode it from base64
    session_key = base64.b64decode(session_key_input.encode())
else:
    # If the user didn't enter a session key, generate a new one
    session_key = Fernet.generate_key()

# Create a Fernet cipher using the session key and CBC mode
cipher = Fernet(session_key)

# Convert the plaintext to bytes
plaintext_bytes = plaintext.encode()

# Pad the plaintext to a multiple of 16 bytes (the block size of AES)
pad_length = 16 - len(plaintext_bytes) % 16
padded_plaintext_bytes = plaintext_bytes + bytes([pad_length] * pad_length)

# Encrypt the padded plaintext using the Fernet cipher
ciphertext = cipher.encrypt(padded_plaintext_bytes)

# Convert the session key and ciphertext to base64-encoded strings
session_key_b64 = base64.b64encode(session_key).decode()
ciphertext_b64 = base64.b64encode(ciphertext).decode()

# Check if the file exists
if os.path.isfile("Storage database.dat"):
    # If the file exists, append the session key and ciphertext to the end of the file
    with open("Storage database.dat", "a") as f:
        f.write(session_key_b64 + '\n')
        f.write(ciphertext_b64 + '\n')
else:
    # If the file doesn't exist, create it and write the session key and ciphertext to the file
    with open("Storage database.dat", "w") as f:
        f.write(session_key_b64 + '\n')
        f.write(ciphertext_b64 + '\n')

# Print a message to indicate that the data has been stored
print("Data has been encrypted and stored in Storage database.dat.")
