import unittest
from game.game_logic import GameState

class TestGameState(unittest.TestCase):
    
    def setUp(self) -> None:
        self.game = GameState()

    def test_init_state_is_menu(self):
        self.assertEqual(self.game.state,"menu") 