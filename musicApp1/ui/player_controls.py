from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QSlider, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from models.song import Song
from pygame import mixer
from ui.custom_slider import CustomSlider  # CustomSlider'ı dahil edin


class PlayerControls(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.is_seeking = False
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        control_layout = QVBoxLayout(self)

        # İlerleme çubuğu
        progress_layout = QHBoxLayout()
        self.time_label = QLabel("0:00")
        self.progress_bar = CustomSlider(Qt.Horizontal)  # CustomSlider kullan
        self.duration_label = QLabel("0:00")

        # İlerleme çubuğu stil ayarları
        self.progress_bar.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #4a4a4a;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #ffffff;
                width: 16px;
                height: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: #0088cc;
                height: 8px;
                border-radius: 4px;
            }
        """)

        progress_layout.addWidget(self.time_label)
        progress_layout.addWidget(self.progress_bar, stretch=1)
        progress_layout.addWidget(self.duration_label)
        control_layout.addLayout(progress_layout)

        # Çalma kontrolleri
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        button_size = 60

        # Ana kontrol butonları
        self.prev_button = QPushButton("⏮")
        self.play_button = QPushButton("▶")
        self.next_button = QPushButton("⏭")
        self.shuffle_button = QPushButton("🔀")
        self.volume_button = QPushButton("🔊")

        # Playlist kontrol butonları
        self.up_button = QPushButton("↑")
        self.down_button = QPushButton("↓")
        self.add_button = QPushButton("➕")
        self.delete_button = QPushButton("🗑️")

        # Tüm butonları bir diziye koy
        all_buttons = [
            self.prev_button, self.play_button, self.next_button,
            self.shuffle_button, self.volume_button,
            self.up_button, self.down_button, self.add_button, self.delete_button
        ]

        # Butonları ayarla
        for button in all_buttons:
            button.setFixedSize(button_size, button_size)
            button.setFont(QFont("Arial", 20))
            buttons_layout.addWidget(button)

        buttons_layout.addStretch()
        control_layout.addLayout(buttons_layout)

        # Ses kontrolü
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(100)
        self.volume_slider.setFixedWidth(100)
        self.volume_slider.hide()

        volume_layout = QHBoxLayout()
        volume_layout.addStretch()
        volume_layout.addWidget(self.volume_slider)
        control_layout.addLayout(volume_layout)

        # İlerleme çubuğu olaylarını bağla
        self.progress_bar.sliderPressed.connect(self.on_seek_start)
        self.progress_bar.sliderReleased.connect(self.on_seek_end)
        self.progress_bar.valueChanged.connect(self.on_seek_change)

    def connect_signals(self):
        # Ana kontrol sinyalleri
        self.prev_button.clicked.connect(self.parent.play_previous)
        self.next_button.clicked.connect(self.parent.play_next)
        self.play_button.clicked.connect(self.parent.toggle_play)
        self.volume_button.clicked.connect(self.parent.toggle_volume_slider)
        self.volume_slider.valueChanged.connect(self.parent.change_volume)
        self.shuffle_button.clicked.connect(self.parent.shuffle_playlist)

        # Playlist kontrol sinyalleri
        self.up_button.clicked.connect(self.parent.playlist_widget.move_item_up)
        self.down_button.clicked.connect(self.parent.playlist_widget.move_item_down)
        self.add_button.clicked.connect(self.parent.add_song)
        self.delete_button.clicked.connect(self.parent.playlist_widget.delete_selected_song)

    def update_play_button_state(self, is_playing):
        try:
            self.play_button.setText("⏸" if is_playing else "▶")
        except Exception as e:
            print(f"Play butonu güncellenirken hata: {e}")

    def update_progress(self, pos, duration):
        try:
            if pos >= 0 and duration > 0:
                self.progress_bar.setValue(int(pos))
                self.progress_bar.setMaximum(int(duration))
                self.time_label.setText(f"{int(pos // 60)}:{int(pos % 60):02d}")
                self.duration_label.setText(f"{int(duration // 60)}:{int(duration % 60):02d}")
        except Exception as e:
            print(f"İlerleme çubuğu güncellenirken hata: {e}")

    def on_seek_start(self):
        self.is_seeking = True

    def on_seek_change(self, value):
        try:
            minutes = value // 60
            seconds = value % 60
            self.time_label.setText(f"{minutes}:{seconds:02d}")
            
            if self.parent.playlist.current:
                self.parent.seek_position(value)
        except Exception as e:
            print(f"Pozisyon güncellenirken hata: {e}")

    def on_seek_end(self):
        self.is_seeking = False

