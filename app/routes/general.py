from .base import *

general_blueprint = Blueprint('general_blueprint', __name__, template_folder='templates')

@general_blueprint.route("/")
def index():
    return render_template('index.html')

@general_blueprint.route("/about")
def about():
    return render_template('about.html')