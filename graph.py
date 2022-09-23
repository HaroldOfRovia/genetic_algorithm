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


def get_sets(edges, del_edge):
    a_set = [del_edge.a]
    b_set = [del_edge.b]
    i = 0
    while len(a_set) + len(b_set) != len(Graph.origin_table):
        if i == len(edges):
            i = 0
        if edges[i].a in a_set and not edges[i].b in a_set:
            a_set.append(edges[i].b)
        elif edges[i].b in a_set and not edges[i].a in a_set:
            a_set.append(edges[i].a)
        elif edges[i].a in b_set and not edges[i].b in b_set:
            b_set.append(edges[i].b)
        elif edges[i].b in b_set and not edges[i].a in b_set:
            b_set.append(edges[i].a)
        i += 1
    return [a_set, b_set]


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
            self.edges = Graph.get_random_sceleton(Graph.all_edges)
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
        return string + "{:5d}".format(self.points) + "\n"

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
    def get_shuffled_edges(edges):
        edges = copy.deepcopy(edges)
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

    @staticmethod
    def get_random_sceleton(original_edges):
        edges = Graph.get_shuffled_edges(original_edges)
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
        if random.random() >= 0.3:
            return False
        del_edge = self.edges.pop(random.randint(0, len(self.edges) - 1))
        sets = get_sets(self.edges, del_edge)
        random.shuffle(Graph.all_edges)
        for new_edge in Graph.all_edges:
            if (new_edge.a in sets[0] and new_edge.b in sets[1]) or (
                    new_edge.a in sets[1] and new_edge.b in sets[0]):
                if del_edge.__eq__(new_edge):  # чтоб не попалось старое ребро, если других нет, то возьмет потом его
                    continue
                self.edges.append(new_edge)
                break
        if len(self.edges) != len(Graph.origin_table) - 1:
            self.edges.append(del_edge)
        else:
            self.points = self.true_scoring_points()
        return True

    def crossing(self, second_graph, quantity):
        edges = copy.deepcopy(self.edges)
        for edge in second_graph.edges:
            if not edge in edges:
                edges.append(copy.deepcopy(edge))
        arr = []
        for i in range(0, quantity):
            arr.append(Graph(Graph.get_random_sceleton(edges)))
            arr[i].mutation()
        return arr

    def hemming_distance(self, second_graph):  # кол-во различных ребер
        i = 0
        for edge in self.edges:
            if not edge in second_graph.edges:
                i += 1
        return i
