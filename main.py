from genAlg import GeneticAlgorithm

# try:
a = GeneticAlgorithm([[0, 5, 2, 0, 7],
                      [5, 0, 1, 0, 11],
                      [2, 1, 0, 6, 8],
                      [0, 0, 6, 0, 1],
                      [7, 11, 8, 1, 0]])
a.build_first_generation()
for i in range(0, 100):
    a.generate_new_generation(3, 1)
print(a)
print(a.entities[0])
# except Exception as e:
#     print(str(e))
