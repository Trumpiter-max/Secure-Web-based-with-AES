from .base import *
from utils.aes_mode_gcm import encrypt, decrypt, create_key, create_iv
from utils.digital_signature import sign, verify, create_private_key, create_public_key, save_public_key
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
        
        # Some config for file upload
        file_hash = sha256_hash(file)
        file_name = generate_file_name(30)
        file_name_pdf = str(file_name) + '.pdf'
        time_save = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        author_name = session['user_name']
        filetitle = request.form.get('title')
        passcode = request.form.get('passcode')
        passcode = bytes(passcode, 'utf-8') # convert to bytes for encryption
        origin_file = file # backup origin file
        # Digital signature for file
        # Create key pair
        private_key = create_private_key()
        public_key = create_public_key(private_key)
        # Save public key to storage
        save_public_key(public_key, file_name)
        signed_file = sign(file, private_key)
        
        # Save to check later
        with open(os.path.join(DOCUMENT_PATH + 'signed/', file_name), 'wb') as save_file:
            save_file.write(signed_file)

        # Encrypt file with AES-GCM
        aes_key = create_key()
        aes_iv = create_iv()
        # Save encrypted file to storage
        encrypt(aes_key, aes_iv, passcode, file.read(), os.path.join(DOCUMENT_PATH + 'encrypted/', file_name))
        # Save origin file to storage
        origin_file.save(os.path.join(DOCUMENT_PATH + 'origin/', file_name_pdf))

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

@secure_blueprint.route("/download/<filename>")
def download(filename):
    file_name = request.form.get('filename')
    file_path = os.path.join(DOCUMENT_PATH + 'origin/', str(filename))
    send_file(file_path, as_attachment=True)
    flash('File downloaded successfully')
    return render_template("load.html")
