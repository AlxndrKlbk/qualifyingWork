
from project.ObjectModels import Grid
import numpy as np
import time

def _material_balance(x, y, a_matrix, b_batrix):
    cell = CellsBox.matrix[y, x]
    print(type(cell.neighbours))
    for direction, coords in cell.neighbours.items():
        for_which = cell.cell_number
        if coords:
            by_which = CellsBox.matrix[coords[0], coords[1]].cell_number
            a_matrix[for_which, by_which] = 1  # считаю коэффициент СЮДА НАДО СДЕЛАТЬ ВЫЗОВ ПЕРЕСЧЕТА МАТБАЛАНСОВ
        else:
            pass

    print(a_matrix)
    pass

Nx = 10
Ny = 10
DesignVariant = [(0, 0, "inject"), (Ny-1, Nx-1, "extract")]


timeBefore = time.time()

CellsBox = Grid.Grid(Nx, Ny, DesignVariant)

timeAfter = time.time()

calculation_steps = int(input("введите число расчетных месяцев:"))  # расчетный шаг в месяцах

for step in range(calculation_steps):
    a_matrix_oil = np.zeros((Ny*Nx, Nx*Ny))  # a_matrix{y,x] где у - номер ячейки, для которой считаем производную, x - по которой
    b_matrix_oil = np.zeros((Ny*Nx))  # один b для каждой ячейки
    a_matrix_water = np.zeros((Ny*Nx, Nx*Ny))
    b_matrix_water = np.zeros((Ny*Nx))
    while True:

        for y in range(Ny):
            for x in range(Nx):
                _material_balance(x, y, a_matrix_oil, b_matrix_oil)
                "#_material_balance(x, y, a_matrix_water, b_matrix_water)"

        pressure_accuracy = False
        if not pressure_accuracy:
            break

    pass

"#поля для перетоков у объекта скважина сделать в виде словарей {направление: [массив значений по месяцам]}"
print(type(calculation_steps))
print(f'тип хранилища ячеек {type(CellsBox)}')
print(f'время на инициализацию сетки: {timeAfter-timeBefore} секунд')



