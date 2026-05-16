"""Asset manager for Space Invaders game."""

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
        
        # Ensure pygame mixer is initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        self._create_directories()
        self._load_assets()
        # Generate fallback assets if loading found nothing
        if not self.images or not self.sounds:
            self._generate_fallback_assets()
            self._load_assets()  # Reload after generating fallbacks

    def _create_directories(self) -> None:
        """Create asset directories if they don't exist."""
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.audio_dir.mkdir(parents=True, exist_ok=True)

    def _generate_fallback_assets(self) -> None:
        """Generate fallback assets if none are found (for testing)."""
        # Generate fallback images only if no PNG files exist
        if not any(self.images_dir.glob('*.png')):
            try:
                from PIL import Image, ImageDraw
                
                # Player sprite (green arrow)
                img = Image.new('RGBA', (40, 20), (0, 0, 0, 0))
                draw = ImageDraw.Draw(img)
                draw.polygon([(0, 0), (40, 0), (20, 20)], fill=(0, 200, 40, 255))
                img.save(self.images_dir / 'player.png')

                # Enemy sprite (red square)
                img = Image.new('RGBA', (36, 24), (200, 50, 50, 255))
                img.save(self.images_dir / 'enemy.png')

                # Barrier sprite (blue block)
                img = Image.new('RGBA', (80, 30), (100, 150, 200, 255))
                img.save(self.images_dir / 'barrier.png')

                # Bullet sprite (yellow dot)
                img = Image.new('RGBA', (4, 10), (255, 255, 0, 255))
                img.save(self.images_dir / 'bullet.png')
            except ImportError:
                pass
        
        # Generate fallback sounds only if no audio files exist
        if not any(list(self.audio_dir.glob('*.wav')) + list(self.audio_dir.glob('*.ogg'))):
            self._create_fallback_sounds()

    def _create_fallback_sounds(self) -> None:
        """Generate fallback sound files if none exist."""
        try:
            import wave
            import struct
            import math
        except ImportError:
            return

        # Shoot sound
        if not (self.audio_dir / 'shoot.wav').exists():
            self._create_beep_sound(self.audio_dir / 'shoot.wav', frequency=800, duration=0.1)

        # Hit sound
        if not (self.audio_dir / 'hit.wav').exists():
            self._create_beep_sound(self.audio_dir / 'hit.wav', frequency=1200, duration=0.2)

        # Game over sound
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

        with wave.open(str(filepath), 'wb') as wav_file:
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

        with wave.open(str(filepath), 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(b''.join(wave_data))

    def _load_assets(self) -> None:
        """Load all assets into memory."""
        self._load_images()
        self._load_sounds()

    def _load_images(self) -> None:
        """Load PNG images from images directory and map to game entities."""
        if not self.images_dir.exists():
            return
        
        # Load all PNG files from images directory
        for img_path in self.images_dir.glob('*.png'):
            try:
                name = img_path.stem  # filename without extension
                self.images[name] = pygame.image.load(str(img_path))
            except (pygame.error, FileNotFoundError):
                pass
        
        # Map specific files to game entity names if they exist
        name_mapping = {
            'gracz': 'player',
            'alien1rzad': 'enemy',
            'alien2rzad': 'barrier',
            'alien3rzad': 'barrier2',
        }
        
        for source_name, target_name in name_mapping.items():
            if source_name in self.images and target_name not in self.images:
                self.images[target_name] = self.images[source_name]

    def _load_sounds(self) -> None:
        """Load WAV/OGG sounds from audio directory."""
        if not self.audio_dir.exists():
            return
        
        # Only try to load sounds if mixer is initialized
        try:
            if not pygame.mixer.get_init():
                return
        except Exception:
            return
        
        # Load all WAV and OGG files from audio directory
        for sound_path in list(self.audio_dir.glob('*.wav')) + list(self.audio_dir.glob('*.ogg')):
            try:
                name = sound_path.stem  # filename without extension
                self.sounds[name] = pygame.mixer.Sound(str(sound_path))
            except (pygame.error, FileNotFoundError):
                pass
        
        # Map OGG files to game event names if available
        sound_mapping = {
            'game_over': 'gameover',
            'enemy_down': 'hit',
            'player_death': 'death',
        }
        
        for source_name, target_name in sound_mapping.items():
            if source_name in self.sounds and target_name not in self.sounds:
                self.sounds[target_name] = self.sounds[source_name]

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
