"""Asset manager for Space Invaders game."""

import os
from pathlib import Path
from typing import Optional

import pygame


class AssetManager:
    """Manages game assets (graphics and sounds)."""

    def __init__(self, assets_dir: str = 'assets') -> None:
        self.assets_dir = Path(assets_dir)
        self.images_dir = self.assets_dir / 'images'
        self.audio_dir = self.assets_dir / 'audio'
        
        self.images: dict = {}
        self.sounds: dict = {}
        
        self._create_directories()
        self._generate_assets()
        self._load_assets()

    def _create_directories(self) -> None:
        """Create asset directories if they don't exist."""
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.audio_dir.mkdir(parents=True, exist_ok=True)

    def _generate_assets(self) -> None:
        """Generate asset files if they don't exist."""
        self._generate_graphics()
        self._generate_sounds()

    def _generate_graphics(self) -> None:
        """Generate PNG graphics for game entities."""
        try:
            from PIL import Image, ImageDraw
        except ImportError:
            return

        # Player sprite (green arrow)
        if not (self.images_dir / 'player.png').exists():
            img = Image.new('RGBA', (40, 20), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.polygon([(0, 0), (40, 0), (20, 20)], fill=(0, 200, 40, 255))
            img.save(self.images_dir / 'player.png')

        # Enemy sprite (red square)
        if not (self.images_dir / 'enemy.png').exists():
            img = Image.new('RGBA', (36, 24), (200, 50, 50, 255))
            img.save(self.images_dir / 'enemy.png')

        # Barrier sprite (blue block)
        if not (self.images_dir / 'barrier.png').exists():
            img = Image.new('RGBA', (80, 30), (100, 150, 200, 255))
            img.save(self.images_dir / 'barrier.png')

        # Bullet sprite (yellow dot)
        if not (self.images_dir / 'bullet.png').exists():
            img = Image.new('RGBA', (4, 10), (255, 255, 0, 255))
            img.save(self.images_dir / 'bullet.png')

    def _generate_sounds(self) -> None:
        """Generate WAV sound files."""
        try:
            import wave
            import struct
        except ImportError:
            return

        # Shoot sound (beep)
        if not (self.audio_dir / 'shoot.wav').exists():
            self._create_beep_sound(self.audio_dir / 'shoot.wav', frequency=800, duration=0.1)

        # Hit sound (higher beep)
        if not (self.audio_dir / 'hit.wav').exists():
            self._create_beep_sound(self.audio_dir / 'hit.wav', frequency=1200, duration=0.2)

        # Game over sound (descending)
        if not (self.audio_dir / 'gameover.wav').exists():
            self._create_descending_sound(self.audio_dir / 'gameover.wav')

    @staticmethod
    def _create_beep_sound(filepath: Path, frequency: int = 800, duration: float = 0.1, sample_rate: int = 22050) -> None:
        """Generate a simple beep sound."""
        try:
            import wave
            import struct
            import math
        except ImportError:
            return

        num_samples = int(sample_rate * duration)
        wave_data = []

        for i in range(num_samples):
            sample = int(32767 * 0.5 * math.sin(2 * math.pi * frequency * i / sample_rate))
            wave_data.append(struct.pack('<h', sample))

        with wave.open(filepath, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(b''.join(wave_data))

    @staticmethod
    def _create_descending_sound(filepath: Path, duration: float = 0.5, sample_rate: int = 22050) -> None:
        """Generate a descending pitch sound."""
        try:
            import wave
            import struct
            import math
        except ImportError:
            return

        num_samples = int(sample_rate * duration)
        wave_data = []
        start_freq = 1000
        end_freq = 300

        for i in range(num_samples):
            progress = i / num_samples
            frequency = start_freq + (end_freq - start_freq) * progress
            sample = int(32767 * 0.5 * math.sin(2 * math.pi * frequency * i / sample_rate))
            wave_data.append(struct.pack('<h', sample))

        with wave.open(filepath, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(b''.join(wave_data))

    def _load_assets(self) -> None:
        """Load all assets into memory."""
        self._load_images()
        self._load_sounds()

    def _load_images(self) -> None:
        """Load PNG images."""
        image_files = ['player.png', 'enemy.png', 'barrier.png', 'bullet.png']
        
        for filename in image_files:
            filepath = self.images_dir / filename
            if filepath.exists():
                try:
                    self.images[filename.replace('.png', '')] = pygame.image.load(filepath)
                except (pygame.error, FileNotFoundError):
                    pass

    def _load_sounds(self) -> None:
        """Load WAV sounds."""
        sound_files = ['shoot.wav', 'hit.wav', 'gameover.wav']
        
        for filename in sound_files:
            filepath = self.audio_dir / filename
            if filepath.exists():
                try:
                    self.sounds[filename.replace('.wav', '')] = pygame.mixer.Sound(filepath)
                except (pygame.error, FileNotFoundError):
                    pass

    def get_image(self, name: str) -> Optional[pygame.Surface]:
        """Get image by name."""
        return self.images.get(name)

    def get_sound(self, name: str) -> Optional[pygame.mixer.Sound]:
        """Get sound by name."""
        return self.sounds.get(name)

    def play_sound(self, name: str) -> None:
        """Play sound by name."""
        sound = self.get_sound(name)
        if sound:
            try:
                sound.play()
            except pygame.error:
                pass

    def has_image(self, name: str) -> bool:
        """Check if image exists."""
        return name in self.images

    def has_sound(self, name: str) -> bool:
        """Check if sound exists."""
        return name in self.sounds

    def get_all_images(self) -> dict:
        """Get all loaded images."""
        return self.images.copy()

    def get_all_sounds(self) -> dict:
        """Get all loaded sounds."""
        return self.sounds.copy()
