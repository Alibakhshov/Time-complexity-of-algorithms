import sys
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QGridLayout, 
                             QLabel, QLineEdit, QTextEdit, QFileDialog, 
                             QMessageBox, QComboBox)

class SortThread(QThread):
    sorted_list = pyqtSignal(list)

    def __init__(self, num_list, sort_func):
        super().__init__()
        self.num_list = num_list
        self.sort_func = sort_func

    def run(self):
        sorted_nums = self.sort_func(self.num_list)
        self.sorted_list.emit(sorted_nums)

class SortApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(200, 200, 400, 400)
        self.setWindowTitle("Sort App")

        # Widgets
        self.num_label = QLabel("Enter numbers separated by space:")
        self.num_edit = QLineEdit()
        self.sort_label = QLabel("Select a sorting algorithm:")
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Bubble Sort", "Selection Sort", "Insertion Sort",
                                  "Merge Sort", "Quick Sort", "Radix Sort", "Counting Sort"])
        self.sort_btn = QPushButton("Sort")
        self.save_btn = QPushButton("Save")
        self.clear_btn = QPushButton("Clear")
        self.exit_btn = QPushButton("Exit")
        self.open_file_btn = QPushButton("Open File")
        self.output_edit = QTextEdit()
        self.output_edit.setReadOnly(True)

        # Layout
        grid = QGridLayout()
        grid.addWidget(self.num_label, 0, 0)
        grid.addWidget(self.num_edit, 1, 0)
        grid.addWidget(self.sort_label, 2, 0)
        grid.addWidget(self.sort_combo, 3, 0)
        grid.addWidget(self.sort_btn, 4, 0)
        grid.addWidget(self.save_btn, 5, 0)
        grid.addWidget(self.clear_btn, 6, 0)
        grid.addWidget(self.open_file_btn, 7, 0)
        grid.addWidget(self.exit_btn, 8, 0)
        grid.addWidget(self.output_edit, 0, 1, 8, 1)
        self.setLayout(grid)

        # Signals and Slots
        self.sort_btn.clicked.connect(self.sort_nums)
        self.save_btn.clicked.connect(self.save_output)
        self.clear_btn.clicked.connect(self.clear_inputs)
        self.open_file_btn.clicked.connect(self.open_file)
        self.exit_btn.clicked.connect(QApplication.instance().quit)
        
        self.show()

    def sort_nums(self):
        num_list = [int(num) for num in self.num_edit.text().split()]
        sort_func = self.get_sort_func()
        self.sort_thread = SortThread(num_list, sort_func)
        self.sort_thread.sorted_list.connect(self.update_output)
        self.sort_thread.start()

    def get_sort_func(self):
        sort_name = self.sort_combo.currentText()
        if sort_name == "Bubble Sort":
            return self.bubble_sort
        elif sort_name == "Selection Sort":
            return self.selection_sort
        elif sort_name == "Insertion Sort":
            return self.insertion_sort
        elif sort_name == "Merge Sort":
            return self.merge_sort
        elif sort_name == "Quick Sort":
            return self.quick_sort
        elif sort_name == "Radix Sort":
            return self.radix_sort
        elif sort_name == "Counting Sort":
            return self.counting_sort

    def bubble_sort(self, num_list):
        n = len(num_list)
        for i in range(n):
            for j in range(n-i-1):
                if num_list[j] > num_list[j+1]:
                    num_list[j], num_list[j+1] = num_list[j+1], num_list[j]
        return num_list
    
    def selection_sort(self, num_list):
        n = len(num_list)
        for i in range(n-1):
            min_idx = i
            for j in range(i+1, n):
                if num_list[j] < num_list[min_idx]:
                    min_idx = j
            num_list[i], num_list[min_idx] = num_list[min_idx], num_list[i]
        return num_list

    def insertion_sort(self, num_list):
        n = len(num_list)
        for i in range(1, n):
            key = num_list[i]
            j = i-1
            while j >= 0 and key < num_list[j]:
                num_list[j+1] = num_list[j]
                j -= 1
            num_list[j+1] = key
        return num_list

    def merge_sort(self, num_list):
        if len(num_list) > 1:
            mid = len(num_list) // 2
            left_half = num_list[:mid]
            right_half = num_list[mid:]

            self.merge_sort(left_half)
            self.merge_sort(right_half)

            i = j = k = 0

            while i < len(left_half) and j < len(right_half):
                if left_half[i] < right_half[j]:
                    num_list[k] = left_half[i]
                    i += 1
                else:
                    num_list[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                num_list[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                num_list[k] = right_half[j]
                j += 1
                k += 1

        return num_list

    def quick_sort(self, num_list):
        if len(num_list) <= 1:
            return num_list

        pivot = num_list[0]
        left = []
        right = []
        for num in num_list[1:]:
            if num <= pivot:
                left.append(num)
            else:
                right.append(num)

        return self.quick_sort(left) + [pivot] + self.quick_sort(right)

    def radix_sort(self, num_list):
        max_num = max(num_list)
        exp = 1
        while max_num // exp > 0:
            self.counting_sort(num_list, exp)
            exp *= 10
        return num_list

    def counting_sort(self, num_list, exp):
        n = len(num_list)
        output = [0] * n
        count = [0] * 10

        for num in num_list:
            count[(num // exp) % 10] += 1

        for i in range(1, 10):
            count[i] += count[i-1]

        i = n-1
        while i >= 0:
            index = (num_list[i] // exp) % 10
            output[count[index] - 1] = num_list[i]
            count[index] -= 1
            i -= 1

        for i in range(n):
            num_list[i] = output[i]

    def update_output(self, sorted_nums):
        self.output_edit.clear()
        self.output_edit.append("Sorted Numbers:")
        self.output_edit.append(str(sorted_nums))

    def save_output(self):
        if self.output_edit.toPlainText():
            file_name, _ = QFileDialog.getSaveFileName(self, "Save File", ".", "Text Files (*.txt)")
            if file_name:
                try:
                    with open(file_name, "w") as file:
                        file.write(self.output_edit.toPlainText())
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
        else:
            QMessageBox.warning(self, "Warning", "There is no output to save.")
            
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if filename:
            try:
                with open(filename, "r") as file:
                    numbers = file.read().strip().split("\n")
                    input_contents = ','.join(numbers)
                    self.output_edit.setPlainText(input_contents)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file: {str(e)}")
                            
    # def open_file(self):
        
    #     fileName, _ = QFileDialog.getOpenFileName(self, "Select File", "", "Text Files (*.txt)")
    #     if fileName:
    #         try:
    #             with open(fileName, "r") as f:
    #                 file_contents = f.read().split('\n')
    #                 input_contents = ','.join(file_contents)
    #                 self.output_edit.setPlainText(input_contents)
    #         except Exception as e:
    #             QMessageBox.critical(self, "Error", f"Failed to open file: {str(e)}")

    def clear_inputs(self):
        self.num_edit.clear()
        self.output_edit.clear()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SortApp()
    sys.exit(app.exec())
                
        
# if name == "main":
#     app = QApplication(sys.argv)
#     window = SortingApp()
#     window.show()
#     sys.exit(app.exec_())