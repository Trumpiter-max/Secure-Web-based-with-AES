import os
import cryptography.exceptions
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import GCM
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend
from .funcCPABE import generate_key, generate_IV, decrypt_key

def create_key(name, policy):
    # Declare the key and IV
    # 256-bit symmetric key
    # key = os.urandom(32)
    key = generate_key(name, policy)
    return key

def create_iv(name, policy):
    # For AES GCM, NIST recommends 96 bit IVs
    # iv = os.urandom(12)
    iv = generate_IV(name, policy)
    return iv

def save_auth_tag(auth_tag, file_path):
    # string the key in a file
    with open(file_path, 'wb') as auth_tag_file:
        auth_tag_file.write(auth_tag)

def encrypt(key, iv, associated_data, plaintext, file_path):
    # Encrypt the plaintext (no padding required for GCM)
    aes_gcm_encryptor = Cipher(AES(key), GCM(iv), default_backend()).encryptor()
    aes_gcm_encryptor.authenticate_additional_data(associated_data)
    ciphertext = aes_gcm_encryptor.update(plaintext) + aes_gcm_encryptor.finalize()
    auth_tag = aes_gcm_encryptor.tag
    save_auth_tag(auth_tag, file_path + '_auth')
    # opening the key
    # string the key in a file
    with open(file_path, 'wb') as cipher:
        cipher.write(ciphertext)
    return ciphertext

def decrypt(key, iv, auth_tag, associated_data, ciphertext, file_path):
    aes_gcm_decryptor = Cipher(AES(key), GCM(iv, auth_tag), default_backend()).decryptor()
    aes_gcm_decryptor.authenticate_additional_data(associated_data)
    recovered_plaintext = aes_gcm_decryptor.update(ciphertext) + aes_gcm_decryptor.finalize()
    # opening the file in write mode and
    # writing the decrypted data
    with open(file_path, 'wb') as dec_file:
        dec_file.write(recovered_plaintext)
    return recovered_plaintext

