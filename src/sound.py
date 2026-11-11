import math
import array
import pygame

class SoundEngine:
    def __init__(self):
        self.enabled = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.enabled = True
            self.hit_sound = self._create_pop_sound(freq=260, duration=0.08)
            self.cue_sound = self._create_pop_sound(freq=140, duration=0.12)
            self.pocket_sound = self._create_drop_sound()
        except Exception:
            self.enabled = False

    def _create_pop_sound(self, freq=200, duration=0.1):
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        buf = array.array('h')
        for i in range(n_samples):
            t = i / sample_rate
            env = math.exp(-t * 35)
            val = int(32767 * env * math.sin(2 * math.pi * freq * t))
            buf.append(val)
            buf.append(val)
        return pygame.mixer.Sound(buffer=buf)

    def _create_drop_sound(self):
        sample_rate = 22050
        n_samples = int(sample_rate * 0.22)
        buf = array.array('h')
        for i in range(n_samples):
            t = i / sample_rate
            freq = max(40, 320 - t * 900)
            env = math.exp(-t * 14)
            val = int(28000 * env * math.sin(2 * math.pi * freq * t))
            buf.append(val)
            buf.append(val)
        return pygame.mixer.Sound(buffer=buf)

    def play_hit(self):
        if self.enabled and self.hit_sound:
            try:
                self.hit_sound.play()
            except Exception:
                pass

    def play_cue(self):
        if self.enabled and self.cue_sound:
            try:
                self.cue_sound.play()
            except Exception:
                pass

    def play_pocket(self):
        if self.enabled and self.pocket_sound:
            try:
                self.pocket_sound.play()
            except Exception:
                pass
