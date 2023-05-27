from routes.base import *
from routes.general import general_blueprint
from routes.user import user_blueprint
from routes.secure import secure_blueprint
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv("APP_SECRET")
app.register_blueprint(general_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(secure_blueprint)


@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True)

