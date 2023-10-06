import sys
import time
from PyQt6.QtWidgets import (
    QApplication, QWidget, 
    QPushButton, QLineEdit, 
    QLabel, QComboBox, 
    QTextEdit, QHBoxLayout, 
    QVBoxLayout, QFileDialog, 
    QMessageBox, QDialog,
    QDialogButtonBox)
from PyQt6 import QtGui
from link_list import App
from adjacency_matrix import ShortestPathFinder
from graph import ShortestPathFinderFromGraph
from greedy_algorithm import ShortestPathApp

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

def quick_sort(arr, start, end):
    stack = [(start, end)]
    while stack:
        start, end = stack.pop()
        if start >= end:
            continue
        pivot = partition(arr, start, end)
        stack.append((start, pivot - 1))
        stack.append((pivot + 1, end))

def partition(arr, start, end):
    pivot = arr[end]
    i = start - 1
    for j in range(start, end):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[end] = arr[end], arr[i + 1]
    return i + 1


def counting_sort(arr):
    # Find the maximum element in the array
    max_element = max(arr)
    
    # Create a count array of size max_element+1 and initialize all its elements to 0
    count = [0] * (max_element+1)
    
    # Count the number of occurrences of each element in the input array
    for i in range(len(arr)):
        count[arr[i]] += 1
    
    # Modify the count array to contain the number of elements <= each element
    for i in range(1, len(count)):
        count[i] += count[i-1]
    
    # Create a result array of the same size as the input array and fill it with 0s
    result = [0] * len(arr)
    
    # Iterate over the input array in reverse order and place each element in its sorted position in the result array
    for i in range(len(arr)-1, -1, -1):
        result[count[arr[i]]-1] = arr[i]
        count[arr[i]] -= 1
    
    # Return the sorted result array
    return result
        
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
        self.setGeometry(100, 150, 1300, 600)
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon("static/img/icon.png"))
        # self.setStyleSheet("background: rgb(20,0,36);")
    
        # Create widgets
        self.input_label = QLabel("Input:")
        self.input_textbox = QLineEdit()
        self.input_textbox.setPlaceholderText("Enter a list of numbers separated by commas")
        self.load_button = QPushButton("Load from File")    
        self.sort_button = QPushButton("Sort")
        self.link_list_button = QPushButton("Linked List")
        self.shortest_path_button_djikarta_algorithm = QPushButton("Adjacency matrix")
        self.shortest_path_from_graph = QPushButton("Shortest Path (Djikarta Algorithm)")
        self.shortest_path_greeedy_algorithm = QPushButton("Shortest Path (Greedy Algorithm)")
        self.save_button = QPushButton("Save to File")
        self.exit_button = QPushButton("Exit")
        self.change_theme_button = QPushButton("Change Theme")
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
        self.length_of_array_label = QLabel(self)
       
        # Create layout
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_textbox)
        input_layout.addWidget(self.load_button)
        algo_layout = QHBoxLayout()
        algo_layout.addWidget(self.algo_label)
        algo_layout.addWidget(self.algo_combobox)
        algo_layout.addWidget(self.time_label)
        algo_layout.addWidget(self.length_of_array_label)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.sort_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.link_list_button)
        button_layout.addWidget(self.shortest_path_button_djikarta_algorithm)
        button_layout.addWidget(self.shortest_path_from_graph)
        button_layout.addWidget(self.shortest_path_greeedy_algorithm)
        button_layout.addWidget(self.exit_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.change_theme_button)
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
        self.exit_button.clicked.connect(self.exit)
        self.clear_button.clicked.connect(self.clear)
        self.link_list_button.clicked.connect(self.link_list_open)
        self.shortest_path_button_djikarta_algorithm.clicked.connect(self.shortest_path_open)
        self.shortest_path_greeedy_algorithm.clicked.connect(self.shortest_path_open_greedy_algorithm)
        self.change_theme_button.clicked.connect(self.change_theme)
        self.show()
        
    def link_list_open(self):
        self.second_window = App()
        self.second_window.show()
        self.close()
        
    def shortest_path_open(self):
        self.third_window = ShortestPathFinder()
        self.third_window.show()
        self.close()
        
    def shortest_path_open_from_graph(self):
        self.third_window = ShortestPathFinderFromGraph()
        self.third_window.show()
        self.close()
        
    def shortest_path_open_greedy_algorithm(self):
        self.fourth_window = ShortestPathApp()
        self.fourth_window.show()
        self.close()
        
        
    
    # change theme to multiple themes
    
    def change_theme(self):
        # Create dialog box
        dialog = QDialog(self)
        dialog.setWindowTitle("Select a Theme")
        layout = QVBoxLayout(dialog)

        # Create theme selection dropdown
        themes = ["Light", "Dark", "Blue", "Green"]
        theme_combobox = QComboBox(dialog)
        theme_combobox.addItems(themes)
        layout.addWidget(theme_combobox)

        # Add OK and Cancel buttons to dialog box
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        print(buttons)

        # Show dialog box and update theme if OK button is clicked
        if dialog.exec() == QDialog.accepted:
            theme = theme_combobox.currentText()
            if theme == "Light":
                self.setStyleSheet("background: rgb(255,255,255);")
                self.input_label.setStyleSheet("color: rgb(0,0,0);")
                self.output_label.setStyleSheet("color: rgb(0,0,0);")
                self.algo_label.setStyleSheet("color: rgb(0,0,0);")
                self.time_label.setStyleSheet("color: rgb(0,0,0);")
                self.input_textbox.setStyleSheet("background: rgb(255,255,255);")
                self.output_textbox.setStyleSheet("background: rgb(255,255,255);")
                self.algo_combobox.setStyleSheet("background: rgb(255,255,255);")
            elif theme == "Dark":
                self.setStyleSheet("background: rgb(0,0,0);")
                self.input_label.setStyleSheet("color: rgb(255,255,255);")
                self.output_label.setStyleSheet("color: rgb(255,255,255);")
                self.algo_label.setStyleSheet("color: rgb(255,255,255);")
                self.time_label.setStyleSheet("color: rgb(255,255,255);")
                self.input_textbox.setStyleSheet("background: rgb(0,0,0);")
                self.output_textbox.setStyleSheet("background: rgb(0,0,0);")
                self.algo_combobox.setStyleSheet("background: rgb(0,0,0);")
            elif theme == "Blue":
                self.setStyleSheet("background: rgb(0,0,255);")
                self.input_label.setStyleSheet("color: rgb(255,255,255);")
                self.output_label.setStyleSheet("color: rgb(255,255,255);")
                self.algo_label.setStyleSheet("color: rgb(255,255,255);")
                self.time_label.setStyleSheet("color: rgb(255,255,255);")
                self.input_textbox.setStyleSheet("background: rgb(0,0,255);")
                self.output_textbox.setStyleSheet("background: rgb(0,0,255);")
                self.algo_combobox.setStyleSheet("background: rgb(0,0,255);")
            elif theme == "Green":
                self.setStyleSheet("background: rgb(0,255,0);")
                self.input_label.setStyleSheet("color: rgb(0,0,0);")
                self.output_label.setStyleSheet("color: rgb(0,0,0);")
                self.algo_label.setStyleSheet("color: rgb(0,0,0);")
                self.time_label.setStyleSheet("color: rgb(0,0,0);")
                self.input_textbox.setStyleSheet("background: rgb(0,255,0);")
                self.output_textbox.setStyleSheet("background: rgb(0,255,0);")
                self.algo_combobox.setStyleSheet("background: rgb(0,255,0);")
            else:
                self.show_error("Invalid theme")
        else:
            return None
            
    # closing the application
    def exit(self):
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
        # start_time = time.time()
        # output = []
        # for step in algo.function(input_list):
        #     output.append(", ".join(str(x) for x in step))
        # end_time = time.time()
        
        # Run sorting algorithm and update output
        start_time = time.time()
        output = []
        if algo_name == "Quick Sort":
            output.append(", ".join(str(x) for x in input_list))
            algo.function(input_list, 0, len(input_list) - 1)
            output.append(", ".join(str(x) for x in input_list))
           
        elif algo_name == "Counting Sort":
            output.append(", ".join(str(x) for x in input_list))
            input_list = algo.function(input_list)
            output.append(", ".join(str(x) for x in input_list))
        else:
            for step in algo.function(input_list):
                output.append(", ".join(str(x) for x in step))
        end_time = time.time()

        time_taken = end_time - start_time
        time_taken_text = "Time taken: {:.6f} seconds".format(time_taken)
        n = "Length of array: {}".format(len(input_list))
        self.time_label.setText(time_taken_text)
        self.length_of_array_label.setText(n)
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
                