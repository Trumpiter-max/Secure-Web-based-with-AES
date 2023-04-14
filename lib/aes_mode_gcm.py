import os
import cryptography.exceptions
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import GCM
from cryptography.hazmat.primitives.hashes import SHA256

# Declare the key and IV
# 256-bit symmetric key
key = os.urandom(256 // 8)
# For AES GCM, NIST recommends 96 bit IVs
iv = os.urandom(96 // 8)

def encrypt(key, iv, associated_data, plaintext):
    # Encrypt the plaintext (no padding required for GCM)
    aes_gcm_encryptor = Cipher(AES(key), GCM(iv)).encryptor()
    aes_gcm_encryptor.authenticate_additional_data(associated_data)
    ciphertext = aes_gcm_encryptor.update(plaintext) + aes_gcm_encryptor.finalize()
    global auth_tag
    auth_tag = aes_gcm_encryptor.tag
    # opening the key
    # string the key in a file
    with open('encrypted.pdf', 'wb') as cipher:
        cipher.write(ciphertext)
    

def decrypt(cipherkey, iv, auth_tag, associated_data, ciphertext):
    aes_gcm_decryptor = Cipher(AES(key), GCM(iv, auth_tag)).decryptor()
    aes_gcm_decryptor.authenticate_additional_data(associated_data)
    recovered_plaintext = aes_gcm_decryptor.update(ciphertext) + aes_gcm_decryptor.finalize()
    # opening the file in write mode and
    # writing the decrypted data
    with open('recovered.pdf', 'wb') as dec_file:
        dec_file.write(recovered_plaintext)

""" Example how to use
if __name__ == "__main__":
    # Message to be kept confidential
    # Associated data - data of who sign in document
    associated_data = b'Context of using AES GCM'
    # Opening the original file to encrypt
    with open('test.pdf', 'rb') as file:
        plaintext = file.read()
    # Store the key
    with open('secret.key', 'wb') as key_file:
        key_file.write(key) 

    # Encrypt and authenticate the plaintext
    encrypt(key, iv, associated_data, plaintext)
    
    # Decrypt and authenticate the ciphertext
    with open('secret.key', 'rb') as secret:
        key_for_decrypt = secret.read()
    with open('encrypted.pdf', 'rb') as encrypted_file:
        ciphertext = encrypted_file.read()
    decrypt(key_for_decrypt, iv, auth_tag, associated_data, ciphertext)

"""