from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QInputDialog, QFileDialog)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont, QIcon
from models.song import Song
from ui.player_controls import PlayerControls
from ui.playlist_widget import PlaylistWidget
from ui.styles import Styles
from pygame import mixer
import random
import os
from models.playlist_manager import PlaylistManager


class MainWindow(QMainWindow):
    def __init__(self, playlist):
        super().__init__()
        # Mixer'ı başlat
        try:
            mixer.init()
        except Exception as e:
            print(f"Mixer başlatma hatası: {e}")
            
        self.playlist = playlist
        self.current_position = 0
        self.setup_ui()
        self.setup_timer()
        self.load_saved_playlist()
        
        # Uygulama ikonu ayarla
        try:
            app_icon = QIcon("assets/icon.png")  # icon.png olarak güncellendi
            self.setWindowIcon(app_icon)
        except Exception as e:
            print(f"İkon yükleme hatası: {e}")

    def setup_ui(self):
        self.setWindowTitle("Müzik Çalar")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(Styles.MAIN_WINDOW)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Üst bilgi alanı
        top_info = QHBoxLayout()
        self.current_song_label = QLabel("Şu an çalan: -")
        self.current_song_label.setFont(QFont("Arial", 16))
        top_info.addWidget(self.current_song_label)
        main_layout.addLayout(top_info)

        # Şarkı listesi widget'ı
        self.playlist_widget = PlaylistWidget(self)
        main_layout.addWidget(self.playlist_widget)

        # Kontrol widget'ı
        self.player_controls = PlayerControls(self)
        main_layout.addWidget(self.player_controls)

        # Status bar
        self.statusBar().setStyleSheet(Styles.STATUS_BAR)
        self.statusBar().showMessage("Hazır")

    def setup_timer(self):
        self.update_timer = QTimer()
        self.update_timer.setInterval(1000)  # Her saniye güncelle
        self.update_timer.timeout.connect(self.update_progress)

    def seek_position(self, position):
        try:
            if self.playlist.current:
                # Eğer pozisyon değişimi çok küçükse, yeniden yükleme yapma
                if abs(self.current_position - position) < 2:
                    return

                current_song = self.playlist.current.song
                
                # Müziği yükle ve çal
                mixer.music.load(current_song.file_path)
                mixer.music.play(start=position)
                
                self.current_position = position
                
                # Çalma durumunu güncelle
                self.playlist.is_playing = True
                self.update_timer.start()
                self.player_controls.update_play_button_state(True)
                
        except Exception as e:
            print(f"Pozisyon değiştirme hatası: {e}")

    def toggle_play(self):
        try:
            if not self.playlist.current:
                if self.playlist.head:
                    self.playlist.current = self.playlist.head
                else:
                    return

            if self.playlist.is_playing:
                Song.pause()
                self.update_timer.stop()
                self.playlist.is_playing = False
                self.statusBar().showMessage("Duraklatıldı")
            else:
                if self.playlist.current:
                    mixer.music.load(self.playlist.current.song.file_path)
                    mixer.music.play(start=self.current_position)
                    self.playlist.is_playing = True
                    self.update_timer.start()
                    self.statusBar().showMessage("Çalınıyor")

            self.player_controls.update_play_button_state(self.playlist.is_playing)
        except Exception as e:
            print(f"Oynatma/duraklatma hatası: {e}")

    def update_progress(self):
        if self.playlist.is_playing and self.playlist.current:
            try:
                self.current_position += 1
                duration = self.playlist.current.song.get_duration()

                if self.current_position >= duration:
                    self.play_next()
                else:
                    self.player_controls.update_progress(self.current_position, duration)

            except Exception as e:
                print(f"İlerleme güncellenirken hata: {e}")

    def add_song(self):
        try:
            files, _ = QFileDialog.getOpenFileNames(
                self, "Şarkı Seç", "", "Music Files (*.mp3 *.wav)"
            )
            if files:
                for file_path in files:
                    song = Song.from_file(file_path)
                    if song:
                        self.playlist.add_song(song)
                self.playlist_widget.update_song_list(self.playlist.get_all_songs())
                PlaylistManager.save_playlist(self.playlist.get_all_songs())
                self.statusBar().showMessage(f"{len(files)} şarkı eklendi")
        except Exception as e:
            print(f"Şarkı ekleme hatası: {e}")

    def play_selected(self, item):
        try:
            index = self.playlist_widget.song_list.row(item)
            current = self.playlist.head
            for _ in range(index):
                current = current.next
            self.playlist.current = current
            self.playlist.play_current()
            self.playlist.is_playing = True
            self.update_timer.start()
            self.update_current_song()
            self.player_controls.update_play_button_state(True)
            self.statusBar().showMessage(f"Çalınıyor: {current.song.title}")
        except Exception as e:
            print(f"Seçili şarkıyı çalma hatası: {e}")
            import traceback
            traceback.print_exc()

    def play_next(self):
        try:
            if self.playlist.play_next():
                self.current_position = 0
                self.update_current_song()
                self.player_controls.update_play_button_state(True)
                self.playlist.is_playing = True
                self.update_timer.start()
                self.player_controls.update_progress(0, self.playlist.current.song.get_duration())
                return True
            return False
        except Exception as e:
            print(f"Sonraki şarkıya geçme hatası: {e}")
            return False

    def play_previous(self):
        try:
            if self.playlist.play_previous():
                self.current_position = 0
                self.update_current_song()
                self.player_controls.update_play_button_state(True)
                self.playlist.is_playing = True
                self.update_timer.start()
                self.player_controls.update_progress(0, self.playlist.current.song.get_duration())
        except Exception as e:
            print(f"Önceki şarkıya geçme hatası: {e}")

    def update_current_song(self):
        try:
            current = self.playlist.get_current_song()
            if current:
                self.current_song_label.setText(f"Şu an çalan: {current.title} - {current.artist}")
                self.statusBar().showMessage(f"Çalınıyor: {current.title}")
            else:
                self.current_song_label.setText("Şu an çalan: -")
                self.statusBar().showMessage("Hazır")
        except Exception as e:
            print(f"Şarkı bilgisi güncelleme hatası: {e}")

    def toggle_volume_slider(self):
        try:
            self.player_controls.volume_slider.setVisible(
                not self.player_controls.volume_slider.isVisible()
            )
        except Exception as e:
            print(f"Ses ayarı görünürlük hatası: {e}")

    def change_volume(self, value):
        try:
            Song.set_volume(value)
            self.statusBar().showMessage(f"Ses seviyesi: {value}%")
        except Exception as e:
            print(f"Ses değiştirme hatası: {e}")

    def shuffle_playlist(self):
        try:
            if self.playlist.size < 2:
                return

            current_song = self.playlist.get_current_song()
            songs = self.playlist.get_all_songs()
            random.shuffle(songs)

            self.playlist = type(self.playlist)()
            for song in songs:
                self.playlist.add_song(song)

            if current_song:
                current = self.playlist.head
                while current:
                    if current.song.file_path == current_song.file_path:
                        self.playlist.current = current
                        break
                    current = current.next

            self.playlist_widget.update_song_list(self.playlist.get_all_songs())
            self.statusBar().showMessage("Çalma listesi karıştırıldı")
        except Exception as e:
            print(f"Playlist karıştırma hatası: {e}")

    def load_saved_playlist(self):
        try:
            playlist_data = PlaylistManager.load_playlist()
            for song_data in playlist_data:
                if os.path.exists(song_data['file_path']):
                    song = Song(
                        song_data['title'],
                        song_data['artist'],
                        song_data['file_path'],
                        song_data['duration']
                    )
                    self.playlist.add_song(song)
            
            # Playlist widget'ını güncelle
            self.playlist_widget.update_song_list(self.playlist.get_all_songs())
        except Exception as e:
            print(f"Kayıtlı playlist yükleme hatası: {e}")

    def closeEvent(self, event):
        try:
            # Önce playlist'i kaydet
            PlaylistManager.save_playlist(self.playlist.get_all_songs())
            
            # Müziği durdur
            if mixer.get_init():
                mixer.music.stop()
                
            # Timer'ı durdur
            if hasattr(self, 'update_timer'):
                self.update_timer.stop()
                
            # Mixer'ı sonlandır
            mixer.quit()
            
            event.accept()
        except Exception as e:
            print(f"Uygulama kapatma hatası: {e}")
            event.accept()