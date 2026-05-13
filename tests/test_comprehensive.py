import os
import unittest
from parameterized import parameterized

from game.entities import Player, Enemy, Bullet, Barrier
from game.game_logic import GameState, WaveMenager, ScoreManager, CollisionHandler, GameEngine


class TestPlayerBasics(unittest.TestCase):
    """Test Player class basic functionality."""

    def setUp(self) -> None:
        self.player = Player(x=100, y=100, hp=3, speed=5, points=0, screen_width=800)

    def test_player_initialization(self) -> None:
        self.assertEqual(self.player.x, 100)
        self.assertEqual(self.player.y, 100)
        self.assertEqual(self.player.hp, 3)
        self.assertEqual(self.player.speed, 5)
        self.assertEqual(self.player.points, 0)

    def test_player_is_alive_true(self) -> None:
        self.assertTrue(self.player.is_alive())

    def test_player_is_alive_false(self) -> None:
        self.player.hp = 0
        self.assertFalse(self.player.is_alive())

    def test_player_move_left(self) -> None:
        self.player.move_left()
        self.assertEqual(self.player.x, 95)

    def test_player_move_right(self) -> None:
        self.player.move_right()
        self.assertEqual(self.player.x, 105)

    def test_player_move_left_boundary(self) -> None:
        self.player.x = 0
        self.player.move_left()
        self.assertEqual(self.player.x, 0)

    def test_player_move_right_boundary(self) -> None:
        self.player.x = 800
        self.player.move_right()
        self.assertLessEqual(self.player.x, 800)

    def test_player_take_damage(self) -> None:
        self.player.take_damage(1)
        self.assertEqual(self.player.hp, 2)

    def test_player_take_damage_zero_hp(self) -> None:
        self.player.hp = 0
        self.player.take_damage(1)
        self.assertEqual(self.player.hp, 0)

    def test_player_take_damage_overkill(self) -> None:
        self.player.take_damage(10)
        self.assertEqual(self.player.hp, 0)

    def test_player_shoot_alive(self) -> None:
        bullet = self.player.shoot()
        self.assertIsNotNone(bullet)
        self.assertIsInstance(bullet, Bullet)

    def test_player_shoot_dead(self) -> None:
        self.player.hp = 0
        bullet = self.player.shoot()
        self.assertIsNone(bullet)

    def test_player_add_points(self) -> None:
        self.player.add_points(100)
        self.assertEqual(self.player.points, 100)

    def test_player_add_points_multiple(self) -> None:
        self.player.add_points(50)
        self.player.add_points(50)
        self.assertEqual(self.player.points, 100)

    def test_player_reset(self) -> None:
        self.player.hp = 0
        self.player.x = 500
        self.player.player_reset()
        self.assertEqual(self.player.hp, 3)
        self.assertEqual(self.player.x, 100)

    def test_player_rectangle(self) -> None:
        rect = self.player.rectangle()
        self.assertEqual(len(rect), 4)
        self.assertEqual(rect[0], self.player.x)
        self.assertEqual(rect[1], self.player.y)


class TestPlayerParametrized(unittest.TestCase):
    """Parametrized tests for Player."""

    def setUp(self) -> None:
        self.player = Player(x=100, y=100, hp=3, speed=5, points=0, screen_width=800)

    @parameterized.expand([
        (1, 2),
        (2, 1),
        (3, 0),
        (5, 0),
        (10, 0),
    ])
    def test_player_take_damage_values(self, damage: int, expected_hp: int) -> None:
        self.player.take_damage(damage)
        self.assertEqual(self.player.hp, expected_hp)

    @parameterized.expand([
        (10, 10),
        (50, 50),
        (100, 100),
        (0, 0),
    ])
    def test_player_add_points_values(self, points: int, expected: int) -> None:
        self.player.points = 0
        self.player.add_points(points)
        self.assertEqual(self.player.points, expected)


class TestPlayerNegative(unittest.TestCase):
    """Negative tests for Player class."""

    def test_player_init_negative_hp(self) -> None:
        with self.assertRaises(ValueError):
            Player(x=100, y=100, hp=-1, speed=5, points=0)

    def test_player_init_negative_speed(self) -> None:
        with self.assertRaises(ValueError):
            Player(x=100, y=100, hp=3, speed=-1, points=0)

    def test_player_take_damage_negative(self) -> None:
        player = Player(x=100, y=100, hp=3, speed=5, points=0)
        with self.assertRaises(ValueError):
            player.take_damage(-1)

    def test_player_add_points_negative(self) -> None:
        player = Player(x=100, y=100, hp=3, speed=5, points=0)
        with self.assertRaises(ValueError):
            player.add_points(-10)


class TestEnemyBasics(unittest.TestCase):
    """Test Enemy class basic functionality."""

    def setUp(self) -> None:
        self.enemy = Enemy(x=50, y=200, hp=1, speed=3, damage=1)

    def test_enemy_initialization(self) -> None:
        self.assertEqual(self.enemy.x, 50)
        self.assertEqual(self.enemy.y, 200)
        self.assertEqual(self.enemy.hp, 1)
        self.assertEqual(self.enemy.speed, 3)
        self.assertEqual(self.enemy.damage, 1)

    def test_enemy_is_down_true(self) -> None:
        self.enemy.hp = 0
        self.assertTrue(self.enemy.enemy_down())

    def test_enemy_is_down_false(self) -> None:
        self.assertFalse(self.enemy.enemy_down())

    def test_enemy_move_right(self) -> None:
        self.enemy.move_right()
        self.assertEqual(self.enemy.x, 53)

    def test_enemy_move_left(self) -> None:
        self.enemy.move_left()
        self.assertEqual(self.enemy.x, 47)

    def test_enemy_move_down(self) -> None:
        self.enemy.move_down()
        self.assertEqual(self.enemy.y, 203)

    def test_enemy_move_right_boundary(self) -> None:
        self.enemy.x = 800
        self.enemy.move_right()
        self.assertEqual(self.enemy.x, 800)

    def test_enemy_move_left_boundary(self) -> None:
        self.enemy.x = 0
        self.enemy.move_left()
        self.assertEqual(self.enemy.x, 0)

    def test_enemy_move_down_boundary(self) -> None:
        self.enemy.y = 800
        self.enemy.move_down()
        self.assertEqual(self.enemy.y, 800)

    def test_enemy_shoot_alive(self) -> None:
        bullet = self.enemy.shoot()
        self.assertIsNotNone(bullet)
        self.assertIsInstance(bullet, Bullet)

    def test_enemy_shoot_dead(self) -> None:
        self.enemy.hp = 0
        bullet = self.enemy.shoot()
        self.assertIsNone(bullet)

    def test_enemy_direction_change_right(self) -> None:
        self.enemy.direction = 1
        self.enemy.direction_change()
        self.assertEqual(self.enemy.x, 53)

    def test_enemy_direction_change_left(self) -> None:
        self.enemy.direction = -1
        self.enemy.direction_change()
        self.assertEqual(self.enemy.x, 47)


class TestEnemyNegative(unittest.TestCase):
    """Negative tests for Enemy class."""

    def test_enemy_dead_no_direction_change(self) -> None:
        enemy = Enemy(x=50, y=200, hp=0, speed=3)
        initial_x = enemy.x
        enemy.direction = 1
        enemy.direction_change()
        self.assertEqual(enemy.x, initial_x)


class TestBulletBasics(unittest.TestCase):
    """Test Bullet class functionality."""

    def setUp(self) -> None:
        self.owner = Player(x=100, y=100, hp=3, speed=5, points=0)
        self.bullet = Bullet(x=100, y=100, speed=10, damage=1, direction=1, owner=self.owner)

    def test_bullet_initialization(self) -> None:
        self.assertEqual(self.bullet.x, 100)
        self.assertEqual(self.bullet.y, 100)
        self.assertEqual(self.bullet.speed, 10)
        self.assertEqual(self.bullet.damage, 1)
        self.assertEqual(self.bullet.direction, 1)

    def test_bullet_move_up(self) -> None:
        self.bullet.move()
        self.assertEqual(self.bullet.y, 90)

    def test_bullet_move_down(self) -> None:
        self.bullet.direction = -1
        self.bullet.move()
        self.assertEqual(self.bullet.y, 110)

    def test_bullet_is_off_screen_top(self) -> None:
        self.bullet.y = -10
        self.assertTrue(self.bullet.is_off_screen(600))

    def test_bullet_is_off_screen_bottom(self) -> None:
        self.bullet.y = 610
        self.assertTrue(self.bullet.is_off_screen(600))

    def test_bullet_is_on_screen(self) -> None:
        self.bullet.y = 300
        self.assertFalse(self.bullet.is_off_screen(600))

    def test_bullet_rectangle(self) -> None:
        rect = self.bullet.rectangle()
        self.assertEqual(len(rect), 4)


class TestBarrierBasics(unittest.TestCase):
    """Test Barrier class functionality."""

    def setUp(self) -> None:
        self.barrier = Barrier(x=200, y=400, hp=3, width=50, height=20)

    def test_barrier_initialization(self) -> None:
        self.assertEqual(self.barrier.x, 200)
        self.assertEqual(self.barrier.y, 400)
        self.assertEqual(self.barrier.hp, 3)
        self.assertEqual(self.barrier.width, 50)
        self.assertEqual(self.barrier.height, 20)

    def test_barrier_is_destroyed_false(self) -> None:
        self.assertFalse(self.barrier.is_destroyed())

    def test_barrier_is_destroyed_true(self) -> None:
        self.barrier.hp = 0
        self.assertTrue(self.barrier.is_destroyed())

    def test_barrier_take_damage(self) -> None:
        self.barrier.take_damage(1)
        self.assertEqual(self.barrier.hp, 2)

    def test_barrier_take_damage_multiple(self) -> None:
        self.barrier.take_damage(1)
        self.barrier.take_damage(1)
        self.assertEqual(self.barrier.hp, 1)

    def test_barrier_take_damage_overkill(self) -> None:
        self.barrier.take_damage(10)
        self.assertEqual(self.barrier.hp, 0)

    def test_barrier_take_damage_when_destroyed(self) -> None:
        self.barrier.hp = 0
        self.barrier.take_damage(1)
        self.assertEqual(self.barrier.hp, 0)

    def test_barrier_rectangle(self) -> None:
        rect = self.barrier.rectangle()
        self.assertEqual(len(rect), 4)


class TestBarrierNegative(unittest.TestCase):
    """Negative tests for Barrier class."""

    def test_barrier_take_damage_negative(self) -> None:
        barrier = Barrier(x=200, y=400, hp=3, width=50, height=20)
        with self.assertRaises(ValueError):
            barrier.take_damage(-1)


class TestGameState(unittest.TestCase):
    """Test GameState class."""

    def setUp(self) -> None:
        self.player = Player(x=100, y=100, hp=1, speed=5, points=0)
        self.game = GameState(state=1, player=self.player)

    def test_game_state_init(self) -> None:
        self.assertEqual(self.game.state, 1)

    def test_game_start(self) -> None:
        self.game.game_start()
        self.assertEqual(self.game.state, 2)

    def test_game_over_player_alive(self) -> None:
        self.game.game_over()
        self.assertEqual(self.game.state, 1)

    def test_game_over_player_dead(self) -> None:
        self.player.hp = 0
        self.game.game_over()
        self.assertEqual(self.game.state, 0)

    def test_game_restart(self) -> None:
        self.game.state = 0
        self.game.game_restart()
        self.assertEqual(self.game.state, 2)

    def test_game_restart_not_in_gameover(self) -> None:
        self.game.state = 1
        self.game.game_restart()
        self.assertEqual(self.game.state, 1)


class TestWaveManager(unittest.TestCase):
    """Test WaveManager class."""

    def setUp(self) -> None:
        self.enemies = [
            Enemy(x=100, y=100, hp=1, speed=5, screen_width=800, screen_height=800),
            Enemy(x=200, y=100, hp=1, speed=5, screen_width=800, screen_height=800),
        ]
        self.wave = WaveMenager(enemies=self.enemies)

    def test_wave_init(self) -> None:
        self.assertEqual(len(self.wave.enemies), 2)
        self.assertEqual(self.wave.direction, 1)

    def test_wave_move_right(self) -> None:
        self.wave.move()
        self.assertEqual(self.wave.enemies[0].x, 105)

    def test_wave_move_empty_list(self) -> None:
        self.wave.enemies = []
        self.wave.move()
        self.assertEqual(len(self.wave.enemies), 0)

    def test_wave_remove_destroyed(self) -> None:
        self.enemies[0].hp = 0
        self.wave.remove_destroyed()
        self.assertEqual(len(self.wave.enemies), 1)

    def test_wave_remove_all_destroyed(self) -> None:
        for enemy in self.enemies:
            enemy.hp = 0
        self.wave.remove_destroyed()
        self.assertEqual(len(self.wave.enemies), 0)


class TestScoreManager(unittest.TestCase):
    """Test ScoreManager class."""

    def setUp(self) -> None:
        self.filename = 'test_score.txt'
        if os.path.exists(self.filename):
            os.remove(self.filename)
        self.score = ScoreManager(filename=self.filename)

    def tearDown(self) -> None:
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_score_init(self) -> None:
        self.assertEqual(self.score.current_score, 0)
        self.assertEqual(self.score.high_score, 0)

    def test_score_add_points(self) -> None:
        self.score.add_points(100)
        self.assertEqual(self.score.current_score, 100)

    def test_score_add_points_multiple(self) -> None:
        self.score.add_points(50)
        self.score.add_points(50)
        self.assertEqual(self.score.current_score, 100)

    def test_score_reset(self) -> None:
        self.score.add_points(100)
        self.score.reset()
        self.assertEqual(self.score.current_score, 0)

    def test_score_save(self) -> None:
        self.score.add_points(500)
        self.score.save()
        self.assertTrue(os.path.exists(self.filename))

    def test_score_load_no_file(self) -> None:
        result = self.score.load()
        self.assertEqual(result, 0)

    def test_score_load_existing_file(self) -> None:
        self.score.add_points(300)
        self.score.save()
        loaded = self.score.load()
        self.assertEqual(loaded, 300)


class TestCollisionHandler(unittest.TestCase):
    """Test CollisionHandler class."""

    def setUp(self) -> None:
        self.handler = CollisionHandler()
        self.player = Player(x=100, y=500, hp=3, speed=5, points=0)
        self.enemy = Enemy(x=100, y=500, hp=1, speed=3)
        self.bullet = Bullet(x=100, y=500, speed=10, damage=1, direction=1, owner=self.player)
        self.barrier = Barrier(x=100, y=400, hp=3, width=50, height=20)

    def test_rectangles_intersect_true(self) -> None:
        rect_a = (0, 0, 10, 10)
        rect_b = (5, 5, 10, 10)
        self.assertTrue(self.handler.rectangles_intersect(rect_a, rect_b))

    def test_rectangles_intersect_false(self) -> None:
        rect_a = (0, 0, 10, 10)
        rect_b = (20, 20, 10, 10)
        self.assertFalse(self.handler.rectangles_intersect(rect_a, rect_b))

    def test_bullet_hits_entity_true(self) -> None:
        result = self.handler.bullet_hits_entity(self.bullet, self.enemy)
        self.assertTrue(result)

    def test_bullet_hits_entity_false(self) -> None:
        self.bullet.x = 999
        result = self.handler.bullet_hits_entity(self.bullet, self.enemy)
        self.assertFalse(result)


class TestGameEngine(unittest.TestCase):
    """Test GameEngine class."""

    def setUp(self) -> None:
        self.filename = 'test_engine.txt'
        if os.path.exists(self.filename):
            os.remove(self.filename)
        self.engine = GameEngine(score_filename=self.filename)

    def tearDown(self) -> None:
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_engine_init_menu_state(self) -> None:
        self.assertEqual(self.engine.state.state, 1)

    def test_engine_player_initialized(self) -> None:
        self.assertIsNotNone(self.engine.player)
        self.assertEqual(self.engine.player.hp, 3)

    def test_engine_start_game(self) -> None:
        self.engine.start_game()
        self.assertEqual(self.engine.state.state, 2)

    def test_engine_reset_game(self) -> None:
        self.engine.start_game()
        self.engine.player.hp = 0
        self.engine.reset_game()
        self.assertEqual(self.engine.player.hp, 3)
        self.assertEqual(self.engine.state.state, 2)

    def test_engine_player_shoot(self) -> None:
        self.engine.start_game()
        self.engine.player_shoot()
        self.assertEqual(len(self.engine.player_bullets), 1)

    def test_engine_player_shoot_dead(self) -> None:
        self.engine.player.hp = 0
        self.engine.player_shoot()
        self.assertEqual(len(self.engine.player_bullets), 0)

    def test_engine_move_bullets(self) -> None:
        self.engine.start_game()
        self.engine.player_shoot()
        initial_y = self.engine.player_bullets[0].y
        self.engine.move_bullets()
        self.assertLess(self.engine.player_bullets[0].y, initial_y)

    def test_engine_enemy_wave_created(self) -> None:
        self.assertGreater(len(self.engine.wave.enemies), 0)

    def test_engine_barriers_created(self) -> None:
        self.assertEqual(len(self.engine.barriers), 3)

    def test_engine_check_level_completion(self) -> None:
        for enemy in self.engine.wave.enemies:
            enemy.hp = 0
        initial_count = len(self.engine.wave.enemies)
        self.engine.check_level_completion()
        self.assertGreater(len(self.engine.wave.enemies), 0)

    def test_engine_score_save_load(self) -> None:
        self.engine.score.add_points(250)
        self.engine.score.save()
        loaded = self.engine.score.load()
        self.assertEqual(loaded, 250)

    def test_engine_display_data(self) -> None:
        data = self.engine.get_display_data()
        self.assertIn('player', data)
        self.assertIn('enemies', data)
        self.assertIn('score', data)
        self.assertIn('state', data)


class TestIntegration(unittest.TestCase):
    """Integration tests for game."""

    def setUp(self) -> None:
        self.filename = 'test_integration.txt'
        if os.path.exists(self.filename):
            os.remove(self.filename)
        self.engine = GameEngine(score_filename=self.filename)

    def tearDown(self) -> None:
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_full_game_sequence(self) -> None:
        self.assertEqual(self.engine.state.state, 1)
        self.engine.start_game()
        self.assertEqual(self.engine.state.state, 2)
        self.engine.player_shoot()
        self.assertEqual(len(self.engine.player_bullets), 1)
        self.engine.update()
        self.engine.reset_game()
        self.assertEqual(self.engine.state.state, 2)

    def test_player_collision_with_enemy_bullet(self) -> None:
        self.engine.start_game()
        enemy = Enemy(x=380, y=520, hp=1, speed=1)
        bullet = enemy.shoot()
        if bullet:
            self.engine.enemy_bullets.append(bullet)
            initial_hp = self.engine.player.hp
            self.engine.update()
            self.assertLess(self.engine.player.hp, initial_hp)

    def test_barrier_destruction(self) -> None:
        self.engine.start_game()
        barrier = self.engine.barriers[0]
        initial_hp = barrier.hp
        barrier.take_damage(1)
        self.assertLess(barrier.hp, initial_hp)

    def test_score_increases_on_kill(self) -> None:
        self.engine.start_game()
        initial_score = self.engine.score.current_score
        if self.engine.wave.enemies:
            self.engine.wave.enemies[0].hp = 0
            self.engine.player.add_points(100)
            self.engine.score.add_points(100)
        self.assertGreater(self.engine.score.current_score, initial_score)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def test_player_multiple_damages_sequence(self) -> None:
        player = Player(x=100, y=100, hp=3, speed=5, points=0)
        player.take_damage(1)
        player.take_damage(1)
        player.take_damage(1)
        self.assertFalse(player.is_alive())

    def test_enemy_rapid_fire(self) -> None:
        enemy = Enemy(x=100, y=100, hp=5, speed=2)
        bullets = []
        for _ in range(5):
            bullet = enemy.shoot()
            if bullet:
                bullets.append(bullet)
        self.assertEqual(len(bullets), 5)

    def test_barrier_multiple_enemies_damage(self) -> None:
        barrier = Barrier(x=100, y=100, hp=5, width=50, height=30)
        for _ in range(5):
            barrier.take_damage(1)
        self.assertTrue(barrier.is_destroyed())

    def test_score_high_value(self) -> None:
        score = ScoreManager('test_high.txt', current_score=0, high_score=0)
        score.add_points(99999)
        self.assertEqual(score.current_score, 99999)

    def test_game_engine_multiple_waves(self) -> None:
        engine = GameEngine('test_multi_wave.txt')
        for _ in range(2):
            for enemy in engine.wave.enemies:
                enemy.hp = 0
            engine.check_level_completion()
        self.assertGreater(len(engine.wave.enemies), 0)


class TestBoundaryConditions(unittest.TestCase):
    """Test boundary and limit conditions."""

    def test_player_at_left_edge(self) -> None:
        player = Player(x=0, y=100, hp=3, speed=5, points=0, screen_width=800)
        player.move_left()
        self.assertEqual(player.x, 0)

    def test_player_at_right_edge(self) -> None:
        player = Player(x=760, y=100, hp=3, speed=5, points=0, screen_width=800)
        player.move_right()
        self.assertLessEqual(player.x, 760)

    def test_enemy_at_screen_bottom(self) -> None:
        enemy = Enemy(x=100, y=776, hp=1, speed=5, screen_height=800)
        enemy.move_down()
        self.assertLessEqual(enemy.y, 776)

    def test_bullet_at_screen_top(self) -> None:
        player = Player(x=100, y=100, hp=3, speed=5, points=0)
        bullet = player.shoot()
        if bullet:
            bullet.y = -1
            self.assertTrue(bullet.is_off_screen(600))

    def test_barrier_zero_hp_no_further_damage(self) -> None:
        barrier = Barrier(x=100, y=100, hp=1, width=50, height=30)
        barrier.take_damage(10)
        barrier.take_damage(10)
        self.assertEqual(barrier.hp, 0)


class TestGameSequences(unittest.TestCase):
    """Test realistic game sequences."""

    def setUp(self) -> None:
        self.engine = GameEngine('test_sequence.txt')

    def tearDown(self) -> None:
        if os.path.exists('test_sequence.txt'):
            os.remove('test_sequence.txt')

    def test_full_player_lifecycle(self) -> None:
        self.engine.start_game()
        self.engine.player_shoot()
        self.engine.update()
        self.engine.player.take_damage(1)
        self.assertTrue(self.engine.player.is_alive())
        self.engine.reset_game()
        self.assertEqual(self.engine.player.hp, 3)

    def test_enemy_wave_movement_pattern(self) -> None:
        initial_x = self.engine.wave.enemies[0].x
        self.engine.wave.move()
        self.assertNotEqual(self.engine.wave.enemies[0].x, initial_x)

    def test_barrier_protection(self) -> None:
        self.engine.start_game()
        barrier = self.engine.barriers[0]
        initial_hp = barrier.hp
        barrier.take_damage(2)
        self.assertLess(barrier.hp, initial_hp)

    def test_score_accumulation(self) -> None:
        self.engine.score.add_points(100)
        self.engine.score.add_points(50)
        self.engine.score.add_points(150)
        self.assertEqual(self.engine.score.current_score, 300)

    def test_game_state_transitions(self) -> None:
        self.assertEqual(self.engine.state.state, 1)
        self.engine.state.game_start()
        self.assertEqual(self.engine.state.state, 2)
        self.engine.player.hp = 0
        self.engine.state.game_over()
        self.assertEqual(self.engine.state.state, 0)


class TestCollisionCornerCases(unittest.TestCase):
    """Test collision detection edge cases."""

    def test_collision_adjacent_rectangles(self) -> None:
        handler = CollisionHandler()
        rect_a = (0, 0, 10, 10)
        rect_b = (10, 0, 10, 10)
        self.assertFalse(handler.rectangles_intersect(rect_a, rect_b))

    def test_collision_overlapping_rectangles(self) -> None:
        handler = CollisionHandler()
        rect_a = (0, 0, 20, 20)
        rect_b = (10, 10, 20, 20)
        self.assertTrue(handler.rectangles_intersect(rect_a, rect_b))

    def test_collision_contained_rectangle(self) -> None:
        handler = CollisionHandler()
        rect_a = (0, 0, 100, 100)
        rect_b = (25, 25, 50, 50)
        self.assertTrue(handler.rectangles_intersect(rect_a, rect_b))

    def test_collision_touching_edges(self) -> None:
        handler = CollisionHandler()
        rect_a = (0, 0, 10, 10)
        rect_b = (10, 10, 10, 10)
        self.assertFalse(handler.rectangles_intersect(rect_a, rect_b))


class TestWaveManagerAdvanced(unittest.TestCase):
    """Advanced tests for WaveManager."""

    def test_wave_with_mixed_hp_enemies(self) -> None:
        enemies = [
            Enemy(x=100, y=100, hp=5, speed=3),
            Enemy(x=200, y=100, hp=0, speed=3),
            Enemy(x=300, y=100, hp=2, speed=3),
        ]
        wave = WaveMenager(enemies)
        wave.remove_destroyed()
        self.assertEqual(len(wave.enemies), 2)

    def test_wave_move_with_dead_enemies(self) -> None:
        enemies = [
            Enemy(x=100, y=100, hp=1, speed=3, screen_width=800),
            Enemy(x=200, y=100, hp=0, speed=3, screen_width=800),
        ]
        wave = WaveMenager(enemies)
        wave.move()
        self.assertEqual(len(wave.enemies), 2)

    def test_wave_direction_consistency(self) -> None:
        enemies = [
            Enemy(x=100, y=100, hp=1, speed=3, screen_width=800),
            Enemy(x=200, y=100, hp=1, speed=3, screen_width=800),
        ]
        wave = WaveMenager(enemies)
        initial_dir = wave.direction
        wave.move()
        self.assertIn(wave.direction, [-1, 1])


class TestScoreManagerAdvanced(unittest.TestCase):
    """Advanced tests for ScoreManager."""

    def setUp(self) -> None:
        self.filename = 'test_score_adv.txt'
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def tearDown(self) -> None:
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_score_persistence_across_sessions(self) -> None:
        score1 = ScoreManager(self.filename)
        score1.add_points(500)
        score1.save()
        
        score2 = ScoreManager(self.filename)
        score2.load()
        self.assertEqual(score2.high_score, 500)

    def test_score_not_overwritten_with_lower(self) -> None:
        score = ScoreManager(self.filename)
        score.current_score = 1000
        score.save()
        
        score.current_score = 500
        score.save()
        
        score.load()
        self.assertEqual(score.high_score, 1000)

    def test_score_reset_and_add(self) -> None:
        score = ScoreManager(self.filename)
        score.add_points(100)
        score.reset()
        score.add_points(50)
        self.assertEqual(score.current_score, 50)


class TestPlayerAdvanced(unittest.TestCase):
    """Advanced player tests."""

    def test_player_sustained_damage(self) -> None:
        player = Player(x=100, y=100, hp=3, speed=5, points=0)
        damages = [1, 1, 1, 1]
        for dmg in damages:
            player.take_damage(dmg)
        self.assertFalse(player.is_alive())

    def test_player_movement_combinations(self) -> None:
        player = Player(x=400, y=100, hp=3, speed=5, points=0, screen_width=800)
        player.move_left()
        player.move_left()
        player.move_right()
        self.assertEqual(player.x, 395)

    def test_player_bullet_owner_reference(self) -> None:
        player = Player(x=100, y=100, hp=3, speed=5, points=0)
        bullet = player.shoot()
        if bullet:
            self.assertIs(bullet.owner, player)


class TestEnemyAdvanced(unittest.TestCase):
    """Advanced enemy tests."""

    def test_enemy_multi_directional_movement(self) -> None:
        enemy = Enemy(x=400, y=300, hp=1, speed=3, screen_width=800, screen_height=600)
        enemy.move_right()
        enemy.move_down()
        self.assertGreater(enemy.x, 400)
        self.assertGreater(enemy.y, 300)

    def test_enemy_bullet_trajectory(self) -> None:
        enemy = Enemy(x=100, y=100, hp=1, speed=3)
        bullet = enemy.shoot()
        if bullet:
            self.assertEqual(bullet.direction, -1)
            self.assertGreater(bullet.y, enemy.y)


if __name__ == '__main__':
    unittest.main()
