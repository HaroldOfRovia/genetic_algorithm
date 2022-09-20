import random
import sys


def correct_table(table):
    if len(table) == 0:
        raise Exception("\nПустой граф!")
    if len(table) != len(table[0]):
        raise Exception("\nНеобходим неориентированный граф!")
    for i in range(len(table)):
        empty = True
        table[i][i] = 0
        for j in range(len(table[i])):
            if table[i][j] != table[j][i]:
                raise Exception("\nНеобходим неориентированный граф!")
            if table[i][j] != 0:
                empty = False
            if (j == len(table[i]) - 1) and empty:
                raise Exception("\nДля данного графа невозможно составить остов!")
    return table


def get_shuffled_edges(table):
    edges = []
    for i in range(len(table)):
        for j in range(i, len(table[i])):
            if table[i][j] != 0:
                edges.append(Edge(i, j))
    random.shuffle(edges)
    return edges


def new_empty_table(count_vert):
    table = []
    for i in range(0, count_vert):
        table.append([])
        for j in range(0, count_vert):
            table[i].append(0)
    return table


class Edge:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return str(self.a) + '-' + str(self.b)


class Graph:
    def __init__(self, table=None):
        if table is None:
            self.table = []
        else:
            self.table = correct_table(table)
        self.score = sys.maxsize

    def __str__(self):
        string = ""
        for i in range(len(self.table)):
            for j in range(len(self.table[i])):
                string += "{:5d}".format(self.table[i][j])
                if j == len(self.table[i]) - 1:
                    string += "\n"
        return string

    def get_random_sceleton(self):
        edges = get_shuffled_edges(self.table)
        vertexes = [edges[0].a, edges[0].b]
        i = 1
        count_vert = len(self.table)
        table = new_empty_table(count_vert)
        table[edges[0].a][edges[0].b] = self.table[edges[0].a][edges[0].b]
        table[edges[0].b][edges[0].a] = self.table[edges[0].b][edges[0].a]
        while len(vertexes) != count_vert:
            if i > count_vert - 1:
                i = 1
            if (edges[i].a in vertexes and not edges[i].b in vertexes) or \
                    (not edges[i].a in vertexes and edges[i].b in vertexes):
                if edges[i].a in vertexes:
                    vertexes.append(edges[i].b)
                else:
                    vertexes.append(edges[i].a)
                table[edges[i].a][edges[i].b] = self.table[edges[i].a][edges[i].b]
                table[edges[i].b][edges[i].a] = self.table[edges[i].b][edges[i].a]
            i += 1
        sceleton = Graph(table)
        return sceleton
