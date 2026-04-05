import unittest
from game.game_logic import GameState
from game.entities import Player
class TestGameState(unittest.TestCase):
    '''
        game states:
        0 - game_over
        1 - menu
        2 - started 
    '''    
    def setUp(self) -> None:
        self.game = GameState(state=1,player=Player(x=100,y=100,hp=1,speed=5,points=0))

    def test_init_state_is_menu(self):
        self.assertEqual(self.game.state,1) 

    def test_games_start(self):
        self.game.game_start()
        self.assertEqual(self.game.state,2)
    
    def test_game_over(self):
        self.game.player.take_damage(1)
        self.game.game_over()
        self.assertEqual(self.game.state,0)
    
    def test_neg_game_over(self):
        self.game.game_over()
        self.assertEqual(self.game.state,1)
    
    def test_game_restart(self):
        self.game.player.take_damage(1)
        self.game.game_over()
        self.game.game_restart()
        self.assertEqual(self.game.state,2)
    
    def test_neg_game_restart(self):
        self.game.game_restart()
        self.assertEqual(self.game.state,1)