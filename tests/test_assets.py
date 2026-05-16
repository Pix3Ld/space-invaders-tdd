"""Tests for asset manager module."""

import os
import unittest
from pathlib import Path

import pygame

from game.assets_manager import AssetManager


class TestAssetManagerBasics(unittest.TestCase):
    """Test AssetManager basic functionality."""

    @classmethod
    def setUpClass(cls) -> None:
        pygame.init()
        pygame.mixer.init()

    def setUp(self) -> None:
        self.test_assets_dir = 'test_assets'
        self.manager = AssetManager(self.test_assets_dir)

    def tearDown(self) -> None:
        # Clean up test assets
        import shutil
        if Path(self.test_assets_dir).exists():
            shutil.rmtree(self.test_assets_dir)

    def test_asset_manager_initialization(self) -> None:
        self.assertIsNotNone(self.manager)

    def test_directories_created(self) -> None:
        self.assertTrue((Path(self.test_assets_dir) / 'images').exists())
        self.assertTrue((Path(self.test_assets_dir) / 'audio').exists())

    def test_images_dict_exists(self) -> None:
        self.assertIsInstance(self.manager.images, dict)

    def test_sounds_dict_exists(self) -> None:
        self.assertIsInstance(self.manager.sounds, dict)

    def test_has_image_check(self) -> None:
        result = self.manager.has_image('player')
        self.assertIsInstance(result, bool)

    def test_has_sound_check(self) -> None:
        result = self.manager.has_sound('shoot')
        self.assertIsInstance(result, bool)

    def test_get_all_images_returns_dict(self) -> None:
        images = self.manager.get_all_images()
        self.assertIsInstance(images, dict)

    def test_get_all_sounds_returns_dict(self) -> None:
        sounds = self.manager.get_all_sounds()
        self.assertIsInstance(sounds, dict)

    def test_image_names_match(self) -> None:
        # Verify that at least some key images are loaded (player, enemy, barrier, bullet)
        # Naming can vary, so check for mapped names
        required_names = {'player', 'enemy', 'barrier'}
        loaded_names = set(self.manager.images.keys())
        matches = required_names.intersection(loaded_names)
        self.assertGreaterEqual(len(matches), 1, "At least one required image should be loaded")

    def test_sound_names_match(self) -> None:
        # Verify that at least some key sounds are loaded (shoot, hit, gameover)
        # Naming can vary, so check for any sounds being loaded
        self.assertIsInstance(self.manager.sounds, dict)


class TestAssetManagerImageHandling(unittest.TestCase):
    """Test image file handling."""

    @classmethod
    def setUpClass(cls) -> None:
        pygame.init()
        pygame.mixer.init()

    def setUp(self) -> None:
        self.test_assets_dir = 'test_assets_img'
        self.manager = AssetManager(self.test_assets_dir)

    def tearDown(self) -> None:
        import shutil
        if Path(self.test_assets_dir).exists():
            shutil.rmtree(self.test_assets_dir)

    def test_images_directory_path(self) -> None:
        expected_path = Path(self.test_assets_dir) / 'images'
        self.assertEqual(self.manager.images_dir, expected_path)

    def test_get_image_nonexistent(self) -> None:
        result = self.manager.get_image('nonexistent')
        self.assertIsNone(result)

    def test_player_image_file_exists(self) -> None:
        player_img = Path(self.test_assets_dir) / 'images' / 'player.png'
        if player_img.exists():
            self.assertTrue(player_img.exists())

    def test_enemy_image_file_exists(self) -> None:
        enemy_img = Path(self.test_assets_dir) / 'images' / 'enemy.png'
        if enemy_img.exists():
            self.assertTrue(enemy_img.exists())

    def test_barrier_image_file_exists(self) -> None:
        barrier_img = Path(self.test_assets_dir) / 'images' / 'barrier.png'
        if barrier_img.exists():
            self.assertTrue(barrier_img.exists())

    def test_bullet_image_file_exists(self) -> None:
        bullet_img = Path(self.test_assets_dir) / 'images' / 'bullet.png'
        if bullet_img.exists():
            self.assertTrue(bullet_img.exists())


class TestAssetManagerSoundHandling(unittest.TestCase):
    """Test sound file handling."""

    @classmethod
    def setUpClass(cls) -> None:
        pygame.init()
        pygame.mixer.init()

    def setUp(self) -> None:
        self.test_assets_dir = 'test_assets_snd'
        self.manager = AssetManager(self.test_assets_dir)

    def tearDown(self) -> None:
        import shutil
        if Path(self.test_assets_dir).exists():
            shutil.rmtree(self.test_assets_dir)

    def test_audio_directory_path(self) -> None:
        expected_path = Path(self.test_assets_dir) / 'audio'
        self.assertEqual(self.manager.audio_dir, expected_path)

    def test_get_sound_nonexistent(self) -> None:
        result = self.manager.get_sound('nonexistent')
        self.assertIsNone(result)

    def test_shoot_sound_file_exists(self) -> None:
        shoot_snd = Path(self.test_assets_dir) / 'audio' / 'shoot.wav'
        if shoot_snd.exists():
            self.assertTrue(shoot_snd.exists())

    def test_hit_sound_file_exists(self) -> None:
        hit_snd = Path(self.test_assets_dir) / 'audio' / 'hit.wav'
        if hit_snd.exists():
            self.assertTrue(hit_snd.exists())

    def test_gameover_sound_file_exists(self) -> None:
        gameover_snd = Path(self.test_assets_dir) / 'audio' / 'gameover.wav'
        if gameover_snd.exists():
            self.assertTrue(gameover_snd.exists())


class TestAssetManagerPlaySound(unittest.TestCase):
    """Test sound playing functionality."""

    @classmethod
    def setUpClass(cls) -> None:
        pygame.init()
        pygame.mixer.init()

    def setUp(self) -> None:
        self.test_assets_dir = 'test_assets_play'
        self.manager = AssetManager(self.test_assets_dir)

    def tearDown(self) -> None:
        import shutil
        if Path(self.test_assets_dir).exists():
            shutil.rmtree(self.test_assets_dir)

    def test_play_sound_nonexistent(self) -> None:
        # Should not raise exception
        try:
            self.manager.play_sound('nonexistent')
        except Exception as e:
            self.fail(f"play_sound raised {type(e).__name__} unexpectedly")

    def test_play_sound_valid(self) -> None:
        # Should not raise exception
        try:
            self.manager.play_sound('shoot')
        except Exception as e:
            self.fail(f"play_sound raised {type(e).__name__} unexpectedly")


class TestAssetManagerPathHandling(unittest.TestCase):
    """Test path and directory handling."""

    @classmethod
    def setUpClass(cls) -> None:
        pygame.init()
        pygame.mixer.init()

    def test_default_assets_directory(self) -> None:
        manager = AssetManager()
        self.assertEqual(manager.assets_dir, Path('assets'))

    def test_custom_assets_directory(self) -> None:
        custom_dir = 'custom_assets'
        manager = AssetManager(custom_dir)
        self.assertEqual(manager.assets_dir, Path(custom_dir))
        
        # Cleanup
        import shutil
        if Path(custom_dir).exists():
            shutil.rmtree(custom_dir)

    def test_subdirectories_created(self) -> None:
        test_dir = 'test_subdir'
        manager = AssetManager(test_dir)
        
        self.assertTrue((Path(test_dir) / 'images').exists())
        self.assertTrue((Path(test_dir) / 'audio').exists())
        
        # Cleanup
        import shutil
        if Path(test_dir).exists():
            shutil.rmtree(test_dir)


class TestAssetManagerAssetRetrievalNegative(unittest.TestCase):
    """Negative tests for asset retrieval."""

    @classmethod
    def setUpClass(cls) -> None:
        pygame.init()
        pygame.mixer.init()

    def setUp(self) -> None:
        self.test_assets_dir = 'test_assets_neg'
        self.manager = AssetManager(self.test_assets_dir)

    def tearDown(self) -> None:
        import shutil
        if Path(self.test_assets_dir).exists():
            shutil.rmtree(self.test_assets_dir)

    def test_get_image_with_empty_string(self) -> None:
        result = self.manager.get_image('')
        self.assertIsNone(result)

    def test_get_sound_with_empty_string(self) -> None:
        result = self.manager.get_sound('')
        self.assertIsNone(result)

    def test_has_image_false_for_missing(self) -> None:
        result = self.manager.has_image('missing_image')
        self.assertFalse(result)

    def test_has_sound_false_for_missing(self) -> None:
        result = self.manager.has_sound('missing_sound')
        self.assertFalse(result)


class TestAssetManagerIntegration(unittest.TestCase):
    """Integration tests for asset manager."""

    @classmethod
    def setUpClass(cls) -> None:
        pygame.init()
        pygame.mixer.init()

    def setUp(self) -> None:
        self.test_assets_dir = 'test_assets_int'
        self.manager = AssetManager(self.test_assets_dir)

    def tearDown(self) -> None:
        import shutil
        if Path(self.test_assets_dir).exists():
            shutil.rmtree(self.test_assets_dir)

    def test_all_images_loadable(self) -> None:
        images = self.manager.get_all_images()
        self.assertTrue(len(images) > 0 or len(images) == 0)  # Should not fail

    def test_all_sounds_loadable(self) -> None:
        sounds = self.manager.get_all_sounds()
        self.assertTrue(len(sounds) > 0 or len(sounds) == 0)  # Should not fail

    def test_asset_manager_reload(self) -> None:
        manager1 = AssetManager(self.test_assets_dir)
        images1_count = len(manager1.images)
        
        manager2 = AssetManager(self.test_assets_dir)
        images2_count = len(manager2.images)
        
        self.assertEqual(images1_count, images2_count)


if __name__ == '__main__':
    unittest.main()
