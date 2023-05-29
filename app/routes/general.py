from .base import *

general_blueprint = Blueprint('general_blueprint', __name__, template_folder='templates', static_folder='static')

@general_blueprint.route("/")
def index():
    return render_template('index.html')

@general_blueprint.route("/about")
def about():
    return render_template('about.html')

@general_blueprint.route("/help")
def help():
    return render_template('help.html')

@general_blueprint.route("/test")
def test():
    return run_command("uname -a")