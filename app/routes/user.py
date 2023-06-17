from .base import *
import hashlib
from datetime import timedelta, date, datetime

user_blueprint = Blueprint('user_blueprint', __name__, template_folder='templates', static_folder='static')

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
        hashed_password =sha256_hash(password)  
        check_password = login_user['password']
        
        if request.form['username'] == '' or request.form['password'] == '':
            flash('Please fill the blanks')
            return redirect(url_for('user_blueprint.login'))
        
        if login_user:
            if hashed_password == check_password:
                session['user_name'] = request.form['username']
                session['logged_in'] = True
                return redirect(url_for('general_blueprint.index'))
            
        flash('Username or password is wrong, try again')
        return redirect(url_for('user_blueprint.login'))  
    return render_template('login.html')

@user_blueprint.route("/register", methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        db = get_db()
        users = db.users
        register_user = users.find_one({'username': request.form['username']})

        if register_user:
            flash(request.form['username'] + ' is already exist')
            return redirect(url_for('user_blueprint.login'))
        
        hashed_password =sha256_hash(request.form['password'])
        userdictionary = {'username': request.form['username'], 'password': hashed_password, 'email': request.form['email'], 'fullname': 'Unknown', 'role': 'Unknown', 'organization': 'Unknown'}
        users.insert_one(userdictionary)
        flash('User registered successfully')
        return redirect(url_for('user_blueprint.login'))  
    return render_template('register.html')

@user_blueprint.route("/profile", methods = ['POST', 'GET'])
def profile():
    if request.method == 'GET':
        if not session.get('logged_in'):
            session['logged_in'] = False
        if session['logged_in'] != True:
            return redirect(url_for('user_blueprint.login'))
        
    db = get_db()
    users = db.users
    user = users.find_one({'username': session['user_name']})
    user_email = user['email']
    full_name = user['fullname']
    role = user['role']
    organization = user['organization']

    if request.method == 'POST':
        new_email = request.form['email']
        new_name = request.form['fullname']
        new_organization = request.form['organize']
        new_role = request.form['role']
        comfirm_password = request.form['password']

        if comfirm_password == '':
            flash('This change requires your password')
            return redirect(url_for('user_blueprint.profile'))
        hashed_password =sha256_hash(comfirm_password)

        if user['password'] == hashed_password:
            if new_email:
                users.update_one({'username': session['user_name']}, {'$set': {'email': new_email}})

            if new_name:
                users.update_one({'username': session['user_name']}, {'$set': {'fullname': new_name}})

            if new_organization:
                users.update_one({'username': session['user_name']}, {'$set': {'organization': new_organization}})
            
            if new_role:
                users.update_one({'username': session['user_name']}, {'$set': {'role': new_role}})

            flash('Changed successfully')
            return redirect(url_for('user_blueprint.profile'))
    return render_template('profile.html', user_email=user_email, full_name=full_name, role=role, organization=organization)

@user_blueprint.route('/logout')
def logout():
    if request.method == 'GET':
        if not session.get('logged_in'):
            session['logged_in'] = False
        if session['logged_in'] != True:
            return redirect(url_for('user_blueprint.login'))

    session.pop('user_name', None)
    session['logged_in'] = False
    flash('You have been logged out')
    return redirect(url_for('general_blueprint.index'))
