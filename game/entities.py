"""Game entities module for Space Invaders."""

from __future__ import annotations

from typing import Optional, Tuple


class Bullet:
    """Represents a projectile fired by player or enemy."""

    def __init__(
        self,
        x: int,
        y: int,
        speed: int,
        damage: int,
        direction: int,
        owner: object,
    ) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.direction = direction
        self.owner = owner

    def move(self) -> None:
        """Move bullet by speed in direction."""
        self.y -= self.speed * self.direction

    def is_off_screen(self, screen_height: int) -> bool:
        """Check if bullet is off screen."""
        return self.y < 0 or self.y > screen_height

    def rectangle(self) -> Tuple[int, int, int, int]:
        """Get bullet rectangle for collision detection."""
        return self.x - 2, self.y, 4, 10


class Player:
    """Represents the player character."""

    width = 40
    height = 20

    def __init__(
        self,
        x: int,
        y: int,
        hp: int,
        speed: int,
        points: int,
        screen_width: int = 800,
    ) -> None:
        if hp < 0 or speed < 0:
            raise ValueError('hp and speed must be non-negative')

        self.x = x
        self.y = y
        self.hp = hp
        self.speed = speed 
        self.points = points
        self.screen_width = screen_width
        self.starting_x = x
        self.starting_y = y
        self.starting_hp = hp
        self.starting_points = points

    def is_alive(self) -> bool:
        """Check if player is alive."""
        return self.hp > 0

    def move_left(self) -> None:
        """Move player left."""
        if self.x - self.speed >= 0:
            self.x -= self.speed

    def move_right(self) -> None:
        """Move player right."""
        if self.x + self.speed <= self.screen_width - self.width:
            self.x += self.speed

    def take_damage(self, dmg: int) -> None:
        """Apply damage to player."""
        if dmg < 0:
            raise ValueError('Damage must be non-negative')
        if self.is_alive():
            self.hp = max(0, self.hp - dmg)

    def shoot(self) -> Optional[Bullet]:
        """Fire a bullet if player is alive."""
        if self.is_alive():
            return Bullet(
                x=self.x + self.width // 2,
                y=self.y,
                speed=10,
                damage=1,
                direction=1,
                owner=self,
            )
        return None

    def player_reset(self) -> None:
        """Reset player to starting state if dead."""
        if not self.is_alive():
            self.x = self.starting_x
            self.y = self.starting_y
            self.hp = self.starting_hp
            self.points = self.starting_points

    def reset(self) -> None:
        """Reset player state.(score)"""
        self.player_reset()

    def add_points(self, value: int) -> None:
        """Add points to player score."""
        if value < 0:
            raise ValueError('Point value must be non-negative')
        self.points += value

    def rectangle(self) -> Tuple[int, int, int, int]:
        """Get player rectangle for collision detection."""
        return self.x, self.y, self.width, self.height


class Enemy:
    """Represents an enemy character."""

    width = 36
    height = 24

    def __init__(
        self,
        x: int,
        y: int,
        hp: int,
        speed: int,
        direction: int = 1,
        damage: int = 1,
        screen_width: int = 800,
        screen_height: int = 800,
    ) -> None:
        self.x = x
        self.y = y
        self.hp = hp
        self.speed = speed
        self.direction = direction
        self.damage = damage
        self.screen_width = screen_width
        self.screen_height = screen_height

    def enemy_down(self) -> bool:
        """Check if enemy is defeated."""
        return self.hp <= 0

    def move_right(self) -> None:
        """Move enemy right."""
        if self.x + self.speed <= self.screen_width - self.width:
            self.x += self.speed

    def move_left(self) -> None:
        """Move enemy left."""
        if self.x - self.speed >= 0:
            self.x -= self.speed

    def move_down(self) -> None:
        """Move enemy down."""
        if self.y + self.speed <= self.screen_height - self.height:
            self.y += self.speed

    def shoot(self) -> Optional[Bullet]:
        """Fire a bullet if enemy is alive."""
        if not self.enemy_down():
            return Bullet(
                x=self.x + self.width // 2,
                y=self.y + self.height,
                speed=10,
                damage=self.damage,
                direction=-1,
                owner=self,
            )
        return None

    def direction_change(self) -> None:
        """Change direction and move."""
        if not self.enemy_down():
            if self.direction == 1:
                self.move_right()
            elif self.direction == -1:
                self.move_left()

    def rectangle(self) -> Tuple[int, int, int, int]:
        """Get enemy rectangle for collision detection."""
        return self.x, self.y, self.width, self.height


class Barrier:
    """Represents a protective barrier."""

    def __init__(
        self,
        x: int,
        y: int,
        hp: int,
        width: int,
        height: int,
    ) -> None:
        self.x = x
        self.y = y
        self.hp = hp
        self.width = width
        self.height = height

    def is_destroyed(self) -> bool:
        """Check if barrier is destroyed."""
        return self.hp <= 0

    def take_damage(self, dmg: int) -> None:
        """Apply damage to barrier."""
        if dmg < 0:
            raise ValueError('Damage must be non-negative')
        if not self.is_destroyed():
            self.hp = max(0, self.hp - dmg)

    def rectangle(self) -> Tuple[int, int, int, int]:
        """Get barrier rectangle for collision detection."""
        return self.x, self.y, self.width, self.height