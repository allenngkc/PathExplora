
class PathfindingAlgorithms:
    def __init__(self, path_data):
        self.path_data = path_data
        self.visited = []
        self.path = []
    
    def update_path_data(self, path_data):
        self.path_data = path_data

    def dfs(self, start, end):
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
            
        print("NO PATH")

    
        
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
