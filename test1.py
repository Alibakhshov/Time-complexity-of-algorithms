import sys
import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Regression Analysis and Outlier Detection")

        self.csv_file = None

        self.scatterplot_label = QLabel(self)
        self.scatterplot_label.setGeometry(20, 70, 450, 450)

        self.squaredR_label = QLabel(self)
        self.squaredR_label.setGeometry(500, 70, 450, 50)

        self.residuals_label = QLabel(self)
        self.residuals_label.setGeometry(500, 130, 450, 450)

        load_button = QPushButton("Load CSV File", self)
        load_button.setGeometry(20, 20, 150, 30)
        load_button.clicked.connect(self.load_csv)

        regression_button = QPushButton("Perform Regression", self)
        regression_button.setGeometry(200, 20, 150, 30)
        regression_button.clicked.connect(self.perform_regression)

        outlier_button = QPushButton("Remove Outliers", self)
        outlier_button.setGeometry(380, 20, 150, 30)
        outlier_button.clicked.connect(self.remove_outliers)

    def load_csv(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.csv_file, _ = QFileDialog.getOpenFileName(self, "Load CSV File", "",
                                                       "CSV Files (*.csv)", options=options)

    def perform_regression(self):
        if not self.csv_file:
            QMessageBox.warning(self, "Error", "Please load a CSV file first.")
            return

        data = pd.read_csv(self.csv_file)
        x = data['x'].values.reshape(-1, 1)
        y = data['y'].values.reshape(-1, 1)

        # Scatterplot
        plt.scatter(x, y)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Scatterplot with Outliers')
        plt.savefig('scatterplot.png')
        plt.clf()

        pixmap = QPixmap('scatterplot.png')
        self.scatterplot_label.setPixmap(pixmap)

        # Regression with outliers
        model = LinearRegression().fit(x, y)
        y_pred = model.predict(x)
        r2 = r2_score(y, y_pred)

        # SquaredR
        self.squaredR_label.setText(f"Squared R: {r2:.4f}")

        # Scatterplot of residuals
        plt.scatter(x, y - y_pred)
        plt.xlabel('x')
        plt.ylabel('Residuals')
        plt.title('Scatterplot of Residuals with Outliers')
        plt.savefig('residuals.png')
        plt.clf()

        pixmap = QPixmap('residuals.png')
        self.residuals_label.setPixmap(pixmap)

        # Report model
        QMessageBox.information(self, "Regression Report", f"Intercept: {model.intercept_[0]:.4f}\nSlope: {model.coef_[0][0]:.4f}\nSquared R: {r2:.4f}")

    def remove_outliers(self):
        if not self.csv_file:
            QMessageBox.warning(self, "Error", "Please load a CSV file first.")
            return

        data = pd.read_csv(self.csv_file)
         x = data['x'].values.reshape(-1, 1)
    y = data['y'].values.reshape(-1, 1)

    # Identify and remove outliers
    model = LinearRegression().fit(x, y)
    y_pred = model.predict(x)
    residuals = y - y_pred
    outliers = residuals > 3 * residuals.std()

    x_no_outliers = x[~outliers]
    y_no_outliers = y[~outliers]

    # Regression without outliers
    model_no_outliers = LinearRegression().fit(x_no_outliers, y_no_outliers)
    y_pred_no_outliers = model_no_outliers.predict(x_no_outliers)
    r2_no_outliers = r2_score(y_no_outliers, y_pred_no_outliers)

    # Scatterplot
    plt.scatter(x_no_outliers, y_no_outliers)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Scatterplot without Outliers')
    plt.savefig('scatterplot.png')
    plt.clf()

    pixmap = QPixmap('scatterplot.png')
    self.scatterplot_label.setPixmap(pixmap)

    # SquaredR
    self.squaredR_label.setText(f"Squared R: {r2_no_outliers:.4f}")

    # Scatterplot of residuals
    plt.scatter(x_no_outliers, y_no_outliers - y_pred_no_outliers)
    plt.xlabel('x')
    plt.ylabel('Residuals')
    plt.title('Scatterplot of Residuals without Outliers')
    plt.savefig('residuals.png')
    plt.clf()

    pixmap = QPixmap('residuals.png')
    self.residuals_label.setPixmap(pixmap)

    # Report model
    QMessageBox.information(self, "Regression Report", f"Intercept: {model_no_outliers.intercept_[0]:.4f}\nSlope: {model_no_outliers.coef_[0][0]:.4f}\nSquared R: {r2_no_outliers:.4f}")