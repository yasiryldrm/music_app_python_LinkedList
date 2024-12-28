from pygame import mixer
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
import os

class Song:
    def __init__(self, title, artist, file_path, duration=0):
        self.title = title
        self.artist = artist
        self.file_path = file_path
        self.duration = duration

    @staticmethod
    def from_file(file_path):
        try:
            # Dosya adından başlık ve sanatçı bilgisini çıkar
            file_name = os.path.basename(file_path)
            name_without_ext = os.path.splitext(file_name)[0]
            
            # Dosya uzantısını kontrol et
            if file_path.lower().endswith('.mp3'):
                audio = MP3(file_path)
                duration = int(audio.info.length)
            elif file_path.lower().endswith('.wav'):
                audio = WAVE(file_path)
                duration = int(audio.info.length)
            else:
                return None

            # Eğer dosya adında tire varsa, sanatçı ve başlık olarak ayır
            if " - " in name_without_ext:
                artist, title = name_without_ext.split(" - ", 1)
            else:
                artist = "Bilinmeyen Sanatçı"
                title = name_without_ext

            return Song(title, artist, file_path, duration)
        except Exception as e:
            print(f"Şarkı yükleme hatası: {e}")
            return None

    def get_duration(self):
        return self.duration

    def play(self):
        try:
            mixer.music.load(self.file_path)
            mixer.music.play()
        except Exception as e:
            print(f"Şarkı çalma hatası: {e}")

    @staticmethod
    def pause():
        try:
            mixer.music.pause()
        except Exception as e:
            print(f"Şarkı duraklatma hatası: {e}")

    @staticmethod
    def unpause():
        try:
            mixer.music.unpause()
        except Exception as e:
            print(f"Şarkı devam ettirme hatası: {e}")

    @staticmethod
    def stop():
        try:
            mixer.music.stop()
        except Exception as e:
            print(f"Şarkı durdurma hatası: {e}")

    @staticmethod
    def set_volume(value):
        try:
            mixer.music.set_volume(value / 100.0)
        except Exception as e:
            print(f"Ses ayarlama hatası: {e}")