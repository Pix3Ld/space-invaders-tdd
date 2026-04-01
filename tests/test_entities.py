import unittest 

from game.entities import Player, Bullet, Enemy

class PlayerTestInit(unittest.TestCase):

    def setUp(self) -> None:
        self.player = Player(x=100,y=100,hp=3,speed=5,points=0,screen_width=800)
    
#=================testy gracza ==================#
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
    
    def test_left_boundry(self):
       
        self.player.x=0
        self.player.move_left()
        self.assertEqual(self.player.x,0)

    def test_right_boundry(self):
       
        self.player.x=100
        self.player.move_right()
        self.assertEqual(self.player.x,105)
    
    def test_near_right_boundry(self):
        
        self.player.x=797
        self.player.move_right()
        self.assertEqual(self.player.x,797)
    
    def test_near_left_boundry(self):
    
        self.player.x=3
        self.player.move_left()
        self.assertEqual(self.player.x,3)
    
    def test_player_dmg(self):
        
        self.player.take_damage(1)
        self.assertEqual(self.player.hp,2)
    
    def test_negative_dmg(self):

        self.player.hp=0
        self.player.take_damage(1)
        self.assertEqual(self.player.hp,0)

#=================testy pocisku ==================#
    def test_player_bullet(self):
        
        bullet = self.player.shoot()
        self.assertIsInstance(bullet, Bullet)

    def test_player_bullet_negative(self):
        
        self.player.hp=0
        bullet = self.player.shoot()
        self.assertIsNone(bullet)
        
    def test_bullet_owner(self):

        bullet = self.player.shoot()
        self.assertIsNotNone(bullet)
        self.assertEqual(bullet.owner,self.player)  # type: ignore

#=================testy resetu ==================#
    def test_player_reset(self):
        self.player.hp=0
        self.player.player_reset()
        self.assertEqual(self.player.x,100)
        self.assertEqual(self.player.y,100)
        self.assertEqual(self.player.hp,3)
        self.assertEqual(self.player.points,0)
    
    def test_negative_reset(self):
        self.player.hp=1
        self.player.points=100
        self.player.player_reset()
        self.assertEqual(self.player.x,100)
        self.assertEqual(self.player.y,100)
        self.assertEqual(self.player.hp,1)
        self.assertEqual(self.player.points,100)
    
#=================testy przeciwnika ==================#
class EnemyTestInit(unittest.TestCase):

    def setUp(self) -> None:
        self.enemy = Enemy(x=50,y=200,hp=1,speed=3,damage=1,diraction=1)
    
    def test_enemy_start_position(self):
        
        self.assertEqual(self.enemy.x,50)
        self.assertEqual(self.enemy.y,200)
    
    def test_enemy_health(self):
        self.assertEqual(self.enemy.hp,1)

    def test_enemy_speed(self):
        self.assertEqual(self.enemy.speed,3)
    
    def test_enemy_damage(self):
        self.assertEqual(self.enemy.damage,1)

    def test_enemy_down(self):
        self.enemy.hp=0
        self.assertTrue(self.enemy.enemy_down())
    
    def test_enemy_move_right(self):
        self.enemy.move_right()
        self.assertEqual(self.enemy.x,53)
    
    def test_neg_move_right(self):
        self.enemy.x=798
        self.enemy.move_right()
        self.assertEqual(self.enemy.x,798)

    def test_enemy_move_left(self):
        self.enemy.move_left()
        self.assertEqual(self.enemy.x,47)
    
    def test_neg_move_left(self):
        self.enemy.x=0
        self.enemy.move_left()
        self.assertEqual(self.enemy.x,0)
    
    def test_enemy_move_down(self):
        self.enemy.move_down()
        self.assertEqual(self.enemy.y,203)
    
    def test_neg_move_down(self):
        self.enemy.y=798
        self.enemy.move_down()
        self.assertEqual(self.enemy.y,798)

    def test_enemy_shoot(self):
        bullet = self.enemy.shoot()
        self.assertIsInstance(bullet,Bullet)

    def test_neg_shoot(self):
        self.enemy.hp=0
        bullet = self.enemy.shoot()
        self.assertIsNone(bullet)
    
    def test_enemy_move_diraction_right(self):
        self.enemy.diraction=1
        self.enemy.diraction_change()
        self.assertEqual(self.enemy.x,53)

    def test_enemy_move_diraction_left(self):
        self.enemy.diraction=-1
        self.enemy.diraction_change()
        self.assertEqual(self.enemy.x,47)

    def test_dead_enemy_diraction_change(self):
        self.enemy.hp=0
        self.enemy.diraction=1
        self.enemy.diraction_change()
        self.assertEqual(self.enemy.x,50)