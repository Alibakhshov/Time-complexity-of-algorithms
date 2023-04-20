from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton
from collections import defaultdict
import sys

class ShortestPathFinder(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the GUI
        self.setWindowTitle("Shortest Path Finder")
        self.layout = QVBoxLayout()

        self.label = QLabel("Enter graph data (e.g., 'A-B:5, B-C:3, C-D:7'): ")
        self.input_lineedit = QLineEdit()
        self.input_lineedit.setPlaceholderText("Enter graph data here")
        self.result_textedit = QTextEdit()
        self.result_textedit.setReadOnly(True)
        self.button = QPushButton("Find Shortest Path")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input_lineedit)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.result_textedit)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.find_shortest_path)

    def find_shortest_path(self):
        # Get graph data from input_lineedit
        graph_data = self.input_lineedit.text()

        # Parse graph data into a dictionary
        graph = defaultdict(dict)
        for edge in graph_data.split(','):
            nodes, weight = edge.split(':')
            node1, node2 = nodes.split('-')
            graph[node1][node2] = int(weight)
            graph[node2][node1] = int(weight)

        # Find shortest path and distance using Dijkstra's algorithm
        start = min(graph.keys())
        distances = {node: float('inf') for node in graph}
        distances[start] = 0
        visited = set()

        while len(visited) < len(graph):
            current_node = min((node for node in graph if node not in visited), key=distances.get)
            visited.add(current_node)

            for neighbor, weight in graph[current_node].items():
                distance = distances[current_node] + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance

        # Format results
        shortest_path = []
        for node in sorted(graph.keys()):
            if node == start:
                shortest_path.append(f"{node} (start)")
            else:
                shortest_path.append(node)

        result = f"Shortest Path: {' -> '.join(shortest_path)}\n"
        result += f"Shortest Distance: {distances}\n"

        # Display results in result_textedit
        self.result_textedit.setPlainText(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ShortestPathFinder()
    window.show()
    sys.exit(app.exec())
