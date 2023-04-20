import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QLabel, QPlainTextEdit

class ShortestPathFinder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Shortest Path Finder")
        self.setGeometry(100, 100, 600, 400)

        # Create widgets
        self.adj_matrix_input = QPlainTextEdit()
        self.adj_matrix_input.setPlaceholderText("Enter adjacency matrix here...")
        self.source_node_input = QTextEdit()
        self.source_node_input.setPlaceholderText("Enter source node here...")
        self.target_node_input = QTextEdit()
        self.target_node_input.setPlaceholderText("Enter target node here...")
        self.result_label = QLabel()
        self.calculate_button = QPushButton("Calculate Shortest Path")
        self.calculate_button.clicked.connect(self.calculate_shortest_path)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Adjacency Matrix (One row per line, separated by '\\n'):"))
        layout.addWidget(self.adj_matrix_input)
        layout.addWidget(QLabel("Source Node:"))
        layout.addWidget(self.source_node_input)
        layout.addWidget(QLabel("Target Node:"))
        layout.addWidget(self.target_node_input)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def calculate_shortest_path(self):
        adj_matrix_text = self.adj_matrix_input.toPlainText()
        source_node_text = self.source_node_input.toPlainText()
        target_node_text = self.target_node_input.toPlainText()

        try:
            # Convert input text to adjacency matrix and source/target node integers
            adj_matrix = []
            lines = adj_matrix_text.split("\n")
            for line in lines:
                row = list(map(int, line.strip().split()))
                adj_matrix.append(row)

            source_node = int(source_node_text.strip())
            target_node = int(target_node_text.strip())

            # Call shortest_path function and display result
            shortest_path = self.shortest_path(adj_matrix, source_node, target_node)
            if shortest_path:
                result = "Shortest Path: " + " -> ".join(map(str, shortest_path))
            else:
                result = "No path found"
            self.result_label.setText(result)

        except ValueError as ve:
            self.result_label.setText("Error: Invalid input. Please enter valid integers for source and target nodes.")
        except Exception as e:
            self.result_label.setText("Error: " + str(e))

    def shortest_path(self, adj_matrix, source, target):
        try:
            num_nodes = len(adj_matrix)
            queue = [source]
            visited = set()
            path = {}

            while queue:
                node = queue.pop(0)
                visited.add(node)

                if node == target:
                    return self.reconstruct_path(source, target, path)

                for neighbor in range(num_nodes):
                    if adj_matrix[node-1][neighbor] > 0 and neighbor + 1 not in visited:
                        path[neighbor + 1] = node
                        queue.append(neighbor + 1)

            return None

        except IndexError as ie:
            raise IndexError("Error: Invalid adjacency matrix. Please check the matrix dimensions and values.")

    def reconstruct_path(self, source, target, path):
        node = target
        shortest_path = [node]
        while node != source:
            node = path[node]
            shortest_path.append(node)
        shortest_path.reverse()

        return shortest_path
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShortestPathFinder()
    window.show()
    sys.exit(app.exec())
