import sys

import pygame

from game.assets_manager import AssetManager
from game.game_logic import GameEngine
from game.renderer import GameRenderer


def main() -> None:
    """Main game loop."""
    pygame.init()
    pygame.mixer.init()
    
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Space Invaders')
    clock = pygame.time.Clock()

    # Initialize assets
    assets = AssetManager()

    engine = GameEngine(asset_manager=assets)
    renderer = GameRenderer(screen, assets=assets)

    can_shoot = True
    shoot_delay = 250
    last_shot_time = 0
    music_channel = None

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

        # Manage background music using a dedicated channel
        if engine.state.state == 2:  # Game playing
            if music_channel is None:
                # Try to play background music
                music_sounds = ['walka_boss', 'walka_audio1', 'walka_audio_to_boss', 'walka_start']
                for sound_name in music_sounds:
                    sound = assets.get_sound(sound_name)
                    if sound:
                        try:
                            # Set volume lower for background music
                            sound.set_volume(0.3)
                            ch = sound.play(-1)  # Loop indefinitely
                            # play() may return None on some systems; guard it
                            if ch is not None:
                                music_channel = ch
                            break
                        except Exception:
                            pass
        else:
            # Stop only background music channel when not playing
            if music_channel is not None:
                try:
                    music_channel.stop()
                except Exception:
                    # Fallback: stop all sounds if channel stop fails
                    try:
                        pygame.mixer.stop()
                    except Exception:
                        pass
                music_channel = None

        if engine.state.state == 2:
            if keys[pygame.K_LEFT]:
                engine.player.move_left()
            if keys[pygame.K_RIGHT]:
                engine.player.move_right()
            if keys[pygame.K_SPACE] and can_shoot:
                engine.player_shoot()
                assets.play_sound('shoot')
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
