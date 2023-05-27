from .base import *
from utils.aes_mode_gcm import encrypt, decrypt
from werkzeug.utils import secure_filename

secure_blueprint = Blueprint('secure_blueprint', __name__, template_folder='templates', static_folder='static')

@secure_blueprint.route("/upload", methods = ['POST', 'GET'])
def upload():
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
        file_name = secure_filename(file.filename)
        time_save = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        author_name = session['user_name']
        file.save(os.path.join(DOCUMENT_PATH, file_name))

    return render_template("upload.html")

@secure_blueprint.route("/load", methods = ['POST', 'GET'])
def load():
    if not session.get('logged_in'):
        session['logged_in'] = False
    if session['logged_in'] != True:
        return redirect(url_for('user_blueprint.login'))
    return "Hello World!"