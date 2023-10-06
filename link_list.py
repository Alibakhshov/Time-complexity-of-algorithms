from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
# from main import Sorter

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def delete_at_beginning(self):
        if self.head is None:
            return
        self.head = self.head.next

    def delete_at_end(self):
        if self.head is None:
            return
        if self.head.next is None:
            self.head = None
            return
        second_last = self.head
        while second_last.next.next:
            second_last = second_last.next
        second_last.next = None

    def delete_at_position(self, position):
        if self.head is None:
            return
        if position == 0:
            self.head = self.head.next
            return
        current_node = self.head
        for i in range(position-1):
            current_node = current_node.next
            if current_node is None:
                return
        if current_node.next is None:
            return
        current_node.next = current_node.next.next

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Linked List Deletion Operations'
        self.left = 100
        self.top = 100
        self.width = 500
        self.height = 200
        self.initUI()
        
    

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.list_label = QLabel(self)
        self.list_label.setText('Enter comma-separated list:')
        self.list_label.move(20, 20)

        self.list_input = QLineEdit(self)
        self.list_input.move(220, 20)
        self.list_input.resize(150, 25)

        self.pos_label = QLabel(self)
        self.pos_label.setText('Enter position to delete (optional):')
        self.pos_label.move(20, 60)

        self.pos_input = QLineEdit(self)
        self.pos_input.move(270, 60)
        self.pos_input.resize(150, 25)

        self.beginning_button = QPushButton('Delete at Beginning', self)
        self.beginning_button.move(20, 100)
        self.beginning_button.clicked.connect(self.delete_at_beginning)

        self.end_button = QPushButton('Delete at End', self)
        self.end_button.move(170, 100)
        self.end_button.clicked.connect(self.delete_at_end)

        self.position_button = QPushButton('Delete at Position', self)
        self.position_button.move(280, 100)
        self.position_button.clicked.connect(self.delete_at_position)
        
        self.back_button = QPushButton('Back', self)
        self.back_button.move(380, 150)
        self.back_button.clicked.connect(self.back)

        self.result_label = QLabel(self)
        self.result_label.move(20, 140)
        self.result_label.resize(330, 80)

        self.show()
        
    # back function
    def back(self):
        self.third_window = Sorter()
        self.third_window.show()
        self.close()

    def delete_at_beginning(self):
        linked_list = LinkedList()
        try:
            values = [int(x) for x in self.list_input.text().split(',')]
            for value in values:
                linked_list.insert_at_end(value)
            linked_list.delete_at_beginning()
            self.result_label.setText('List after deletion: ' + self.get_list(linked_list))
        except:
            self.result_label.setText('Invalid input')

    def delete_at_end(self):
        linked_list = LinkedList()
        try:
            values = [int(x) for x in self.list_input.text().split(',')]
            for value in values:
                linked_list.insert_at_end(value)
            linked_list.delete_at_end()
            self.result_label.setText('List after deletion: ' + self.get_list(linked_list))
        except:
            self.result_label.setText('Invalid input')

    def delete_at_position(self):
        linked_list = LinkedList()
        try:
            values = [int(x) for x in self.list_input.text().split(',')]
            for value in values:
                linked_list.insert_at_end(value)
            position = int(self.pos_input.text())
            linked_list.delete_at_position(position)
            self.result_label.setText('List after deletion: ' + self.get_list(linked_list))
        except:
            self.result_label.setText('Invalid input')
            
    def get_list(self, linked_list):
        current_node = linked_list.head
        result = ''
        while current_node is not None:
            result += str(current_node.data) + ', '
            current_node = current_node.next
        return result[:-2]

if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    app.exec()
    
