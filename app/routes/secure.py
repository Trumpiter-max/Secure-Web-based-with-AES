from .base import *
from utils.aes_mode_gcm import encrypt, decrypt

secure_blueprint = Blueprint('secure_blueprint', __name__, template_folder='templates')

@secure_blueprint.route("/upload", methods = ['POST', 'GET'])
def upload():
    if session['loggedin'] != True:
        return redirect(url_for('user_blueprint.login'))
    return render_template("upload.html")