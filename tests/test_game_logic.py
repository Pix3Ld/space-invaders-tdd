import os
import unittest
from game.game_logic import GameState,WaveMenager,ScoreManager,CollisionHandler
from game.entities import Player ,Enemy,Bullet,Barrier

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

class TestWaveMenager(unittest.TestCase):

    def setUp(self) -> None:
        self.enemies=[
            Enemy(x=100,y=100,hp=1,speed=5,screen_width=800,screen_height=800),
            Enemy(x=200,y=100,hp=1,speed=5,screen_width=800,screen_height=800),
            Enemy(x=100,y=200,hp=1,speed=5,screen_width=800,screen_height=800),
            Enemy(x=200,y=200,hp=1,speed=5,screen_width=800,screen_height=800)
        ]
        self.wave = WaveMenager(enemies=self.enemies)
    
    def test_wave_has_four_enemies(self):
        self.assertEqual(len(self.wave.enemies),4)
    
    def test_wave_direction(self):
        self.assertEqual(self.wave.direction,1)
    
    def test_enemy_right_movement(self):
        self.wave.move()
        self.assertEqual(self.wave.enemies[0].x,105)
        self.assertEqual(self.wave.enemies[1].x,205)
        self.assertEqual(self.wave.enemies[2].x,105)
        self.assertEqual(self.wave.enemies[3].x,205)
    
    def test_enemy_left_movement(self):
        self.wave.direction = -1
        self.wave.move()
        self.assertEqual(self.wave.enemies[0].x,95)
        self.assertEqual(self.wave.enemies[1].x,195)
        self.assertEqual(self.wave.enemies[2].x,95)
        self.assertEqual(self.wave.enemies[3].x,195)

    def test_wave_direction_changes_at_right_edge(self):
        for enemy in self.enemies:
            enemy.x = 800
        self.wave.move()
        self.assertEqual(self.wave.direction, -1)  # kierunek zmieniony

    def test_wave_direction_changes_at_left_edge(self):
        self.wave.direction = -1
        for enemy in self.enemies:
            enemy.x = 0
        self.wave.move()
        self.assertEqual(self.wave.direction, 1)  # kierunek zmieniony

    def test_wave_moves_down_at_edge(self):
        for enemy in self.enemies:
            enemy.x = 797
        old_y = self.enemies[0].y
        self.wave.move()
        self.assertEqual(self.enemies[0].y, old_y + 5)


class TestScoreManager(unittest.TestCase):

    def setUp(self):
        self.score = ScoreManager(filename="test_scores.txt")
    
    def tearDown(self):
        if os.path.exists("test_scores.txt"):
            os.remove("test_scores.txt")

    def test_initial_score_is_zero(self):
        
        self.assertEqual(self.score.current_score, 0)

    def test_add_points(self):
        
        self.score.add_points(100)
        self.assertEqual(self.score.current_score, 100)

    def test_reset_score(self):
        
        self.score.add_points(100)
        self.score.reset()
        self.assertEqual(self.score.current_score, 0)

    def test_save_and_load_high_score(self):

        self.score.add_points(500)
        self.score.save()
        loaded = self.score.load()
        self.assertEqual(loaded, 500)
        
    def test_load_returns_zero_when_no_file(self):
        loaded = self.score.load()
        self.assertEqual(loaded, 0)

class TestCollisionHandler(unittest.TestCase):

    def setUp(self):
        self.handler = CollisionHandler()
        self.player = Player(x=100, y=500, hp=3, speed=5, points=0)
        self.enemy = Enemy(x=100, y=500, hp=1, speed=3)
        self.bullet = Bullet(x=100, y=500, speed=10, damage=1, direction=1, owner=self.player)
        self.barrier = Barrier(x=100, y=400, hp=3, width=50, height=20)

    def test_bullet_hits_enemy(self):
        result = self.handler.bullet_hits_entity(self.bullet, self.enemy)
        self.assertTrue(result)

    def test_bullet_misses_enemy(self):
        self.bullet.x = 999
        result = self.handler.bullet_hits_entity(self.bullet, self.enemy)
        self.assertFalse(result)
    
    def test_bullet_hits_player(self):
        outcome = self.handler.bullet_hits_entity(self.bullet,self.player)
        self.assertTrue(outcome)