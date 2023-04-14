from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from flask_pymongo import PyMongo
from lib.aes_mode_gcm import encrypt, decrypt
import os

app = Flask(__name__, static_folder='static')

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG, ssl_context='secret')