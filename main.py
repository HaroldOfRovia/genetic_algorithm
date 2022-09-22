from graph import Graph
from genAlg import GeneticAlgorithm

# try:
a = GeneticAlgorithm([[0, 5, 2, 0, 7],
                      [5, 0, 1, 0, 11],
                      [2, 1, 0, 6, 8],
                      [0, 0, 6, 0, 1],
                      [7, 11, 8, 1, 0]])
a.build_first_generation()
# except Exception as e:
#     print(str(e))
