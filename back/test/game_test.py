import sys, os
import unittest
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))
from game import Move, Board

class BoardTest(unittest.TestCase):
    def test_vertical_winner(self):
        """check winner when user puts four marks over vertical"""
        board=Board()
        board.check_move(Move(x=0,y=0,mark=2))
        board.check_move(Move(x=0,y=1,mark=2))
        board.check_move(Move(x=0,y=2,mark=2))
        board.check_move(Move(x=0,y=3,mark=2))
        self.assertEqual(board.check_winner(Move(mark=2)), True)

    def test_horizontal_winner(self):
        """check winner when user puts four marks over horizontal"""
        board=Board()
        board.check_move(Move(x=0,y=0,mark=1))
        board.check_move(Move(x=1,y=0,mark=1))
        board.check_move(Move(x=2,y=0,mark=1))
        board.check_move(Move(x=3,y=0,mark=1))
        self.assertEqual(board.check_winner(Move(mark=1)), True)
    
    def test_first_diagonal_winner(self):
        """check winner when user puts four marks over the main diagonal"""
        board=Board()
        board.check_move(Move(x=0,y=0,mark=2))
        board.check_move(Move(x=1,y=1,mark=2))
        board.check_move(Move(x=2,y=2,mark=2))
        board.check_move(Move(x=3,y=3,mark=2))
        self.assertEqual(board.check_winner(Move(mark=2)), True)
        
    def test_second_diagonal_winner(self):
        """check winner when user puts four marks over the second diagonal"""
        board=Board()
        board.check_move(Move(x=0,y=6,mark=2))
        board.check_move(Move(x=1,y=5,mark=2))
        board.check_move(Move(x=2,y=4,mark=2))
        board.check_move(Move(x=3,y=3,mark=2))
        self.assertEqual(board.check_winner(Move(mark=2)), True)
    
    def test_vertical_move(self):
        """check neither winner over vertical"""
        board=Board()
        board.check_move(Move(x=0,y=0,mark=2))
        board.check_move(Move(x=0,y=1,mark=2))
        board.check_move(Move(x=0,y=3,mark=2))
        self.assertEqual(board.check_winner(Move(mark=2)), False)

    def test_horizontal_move(self):
        """check neither winner over horizontal"""
        board=Board()
        board.check_move(Move(x=0,y=0,mark=1))
        board.check_move(Move(x=1,y=0,mark=1))
        board.check_move(Move(x=3,y=0,mark=1))
        self.assertEqual(board.check_winner(Move(mark=1)), False)
        
    def test_first_diagonal_move(self):
        """check neither winner over main diagonal"""
        board=Board()
        board.check_move(Move(x=0,y=0,mark=2))
        board.check_move(Move(x=1,y=1,mark=2))
        board.check_move(Move(x=3,y=3,mark=2))
        self.assertEqual(board.check_winner(Move(mark=2)), False)
        
    def test_second_diagonal_move(self):
        """check neither winner over second diagonal"""
        board=Board()
        board.check_move(Move(x=0,y=6,mark=2))
        board.check_move(Move(x=1,y=5,mark=2))
        board.check_move(Move(x=2,y=4,mark=2))
        self.assertEqual(board.check_winner(Move(mark=2)), False)
        
    def test_move_right(self):
        """check stack behavior when user puts mark on the right side"""
        board=Board()
        board.add_move(Move(side="r", x=0, mark=1))
        board.add_move(Move(side="r", x=0, mark=1))
        board.add_move(Move(side="r", x=0, mark=1))
        board.add_move(Move(side="r", x=0, mark=1))
        board.add_move(Move(side="l", x=0, mark=1))
        board.add_move(Move(side="r", x=0, mark=2))
        print(board.board[0])
        self.assertEqual(board.board[0]==[1,0,1,1,1,1,2], True)
    
    def test_game_winner_a(self):
        """check when player a wins"""
        board=Board()
        board.add_move(Move(side="l", x=0, mark=1))
        board.add_move(Move(side="l", x=0, mark=1))
        board.add_move(Move(side="l", x=0, mark=1))
        board.add_move(Move(side="l", x=0, mark=1))
        board.add_move(Move(side="l", x=0, mark=1))
        board.add_move(Move(side="r", x=0, mark=2))
        self.assertEqual(board.check_winner(Move(mark=1)), True)
        
    def test_game_winner_b(self):
        """check when player b wins"""
        board=Board()
        board.add_move(Move(side="r", x=1, mark=2))
        board.add_move(Move(side="r", x=1, mark=2))
        board.add_move(Move(side="r", x=1, mark=2))
        board.add_move(Move(side="r", x=1, mark=2))
        board.add_move(Move(side="l", x=1, mark=1))
        board.add_move(Move(side="r", x=1, mark=2))
        self.assertEqual(board.check_winner(Move(mark=2)), True)
        
    def test_game_no_winner(self):
        """check when neither wins"""
        board=Board()
        board.add_move(Move(side="r", x=2, mark=2))
        board.add_move(Move(side="l", x=2, mark=2))
        board.add_move(Move(side="r", x=2, mark=1))
        board.add_move(Move(side="l", x=2, mark=1))
        board.add_move(Move(side="r", x=2, mark=1))
        board.add_move(Move(side="r", x=2, mark=2))
        self.assertEqual(board.check_winner(Move(mark=1)) or board.check_winner(Move(mark=2)), False)
    
if __name__ == '__main__':
    unittest.main()