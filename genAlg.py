import math

from graph import *


def sort_by_points(entity):
    return entity.points


class GeneticAlgorithm:
    def __init__(self, table):
        Graph.origin_table = table
        Graph.all_edges = Graph.get_edges()
        Graph.correct_table()
        self.entities = []
        self.bests_scores = [sys.maxsize]
        self.generation_size = 2 * len(Graph.all_edges)

    def __str__(self):
        return str(self.bests_scores)

    def build_first_generation(self):
        for i in range(self.generation_size):
            graph = Graph()
            graph.mutation()
            if graph.points < self.bests_scores[-1]:
                self.bests_scores[-1] = graph.points
            self.entities.append(graph)

    def generate_new_generation(self, pair_selection=1, children_selection=1):
        entities = []
        if pair_selection == 1:
            entities = self.panmixia()
        elif pair_selection == 2:
            entities = self.outbreeding()
        elif pair_selection == 3:
            entities = self.outbreeding()
        entities += self.entities
        if children_selection == 1:
            self.entities = self.truncation(entities)
        elif children_selection == 2:
            new_age = self.elite_selection(entities)
            if pair_selection == 1:
                entities = self.panmixia()
            elif pair_selection == 2:
                entities = self.outbreeding()
            for entity in entities:
                if len(new_age) == self.generation_size:
                    break
                new_age.append(entity)
            self.entities = new_age
        self.entities.sort(key=sort_by_points)
        self.bests_scores.append(self.entities[0].points)

    def panmixia(self):  # каждой особе случайный номер другой особи
        arr = []
        for entity in self.entities:
            arr += entity.crossing(self.entities[random.randint(0, self.generation_size - 1)], 1)
        return arr

    def outbreeding(self):  # каждой особе другая особь с наибольшим расстоянием Хемминга
        arr = []
        for entity in self.entities:
            best_second_half = self.entities[0]
            biggest_distance = entity.hemming_distance(self.entities[0])
            for i in self.entities:
                distance = entity.hemming_distance(i)
                if distance > biggest_distance:
                    biggest_distance = distance
                    best_second_half = i
            arr += entity.crossing(best_second_half, 1)
        return arr

    def inbreeding(self):  # каждой особе другая особь с наименьшим расстоянием Хемминга
        arr = []
        for entity in self.entities:
            best_second_half = self.entities[0]
            biggest_distance = entity.hemming_distance(self.entities[0])
            for i in self.entities:
                distance = entity.hemming_distance(i)
                if distance < biggest_distance:
                    biggest_distance = distance
                    best_second_half = i
            arr += entity.crossing(best_second_half, 1)
        return arr

    def truncation(self, entities):  # отбор усечением
        entities.sort(key=sort_by_points)
        return entities[0:self.generation_size]

    def elite_selection(self, entities):  # отбираются 20% лучших, остальные создаются занаво
        entities.sort(key=sort_by_points)
        return entities[0:math.ceil(self.generation_size * 0.2)]
