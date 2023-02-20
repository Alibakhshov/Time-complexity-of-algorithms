import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit
from PyQt6.QtCore import Qt

def radix_sort(arr):
    RADIX = 10
    maxLength = False
    tmp, placement = -1, 1

    while not maxLength:
        maxLength = True
        buckets = [list() for _ in range(RADIX)]

        for i in arr:
            tmp = i // placement
            buckets[tmp % RADIX].append(i)
            if maxLength and tmp > 0:
                maxLength = False

        a = 0
        for b in range(RADIX):
            buck = buckets[b]
            for i in buck:
                arr[a] = i
                a += 1

        placement *= RADIX

    return arr

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("Radix Sort Algorithm")

        # Create labels
        self.label1 = QLabel("Enter the numbers separated by commas:", self)
        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label2 = QLabel("Sorted Array:", self)
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create line edit
        self.line_edit = QLineEdit(self)

        # Create text edit
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        # Create sort button
        self.sort_button = QPushButton("Sort", self)
        self.sort_button.clicked.connect(self.sort)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.sort_button)
        layout.addWidget(self.label2)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

        self.show()

    def sort(self):
        # Get input and convert to array
        input_text = self.line_edit.text()
        arr = [int(x) for x in input_text.split(",")]

        # Sort the array
        sorted_arr = radix_sort(arr)

        # Display the sorted array
        self.text_edit.setText(", ".join([str(x) for x in sorted_arr]))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
