from graph import Graph


class GeneticAlgorithm:
    def __init__(self, table):
        self.origin = Graph(table)
        self.bests_scores = []

    def __str__(self):
        return str(self.origin)
