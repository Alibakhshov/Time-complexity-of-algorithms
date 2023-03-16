import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # set window title and size
        self.setWindowTitle("Regression Analysis")
        self.setGeometry(100, 100, 800, 600)

        # create a button to load data
        self.load_data_button = QPushButton("Load Data", self)
        self.load_data_button.setGeometry(50, 50, 100, 50)
        self.load_data_button.clicked.connect(self.load_data)

        # create a label to display the filename
        self.file_label = QLabel("", self)
        self.file_label.setGeometry(200, 50, 400, 50)

        # create a button to perform regression with outliers
        self.regression_with_outliers_button = QPushButton("Regression with Outliers", self)
        self.regression_with_outliers_button.setGeometry(50, 150, 200, 50)
        self.regression_with_outliers_button.clicked.connect(self.regression_with_outliers)

        # create a button to remove outliers
        self.remove_outliers_button = QPushButton("Remove Outliers", self)
        self.remove_outliers_button.setGeometry(50, 250, 200, 50)
        self.remove_outliers_button.clicked.connect(self.remove_outliers)

        # create a button to perform regression without outliers
        self.regression_without_outliers_button = QPushButton("Regression without Outliers", self)
        self.regression_without_outliers_button.setGeometry(50, 350, 200, 50)
        self.regression_without_outliers_button.clicked.connect(self.regression_without_outliers)

    def load_data(self):
        # open a file dialog to select the CSV file
        filename, _ = QFileDialog.getOpenFileName(self, "Load Data", "", "CSV Files (*.csv)")
        if filename:
            # load the data into a pandas DataFrame
            self.data = pd.read_csv(filename)
            self.file_label.setText(f"File: {filename}")

    def regression_with_outliers(self):
        # check if data has been loaded
        if not hasattr(self, "data"):
            return

        # perform regression with outliers
        x = self.data["x"]
        y = self.data["y"]
        coeffs = np.polyfit(x, y, 1)
        m = coeffs[0]
        b = coeffs[1]
        y_pred = m * x + b
        residuals = y - y_pred
        squared_r = np.corrcoef(x, y)[0,1] ** 2
        outlier_mask = np.abs(residuals) > 3 * np.std(residuals)

        # create a scatterplot
        fig, ax = plt.subplots()
        ax.scatter(x, y)
        ax.plot(x, y_pred, color="red")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Regression with Outliers")

        # create a scatterplot of residuals
        fig2, ax2 = plt.subplots()
        ax2.scatter(x[outlier_mask], residuals[outlier_mask], color="red")
        ax2.scatter(x[~outlier_mask], residuals[~outlier_mask], color="blue")
        ax2.axhline(y=0, color="black", linestyle="--")
        ax2.set_xlabel("x")
        ax2.set_ylabel("Residuals")
        ax2.set_title("Scatterplot of Residuals")

        # display the squared R
        print(f"Squared R: {squared_r}")

        # display the model coefficients
        print(f"Model: y = {m:.2f}x + {b:.2f}")

        # display the number of outliers
        num_outliers = np.sum(outlier_mask)
        print(f"Number of Outliers: {num_outliers}")

        # show the plots
        plt.show()

    def remove_outliers(self):
        # check if data has been loaded
        if not hasattr(self, "data"):
            return

        # remove outliers from the data
        x = self.data["x"]
        y = self.data["y"]
        residuals = y - np.polyfit(x, y, 1)[0] * x
        outlier_mask = np.abs(residuals) > 3 * np.std(residuals)
        self.data = self.data[~outlier_mask]
        self.file_label.setText("File: Data (outliers removed)")

    def regression_without_outliers(self):
        # check if data has been loaded
        if not hasattr(self, "data"):
            return

        # perform regression without outliers
        x = self.data["x"]
        y = self.data["y"]
        coeffs = np.polyfit(x, y, 1)
        m = coeffs[0]
        b = coeffs[1]
        y_pred = m * x + b
        residuals = y - y_pred
        squared_r = np.corrcoef(x, y)[0,1] ** 2

        # create a scatterplot
        fig, ax = plt.subplots()
        ax.scatter(x, y)
        ax.plot(x, y_pred, color="red")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Regression without Outliers")

        # create a scatterplot of residuals
        fig2, ax2 = plt.subplots()
        ax2.scatter(x, residuals)
        ax2.axhline(y=0, color="black", linestyle="--")
        ax2.set_xlabel("x")
        ax2.set_ylabel("Residuals")
        ax2.set_title("Scatterplot of Residuals")

        # display the squared R
        print(f"Squared R: {squared_r}")

        # display the model coefficients
        print(f"Model: y = {m:.2f}x + {b:.2f}")

        # show the plots
        plt.show()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
            
        



            
