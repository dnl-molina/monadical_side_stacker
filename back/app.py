import sys
import os
import threading

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from db import Database
from backsocket import start_server

def init_db():
    db=Database.get_instance()
    db.query("create table if not exists game(id INTEGER PRIMARY KEY AUTOINCREMENT, user_a string, user_b string, board string)")
    db.query("create table if not exists user(user string primary key)")

init_db()
start_server()
