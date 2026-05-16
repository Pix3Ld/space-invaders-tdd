"""Game logic module for Space Invaders."""

from __future__ import annotations

import os
import random
from typing import Any, List, Optional, Tuple, Union

from game.entities import Barrier, Bullet, Enemy, Player


class GameState:
    """Manages game state transitions."""

    def __init__(self, state: int, player: Player) -> None:
        self.state = state
        self.player = player

    def game_start(self) -> None:
        """Start the game from menu."""
        self.state = 2

    def game_over(self) -> None:
        """End the game when player dies."""
        if not self.player.is_alive():
            self.state = 0

    def game_restart(self) -> None:
        """Restart game from game over state."""
        if self.state == 0:
            self.state = 2


class WaveMenager:
    """Manages enemy wave movement and actions."""

    def __init__(self, enemies: List[Enemy]) -> None:
        self.enemies = enemies
        self.direction = 1

    def move(self) -> None:
        """Move all enemies and handle direction changes."""
        if not self.enemies:
            return

        right_edge = any(
            enemy.x + enemy.width + enemy.speed > enemy.screen_width
            for enemy in self.enemies
            if not enemy.enemy_down()
        )
        left_edge = any(
            enemy.x - enemy.speed < 0
            for enemy in self.enemies
            if not enemy.enemy_down()
        )

        if right_edge or left_edge:
            self.direction *= -1
            for enemy in self.enemies:
                enemy.move_down()

        for enemy in self.enemies:
            if not enemy.enemy_down():
                enemy.direction = self.direction
                enemy.direction_change()

    def remove_destroyed(self) -> None:
        """Remove dead enemies from wave."""
        self.enemies = [enemy for enemy in self.enemies if not enemy.enemy_down()]


class ScoreManager:
    """Manages game scoring and high scores."""

    def __init__(
        self,
        filename: str,
        current_score: int = 0,
        high_score: int = 0,
    ) -> None:
        self.filename = filename
        self.current_score = current_score
        self.high_score = high_score

    def add_points(self, points: int) -> None:
        """Add points to current score."""
        self.current_score += points

    def reset(self) -> None:
        """Reset current score to zero."""
        self.current_score = 0

    def save(self) -> None:
        """Save high score to file if current exceeds it."""
        if self.current_score > self.high_score:
            self.high_score = self.current_score
            try:
                with open(self.filename, 'w', encoding='utf-8') as file_handle:
                    file_handle.write(str(self.high_score))
            except OSError:
                pass

    def load(self) -> int:
        """Load high score from file."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file_handle:
                value = int(file_handle.read().strip() or '0')
                self.high_score = value
                return value
        except (FileNotFoundError, ValueError, OSError):
            return 0


class CollisionHandler:
    """Handles collision detection between game entities."""

    @staticmethod
    def rectangles_intersect(
        rect_a: Tuple[int, int, int, int], rect_b: Tuple[int, int, int, int]
    ) -> bool:
        """Check if two rectangles intersect."""
        ax, ay, aw, ah = rect_a
        bx, by, bw, bh = rect_b
        return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by

    def bullet_hits_entity(self, bullet: Bullet, entity: Union[Player, Enemy, Barrier]) -> bool:
        """Check if bullet collides with entity."""
        try:
            entity_rect = entity.rectangle()
        except AttributeError:
            entity_rect = (entity.x, entity.y, 0, 0)  # type: ignore
        return self.rectangles_intersect(entity_rect, bullet.rectangle())


class GameEngine:
    """Main game engine managing all game logic."""

    screen_width = 800
    screen_height = 600

    def __init__(self, score_filename: str = 'highscore.txt', asset_manager: Optional[Any] = None) -> None:
        self.player = Player(
            x=380,
            y=540,
            hp=3,
            speed=6,
            points=0,
            screen_width=self.screen_width,
        )
        self.state = GameState(state=1, player=self.player)
        self.score = ScoreManager(filename=score_filename)
        self.collision = CollisionHandler()
        self.wave = WaveMenager(self.spawn_wave())
        self.player_bullets: List[Bullet] = []
        self.enemy_bullets: List[Bullet] = []
        self.barriers = self.create_barriers()
        self.asset_manager = asset_manager
        self.score.load()

    def spawn_wave(self) -> List[Enemy]:
        """Create initial enemy wave."""
        enemies: List[Enemy] = []
        rows = 4
        columns = 8
        horizontal_spacing = 70
        vertical_spacing = 60
        x_start = 60
        y_start = 60

        for row in range(rows):
            for col in range(columns):
                enemy = Enemy(
                    x=x_start + col * horizontal_spacing,
                    y=y_start + row * vertical_spacing,
                    hp=1,
                    speed=3,
                    direction=1,
                    damage=1,
                    screen_width=self.screen_width,
                    screen_height=self.screen_height,
                )
                enemies.append(enemy)
        return enemies

    def create_barriers(self) -> List[Barrier]:
        """Create protective barriers."""
        barriers: List[Barrier] = []
        barrier_y = 470
        barrier_width = 80
        barrier_height = 30
        gap = 140
        num_barriers = 4
        total_width = num_barriers * barrier_width + (num_barriers - 1) * gap
        x_start = (self.screen_width - total_width) // 2

        for index in range(num_barriers):
            barriers.append(
                Barrier(
                    x=x_start + index * (barrier_width + gap),
                    y=barrier_y,
                    hp=6,
                    width=barrier_width,
                    height=barrier_height,
                )
            )
        return barriers

    def start_game(self) -> None:
        """Start the game."""
        self.state.game_start()

    def reset_game(self) -> None:
        """Reset game to initial state."""
        self.player.player_reset()
        self.player.x = self.player.starting_x
        self.player.y = self.player.starting_y
        self.player.hp = self.player.starting_hp
        self.player.points = self.player.starting_points
        self.player_bullets.clear()
        self.enemy_bullets.clear()
        self.wave = WaveMenager(self.spawn_wave())
        self.barriers = self.create_barriers()
        self.score.reset()
        self.score.load()
        self.state.game_restart()

    def player_shoot(self) -> None:
        """Fire bullet from player."""
        bullet = self.player.shoot()
        if bullet is not None:
            self.player_bullets.append(bullet)

    def enemy_shoot(self) -> None:
        """Fire bullets from random alive enemy."""
        alive_enemies = [enemy for enemy in self.wave.enemies if not enemy.enemy_down()]
        if not alive_enemies:
            return
        if random.random() < 0.03:
            shooter = random.choice(alive_enemies)
            bullet = shooter.shoot()
            if bullet is not None:
                self.enemy_bullets.append(bullet)

    def move_bullets(self) -> None:
        """Update bullet positions and remove off-screen bullets."""
        for bullet in self.player_bullets:
            bullet.move()
        for bullet in self.enemy_bullets:
            bullet.move()
        self.player_bullets = [b for b in self.player_bullets if not b.is_off_screen(self.screen_height)]
        self.enemy_bullets = [b for b in self.enemy_bullets if not b.is_off_screen(self.screen_height)]

    def process_collisions(self) -> None:
        """Handle all collision detection and damage."""
        for bullet in list(self.player_bullets):
            for enemy in self.wave.enemies:
                if self.collision.bullet_hits_entity(bullet, enemy):
                    enemy.hp = max(0, enemy.hp - bullet.damage)
                    if bullet in self.player_bullets:
                        self.player_bullets.remove(bullet)
                    if enemy.enemy_down():
                        self.player.add_points(100)
                        self.score.add_points(100)
                        if self.asset_manager:
                            self.asset_manager.play_sound('hit')
                    break

            for barrier in self.barriers:
                if not barrier.is_destroyed() and bullet in self.player_bullets and self.collision.bullet_hits_entity(bullet, barrier):
                    barrier.take_damage(bullet.damage)
                    if bullet in self.player_bullets:
                        self.player_bullets.remove(bullet)
                    if barrier.is_destroyed() and self.asset_manager:
                        self.asset_manager.play_sound('enemy_down')
                    break

        for bullet in list(self.enemy_bullets):
            # Check collision with player
            if self.collision.bullet_hits_entity(bullet, self.player):
                self.player.take_damage(bullet.damage)
                if bullet in self.enemy_bullets:
                    self.enemy_bullets.remove(bullet)
                if not self.player.is_alive():
                    self.state.game_over()  # Immediately end game when player dies
                    if self.asset_manager:
                        self.asset_manager.play_sound('gameover')
                continue

            # Check collision with barriers (skip destroyed)
            for barrier in self.barriers:
                if not barrier.is_destroyed() and self.collision.bullet_hits_entity(bullet, barrier):
                    barrier.take_damage(bullet.damage)
                    if bullet in self.enemy_bullets:
                        self.enemy_bullets.remove(bullet)
                    if barrier.is_destroyed() and self.asset_manager:
                        self.asset_manager.play_sound('enemy_down')
                    break
        
        # Check collision between enemies and player (alien invasion)
        if not self.player.is_alive():
            return
        
        for enemy in self.wave.enemies:
            if not enemy.enemy_down() and self.collision.bullet_hits_entity(enemy, self.player):
                self.player.take_damage(1)
                if not self.player.is_alive() and self.asset_manager:
                    self.asset_manager.play_sound('gameover')
                break

    def update(self) -> None:
        """Update game state each frame."""
        if self.state.state != 2:
            return

        self.wave.move()
        self.enemy_shoot()
        self.move_bullets()
        self.process_collisions()
        self.wave.remove_destroyed()
        self.check_level_completion()
        self.check_game_over()

    def check_level_completion(self) -> None:
        """Spawn new wave when all enemies defeated."""
        if not any(not enemy.enemy_down() for enemy in self.wave.enemies):
            self.wave = WaveMenager(self.spawn_wave())

    def check_game_over(self) -> None:
        """Check if game over condition is met."""
        # Check if player is dead
        if not self.player.is_alive():
            self.state.game_over()
        
        # Check if any alive enemy reached the bottom
        for enemy in self.wave.enemies:
            if not enemy.enemy_down() and enemy.y + enemy.height >= self.player.y:
                self.state.game_over()
                break
        
        if self.state.state == 0:
            self.score.save()

    def get_display_data(self) -> dict:
        """Get data for rendering."""
        return {
            'player': self.player,
            'enemies': list(self.wave.enemies),
            'player_bullets': list(self.player_bullets),
            'enemy_bullets': list(self.enemy_bullets),
            'barriers': list(self.barriers),
            'score': self.score.current_score,
            'high_score': self.score.high_score,
            'player_hp': self.player.hp,
            'state': self.state.state,
        }
    