import os
import cryptography.exceptions
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import GCM
from cryptography.hazmat.primitives.hashes import SHA256

def aes_gcm_authenticated_decryption(cipherkey, iv, auth_tag, associated_data, ciphertext, private_key):
    # Decrypt AES key with RSA private key
    oaep_padding = padding.OAEP(mgf=padding.MGF1(algorithm=SHA256()), algorithm=SHA256(), label=None)
    key = private_key.decrypt(cipherkey, oaep_padding)
    aes_gcm_decryptor = Cipher(AES(key), GCM(iv, auth_tag)).decryptor()
    aes_gcm_decryptor.authenticate_additional_data(associated_data)
    recovered_plaintext = aes_gcm_decryptor.update(ciphertext) + aes_gcm_decryptor.finalize()
    return recovered_plaintext

def signature_verification(message, signature, pss_padding, sha256, public_key):
    try:
        public_key.verify(signature, message, pss_padding, sha256)
    except cryptography.exceptions.InvalidSignature:
        # Should not happen
        assert False
    else:
        assert True

if __name__ == "__main__":

    # RSA-PSS
    sha256 = hashes.SHA256()
    pss_padding = padding.PSS(mgf=padding.MGF1(sha256), salt_length=padding.PSS.MAX_LENGTH)

    # Recipient's private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Public key to make available to sender
    public_key = private_key.public_key()

    # 256-bit symmetric key
    key = os.urandom(256 // 8)

    # For AES GCM, NIST recommends 96 bit IVs
    iv = os.urandom(96 // 8)

    # Our message to be kept confidential
    plaintext = b'Fundamental Cryptography in Python'

    # Associated data
    associated_data = b'Context of using AES GCM'

    # Signature creation
    signature = private_key.sign(plaintext, pss_padding, sha256)

    # Signature verification
    signature_verification(plaintext, signature, pss_padding, sha256, public_key)

    # Encrypt the plaintext (no padding required for GCM)
    aes_gcm_encryptor = Cipher(AES(key), GCM(iv)).encryptor()
    aes_gcm_encryptor.authenticate_additional_data(associated_data)
    ciphertext = aes_gcm_encryptor.update(plaintext) + aes_gcm_encryptor.finalize()
    auth_tag = aes_gcm_encryptor.tag
    # Encrypt AES key with RSA public key
    oaep_padding = padding.OAEP(mgf=padding.MGF1(algorithm=SHA256()), algorithm=SHA256(), label=None)
    cipherkey = public_key.encrypt(key, oaep_padding)

    # Decrypt and authenticate the ciphertext
    recovered_plaintext = aes_gcm_authenticated_decryption(cipherkey, iv, auth_tag, associated_data, ciphertext, private_key)
    assert (recovered_plaintext == plaintext)
    print(recovered_plaintext)

    # Wrong key
    wrong_key = os.urandom(256 // 8)
    wrong_cipherkey = public_key.encrypt(wrong_key, oaep_padding)
    try:
        recovered_plaintext = aes_gcm_authenticated_decryption(wrong_cipherkey, iv, auth_tag, associated_data, ciphertext, private_key)
    except cryptography.exceptions.InvalidTag:
        pass
    else:
        # Should not happen
        assert False

    # Wrong iv
    wrong_iv = os.urandom(96 // 8)
    try:
        recovered_plaintext = aes_gcm_authenticated_decryption(cipherkey, wrong_iv, auth_tag, associated_data, ciphertext, private_key)
    except cryptography.exceptions.InvalidTag:
        pass
    else:
        # Should not happen
        assert False

    # Wrong authentication tag
    wrong_auth_tag = os.urandom(128 // 8)
    try:
        recovered_plaintext = aes_gcm_authenticated_decryption(cipherkey, iv, wrong_auth_tag, associated_data, ciphertext, private_key)
    except cryptography.exceptions.InvalidTag:
        pass
    else:
        # Should not happen
        assert False

    # Wrong associated data
    wrong_associated_data = b'Wrong Context of using AES GCM'
    try:
        recovered_plaintext = aes_gcm_authenticated_decryption(cipherkey, iv, auth_tag, wrong_associated_data, ciphertext, private_key)
    except cryptography.exceptions.InvalidTag:
        pass
    else:
        # Should not happen
        assert False

    # Wrong ciphertext
    wrong_ciphertext = ciphertext[:len(ciphertext)-1] + bytes([(ciphertext[-1] + 1) % 256])
    try:
        recovered_plaintext = aes_gcm_authenticated_decryption(cipherkey, iv, auth_tag, associated_data, wrong_ciphertext, private_key)
    except cryptography.exceptions.InvalidTag:
        pass
    else:
        # Should not happen
        assert False

