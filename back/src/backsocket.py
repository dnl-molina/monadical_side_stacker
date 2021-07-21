import asyncio
import websockets
import json
import threading
import logging
import os
import re
import sys
from game import Board, Move, Game, User
from db import Database

logging.basicConfig(filename=os.path.join(os.path.dirname(os.path.dirname(__file__)), "log/websocket.log"), level='INFO')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    
server=None
socketserver=None

class Server:
    """general purpose websocket class for manage all clients"""
    def __init__(self,server):
        self.sockets=[]
        self.server=server
        self.clients=[]

    def add(self, client):
        """add a client to the list of available clients for the socket"""
        try:
            for c in self.clients:
                if c["id"]==id(client):return
            dclient={"id":id(client), "client":client}
            self.clients.append(dclient)
            return dclient        
        except Exception as e:
            logging.error("Error when try to add client", exc_info=exc_info)
    
    async def send_message(self, client, d):
        """send a message to an specific client"""
        try:
            await self.send(client,d)        
        except Exception as e:
            logging.error("Error sending message", exc_info=exc_info)
                
    
    async def send(self, client, d):
        """send content to the client"""
        try:
            for c in self.clients:
                if c["id"]==client["id"]:
                    if not c["client"].closed:
                        logging.debug("se va a enviar el mensaje")
                        await c["client"].send(d)
                    else:
                        logging.debug("el cliente esta cerrado")                
        except Exception as e:
            logging.error("Error sending info", exc_info=exc_info)
    
    async def send_all(self, d):
        """send info to all users"""
        try:
            for c in self.clients:
                try:
                    await c["client"].send(json.dumps(d))                
                except:pass
        except Exception as e:
            logging.error("error when try to send info to all users", exc_info=exc_info)
        

class GameServer(Server):
    """class for deal with game actions over websocket like: login, movements, ask to the user if he want to play with another user..."""
    def __init__(self, server):
        super().__init__(server)
    
    async def reset(self, client, info):
        """reset the game"""
        try:
            db=Database().get_instance()
            blank_board=Board().board
            id_board=info.get("id")
            db.query(f"update game set board='{json.dumps(blank_board)}' where id={id_board}")
            game=db.query(f"select * from game where id={id_board}")[0]
            game["board"]=json.loads(game.get("board"))
            await server.send_all(game)                
        except Exception as e:
            logging.error("error when try to reset the game", exc_info=exc_info)
    
    async def login(self, client, info):
        """send all users to others users"""
        try:
            db=Database().get_instance()
            
            u=User()
            u.user=info.get("username")
            u.save()
            
            users=db.query("select * from user")
            await server.send_all({"users":users})
            
        except Exception as e:
            logging.error("error when the user make a new move in the game", exc_info=exc_info)
            
    async def move(self, client, info):
        """make a movement into the game"""
        try:
            db=Database().get_instance()
            game=db.query("select * from game where id="+info.get("id"))[0]
            matrix_board=json.loads(game.get("board").replace("None","0"))
            board=Board(matrix_board)
            move=Move(side=info.get("side"), mark=info.get("mark"), x=info.get("row"))
            board.add_move(move)
            win=board.check_winner(move)
            g=Game(user_a=game.get("user_a"), user_b=game.get("user_b"), board=board.board)
            g.update()
            await server.send_all({"id":game.get("id"),"command":"move", "user_a":g.user_a, "user_b":g.user_b, "board":g.board,"win":win,"winner_mark":info.get("mark") if win else "","mark":info.get("mark")})
        except Exception as e:
            logging.error("error when the user make a new move in the game", exc_info=exc_info)
   
async def read_message(websocket, path):
    try:
        global server
        client = server.add(websocket)
        try:
            async for message in websocket:
                d = json.loads(message)
                await message_received(client,server,d)
        except:pass                
    except Exception as e:
        logging.error("error on read_message", exc_info=exc_info)
    

async def message_received(client, server, d):
    try:
        logging.info(d)
        username=d.get("username")
        if d.get("command")=="move":await server.move(client, d)
        if d.get("command")=="reset":await server.reset(client, d)
        if d.get("command")=="login":await server.login(client, d)
    except Exception as e:
        logging.error("error on read_message", exc_info=exc_info)
        
def start_server():
    try:
        global server
        global socketserver
        socketserver = websockets.serve(read_message, "0.0.0.0", 3002)
        server=GameServer(socketserver)
        
        loop=asyncio.get_event_loop()
        loop.run_until_complete(socketserver)
        loop.run_forever()                
    except Exception as e:
        logging.error("error on start_server", exc_info=exc_info)
    
if __name__ == '__main__':
    start_server()
    