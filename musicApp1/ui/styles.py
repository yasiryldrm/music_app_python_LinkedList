class Styles:
    MAIN_WINDOW = """
        QMainWindow {
            background-color: #1e1e1e;
        }
        QLabel {
            color: white;
            font-size: 14px;
        }
        QPushButton {
            background-color: #333;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #444;
        }
        QListWidget {
            background-color: #2d2d2d;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 5px;
        }
        QListWidget::item {
            height: 30px;
        }
        QListWidget::item:selected {
            background-color: #444;
        }
        QSlider::groove:horizontal {
            border: 1px solid #999999;
            height: 8px;
            background: #4d4d4d;
            margin: 2px 0;
        }
        QSlider::handle:horizontal {
            background: #ffffff;
            border: 1px solid #5c5c5c;
            width: 18px;
            margin: -2px 0;
            border-radius: 3px;
        }
        QInputDialog {
            background-color: #2d2d2d;
            color: white;
        }
        QInputDialog QLabel {
            color: white;
        }
        QInputDialog QLineEdit {
            background-color: #333;
            color: white;
            border: 1px solid #555;
            padding: 5px;
        }
        QFileDialog {
            background-color: #2d2d2d;
            color: white;
        }
    """

    STATUS_BAR = """
        color: white; 
        background-color: #333;
    """