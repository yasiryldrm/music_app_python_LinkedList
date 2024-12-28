import sys
from PyQt5.QtWidgets import QApplication
from data_structures.linked_list import PlayList
from ui.main_window import MainWindow
import traceback


def exception_hook(exctype, value, tb):
    print('Exception hook:')
    print('Type:', exctype)
    print('Value:', value)
    print('Traceback:', ''.join(traceback.format_tb(tb)))
    sys.exit(1)


def main():
    try:
        app = QApplication(sys.argv)
        sys.excepthook = exception_hook

        playlist = PlayList()
        window = MainWindow(playlist)
        window.show()

        return app.exec_()
    except Exception as e:
        print(f"Uygulama başlatılırken hata oluştu: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())