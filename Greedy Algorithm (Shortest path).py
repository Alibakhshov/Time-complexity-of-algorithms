graph = {     'a': {'b': 79, 'c': 43},     
         'b': {'a': 79, 'd': 29, 'e': 38},     
         'c': {'a': 43, 'f': 39},     
         'd': {'b': 29, 'k': 23},     
         'e': {'b': 38, 'h': 23},     
         'f': {'c': 39, 'g': 4},     
         'g': {'f': 4, 'h': 23},     
         'h': {'e': 23, 'g': 23, 'i': 92},     
         'i': {'h': 92, 'j': 87},     
         'j': {'i': 87, 'k': 26},     
         'k': {'d': 23, 'j': 26, 'l': 30},     
         'l': {'k': 30, 'm': 34},     
         'm': {'l': 34, 'n': 25},     
         'n': {'m': 25, 'o': 84},     
         'o': {'n': 84, 'p': 88},     
         'p': {'o': 88, 'q': 96},     
         'q': {'p': 96, 'r': 83},     
         'r': {'q': 83, 's': 56},     
         's': {'r': 56, 't': 88},     
         't': {'s': 88, 'u': 71},     
         'u': {'t': 71, 'v': 58},     
         'v': {'u': 58, 'w': 59},    
         'w': {'v': 59, 'x': 55},    
         'x': {'w': 55, 'y': 55},   
         'y': {'x': 55, 'z': 68},    
         'z': {'y': 68, 'd': 49} 
}

def greedy_shortest_distance(graph, start, end):
    # Initialize a dictionary to store the distances from the start node to other nodes.
    distances = {node: float('inf') for node in graph}
    distances[start] = 0  # The distance from start node to itself is 0.
    
    # Initialize a dictionary to store the previous node on the shortest path.
    previous = {}
    
    # Create a set of unvisited nodes.
    unvisited = set(graph)
    
    while unvisited:
        # Find the node with the minimum distance from the start node among unvisited nodes.
        current_node = min(unvisited, key=lambda node: distances[node])
        unvisited.remove(current_node)
        
        # If the current node is the end node, we have found the shortest path.
        if current_node == end:
            shortest_path = []
            while current_node in previous:
                shortest_path.insert(0, current_node)
                current_node = previous[current_node]
            shortest_path.insert(0, start)
            return shortest_path, distances[end]
        
        # Explore neighbors of the current node.
        for neighbor, weight in graph[current_node].items():
            potential_distance = distances[current_node] + weight
            if potential_distance < distances[neighbor]:
                distances[neighbor] = potential_distance
                previous[neighbor] = current_node
    
    # If we reach here, there is no path from start to end.
    return None, float('inf')

# Find the shortest path and distance from 'a' to 'e'.
shortest_path, shortest_distance = greedy_shortest_distance(graph, 'a', 'e')
if shortest_path:
    print(f"Shortest Path from 'a' to 'e': {' -> '.join(shortest_path)}")
    print(f"Shortest Distance from 'a' to 'e': {shortest_distance}")
else:
    print("There is no path from 'a' to 'e.")
