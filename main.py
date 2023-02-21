import sys
import os
import time
import threading
import matplotlib.pyplot as plt
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QComboBox, QTextEdit, QHBoxLayout, QVBoxLayout, QFileDialog, QMessageBox
import re
from PyQt6 import QtGui
import time

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
        yield arr


def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
        yield arr


def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:]
        yield from merge_sort(L)
        yield from merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
        yield arr


def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
        yield arr
    arr[i+1], arr[high] = arr[high], arr[i+1]
    yield arr
    return i+1

def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        yield from quick_sort(arr, low, pi-1)
        yield from quick_sort(arr, pi+1, high)
        
                


def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1
    for i in range(1, 10):
        count[i] += count[i-1]
    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1
    for i in range(n):
        arr[i] = output[i]
        yield arr
        
def radix_sort(arr):
    max_num = max(arr)
    exp = 1
    while max_num // exp > 0:
        yield from counting_sort(arr, exp)
        exp *= 10


class SortingAlgorithm:
    def __init__(self, name, function):
        self.name = name
        self.function = function
        


class Sorter(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        
        # Set window properties
        self.setWindowTitle("Sorting Algorithm Visualizer")
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon("static/img/icon.png"))
        self.setStyleSheet("background: rgb(20,0,36);")
    
        # Create widgets
        self.input_label = QLabel("Input:")
        self.input_textbox = QLineEdit()
        self.input_textbox.setPlaceholderText("Enter a list of numbers separated by commas")
        self.load_button = QPushButton("Load from File")
        self.sort_button = QPushButton("Sort")
        self.save_button = QPushButton("Save to File")
        self.exit_button = QPushButton("Exit")
        # self.exit_button.setStyleSheet("background-color: #0f140c;")
        self.clear_button = QPushButton("Clear")
        self.output_label = QLabel("Output:")
        self.output_textbox = QTextEdit()
        self.output_textbox.setReadOnly(True)
        self.algo_label = QLabel("Algorithm:")
        self.algo_combobox = QComboBox()
        self.algo_combobox.addItem("Bubble Sort")
        self.algo_combobox.addItem("Selection Sort")
        self.algo_combobox.addItem("Insertion Sort")
        self.algo_combobox.addItem("Merge Sort")
        self.algo_combobox.addItem("Quick Sort")
        self.algo_combobox.addItem("Counting Sort")
        self.algo_combobox.addItem("Radix Sort")
        self.time_label = QLabel(self)
       


        # Create layout
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_textbox)
        input_layout.addWidget(self.load_button)
        algo_layout = QHBoxLayout()
        algo_layout.addWidget(self.algo_label)
        algo_layout.addWidget(self.algo_combobox)
        algo_layout.addWidget(self.time_label)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.sort_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.exit_button)
        button_layout.addWidget(self.clear_button)
        output_layout = QVBoxLayout()
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_textbox)
        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(algo_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(output_layout)
        
        self.setLayout(main_layout)

        # Connect signals to slots
        self.load_button.clicked.connect(self.load_file)
        self.sort_button.clicked.connect(self.sort_list)
        self.save_button.clicked.connect(self.save_file)
        self.exit_button.clicked.connect(self.close)
        self.clear_button.clicked.connect(self.clear)
        self.show()

    # closing the application
    def close(self):
        QApplication.quit()
        
    def clear(self):
        self.input_textbox.clear()
        self.output_textbox.clear()
        self.time_label.clear()

        
    def load_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if filename:
            try:
                with open(filename, "r") as file:
                    numbers = file.read().strip().split("\n")
                    self.input_textbox.setText(",".join(numbers))
            except Exception as e:
                self.show_error("Error loading file: " + str(e))
        
    def sort_list(self):
        # Get input list
        input_str = self.input_textbox.text()
        try:
            input_list = [int(x.strip()) for x in input_str.split(",")]
        except Exception as e:
            self.show_error("Invalid input: " + str(e))
            return

        # Get selected algorithm
        algo_name = self.algo_combobox.currentText()
        algo = SortingAlgorithm(algo_name, None)
        if algo_name == "Bubble Sort":
            algo.function = bubble_sort
        elif algo_name == "Selection Sort":
            algo.function = selection_sort  
        elif algo_name == "Insertion Sort":
            algo.function = insertion_sort
        elif algo_name == "Merge Sort":
            algo.function = merge_sort
        elif algo_name == "Quick Sort":
            algo.function = quick_sort
        elif algo_name == "Counting Sort":
            algo.function = counting_sort
        elif algo_name == "Radix Sort":
            algo.function = radix_sort

        # Run sorting algorithm and update output
        start_time = time.time()
        output = []
        for step in algo.function(input_list):
            output.append(", ".join(str(x) for x in step))
        end_time = time.time()

        time_taken = end_time - start_time
        time_taken_text = "Time taken: {:.6f} seconds".format(time_taken)
        self.time_label.setText(time_taken_text)

        self.output_textbox.setText("\n".join(output))
    
    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if filename:
            try:
                with open(filename, "w") as file:
                    file.write(self.output_textbox.toPlainText())
            except Exception as e:
                self.show_error("Error saving file: " + str(e))

    def show_error(self, message):
        msg = QMessageBox()
        # msg.setIcon(QMessageBox.Critical)
        msg.setIcon(QMessageBox.critical(None, "Error", "Error loading file: " + str(e)))

        msg.setText("Error")
        msg.setInformativeText(message)
        msg.setWindowTitle("Error")
        msg.exec_()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Sorter()
    sys.exit(app.exec())
                