from db import Database
from flask_cors import CORS
from game import User,Game
from db import Database
import os
import sys
import logging
from flask import Flask, jsonify, request

app = Flask(__name__)
CORS(app)

logging.basicConfig(filename=os.path.join(os.path.dirname(os.path.dirname(__file__)), "log/api.log"), level='INFO')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

@app.route("/users", methods=['GET'])
def users():
    try:
        db=Database.get_instance()
        return jsonify(db.query("select * from user"))        
    except Exception as e:
        logging.error("error when query for users", exc_info=exc_info)
        return jsonify({"ok":False,"error":str(e)})
    
@app.route("/login", methods=['POST'])
def login():
    try:
        username=request.json.get('user')
        u=User()
        u.user=username
        u.save()
        return jsonify({"ok":True})        
    except Exception as e:
        logging.error("error when register new user", exc_info=exc_info)
        return jsonify({"ok":False,"error":str(e)})
    
@app.route("/game", methods=['POST'])
def game():
    try:
        data=request.json
        user_a=data.get('user_a')
        user_b=data.get('user_b')
        db=Database.get_instance()
        games=db.query(f"select * from game where user_a='{user_a}' and user_b='{user_b}' or user_a='{user_b}' and user_b='{user_a}'")
        if len(games)==0:
            g=Game(user_a=user_a, user_b=user_b, board=[[0 for x in range(7)] for l in range(7)])
            g.save()
        
        games=db.query(f"select * from game where user_a='{user_a}' and user_b='{user_b}' or user_a='{user_b}' and user_b='{user_a}'")
        return jsonify(games[0])   
    except Exception as e:
        logging.error("error when update or start a new game", exc_info=exc_info)
        return jsonify({"ok":False,"error":str(e)})
    
if __name__ == '__main__':
    app.run(port=3001, host="0.0.0.0")