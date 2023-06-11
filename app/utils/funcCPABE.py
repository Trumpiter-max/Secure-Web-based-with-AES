# This is CP-ABE AES key generation and encryption

from CP_ABE import CPabe_SP21
from charm.toolbox.pairinggroup import PairingGroup, ZR, GT, extract_key
from charm.toolbox.symcrypto import AuthenticatedCryptoAbstraction
from charm.core.engine.util import objectToBytes, bytesToObject

# Initialize CP-ABE
groupObj = PairingGroup('BN254')
cpabe = CPabe_SP21(groupObj)

# Define attribute universe, user attributes, and access policy
U = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN']
B = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE']
P = ['ONE', 'TWO', 'THREE']

(spk, smk) = cpabe.setup(10)
file_name = "Attribute_list.txt"

def save_list_to_txt(file_name, string_list):
    with open(file_name, "w") as f:
        for item in string_list:
            f.write(item + "\n")

def load_list_from_txt(file_name):
    with open(file_name, "r") as f:
        string_list = [line.strip() for line in f.readlines()]
    return string_list

def generate_key(pk = spk, mk = smk):
    groupObj = PairingGroup('BN254')
    cpabe = CPabe_SP21(groupObj)

    rand_Obj = groupObj.random(GT)

    rand_bytes = objectToBytes(rand_Obj, groupObj)
    #print(rand_bytes)
    
    # Save the public key to a file
    public_key_file = "public_key.bin"
    with open(public_key_file, "wb") as f:
        f.write(objectToBytes(pk, groupObj))


	# Save the master key to a file
    master_key_file = "master_key.bin"
    with open(master_key_file, "wb") as f:
    	f.write(objectToBytes(mk, groupObj))

    # Load the public key from the file
    with open(public_key_file, "rb") as f:
    	loaded_pk = bytesToObject(f.read(), groupObj)

	# Convert the inner dictionary keys back to integers
    for key in loaded_pk:
        if isinstance(loaded_pk[key], dict):
            loaded_pk[key] = {int(inner_key): value for inner_key, value in loaded_pk[key].items()}
      
	# Load the master key from the file
    with open(master_key_file, "rb") as f:
        loaded_mk = bytesToObject(f.read(), groupObj)


    input_symmetric_key_gt = bytesToObject(rand_bytes, groupObj)

    # Encrypt the input symmetric key using the CP-ABE scheme
    ct = cpabe.encrypt(loaded_pk, input_symmetric_key_gt, P, U)

    # Save the encrypted symmetric key to a file
    encrypted_key_file = "encrypted_object.bin"
    with open(encrypted_key_file, 'wb') as f:
        f.write(objectToBytes(ct, groupObj))

    return rand_bytes[:32]
    

def decrypt_key():
    public_key_file = "public_key.bin"
    # Load the public key from the file
    with open(public_key_file, "rb") as f:
        loaded_pk = bytesToObject(f.read(), groupObj)

    # Convert the inner dictionary keys back to integers
    for key in loaded_pk:
        if isinstance(loaded_pk[key], dict):
            loaded_pk[key] = {int(inner_key): value for inner_key, value in loaded_pk[key].items()}
        
    master_key_file = "master_key.bin"
    # Load the master key from the file
    with open(master_key_file, "rb") as f:
        loaded_mk = bytesToObject(f.read(), groupObj)
        
    # Load the Attribute from a text file
    loaded_B = load_list_from_txt(file_name)

    dk = cpabe.keygen(loaded_pk, loaded_mk, loaded_B, U)

    encrypted_key_file = "encrypted_object.bin"

    # Load the encrypted symmetric key from the file
    with open(encrypted_key_file, "rb") as f:
        loaded_ct = bytesToObject(f.read(), groupObj)

    # Decrypt the symmetric key using the CP-ABE scheme
    decrypted_key_gt = cpabe.decrypt(loaded_pk, dk, loaded_ct)

    decrypted_key_bytes = objectToBytes(decrypted_key_gt, groupObj)
    decrypted_key_bytes = decrypted_key_bytes[:32]

    return decrypted_key_bytes

    
    
    	
    	






