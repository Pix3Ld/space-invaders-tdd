import unittest 

from game.entities import Player

class PlayerTestInit(unittest.TestCase):

    def setUp(self) -> None:
        self.player = Player(x=100,y=100,hp=3,speed=5)
    
#=================testy==================#
    def test_player_start_position(self):
        self.assertEqual(self.player.x,100)
        self.assertEqual(self.player.y,100)

    def test_player_health(self):
        self.assertEqual(self.player.hp,3)

    def test_player_speed(self):
        self.assertEqual(self.player.speed,5)
    
    def test_player_is_alive(self):
        self.assertTrue(self.player.is_alive())
    
    def test_player_left_position(self):
        self.player.move_left()
        self.assertEqual(self.player.x,95)

    def test_player_right_position(self):
        self.player.move_right()
        self.assertEqual(self.player.x,105)
