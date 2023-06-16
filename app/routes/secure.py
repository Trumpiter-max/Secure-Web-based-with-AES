from .base import *
from utils.aes_mode_gcm import encrypt, decrypt, create_key, create_iv
from utils.digital_signature import sign, verify, create_private_key, create_public_key, save_public_key, read_public_key
from utils.funcCPABE import decrypt_IV, decrypt_key
from werkzeug.utils import secure_filename

secure_blueprint = Blueprint('secure_blueprint', __name__, template_folder='templates', static_folder='static')

@secure_blueprint.route("/upload", methods = ['POST', 'GET'])
def upload():
    if request.method == 'GET':
        if not session.get('logged_in'):
            session['logged_in'] = False
        if session['logged_in'] != True:
            return redirect(url_for('user_blueprint.login'))
    
    if request.method == 'POST':
        # Handle file upload
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if not file.filename:
            return redirect(request.url)
        if not file.filename.lower().endswith('.pdf'):
            flash('Only PDF files are allowed')
            return redirect(request.url)
        
        # Save origin file to storage
        file_name = generate_file_name(40)
        file.filename = file_name + '.pdf'
        with open(os.path.join(DOCUMENT_PATH + 'origin/', secure_filename(file.filename)), 'wb') as origin_file:
            origin_file.write(file.read())

        # Some config for file upload
        file_hash = sha256_hash(file)
        time_save = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        author_name = session['user_name']

        # Addition information for file
        filetitle = request.form.get('title')
        passcode = request.form.get('passcode')
        passcode = bytes(passcode, 'utf-8') # convert to bytes for encryption
        
        # Digital signature for file
        # Create key pair
        private_key = create_private_key()
        public_key = create_public_key(private_key)
        # Save public key to storage
        save_public_key(public_key, file_name)
        signed_file = sign(file, private_key)
        
        with open(os.path.join(DOCUMENT_PATH + 'origin/', secure_filename(file.filename)), 'rb') as file_check:
            signed_file = sign(file_check, private_key)
            # Save to check later
            with open(os.path.join(DOCUMENT_PATH + 'signed/', file_name), 'wb') as save_file:
                save_file.write(signed_file)

        # Encrypt file with AES-GCM
        aes_key = create_key(file_name)
        aes_iv = create_iv(file_name)
        # Save encrypted file to storage
        with open("/var/www/storage/documents/origin/" + secure_filename(file.filename), "rb") as file_data:
            encrypt(aes_key, aes_iv, passcode, file_data.read(), os.path.join(DOCUMENT_PATH + 'encrypted/', file_name))

        # Save to database
        db = get_db()
        documents = db.documents
        file_data = {'title': filetitle, 'filename': file_name, 'author': author_name, 'time': time_save, 'hash': file_hash}
        documents.insert_one(file_data)
        flash('File uploaded successfully')
    return render_template("upload.html")

@secure_blueprint.route("/load", methods = ['POST', 'GET'])
def load():
    if request.method == 'GET':
        if not session.get('logged_in'):
            session['logged_in'] = False
        if session['logged_in'] != True:
            return redirect(url_for('user_blueprint.login'))
    
    db = get_db()
    documents = db.documents.find()

    return render_template("load.html", documents=documents)

@secure_blueprint.route("/download", methods = ['POST', 'GET'])
def download():
    # Get the passcode from the form
    filename = request.args.get('filename')
    passcode = request.args.get('passcode')

    if passcode and filename:
        passcode = bytes(passcode, 'utf-8')  # convert to bytes for decryption
        # Load encrypted file from storage
        encrypted_file_path = os.path.join(DOCUMENT_PATH + 'encrypted/', str(filename))
        with open(encrypted_file_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()
            
        db = get_db()
        role = db.users.find_one({'username': session['user_name']})['role'] 
        organization = db.users.find_one({'username': session['user_name']})['organization']
        
        try:
            # Decrypt the file
            aes_key = decrypt_key(str(role), str(organization), str(filename))
            aes_iv = decrypt_IV(str(role), str(organization), str(filename))
            with open(os.path.join(DOCUMENT_PATH + 'encrypted/', str(filename) + '_auth'), 'rb') as auth_data:
                auth_tag = auth_data.read()
            recovered_path = os.path.join(TEMP_PATH + 'recovered/', secure_filename(str(filename) + '.pdf'))
            decrypted_data = decrypt(aes_key, aes_iv, auth_tag, passcode, encrypted_data, recovered_path)
        except:
            flash('Seems this file is not for you')
            return redirect(url_for('secure_blueprint.load'))

        # Load signed file from storage
        signed_file_path = os.path.join(DOCUMENT_PATH + 'signed/', str(filename))
        with open(signed_file_path, 'rb') as signed_file:
            signed_data = signed_file.read()

        
        with open(os.path.join(TEMP_PATH + 'recovered/', secure_filename(str(filename) + '.pdf')), 'rb') as recovered_file:
            try:
                # Load public key from storage
                public_key_data = read_public_key(os.path.join('/var/www/storage/keys/sign_key', str(filename) + '.pem')) 
                # Verify the digital signature
                is_verified = verify(recovered_file, signed_data, public_key_data)
                if not is_verified:
                    flash(is_verified)
                    return redirect(url_for('secure_blueprint.load'))
            except:
                flash('File integrity check failed. The file has been modified')
                return redirect(url_for('secure_blueprint.load'))

        # Save the decrypted file to a temporary directory
        temp_decrypted_file_path = os.path.join(TEMP_PATH + 'final/', secure_filename(str(filename) + '.pdf'))
        with open(temp_decrypted_file_path, 'wb') as temp_decrypted_file:
            temp_decrypted_file.write(decrypted_data)
        # Send the decrypted file as an attachment
        send_file(temp_decrypted_file_path, as_attachment=True)
        # Remove the temporary decrypted file
        os.remove(temp_decrypted_file_path)
        flash('File downloaded successfully')
        # return redirect(url_for('secure_blueprint.load'))
    
    return redirect(url_for('secure_blueprint.load'))


