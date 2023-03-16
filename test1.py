import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class FirstWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.button = QPushButton('Open Second Window', self)
        self.button.clicked.connect(self.open_second_window)

        vbox = QVBoxLayout()
        vbox.addWidget(self.button)
        self.setLayout(vbox)

        self.setGeometry(100, 100, 300, 300)
        self.setWindowTitle('First Window')
        self.show()

    def open_second_window(self):
        self.second_window = SecondWindow()
        self.second_window.show()
        self.close()

class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 300)
        self.setWindowTitle('Second Window')

def main():
    app = QApplication(sys.argv)
    window = FirstWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
