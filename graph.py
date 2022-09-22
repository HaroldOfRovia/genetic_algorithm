import random
import copy
import sys


def new_empty_table(count_vert):
    table = []
    for i in range(0, count_vert):
        table.append([])
        for j in range(0, count_vert):
            table[i].append(0)
    return table


def get_sets(edge):
    pass


class Edge:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return str(self.a) + '-' + str(self.b)

    def __contains__(self, item):
        return self.a == item or self.b == item

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b


class Graph:
    origin_table = []
    all_edges = []

    def __init__(self, edges=None):
        if edges is None:
            self.edges = self.get_random_sceleton()
        else:
            self.edges = edges
        self.points = self.true_scoring_points()

    def __str__(self):
        string = ""
        table = self.get_table()
        for i in range(len(table)):
            for j in range(len(table[i])):
                string += "{:5d}".format(table[i][j])
                if j == len(table[i]) - 1:
                    string += "\n"
        return string

    @staticmethod
    def correct_table():
        if len(Graph.origin_table) == 0:
            raise Exception("\nПустой граф!")
        if len(Graph.origin_table) != len(Graph.origin_table[0]):
            raise Exception("\nНеобходим неориентированный граф!")
        for i in range(len(Graph.origin_table)):
            empty = True
            Graph.origin_table[i][i] = 0
            for j in range(len(Graph.origin_table[i])):
                if Graph.origin_table[i][j] != Graph.origin_table[j][i]:
                    raise Exception("\nНеобходим неориентированный граф!")
                if Graph.origin_table[i][j] != 0:
                    empty = False
                if (j == len(Graph.origin_table[i]) - 1) and empty:
                    raise Exception("\nДля данного графа невозможно составить остов!")

    @staticmethod
    def get_shuffled_edges():
        edges = copy.deepcopy(Graph.all_edges)
        random.shuffle(edges)
        return edges

    @staticmethod
    def get_edges():
        edges = []
        for i in range(len(Graph.origin_table)):
            for j in range(i, len(Graph.origin_table[i])):
                if Graph.origin_table[i][j] != 0:
                    edges.append(Edge(i, j))
        return edges

    def get_table(self):
        table = new_empty_table(len(Graph.origin_table))
        for edge in self.edges:
            table[edge.a][edge.b] = Graph.origin_table[edge.a][edge.b]
            table[edge.b][edge.a] = Graph.origin_table[edge.b][edge.a]
        return table

    def get_random_sceleton(self):
        edges = self.get_shuffled_edges()
        included_edges = [edges[0]]
        vertexes = [edges[0].a, edges[0].b]
        i = 1
        j = 0
        while len(included_edges) != len(Graph.origin_table) - 1:
            if i > len(edges) - 1:
                i = 1
            if (edges[i].a in vertexes and not edges[i].b in vertexes) or \
                    (not edges[i].a in vertexes and edges[i].b in vertexes):
                included_edges.append(edges[i])
                if edges[i].a in vertexes:
                    vertexes.append(edges[i].b)
                else:
                    vertexes.append(edges[i].a)
            i += 1
            j += 1
        return included_edges

    def arrange_edges(self):
        edges = []
        for edge in self.edges:
            if len(edges) == 0:
                edges.append(edge)
            else:
                for i in range(len(self.edges)):
                    if edges[i].a < edge.a:
                        continue
                    else:
                        edges.insert(i, edge)
                        break
        self.edges = edges

    def scoring_points_one_vertex(self, ignore, index=0, visited=None):
        all_vis_points = 0
        if len(ignore) == len(Graph.origin_table) - 1:
            return 0
        if visited is None:
            visited = []
        available_path = []
        score = 0
        for edge in self.edges:
            if edge.__contains__(index) and not edge in visited:
                available_path.append(edge)
        if len(available_path) == 0:
            if index in ignore:
                return [-1, 1]
            else:
                return [0, 1]
        for path in available_path:
            vis_points = 0
            visited.append(path)
            arr = self.scoring_points_one_vertex(ignore, path.a if index == path.b else path.b, visited)
            if arr[0] == -1:
                visited.pop(-1)
                continue
            score += arr[0]
            vis_points += arr[1]
            if len(visited) != 0:
                score += Graph.origin_table[visited[-1].a][visited[-1].b] * vis_points
                visited.pop(-1)
            all_vis_points += vis_points
        if not index in ignore:
            all_vis_points += 1
        return [score, all_vis_points]

    def true_scoring_points(self):
        ignore = []
        points = 0
        for i in range(len(Graph.origin_table) - 1):
            points += self.scoring_points_one_vertex(ignore, i)[0]
            ignore.append(i)
        return points

    def mutation(self):
        edge = self.edges.pop(random.randint(0, len(self.edges)))
        get_sets(edge)
