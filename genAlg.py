from graph import *


class GeneticAlgorithm:
    def __init__(self, table):
        Graph.origin_table = table
        Graph.all_edges = Graph.get_edges()
        Graph.correct_table()
        self.bests_scores = []
        self.generation_size = 2*len(Graph.get_shuffled_edges())

    def __str__(self):
        return str(self.origin)

    def build_first_generation(self):
        a = Graph()
        print(a)
        print(a.points)
