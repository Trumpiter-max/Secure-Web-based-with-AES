from .base import *

user_blueprint = Blueprint('user_blueprint', __name__, template_folder='templates')

@user_blueprint.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        db = get_db()
        users = db.users
        login_user = users.find_one({'username': request.form['username']})

        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == \
                    login_user['password'].encode('utf-8'):
                session['username'] = request.form['username']
                return redirect(url_for('index'))
        flash('Username and password combination is wrong')
        return redirect(url_for('register'))
    
    return render_template('login.html')

@user_blueprint.route("/register", methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        db = get_db()
        users = db.users
        register_user = users.find_one({'username': request.form['username']})

        if register_user:
            flash(request.form['username'] + ' username is already exist')
            return redirect(url_for('login'))
        
        hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(14))
        users.insert({'username': request.form['username'], 'password': hashed, 'email': request.form['email']})
        return redirect(url_for('login'))
    
    return render_template('register.html')

@user_blueprint.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@user_blueprint.route('/testdb')
def get_data():
    db = get_db()
    _animals = db.animal_tb.find()
    animals = [{"id": animal["id"], "name": animal["name"], "type": animal["type"]} for animal in _animals]
    return jsonify({"animals": animals})