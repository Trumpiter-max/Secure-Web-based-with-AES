from .base import *
import hashlib
from datetime import timedelta, date, datetime

user_blueprint = Blueprint('user_blueprint', __name__, template_folder='templates')

def md5hash(data):
    return str(hashlib.md5(data.encode()).hexdigest())

def MakeSessionPermanent(expire_time):
    session.permanent = True
    user_blueprint.permanent_session_lifetime = timedelta(minutes=expire_time)

@user_blueprint.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        db = get_db()
        users = db.users
        login_user = users.find_one({'username': request.form['username']})
        password = request.form['password']
        hashed_password = md5hash(password)  
        check_password = login_user['password']
        
        if request.form['username'] == '' or request.form['password'] == '':
            flash('Please fill the blanks')
            return redirect(url_for('user_blueprint.login'))
        
        if login_user:
            if hashed_password == check_password:
                session['username'] = request.form['username']
                session['loggedin'] = True
                return redirect(url_for('general_blueprint.index'))
            
        flash('Username or password is wrong, try again')
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
            return redirect(url_for('user_blueprint.login'))
        
        hashed_password = md5hash(request.form['password'])
        userdictionary = {'username': request.form['username'], 'password': hashed_password, 'email': request.form['email']}
        users.insert_one(userdictionary)
        flash('User registered successfully')
        return redirect(url_for('user_blueprint.login'))  
    return render_template('register.html')

@user_blueprint.route('/logout')
def logout():
    session.pop('username', None)
    session['loggedin'] = False
    flash('You have been logged out')
    return redirect(url_for('general_blueprint.index'))
