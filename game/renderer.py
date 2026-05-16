import pygame
from typing import Optional

from game.assets_manager import AssetManager
from game.entities import Barrier, Bullet, Enemy, Player
from game.game_logic import GameEngine


class GameRenderer:
    """Renders the game state to the screen."""

    def __init__(
        self,
        screen: pygame.Surface,
        screen_width: int = 800,
        screen_height: int = 600,
        assets: Optional[AssetManager] = None,
    ) -> None:
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.assets = assets

    def draw_text(
        self,
        message: str,
        size: int,
        color: tuple,
        x: int,
        y: int,
        center: bool = True,
    ) -> None:
        """Draw text on screen."""
        if size < 8:
            raise ValueError("Font size must be at least 8")
        
        font = pygame.font.Font(None, size)
        text = font.render(message, True, color)
        rect = text.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(text, rect)

    def draw_entity(self, entity: object, color: tuple) -> None:
        """Draw entity using image or rectangle."""
        if not hasattr(entity, 'rectangle'):
            return

        try:
            rect_tuple = entity.rectangle()#type: ignore
            rect = pygame.Rect(rect_tuple)
        except (TypeError, ValueError):
            return

        # Try to draw with image if available
        if self.assets:
            if isinstance(entity, Player):
                img = self.assets.get_image('player')
                if img:
                    scaled_img = pygame.transform.scale(img, (rect.width, rect.height))
                    self.screen.blit(scaled_img, (rect.x, rect.y))
                    return
            elif isinstance(entity, Enemy):
                img = self.assets.get_image('enemy')
                if img:
                    scaled_img = pygame.transform.scale(img, (rect.width, rect.height))
                    self.screen.blit(scaled_img, (rect.x, rect.y))
                    return
            elif isinstance(entity, Barrier):
                img = self.assets.get_image('barrier')
                if img:
                    scaled_img = pygame.transform.scale(img, (rect.width, rect.height))
                    self.screen.blit(scaled_img, (rect.x, rect.y))
                    return
            elif isinstance(entity, Bullet):
                img = self.assets.get_image('bullet')
                if img:
                    scaled_img = pygame.transform.scale(img, (rect.width, rect.height))
                    self.screen.blit(scaled_img, (rect.x, rect.y))
                    return

        # Fallback to colored rectangles
        pygame.draw.rect(self.screen, color, rect)

    def render_menu(self, engine: GameEngine) -> None:
        """Render main menu screen."""
        self.screen.fill((10, 10, 40))
        self.draw_text('SPACE INVADERS', 72, (255, 255, 255), self.screen_width // 2, 100)
        self.draw_text('Press SPACE to start', 32, (200, 200, 200), self.screen_width // 2, 250)
        self.draw_text('Arrow Keys: Move | SPACE: Shoot', 20, (180, 180, 180), self.screen_width // 2, 310)
        self.draw_text('ESC: Quit', 20, (180, 180, 180), self.screen_width // 2, 345)
        self.draw_text(f'HIGH SCORE: {engine.score.high_score}', 28, (255, 200, 0), 
                      self.screen_width // 2, 450)

    def render_game_over(self, engine: GameEngine) -> None:
        """Render game over screen."""
        self.screen.fill((40, 0, 0))
        self.draw_text('GAME OVER', 72, (255, 100, 100), self.screen_width // 2, 120)
        self.draw_text(f'SCORE: {engine.score.current_score}', 40, (255, 255, 255), 
                      self.screen_width // 2, 220)
        self.draw_text(f'HIGH SCORE: {engine.score.high_score}', 32, (255, 200, 0), 
                      self.screen_width // 2, 290)
        self.draw_text('Press R to restart or ESC to exit', 24, (200, 200, 200), 
                      self.screen_width // 2, 400)

    def render_game(self, engine: GameEngine) -> None:
        """Render active game screen."""
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (20, 20, 80), 
                        pygame.Rect(0, 0, self.screen_width, self.screen_height))

        # Draw UI
        self.draw_text(f'SCORE: {engine.score.current_score}', 24, (255, 255, 255), 
                      70, 15, center=False)
        self.draw_text(f'HIGH: {engine.score.high_score}', 24, (255, 200, 0), 
                      70, 40, center=False)
        self.draw_text(f'HP: {engine.player.hp}/3', 24, (100, 255, 100), 
                      70, 65, center=False)

        # Draw player
        self.draw_entity(engine.player, (0, 200, 40))

        # Draw enemies
        for enemy in engine.wave.enemies:
            color = (200, 50, 50) if not enemy.enemy_down() else (100, 100, 100)
            self.draw_entity(enemy, color)

        # Draw bullets
        for bullet in engine.player_bullets:
            self.draw_entity(bullet, (255, 255, 0))
        for bullet in engine.enemy_bullets:
            self.draw_entity(bullet, (255, 100, 100))

        # Draw barriers
        for barrier in engine.barriers:
            if not barrier.is_destroyed():
                color = (100, 150, 200)
                self.draw_entity(barrier, color)

    def render(self, engine: GameEngine) -> None:
        """Main render method called each frame."""
        if engine.state.state == 1:
            self.render_menu(engine)
        elif engine.state.state == 2:
            self.render_game(engine)
        elif engine.state.state == 0:
            self.render_game_over(engine)
        
        pygame.display.flip()
