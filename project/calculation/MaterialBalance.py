import sys
from project.ObjectModels import Grid
import numpy as np
import time
import copy


def _material_balance(x, y, a_matrix, b_matrix, scenario=None):
    def _calculate_material_balance_water(step, direction = None, coordinates = None):
        """This function calculate material balance water phase

        :param step: moment of time
        :param direction: if this parameter given, should take one pressure from last step
        :param coordinates: index for neighbour cells
        :return: material balance value
        """
        pressures_copy = copy.deepcopy(neighbours_pressure)

        if cell.well_presence:
            Pwell = cell.well_presence.well_pressure

        if direction:
            x = coordinates[1]
            y = coordinates[0]
            pressures_copy[direction] = CellsBox.matrix[y, x].get_prev_pressure_water(step)

        # написать вычисление потоков как в excel

        return 0
        pass

    cell = CellsBox.matrix[y, x]
    neighbours_pressure = {"itself":  None, "west": None, "north": None, "east": None, "south": None}
    for direction, coordinates in cell.neighbours.items():
        if coordinates:
            neighbours_pressure[direction] = CellsBox.matrix[coordinates[0], coordinates[1]].get_pressure_water(step)
        else:  # если входим в это условие, то значит соседняя ячейка это аквифер
            neighbours_pressure[direction] = Grid.GridsElements.GridsCell.beginningPressure

    for direction, coordinates in cell.neighbours.items():
        for_which = cell.cell_number  # ячейка, для которой считаем мб
        if coordinates and scenario == "water":
            by_which = CellsBox.matrix[coordinates[0], coordinates[1]].cell_number  # ячейка, из которой берем приближение давления
            mb_current_pressure = _calculate_material_balance_water(step)  # пересчет мб с текущими давлениями
            mb_dif_pressure = _calculate_material_balance_water(step, direction, coordinates) # пересчет мб с давлением прошлого шага
            delta_pressure = CellsBox.matrix[coordinates[0], coordinates[1]].delta_pressure_water(step)
            a_matrix[for_which, by_which] = (mb_current_pressure - mb_dif_pressure)/delta_pressure# считаю коэффициент a
        elif coordinates and scenario == "oil":
            by_which = CellsBox.matrix[coordinates[0], coordinates[1]].cell_number  # ячейка, из которой берем приближение давления
            mb_current_pressure = _calculate_material_balance_water(step)  # пересчет мб с текущими давлениями
            mb_dif_pressure = _calculate_material_balance_water(step, direction, coordinates)  # пересчет мб с давлением прошлого шага
            delta_pressure = CellsBox.matrix[coordinates[0], coordinates[1]].delta_pressure_water(step)
            a_matrix[for_which, by_which] = (mb_current_pressure - mb_dif_pressure) / delta_pressure  # считаю коэффициент a


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
                '#_material_balance(x, y, a_matrix_oil, b_matrix_oil, scenario="oil")'
                _material_balance(x, y, a_matrix_water, b_matrix_water, scenario="water")

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



