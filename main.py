import sys
import pygame

from game.game_logic import GameEngine
from game.renderer import GameRenderer


def main() -> None:
    """Main game loop."""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Space Invaders')
    clock = pygame.time.Clock()

    engine = GameEngine()
    renderer = GameRenderer(screen)

    can_shoot = True
    shoot_delay = 250
    last_shot_time = 0

    running = True
    while running:
        delta = clock.tick(60)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if engine.state.state == 1 and event.key == pygame.K_SPACE:
                    engine.start_game()
                if engine.state.state == 0 and event.key == pygame.K_r:
                    engine.reset_game()

        if engine.state.state == 2:
            if keys[pygame.K_LEFT]:
                engine.player.move_left()
            if keys[pygame.K_RIGHT]:
                engine.player.move_right()
            if keys[pygame.K_SPACE] and can_shoot:
                engine.player_shoot()
                can_shoot = False
                last_shot_time = pygame.time.get_ticks()

            if not can_shoot and pygame.time.get_ticks() - last_shot_time > shoot_delay:
                can_shoot = True

        engine.update()
        renderer.render(engine)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
