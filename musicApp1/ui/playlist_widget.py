from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QMenu
from PyQt5.QtCore import Qt
from pygame import mixer


class PlaylistWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        list_header = QLabel("Çalma Listesi")
        layout.addWidget(list_header)
        self.song_list = QListWidget()
        layout.addWidget(self.song_list)
        
        # Çift tıklama olayını bağla
        self.song_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        
        # Sağ tık menüsü için context menu'yü etkinleştir
        self.song_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.song_list.customContextMenuRequested.connect(self.show_context_menu)

    def on_item_double_clicked(self, item):
        try:
            index = self.song_list.row(item)
            current = self.parent.playlist.get_node_at_index(index)
            if current:
                self.parent.playlist.current = current
                self.parent.current_position = 0  # Pozisyonu sıfırla
                self.parent.playlist.play_current()
                self.parent.playlist.is_playing = True
                self.parent.update_timer.start()
                self.parent.update_current_song()
                self.parent.player_controls.update_play_button_state(True)
                # Progress bar'ı sıfırla
                self.parent.player_controls.update_progress(0, current.song.get_duration())
        except Exception as e:
            print(f"Şarkı çalma hatası: {e}")

    def update_song_list(self, songs):
        self.song_list.clear()
        for song in songs:
            self.song_list.addItem(f"{song.title} - {song.artist}")

    def show_context_menu(self, position):
        menu = QMenu()
        delete_action = menu.addAction("Sil")
        action = menu.exec_(self.song_list.mapToGlobal(position))
        
        if action == delete_action:
            self.delete_selected_song()

    def delete_selected_song(self):
        try:
            current_row = self.song_list.currentRow()
            if current_row >= 0:
                current = self.parent.playlist.get_node_at_index(current_row)
                if current:
                    # Eğer çalan şarkı siliniyorsa, önce durdur
                    if current == self.parent.playlist.current:
                        self.parent.playlist.is_playing = False
                        self.parent.update_timer.stop()
                        mixer.music.stop()
                        self.parent.current_position = 0
                        self.parent.player_controls.update_play_button_state(False)

                    # Şarkıyı playlist'ten sil
                    self.parent.playlist.remove_song(current)
                    
                    # UI'ı güncelle
                    self.song_list.takeItem(current_row)
                    
                    # Playlist'i kaydet
                    from models.playlist_manager import PlaylistManager
                    PlaylistManager.save_playlist(self.parent.playlist.get_all_songs())
                    
                    self.parent.statusBar().showMessage("Şarkı silindi")
        except Exception as e:
            print(f"Şarkı silme hatası: {e}")
            import traceback
            traceback.print_exc()

    def move_item_up(self):
        current_row = self.song_list.currentRow()
        if current_row > 0:
            # UI'da şarkıyı yukarı taşı
            self.song_list.insertItem(current_row - 1, self.song_list.takeItem(current_row))
            self.song_list.setCurrentRow(current_row - 1)
            
            # Playlist'te şarkıların sırasını güncelle
            current = self.parent.playlist.get_node_at_index(current_row)
            prev = self.parent.playlist.get_node_at_index(current_row - 1)
            
            if current and prev:
                # Bağlantıları güncelle
                if prev.prev:
                    prev.prev.next = current
                else:
                    self.parent.playlist.head = current
                    
                if current.next:
                    current.next.prev = prev
                else:
                    self.parent.playlist.tail = prev
                    
                current.prev = prev.prev
                prev.next = current.next
                current.next = prev
                prev.prev = current
                
                # Playlist'i kaydet
                from models.playlist_manager import PlaylistManager
                PlaylistManager.save_playlist(self.parent.playlist.get_all_songs())

    def move_item_down(self):
        current_row = self.song_list.currentRow()
        if current_row < self.song_list.count() - 1:
            # UI'da şarkıyı aşağı taşı
            self.song_list.insertItem(current_row + 1, self.song_list.takeItem(current_row))
            self.song_list.setCurrentRow(current_row + 1)
            
            # Playlist'te şarkıların sırasını güncelle
            current = self.parent.playlist.get_node_at_index(current_row)
            next_node = self.parent.playlist.get_node_at_index(current_row + 1)
            
            if current and next_node:
                # Bağlantıları güncelle
                if current.prev:
                    current.prev.next = next_node
                else:
                    self.parent.playlist.head = next_node
                    
                if next_node.next:
                    next_node.next.prev = current
                else:
                    self.parent.playlist.tail = current
                    
                next_node.prev = current.prev
                current.next = next_node.next
                next_node.next = current
                current.prev = next_node
                
                # Playlist'i kaydet
                from models.playlist_manager import PlaylistManager
                PlaylistManager.save_playlist(self.parent.playlist.get_all_songs())