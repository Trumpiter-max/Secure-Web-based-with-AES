from .cpabe import CPabe_BSW07
from charm.toolbox.pairinggroup import PairingGroup, ZR, GT, extract_key
from charm.toolbox.symcrypto import AuthenticatedCryptoAbstraction
from charm.core.engine.util import objectToBytes, bytesToObject
from charm.toolbox.secretutil import SecretUtil

# Initialize CP-ABE
groupObj = PairingGroup('SS512')
cpabe = CPabe_BSW07(groupObj)
policy_name = "/var/www/storage/policy/Property_policy.txt"

def choose_policy_name(choice):
    policy_names = {
        1: "LandOwnership_policy.txt",
        2: "Construction_policy.txt",
        3: "Property_policy.txt",
        4: "Agreement_policy.txt",
    }
    return policy_names.get(choice, "Invalid choice")

def generate_key(name):
    groupObj = PairingGroup('SS512')
    cpabe = CPabe_BSW07(groupObj)
    rand_Obj = groupObj.random(GT)
    rand_bytes = objectToBytes(rand_Obj, groupObj)
    public_key_file = "/var/www/storage/keys/cpabe_key/public_key.bin"
    # Load the public key from the file
    with open(public_key_file, "rb") as f:
        loaded_pk = bytesToObject(f.read(), groupObj)
    # Convert the inner dictionary keys back to integers
    for key in loaded_pk:
        if isinstance(loaded_pk[key], dict):
            loaded_pk[key] = {int(inner_key): value for inner_key, value in loaded_pk[key].items()}
        
    #access_policy = '(hello and (three or one))'
    with open(policy_name, 'r') as file:
        P = file.read()
        
    # Encrypt the input symmetric key using the CP-ABE scheme
    ct = cpabe.encrypt(loaded_pk, rand_Obj, P)
    # Save the encrypted symmetric key to a file
    encrypted_key_file = "/var/www/storage/keys/aes_key/" + name + "_encrypted_key.bin"
    with open(encrypted_key_file, 'wb') as f:
        f.write(objectToBytes(ct, groupObj))
    return rand_bytes[:32]
    
def generate_IV(name):
    groupObj = PairingGroup('SS512')
    cpabe = CPabe_BSW07(groupObj)
    rand_Obj = groupObj.random(GT)
    rand_bytes = objectToBytes(rand_Obj, groupObj)
    public_key_file = "/var/www/storage/keys/cpabe_key/public_key.bin"
    # Load the public key from the file
    with open(public_key_file, "rb") as f:
        loaded_pk = bytesToObject(f.read(), groupObj)
    # Convert the inner dictionary keys back to integers
    for key in loaded_pk:
        if isinstance(loaded_pk[key], dict):
            loaded_pk[key] = {int(inner_key): value for inner_key, value in loaded_pk[key].items()}
        
    #access_policy = '(hello and (three or one))'
    with open(policy_name, 'r') as file:
        P = file.read()
        
    # Encrypt the input symmetric key using the CP-ABE scheme
    ct = cpabe.encrypt(loaded_pk, rand_Obj, P)
    # Save the encrypted symmetric key to a file
    encrypted_key_file = "/var/www/storage/keys/aes_key/" + name + "_encrypted_IV.bin"
    with open(encrypted_key_file, 'wb') as f:
        f.write(objectToBytes(ct, groupObj))
    return rand_bytes[:12]	
	
def decrypt_key(role, organization, name):
    public_key_file = "/var/www/storage/keys/cpabe_key/public_key.bin"
    # Load the public key from the file
    with open(public_key_file, "rb") as f:
        loaded_pk = bytesToObject(f.read(), groupObj)
    # Convert the inner dictionary keys back to integers
    for key in loaded_pk:
        if isinstance(loaded_pk[key], dict):
            loaded_pk[key] = {int(inner_key): value for inner_key, value in loaded_pk[key].items()}
    master_key_file = "/var/www/storage/keys/cpabe_key/master_key.bin"
    # Load the master key from the file
    with open(master_key_file, "rb") as f:
        loaded_mk = bytesToObject(f.read(), groupObj)
    
    B = [organization, role]
    loaded_B = [word.split()[0].upper() for word in B]

    dk = cpabe.keygen(loaded_pk, loaded_mk, loaded_B)
    encrypted_key_file = "/var/www/storage/keys/aes_key/" + name + "_encrypted_key.bin"
    # Load the encrypted symmetric key from the file
    with open(encrypted_key_file, "rb") as f:
        loaded_ct = bytesToObject(f.read(), groupObj)
    # Decrypt the symmetric key using the CP-ABE scheme
    decrypted_key_gt = cpabe.decrypt(loaded_pk, dk, loaded_ct)
    decrypted_key_bytes = objectToBytes(decrypted_key_gt, groupObj)
    decrypted_key_bytes = decrypted_key_bytes[:32]
    return decrypted_key_bytes

def decrypt_IV(role, organization, name):
    public_key_file = "/var/www/storage/keys/cpabe_key/public_key.bin"
    # Load the public key from the file
    with open(public_key_file, "rb") as f:
        loaded_pk = bytesToObject(f.read(), groupObj)
    # Convert the inner dictionary keys back to integers
    for key in loaded_pk:
        if isinstance(loaded_pk[key], dict):
            loaded_pk[key] = {int(inner_key): value for inner_key, value in loaded_pk[key].items()}
    master_key_file = "/var/www/storage/keys/cpabe_key/master_key.bin"
    # Load the master key from the file
    with open(master_key_file, "rb") as f:
        loaded_mk = bytesToObject(f.read(), groupObj)
    
    B = [organization, role]
    loaded_B = [word.split()[0].upper() for word in B]

    dk = cpabe.keygen(loaded_pk, loaded_mk, loaded_B)
    encrypted_key_file = "/var/www/storage/keys/aes_key/" + name + "_encrypted_IV.bin"
    # Load the encrypted symmetric key from the file
    with open(encrypted_key_file, "rb") as f:
        loaded_ct = bytesToObject(f.read(), groupObj)
    # Decrypt the symmetric key using the CP-ABE scheme
    decrypted_key_gt = cpabe.decrypt(loaded_pk, dk, loaded_ct)
    decrypted_key_bytes = objectToBytes(decrypted_key_gt, groupObj)
    decrypted_key_bytes = decrypted_key_bytes[:12]
    return decrypted_key_bytes
