import math
import random
import copy
import matplotlib.pyplot as plt
from genAlg import GeneticAlgorithm
from tkinter.filedialog import *


def new_empty_table(count_vert):
    table = []
    for q in range(0, count_vert):
        table.append([])
        for e in range(0, count_vert):
            table[q].append(0)
    return table


def generate_task(size=15):
    task = new_empty_table(size)
    for i in range(0, size):
        for j in range(i, size):
            task[i][j] = random.randint(1, 100)
            task[j][i] = task[i][j]
    return task


def all_types_solutions(task, file):
    try:
        answers = []
        for i in range(1, 4):
            answers.append([])
            for j in range(1, 4):
                task_clone = copy.deepcopy(task)
                answers[-1].append(one_solve(task_clone, file, i, j))
                plt.plot(answers[-1][-1])
            '''
            синий - Отбор усечением
            оранжевый - Элитарный отбор
            зленый - Отбор вытеснением
            '''
            plt.savefig('answer_chart_parents_choice' + str(i) + '.png')
            plt.close()
        for i in range(0, 3):
            for an in answers:
                plt.plot(an[i])
            '''
            синий - Панмиксия
            оранжевый - Аутбридинг
            зленый - Инбридинг
            '''
            plt.savefig('answer_chart_children_choice' + str(i + 1) + '.png')
            plt.close()
    except Exception as e:
        print(str(e))


def one_solve(task, file, i, j):
    task.build_first_generation()
    re = 0
    cycle = 1
    min_answer = task.min_score
    while re < math.ceil(task.generation_size / 2):
        task.generate_new_generation(1, 3)
        if min_answer > task.min_score:
            re = 0
            min_answer = task.min_score
        else:
            re += 1
        cycle += 1
        print("cycle:" + str(cycle) + "; i: " + str(re) + "; min score: " + str(
            task.min_score) + "; solution method: (" + str(
            i) + ";" + str(j) + ")")
    file.write(
        "cycle:" + str(cycle) + "; i: " + str(re) + "; min score: " + str(
            task.min_score) + "; solution method: (" + str(
            i) + ";" + str(j) + ")" + "\n")
    file.write(str(task.bests_scores) + "\n")
    print()
    return task.bests_scores


def read_file(filename):
    file = open(filename, "r")
    table = []
    while True:
        line = file.readline()
        if not line:
            break
        table.append([])
        line_tmp = line.split(", ")
        for i in range(0, len(line_tmp) - 1):
            table[-1].append(int(line_tmp[i]))
    file.close()
    return table


def write_task(file, table):
    for string in table:
        for item in string:
            file.write(str(item) + ", ")
        file.write("\n")


def main():
    file = open('answer.txt', 'w')
    try:
        val1 = input(
            "1. Ввести размер для слуйчайного полного графа.\n2. Выбрать файл с задачей.\n3. Завершить работу.\n")
        if int(val1) == 1:
            table = generate_task(int(input("Размер: ")))
        elif int(val1) == 2:
            table = read_file(askopenfilename())
        else:
            return
        write_task(file, table)
        task = GeneticAlgorithm(table)

        val2 = input(
            "1. Посчитать всеми вариантами.\n2. Выбрать выбор родителей и отсеивание.\n3. Завершить работу.\n")
        if int(val2) == 1:
            all_types_solutions(task, file)
        elif int(val2) == 2:
            p = int(input("1. Панмексия.\n2. Аутбридинг.\n3. Инбридинг.\n"))
            c = int(input("1. Отбор усечением.\n2. Элитарный отбор.\n3. Отбор вытеснением.\n"))
            if not p in [1, 2, 3] and not c in [1, 2, 3]:
                print("Некорректный ввод.")
                return
            plt.plot(one_solve(task, file, p, c))
            plt.savefig('single_answer_chart.png')
            plt.close()
        else:
            return
    except ValueError:
        return
    except Exception as ex:
        print(ex)
    finally:
        file.close()


main()
