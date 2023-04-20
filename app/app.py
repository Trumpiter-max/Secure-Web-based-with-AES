from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import socket
from utils.aes_mode_gcm import encrypt, decrypt
import os

app = Flask(__name__, static_folder='static')
app.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGO_INITDB_ROOT_USERNAME'] + ':' + os.environ['MONGO_INITDB_ROOT_PASSWORD'] + '@' + os.environ['MONGO_HOST'] + ':27017/' + os.environ['MONGO_INITDB_DATABASE']
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
mongodb = PyMongo(app)


@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route('/todo')
def todo():
    _todos = mongodb.todo.find()
    item = {}
    data = []
    for todo in _todos:
        item = {
            'id': str(todo['_id']),
            'todo': todo['todo']
        }
        data.append(item)
    return jsonify(
        status=True,
        data=data
    )

@app.route('/todo', methods=['POST'])
def createTodo():
    data = request.get_json(force=True)
    item = {
        'todo': data['todo']
    }
    mongodb.todo.insert_one(item)
    return jsonify(
        status=True,
        message='To-do saved successfully!'
    ), 201

if __name__ == "__main__":
	env = os.environ.get('FLASK_ENV', 'production')
	port = int(os.environ.get('PORT', 5000))
	debug = False if env == 'production' else True
	app.run(host='0.0.0.0', port=port, debug=debug)