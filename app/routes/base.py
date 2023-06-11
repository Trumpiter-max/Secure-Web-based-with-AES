# This file contains the base routes for the application
# Base libraries
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory, Blueprint
# Used to connect to database
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
# Used to save log file without web server
# from logging.config import dictConfig
from datetime import datetime
import socket
import os, subprocess
import re
import hashlib
import random, string

# Some defined variables

DOCUMENT_PATH = "/var/www/storage/documents/"
TEMP_PATH = "var/www/storage/temp/"

# Config logging

# config log format file for flask without using gunicorn
'''
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s | %(module)s] %(message)s",
                "datefmt": "%B %d, %Y %H:%M:%S %Z",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "file": {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'debug.log',
                'maxBytes': 4194304, 
                'backupCount': 10,
                'level': 'DEBUG',
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console", "file"]},
    }
)
'''

# Some helpful functions

def get_db():
    client = MongoClient(host='mongodb',
                        port=27017, 
                        username='admin', 
                        password='admin',
                        authSource="admin")
    db = client["sampledb"] # connect to database
    return db

def validate_input(input):
    regex = r"(\s*([\0\b\'\"\n\r\t\%\_\\]*\s*(((select\s*.+\s*from\s*.+)|(select\s*.+\s*if\s*.+)|(union\s*.+\s*select\s*.+)|(insert\s*.+\s*into\s*.+)|(update\s*.+\s*set\s*.+)|(delete\s*.+\s*from\s*.+)|(drop\s*.+)|(truncate\s*.+)|(\s*.+#|--)|(alter\s*.+)|(exec\s*.+)|(\s*(all|any|not|and|between|in|like|or|some|contains|containsall|containskey|where|sleep|waitfor|delay)\s*.+[\=\>\<=\!\~]+.+)|(let\s+.+[\=]\s*.*)|(begin\s*.*\s*end)|(\s*[\/\*]+\s*.*\s*[\*\/]+)|(\s*(\-\-)\s*.*\s+)|(\s*(contains|containsall|containskey)\s+.*)))(\s*[\;]\s*)*)+)"
    if re.match(regex, input):
        return False
    return True

def sha256_hash(data):
    if (type(data) == str):
        return str(hashlib.sha256(data.encode('UTF-8')).hexdigest())
    else:
        sha256_hash = hashlib.sha256()
        for byte_block in iter(lambda: data.read(4096),b""):
            sha256_hash.update(byte_block)
    return str(sha256_hash.hexdigest())

def run_command(command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()

def generate_file_name(length):
    letters = string.ascii_lowercase + string.digits
    filename = ''.join(random.choice(letters) for i in range(length))
    return filename