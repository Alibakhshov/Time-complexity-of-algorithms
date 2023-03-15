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


# Please, create a beautiful designed GUI with pyqt6 that visually shows how the tasks are performed below. Add a button that asks to load the csv file with data. Please make sure the code perform each tasks and comment it

# Dataset contains x and y columns with 1000 rows possibly with outliers.
# Tasks: 
# 1. Regression with outliers (20 points)
#        a. Scatterplot
#        b. SquaredR
#        c. Scatterplot of residuals
#        d. Report your model
# 2. Identify and remove outliers (10 points)
# 3. Regression without outliers (20 points)
#       a. Scatterplot
#       b. SquaredR
#       c. Scatterplot of residuals
#       d. Report your model