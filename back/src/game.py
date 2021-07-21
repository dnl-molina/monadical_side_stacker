from dataclasses import dataclass
from db import Database
import json

BOARD_WIDTH=7
BOARD_HEIGHT=7
MARKS_FOR_WIN=4

"""Movements to check winner"""
INCREASES=[
    {"increase_x":1,"increase_y":1},
    {"increase_x":1,"increase_y":-1},
    {"increase_x":1,"increase_y":0},
    {"increase_x":0,"increase_y":1}
]
    

@dataclass
class Move:
    """Data class for save the movement of one user"""
    side:str="r"
    username:str=""
    mark:int=0
    board:int=0
    x:int=0
    y:int=0


@dataclass
class User:
    user:str=""
    def save(self):
        db=Database.get_instance()
        if len(db.query(f"select * from user where user='{self.user}'"))==0:
            usr={"user":self.user}
            db.insert("user", usr)
    
class Board:
    """Class for simulate the logic of the game, create the board, make movements and check if some user wins"""
    def __init__(self, board=None):
        if not board:
            self.board=[[0 for x in range(BOARD_WIDTH)] for l in range(BOARD_HEIGHT)]
        else:
            self.board=board
    
    def add_move(self, m):
        """make a stack move from the right side or left side over a row"""
        if m.side=="r":row=list(reversed(self.board[m.x]))
        else:row=self.board[m.x]
            
        new_row=[]
        new_row.append(m.mark)
        skipped=False
        for x in row:
            if x == 0 and not skipped:
                skipped=True
                continue
            new_row.append(x)
            if len(new_row)==BOARD_WIDTH:break
        
        if m.side=="r":self.board[m.x]=list(reversed(new_row))
        else:self.board[m.x]=new_row
        
    def check_move(self, m):
        """check the move(x,y) on the board"""
        self.board[m.x][m.y]=m.mark
    
    def check_winner(self, m):
        """check if the user with the specific mark won the game"""
        rows=[]
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                for increase in INCREASES:
                    if self.check_winner_closes(x, y, m.mark, 0,increase):
                        return True
        return False
    
    def is_in_bounds(self, x, y):
        """check if the position is in the bounds of the board"""
        return x in range(0,BOARD_WIDTH) and y in range(0,BOARD_HEIGHT)
    
    def check_winner_closes(self, x, y, mark, counter, increase):
        """check the nearest elements in all directions with the same mark"""
        if self.is_in_bounds(x,y) and self.board[x][y]==mark:
            x+=increase["increase_x"]
            y+=increase["increase_y"]
            counter+=1
            if counter==MARKS_FOR_WIN:return True
            return self.check_winner_closes(x,y,mark,counter,increase)
        else:
            return False
        
@dataclass
class Game:
    """Data class for save the movement of one user"""
    board:list=None
    user_a:str=""
    user_b:str=""
    
    def __post_init__(self):
        self.id=self.user_a+"."+self.user_b
        
    def save(self):
        game={"board":self.board, "user_a":self.user_a, "user_b":self.user_b, "id":self.id}
        Database.get_instance().insert("game", game)
        
    def update(self):
        Database.get_instance().query(f"update game set board='{json.dumps(self.board)}' where user_a='{self.user_a}' and user_b='{self.user_b}'")
