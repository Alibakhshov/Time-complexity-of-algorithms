import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QLineEdit


class ShortestPathApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Shortest Path Greedy Algorithm')
        self.setGeometry(100, 100, 400, 300)

        self.graph_label = QLabel('Enter graph information (e.g., "a to b, 5"):')
        self.graph_text = QTextEdit()
        self.nodes_label = QLabel('Enter nodes for the shortest path (e.g., "a to e"):')
        self.nodes_input = QLineEdit()
        self.result_label = QLabel('Shortest Path:')
        self.path_text = QTextEdit()

        self.calculate_button = QPushButton('Calculate Shortest Path')
        self.calculate_button.clicked.connect(self.calculate_shortest_path)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.graph_label)
        self.layout.addWidget(self.graph_text)
        self.layout.addWidget(self.nodes_label)
        self.layout.addWidget(self.nodes_input)
        self.layout.addWidget(self.calculate_button)
        self.layout.addWidget(self.result_label)
        self.layout.addWidget(self.path_text)

        self.setLayout(self.layout)

    def calculate_shortest_path(self):
        try:
            graph_input = self.graph_text.toPlainText().strip()
            if not graph_input:
                raise ValueError("Graph information is missing")

            nodes = {}
            lines = graph_input.split('\n')
            for line in lines:
                parts = line.split(',')
                if len(parts) != 2:
                    raise ValueError("Invalid graph input format")
                node_names, value = parts[0].strip(), int(parts[1].strip())
                node_from, node_to = node_names.split(' to ')
                if node_from not in nodes:
                    nodes[node_from] = {}
                nodes[node_from][node_to] = value

            nodes_input = self.nodes_input.text().strip()
            if not nodes_input:
                raise ValueError("Nodes for the shortest path are missing")

            start_node, end_node = nodes_input.split(' to ')

            # Greedy Algorithm to find the shortest path
            current_node = start_node
            path = [current_node]
            total_value = 0

            while current_node != end_node:
                neighbors = nodes[current_node]
                next_node = min(neighbors, key=neighbors.get)
                total_value += neighbors[next_node]
                current_node = next_node
                path.append(current_node)

            self.path_text.setPlainText(" -> ".join(path))
            self.result_label.setText(f'Shortest Path Value: {total_value}')
        except Exception as e:
            self.path_text.setPlainText('')
            self.result_label.setText(f'Error: {str(e)}')


def main():
    app = QApplication(sys.argv)
    ex = ShortestPathApp()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
