from .CP_ABE import CPabe_SP21
from charm.toolbox.pairinggroup import PairingGroup, ZR, GT, extract_key
from charm.toolbox.symcrypto import AuthenticatedCryptoAbstraction
from charm.core.engine.util import objectToBytes, bytesToObject

# Initialize CP-ABE
groupObj = PairingGroup('BN254')
cpabe = CPabe_SP21(groupObj)

def set_up(attributes):
    result = []
    for i in range(len(attributes)):
        for j in range(i + 1, len(attributes)):
            combined = f"{attributes[i]} {attributes[j]}"
            result.append(combined)
    return result

def choose_policy_name(choice):
    policy_names = {
        1: "LandOwnership_policy.txt",
        2: "Construction_policy.txt",
        3: "Property_policy.txt",
        4: "Agreement_policy.txt",
    }
    return policy_names.get(choice, "Invalid choice")

#user_input = int(input("Please choose a policy by entering a number (1-4): "))
#policy_name = choose_policy_name(user_input)
policy_name = "/var/www/storage/policy/Property_policy.txt"
# Define attribute universe
Attributes = ['ABC Real Estate Agency', 'Green Spaces', 'Thu Duc Peoples Committee', 'Property Manager', 'Legal Assistant', 'Architecture', 'Real Estate Brokers', 'Financial Experts', 'Chairman', 'Director Of Real Estate']
U = set_up(Attributes)
U += ['TAG']

def contains_list(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    return set2.issubset(set1)

def save_list_to_txt(file_name, string_list):
    with open(file_name, "w") as f:
        for item in string_list:
            f.write(item + "\n")

def load_list_from_txt(file_name):
    with open(file_name, "r") as f:
        string_list = [line.strip() for line in f.readlines()]
    return string_list

def generate_key():
    groupObj = PairingGroup('BN254')
    cpabe = CPabe_SP21(groupObj)
    rand_Obj = groupObj.random(GT)
    rand_bytes = objectToBytes(rand_Obj, groupObj)
    public_key_file = "/var/www/storage/keys/cpabe_key/public_key.bin"
    master_key_file = "/var/www/storage/keys/cpabe_key/master_key.bin"
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
    P = load_list_from_txt(policy_name)
    input_symmetric_key_gt = bytesToObject(rand_bytes, groupObj)
    # Encrypt the input symmetric key using the CP-ABE scheme
    ct = cpabe.encrypt(loaded_pk, input_symmetric_key_gt, P, U)
    # Save the encrypted symmetric key to a file
    encrypted_key_file = "/var/www/storage/keys/cpabe_key/encrypted_key.bin"
    with open(encrypted_key_file, 'wb') as f:
        f.write(objectToBytes(ct, groupObj))
    return rand_bytes[:32]
    
def generate_IV():
    groupObj = PairingGroup('BN254')
    cpabe = CPabe_SP21(groupObj)
    rand_Obj = groupObj.random(GT)
    rand_bytes = objectToBytes(rand_Obj, groupObj)
    public_key_file = "/var/www/storage/keys/cpabe_key/public_key.bin"
    master_key_file = "/var/www/storage/keys/cpabe_key/master_key.bin"
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
    P = load_list_from_txt(policy_name)
    input_symmetric_key_gt = bytesToObject(rand_bytes, groupObj)
    # Encrypt the input symmetric key using the CP-ABE scheme
    ct = cpabe.encrypt(loaded_pk, input_symmetric_key_gt, P, U)
    # Save the encrypted symmetric key to a file
    encrypted_key_file = "/var/www/storage/keys/cpabe_key/encrypted_IV.bin"
    with open(encrypted_key_file, 'wb') as f:
        f.write(objectToBytes(ct, groupObj))
    return rand_bytes[:12]	

	
	
def decrypt_key():
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
    file_name = "/var/www/storage/attribute/Attribute_list.txt"
    # Load the Attribute from a text file
    loaded_B = load_list_from_txt(file_name)
    B = set_up(loaded_B)
    P = load_list_from_txt(policy_name)
    result = contains_list(P, B)
    print(result)
    if result:
    	P += ['TAG']
    dk = cpabe.keygen(loaded_pk, loaded_mk, P, U)
    encrypted_key_file = "/var/www/storage/keys/cpabe_key/encrypted_key.bin"
    # Load the encrypted symmetric key from the file
    with open(encrypted_key_file, "rb") as f:
        loaded_ct = bytesToObject(f.read(), groupObj)
    # Decrypt the symmetric key using the CP-ABE scheme
    decrypted_key_gt = cpabe.decrypt(loaded_pk, dk, loaded_ct)
    decrypted_key_bytes = objectToBytes(decrypted_key_gt, groupObj)
    decrypted_key_bytes = decrypted_key_bytes[:32]
    return decrypted_key_bytes

def decrypt_IV():
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
    file_name = "/var/www/storage/attribute/Attribute_list.txt"
    # Load the Attribute from a text file
    loaded_B = load_list_from_txt(file_name)
    B = set_up(loaded_B)
    P = load_list_from_txt(policy_name)
    result = contains_list(P, B)
    print(result)
    if result:
    	P += ['TAG']
    dk = cpabe.keygen(loaded_pk, loaded_mk, P, U)
    encrypted_key_file = "/var/www/storage/keys/cpabe_key/encrypted_IV.bin"
    # Load the encrypted symmetric key from the file
    with open(encrypted_key_file, "rb") as f:
        loaded_ct = bytesToObject(f.read(), groupObj)
    # Decrypt the symmetric key using the CP-ABE scheme
    decrypted_key_gt = cpabe.decrypt(loaded_pk, dk, loaded_ct)
    decrypted_key_bytes = objectToBytes(decrypted_key_gt, groupObj)
    decrypted_key_bytes = decrypted_key_bytes[:12]
    return decrypted_key_bytes
