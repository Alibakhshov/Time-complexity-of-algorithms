import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

from link_list import App

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 400, 300)

        button = QPushButton("Open Second Window", self)
        button.setGeometry(150, 150, 100, 50)
        button.clicked.connect(self.open_second_window)

    def open_second_window(self):
        self.second_window = App()
        self.second_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
