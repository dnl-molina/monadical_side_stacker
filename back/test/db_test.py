import sys, os
import unittest
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))
from db import Database

class DatabaseTest(unittest.TestCase):
    def test_connect(self):
        """check if db is available"""
        DATABASE_NAME="test.db"
        path=os.path.join(os.path.dirname(os.path.dirname(__file__)), DATABASE_NAME)
        if os.path.exists(path):os.remove(path)
        db=Database(DATABASE_NAME)
        db.query("create table if not exists game (id INTEGER PRIMARY KEY AUTOINCREMENT, user_a string, user_b string, winner string, board string);")
        self.assertEqual(os.path.exists(path), True)

    def test_insert(self):
        """check if could insert a new record in the database"""
        db=Database("test.db")
        db.query("insert into game (user_a, user_b, winner, board) values('a', 'b', 'sinner', 'asdf');");
        self.assertEqual(len(db.query("select * from game"))>=1, True)
        
    def test_select(self):
        """check if could make a select over the database"""
        db=Database("test.db")
        db.query("insert into game (user_a, user_b, winner, board) values('a', 'b', 'sinner', 'asdf');");
        items=db.query("select * from game")
        for item in items:
            if item["user_a"]=="a":
                self.assertEqual(True, True)
                return
        self.assertEqual(False, True)
        
if __name__ == '__main__':
    unittest.main()