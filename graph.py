class Node:
    def __init__(self, id, line_pos):
        self.id = id # 资源名称
        self.line_pos = line_pos # 资源所在行数
    
    def print(self):
        print(self.id, self.line_pos)


class Graph:
    def __init__(self):
        self.vertices = {}
    
    def add_vertex(self, node):
        self.vertices[node.id] = node


    def add_edge(self, vertex1, vertex2):
        if vertex1 in self.vertices and vertex2 in self.vertices:
            self.vertices[vertex1].add(vertex2)
            self.vertices[vertex2].add(vertex1)
            
    def get_neighbors(self, vertex):
        return self.vertices[vertex]
    
    def print(self):
        for key in self.vertices:
            self.vertices[key].print()

    def print_vertices(self):
        for key in self.vertices:
            print(key)