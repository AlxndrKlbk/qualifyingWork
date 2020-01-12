import sys
from project.ObjectModels import Grid
import numpy as np
import time


def _material_balance(x, y, a_matrix, b_matrix):
    cell = CellsBox.matrix[y, x]
    for direction, coordinates in cell.neighbours.items():
        for_which = cell.cell_number
        if coordinates:
            by_which = CellsBox.matrix[coordinates[0], coordinates[1]].cell_number
            a_matrix[for_which, by_which] = 1  # считаю коэффициент СЮДА НАДО СДЕЛАТЬ ВЫЗОВ ПЕРЕСЧЕТА МАТБАЛАНСОВ


Nx = 100
Ny = 100
DesignVariant = [(0, 0, "inject"), (Ny-1, Nx-1, "extract")]


timeBefore = time.time()

CellsBox = Grid.Grid(Nx, Ny, DesignVariant)

timeAfter = time.time()


calculation_steps = int(input("введите число расчетных месяцев:"))  # расчетный шаг в месяцах

a_matrix_oil = np.zeros((Ny * Nx, Nx * Ny), dtype="float16")  # a_matrix{y,x] где у - номер ячейки, для которой считаем производную, x - по которой
b_matrix_oil = np.zeros((Ny * Nx), dtype="float16")  # один b для каждой ячейки
a_matrix_water = np.zeros((Ny * Nx, Nx * Ny), dtype="float16")
b_matrix_water = np.zeros((Ny * Nx), dtype="float16")
for step in range(calculation_steps):
    while True:
        for y in range(Ny):
            for x in range(Nx):
                _material_balance(x, y, a_matrix_oil, b_matrix_oil)
                "#_material_balance(x, y, a_matrix_water, b_matrix_water)"

        # for i in range(Nx*Ny):
        #     for j in range(Nx*Ny):
        #         print(a_matrix_oil[i, j], end=" ")
        #     print("\n")

        pressure_accuracy = False
        if not pressure_accuracy:
            break

    pass

"#поля для перетоков у объекта скважина сделать в виде словарей {направление: [массив значений по месяцам]}"
print(f'тип хранилища ячеек {type(CellsBox)}')
print(f'время на инициализацию сетки: {timeAfter-timeBefore} секунд')



