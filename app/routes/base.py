from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory, Blueprint
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import socket
import os

def get_db():
    client = MongoClient(host='mongodb',
                        port=27017, 
                        username='admin', 
                        password='admin',
                        authSource="admin")
    db = client["sampledb"] # connect to database
    return db

