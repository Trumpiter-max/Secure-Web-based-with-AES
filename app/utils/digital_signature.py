from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import os

SIGN_KEY_PATH = "/var/www/storage/keys/sign_key/"

def sign(file, private_key):
    chosen_hash = hashes.SHA256()
    hasher = hashes.Hash(
        chosen_hash, 
        default_backend()
    )
    
    # Get byte from file 
    byte = file.read(1)
    while byte:
        byte = file.read(1)
        hasher.update(byte)

    digest = hasher.finalize()
    signature = private_key.sign(
        digest,
        ec.ECDSA(utils.Prehashed(chosen_hash))
    )
    return signature

def verify(file, signature, public_key):
    chosen_hash = hashes.SHA256()
    hasher = hashes.Hash(
        chosen_hash, 
        default_backend()
    )

    # Get byte from file 
    byte = file.read(1)
    while byte:
        byte = file.read(1)
        hasher.update(byte)
    
    digest = hasher.finalize()

    checker = public_key.verify(
        signature,
        digest,
        ec.ECDSA(utils.Prehashed(chosen_hash))
    )
    return checker

def create_private_key():
    private_key = ec.generate_private_key(
        ec.SECP384R1(),
        default_backend()
    )
    return private_key

def create_public_key(private_key):
    public_key = private_key.public_key()
    return public_key

def save_public_key(public_key, key_name):
    if (key_name == None or key_name == ""):
        return 0
    save_path = os.path.join(SIGN_KEY_PATH, key_name + ".pem")
    public_key_pem = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    with open(save_path, 'wb') as key:
        key.write(public_key_pem)
    return 1

def read_public_key(key_path):
    key_file = open(key_path, 'rb')
    content = key_file.read()
    public_key = serialization.load_pem_public_key(content, backend=default_backend())
    key_file.close()
    return public_key
