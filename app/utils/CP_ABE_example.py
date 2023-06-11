#This is a demo of AES GCM mode using AES key generated and encrypted by CPABE

import os
from base64 import b64encode, b64decode
from funcCPABE import generate_key, decrypt_key
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def load_key(filename):
    with open(filename, 'rb') as f:
        key = f.read()
    return key

# Function to encrypt the data
def encrypt(plaintext, key):
    # Generate a random nonce
    nonce = os.urandom(12)

    # Create the AES-GCM cipher
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())

    # Encrypt the plaintext
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return (nonce, ciphertext, encryptor.tag)

# Function to decrypt the data
def decrypt(nonce, ciphertext, tag, key):
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())

    # Decrypt the ciphertext
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

# Example usage
key_file = 'plain_key.bin'

# Load the AES key from the file
key = generate_key()
print(f"key: {key}")
plaintext = b"This is a secret message."

# Encrypt the plaintext
nonce, ciphertext, tag = encrypt(plaintext, key)
print("Nonce: ", b64encode(nonce).decode('utf-8'))
print("Ciphertext: ", b64encode(ciphertext).decode('utf-8'))
print("Tag: ", b64encode(tag).decode('utf-8'))

# Decrypt the ciphertext
key = decrypt_key()
print(f"decrypted key: {key}")
decrypted_text = decrypt(nonce, ciphertext, tag, key)
print("Decrypted text: ", decrypted_text.decode('utf-8'))
