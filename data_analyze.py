import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, pearsonr, normaltest, shapiro, anderson
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox,
                             QLabel, QComboBox, QRadioButton, QCheckBox, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6 import QtWidgets



class HeartDataAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Heart Data Analyzer')
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(100, 100, 1200, 600)
        
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        
        self.info_label = QLabel('Load a CSV file to start analyzing the data', self)
        self.info_label.setGeometry(20, 20, 350, 20)
        self.info_label.setFont(font)
        
        self.load_button = QPushButton('Load CSV file', self)
        self.load_button.setGeometry(20, 50, 120, 30)
        self.load_button.clicked.connect(self.load_csv_file)
        
        # exit button
        self.exit_button = QPushButton('Exit', self)
        self.exit_button.setGeometry(20, 530, 120, 30)
        self.exit_button.clicked.connect(self.close)

        
        self.analyze_button = QPushButton('Analyze Data', self)
        self.analyze_button.setGeometry(20, 90, 120, 30)
        self.analyze_button.setEnabled(False)
        self.analyze_button.clicked.connect(self.analyze_data)
        
        self.method_label = QLabel('Select analysis method:', self)
        self.method_label.setGeometry(20, 140, 200, 20)
        self.method_label.setFont(font)
        
        self.method_combo = QComboBox(self)
        self.method_combo.setGeometry(20, 170, 250, 30)
        self.method_combo.addItems(['1. Classify columns', '2. Histograms', '3. Contingency tables',
                                    '4. Q-Q plots', '5. Boxplots', '6. Scatterplots'])
        self.method_combo.setEnabled(False)
        
        self.result_table = QTableWidget(self)
        self.result_table.setGeometry(300, 50, 880, 530)
        self.result_table.verticalHeader().setVisible(False)
        #self.result_table.horizontalHeader().resizeSections(QtWidgets.QHeaderView.ResizeToContentsMode)



        self.result_table.setColumnCount(2)
        self.result_table.setHorizontalHeaderLabels(['Variable', 'Type/Result'])
        
        self.show()
        
    # close button function
    def close(self):
        close = QMessageBox.question(self, 'Exit', 'Are you sure you want to exit?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if close == QMessageBox.StandardButton.Yes:
            sys.exit()
        else:
            pass
        
    def load_csv_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open CSV file', '', 'CSV files (*.csv)')
        if file_name:
            self.data = pd.read_csv(file_name, index_col=0)
            self.info_label.setText('File loaded successfully')
            self.analyze_button.setEnabled(True)
            self.method_combo.setEnabled(True)
        
    def analyze_data(self):
        method = self.method_combo.currentText().split('.')[0]
        if method == '1':
            self.classify_columns()
        elif method == '2':
            self.plot_histograms()
        elif method == '3':
            self.contingency_tables()
        elif method == '4':
            self.plot_qqplots()
        elif method == '5':
            self.plot_boxplots()
        elif method == '6':
            self.scatterplots_and_correlation()
        
            

        
    def classify_columns(self):
        var_types = {'quantitative': ['age', 'height', 'weight', 'ap_hi', 'ap_lo'],
                 'qualitative': ['gender', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'cardio'],
                 'ordinal': ['cholesterol', 'gluc']}
        
        for col in self.data.columns:
            if col in var_types['quantitative']:
                var_type = 'quantitative'
            elif col in var_types['qualitative']:
                var_type = 'qualitative'
            elif col in var_types['ordinal']:
                var_type = 'ordinal'
            else:
                var_type = 'identity'
            self.result_table.insertRow(self.result_table.rowCount())
            self.result_table.setItem(self.result_table.rowCount()-1, 0, QTableWidgetItem(col))
            self.result_table.setItem(self.result_table.rowCount()-1, 1, QTableWidgetItem(var_type))

    def plot_histograms(self):
        for col in self.data.columns:
            if col in ['id', 'cardio']:
                continue
            plt.hist(self.data[col])
            plt.title(col)
            plt.xlabel('Values')
            plt.ylabel('Frequency')
            plt.show()
        
    def contingency_tables(self):
        for i, col1 in enumerate(self.data.columns):
            if col1 in ['id', 'cardio']:
                continue
            for j, col2 in enumerate(self.data.columns[i+1:], i+1):
                if col2 in ['id', 'cardio']:
                    continue
                contingency_table = pd.crosstab(self.data[col1], self.data[col2])
                self.result_table.insertRow(self.result_table.rowCount())
                self.result_table.setItem(self.result_table.rowCount()-1, 0, QTableWidgetItem(f'{col1} vs {col2}'))
                self.result_table.setItem(self.result_table.rowCount()-1, 1, QTableWidgetItem(str(contingency_table)))
                
    def plot_qqplots(self):
        for col in self.data.columns:
            if col in ['id', 'gender', 'smoke', 'alco', 'active', 'cardio']:
                continue
            norm_values = np.random.normal(np.mean(self.data[col]), np.std(self.data[col]), len(self.data[col]))
            norm_values.sort()
            col_values = self.data[col].sort_values()
            plt.plot(norm_values, col_values, 'o')
            plt.plot([np.min((norm_values.min(), col_values.min())), np.max((norm_values.max(), col_values.max()))],
                    [np.min((norm_values.min(), col_values.min())), np.max((norm_values.max(), col_values.max()))], 'r')
            plt.title(col)
            plt.xlabel('Theoretical Quantiles')
            plt.ylabel('Sample Quantiles')
            plt.show()
            
            
                        
            # p = norm.test(self.data[col])
            p = normaltest(self.data[col])
            # Test for normality of each column
            for col in self.data.columns:
                p = normaltest(self.data[col])[1]  # extract the p-value from the tuple
                if p < 0.05:
                    self.result_table.insertRow(self.result_table.rowCount())
                    self.result_table.setItem(self.result_table.rowCount()-1, 0, QTableWidgetItem(col))

            # if p < 0.05:
            #     self.result_table.insertRow(self.result_table.rowCount())
            #     self.result_table.setItem(self.result_table.rowCount()-1, 0, QTableWidgetItem(col))
            #     self.result_table.setItem(self.result_table.rowCount()-1, 1, QTableWidgetItem('Not normal'))
            # else:
            #     self.result_table.insertRow(self.result_table.rowCount())
            #     self.result_table.setItem(self.result_table.rowCount()-1, 0, QTableWidgetItem(col))
            #     self.result_table.setItem(self.result_table.rowCount()-1, 1, QTableWidgetItem('Normal'))
                
    def plot_boxplots(self):
        for col in self.data.columns:
            if col in ['id', 'gender', 'smoke', 'alco', 'active', 'cardio']:
                continue
            plt.boxplot(self.data[col], vert=False)
            plt.title(col)
            plt.show()
            
    def scatterplots_and_correlation(self):
        for i, col1 in enumerate(self.data.columns):
            if col1 in ['id', 'gender', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'cardio']:
                continue
            for j, col2 in enumerate(self.data.columns[i+1:], i+1):
                if col2 in ['id', 'gender', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'cardio']:
                    continue
                plt.scatter(self.data[col1], self.data[col2])
                plt.title(f'{col1} vs {col2}')
                plt.xlabel(col1)
                plt.ylabel(col2)
                plt.show()
                correlation_coefficient = self.data[[col1, col2]].corr().iloc[0, 1]
                self.result_table.insertRow(self.result_table.rowCount())
                self.result_table.setItem(self.result_table.rowCount()-1, 0, QTableWidgetItem(f'{col1} vs {col2}'))
                self.result_table.setItem(self.result_table.rowCount()-1, 1, QTableWidgetItem(str(correlation_coefficient)))
                if correlation_coefficient > 0.8:
                    self.result_table.setItem(self.result_table.rowCount()-1, 2, QTableWidgetItem('Strong positive correlation'))
                elif correlation_coefficient > 0.6:
                    self.result_table.setItem(self.result_table.rowCount()-1, 2, QTableWidgetItem('Moderate positive correlation'))
                elif correlation_coefficient > 0.4:
                    self.result_table.setItem(self.result_table.rowCount()-1, 2, QTableWidgetItem('Weak positive correlation'))
                elif correlation_coefficient > -0.4:
                    self.result_table.setItem(self.result_table.rowCount()-1, 2, QTableWidgetItem('No correlation'))
                elif correlation_coefficient > -0.6:
                    self.result_table.setItem(self.result_table.rowCount()-1, 2, QTableWidgetItem('Weak negative correlation'))
                elif correlation_coefficient > -0.8:
                    self.result_table.setItem(self.result_table.rowCount()-1, 2, QTableWidgetItem('Moderate negative correlation'))
                else:
                    self.result_table.setItem(self.result_table.rowCount()-1, 2, QTableWidgetItem('Strong negative correlation'))
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HeartDataAnalyzer()
    window.show()
    sys.exit(app.exec())

        