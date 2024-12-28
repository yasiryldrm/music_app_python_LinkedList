import json
import os

class PlaylistManager:
    PLAYLIST_FILE = "playlist.json"

    @staticmethod
    def save_playlist(songs):
        try:
            # Şarkı bilgilerini JSON formatına dönüştür
            playlist_data = [{
                'title': song.title,
                'artist': song.artist,
                'file_path': song.file_path,
                'duration': song.duration
            } for song in songs]

            # JSON dosyasına kaydet
            with open(PlaylistManager.PLAYLIST_FILE, 'w', encoding='utf-8') as f:
                json.dump(playlist_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Playlist kaydetme hatası: {e}")

    @staticmethod
    def load_playlist():
        try:
            if os.path.exists(PlaylistManager.PLAYLIST_FILE):
                with open(PlaylistManager.PLAYLIST_FILE, 'r', encoding='utf-8') as f:
                    playlist_data = json.load(f)
                return playlist_data
            return []
        except Exception as e:
            print(f"Playlist yükleme hatası: {e}")
            return [] 