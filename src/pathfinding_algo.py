from collections import deque
from heapq import heappop, heappush

class PathfindingAlgorithms:
    def __init__(self, path_data):
        self.path_data = path_data
        self.visited = []
        self.path = []
    
    def update_path_data(self, path_data):
        self.path_data = path_data


    # This DFS does not guarantee shortest path since the algorithm does not consider the path length while exploring
    def dfs(self, start, end): # Does not give optimal solution (when searching like this) (This is an intended behavior)
        self.visited.clear()
        self.path.clear()

        stack = [[start, [start]]]
        while stack:
            node, path = stack.pop()

            if node == end:
                self.path = path
                return self.path
            
            if node not in self.visited:
                self.visited.append(node)

                neighbors = self.get_neighbours(node)
                for neighbor in neighbors:
                    if neighbor not in self.visited and self.path_data[neighbor[0]][neighbor[1]] != 1:
                        stack.append([neighbor, path + [neighbor]])
            
        print("NO PATH") # TODO handle if user decided to try mess up the program

    def bfs(self, start, end):
        self.visited.clear()
        self.path.clear()

        queue = deque([(start, [start])])
        visited_nodes = []  # List to store all visited nodes

        while queue:
            node, path = queue.popleft()

            if node not in self.visited:
                self.visited.append(node)
                visited_nodes.append(node)

                if node == end:
                    self.path = path
                    return visited_nodes  # Return all visited nodes

                neighbors = self.get_neighbours(node)
                for neighbor in neighbors:
                    if neighbor not in self.visited and self.path_data[neighbor[0]][neighbor[1]] != 1:
                        queue.append((neighbor, path + [neighbor]))

        print("NO PATH")

    def dijkstra(self, start, end):
        self.visited.clear()
        self.path.clear()

        start = tuple(start)
        end = tuple(end)
        distances = {start: 0}
        previous = {}
        queue = [(0, start)]

        while queue:
            current_distance, current_node = heappop(queue)

            if current_node not in self.visited:
                self.visited.append(current_node)

                if current_node == end:
                    # Reconstruct the path from end to start
                    node = end
                    while node in previous:
                        self.path.append(list(node))
                        node = previous[node]
                    self.path.append(list(start))
                    self.path.reverse()
                    return self.path

                neighbors = self.get_neighbours(list(current_node))
                for neighbor in neighbors:
                    neighbor = tuple(neighbor)
                    if neighbor not in self.visited and self.path_data[neighbor[0]][neighbor[1]] != 1:
                        distance = current_distance + 1  # Assuming unit weight
                        if neighbor not in distances or distance < distances[neighbor]:
                            distances[neighbor] = distance
                            previous[neighbor] = current_node
                            heappush(queue, (distance, neighbor))

        print("NO PATH")
        

    # For second layering, finding the shortest path with BFS iteratively 
    def shortest_path(self, start, end):
        visited = []
        queue = deque([(start, [])])

        while queue:
            node, path = queue.popleft()
            path.append(node)

            if node == end:
                return path
            
            if node not in visited:
                visited.append(node)

                nei = []
                directions = [[0,1], [0,-1], [1,0], [-1,0]]
                for dir in directions:
                    temp_row = node[0] + dir[0]
                    temp_col = node[1] + dir[1]

                    if 0 <= temp_row < len(self.path_data) and 0 <= temp_col < len(self.path_data[0]):
                        if self.path_data[temp_row][temp_col] == 4:
                            nei.append([temp_row, temp_col])

                for neighbor in nei:
                    queue.append((neighbor, list(path)))  # Create a copy of the current path

        print("Cant find any")
        return None

    # Returns the neighbours of node given within self.path_data, global function
    def get_neighbours(self, node):
        neighbours = []
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]

        for direction in directions:
            temp_row = node[0] + direction[0]
            temp_col = node[1] + direction[1]

            if 0 <= temp_row < len(self.path_data) and 0 <= temp_col < len(self.path_data[0]):
                if self.path_data[temp_row][temp_col] != 1:
                    neighbours.append([temp_row, temp_col])
        
        return neighbours
