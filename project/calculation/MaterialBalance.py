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

        if direction:
            x = coordinates[1]
            y = coordinates[0]
            pressures_copy[direction] = CellsBox.matrix[y, x].get_prev_pressure_water(step)

        "# если в ячейке есть скважина, проверяю ее назначение и пересчитываю накопленные параметры"
        injection = 0
        production = 0
        if cell.well_presence:
            well = cell.well_presence
            pressure_well = cell.well_presence.well_pressure
            if pressure_well < pressures_copy["itself"]:
                injection = well.get_accumulated_injection(step)
                production = well.water_production(cell, step)
            elif pressure_well >= pressures_copy["itself"]:
                injection = well.water_injection(cell, step)
                production = well.get_accumulated_water_production(step)

        "# записываю давление в текущей ячейке в переменную, чтобы дальше удобно считать поток по соседям"
        cell_pressure = pressures_copy.pop("itself")  # cell_pressure давление в ячейке, для которой считается Матбаланс
        summary_flow = 0
        for flow_to, pressure in pressures_copy.items():
            summary_flow += cell.calculate_flow_water(flow_to, pressure, cell_pressure, CellsBox, step)
        ini_water = Grid.GridsElements.GridsCell.beginningWater
        ce = Grid.GridsElements.GridsCell.ce

        MatBal = Grid.GridsElements.GridsCell.beginningPressure - cell_pressure - ((production + injection + summary_flow)/
                                                                                   (ini_water * ce))
        return MatBal

    def _calculate_material_balance_oil(step, direction = None, coordinates = None):
        """This function calculate material balance oil phase

        :param step: moment of time
        :param direction: if this parameter given, should take one pressure from last step
        :param coordinates: index for neighbour cells
        :return: material balance value
        """
        pressures_copy = copy.deepcopy(neighbours_pressure)

        if direction:
            x = coordinates[1]
            y = coordinates[0]
            pressures_copy[direction] = CellsBox.matrix[y, x].get_prev_pressure_oil(step)

        "# если в ячейке есть скважина, проверяю ее назначение и пересчитываю накопленные параметры"
        injection = 0
        production = 0
        if cell.well_presence:
            well = cell.well_presence
            pressure_well = cell.well_presence.well_pressure
            if pressure_well < pressures_copy["itself"]:
                production = well.oil_production(cell, step)
            elif pressure_well >= pressures_copy["itself"]:
                production = well.get_accumulated_oil_production(step)

        "# записываю давление в текущей ячейке в переменную, чтобы дальше удобно считать поток по соседям"
        cell_pressure = pressures_copy.pop("itself")  # cell_pressure давление в ячейке, для которой считается Матбаланс
        summary_flow = 0
        for flow, pressure in pressures_copy.items():
            summary_flow += cell.calculate_flow_oil(flow, pressure, cell_pressure, CellsBox, step)
        ini_oil = Grid.GridsElements.GridsCell.beginningOil
        ce = Grid.GridsElements.GridsCell.ce

        MatBal = Grid.GridsElements.GridsCell.beginningPressure - cell_pressure - ((production + injection + summary_flow)/
                                                                                   (ini_oil * ce))
        return MatBal

    cell = CellsBox.matrix[y, x]
    neighbours_pressure = {"itself":  None, "west": None, "north": None, "east": None, "south": None}
    "# давления из ячеек соседнего окружения, если соседняя ячейка за контуром, то беру начальное пластовое"
    for direction, coordinates in cell.neighbours.items():
        if coordinates and scenario == "water":
            neighbours_pressure[direction] = CellsBox.matrix[coordinates[0], coordinates[1]].get_pressure_water(step)
        elif coordinates and scenario == "oil":
            neighbours_pressure[direction] = CellsBox.matrix[coordinates[0], coordinates[1]].get_pressure_oil(step)
        else:  # если входим в это условие, то значит соседняя ячейка это аквифер
            neighbours_pressure[direction] = Grid.GridsElements.GridsCell.beginningPressure

    "# заполнение матриц а, матрица в вписывается значение мб с текущими давлениями, чтобы после снова не считать "
    for direction, coordinates in cell.neighbours.items():
        for_which = cell.cell_number  # ячейка, для которой считаем мб
        if coordinates and scenario == "water":
            by_which = CellsBox.matrix[coordinates[0], coordinates[1]].cell_number  # ячейка, из которой берем приближение давления
            mb_current_pressure = _calculate_material_balance_water(step)  # пересчет мб с текущими давлениями
            b_matrix_water[for_which] = -mb_current_pressure
            mb_dif_pressure = _calculate_material_balance_water(step, direction, coordinates) # пересчет мб с давлением прошлого шага
            delta_pressure = CellsBox.matrix[coordinates[0], coordinates[1]].delta_pressure_water(step)
            a_matrix[for_which, by_which] = (mb_current_pressure - mb_dif_pressure)/delta_pressure# считаю коэффициент a
        elif coordinates and scenario == "oil":
            by_which = CellsBox.matrix[coordinates[0], coordinates[1]].cell_number  # ячейка, из которой берем приближение давления
            mb_current_pressure = _calculate_material_balance_oil(step)  # пересчет мб с текущими давлениями
            b_matrix_oil[for_which] = -mb_current_pressure
            mb_dif_pressure = _calculate_material_balance_oil(step, direction, coordinates)  # пересчет мб с давлением прошлого шага
            delta_pressure = CellsBox.matrix[coordinates[0], coordinates[1]].delta_pressure_oil(step)
            if delta_pressure == 0:
                print(f'ячейка для которой {cell.cell_number}')
                print(f'ячейка по которой {CellsBox.matrix[coordinates[0], coordinates[1]].cell_number}')
                delta_pressure = CellsBox.matrix[coordinates[0], coordinates[1]].delta_pressure_oil(step)
                yoba = "boba"

            a_matrix[for_which, by_which] = (mb_current_pressure - mb_dif_pressure) / delta_pressure  # считаю коэффициент a




"# Выше матбаланс, готовь акваланг"
Nx = 10
Ny = 10
#DesignVariant = [(0, 0, "inject"), (Ny-1, Nx-1, "extract")]
DesignVariant = [(int(Ny/2), int(Nx/2), "extract")]


timeBefore = time.time()

CellsBox = Grid.Grid(Nx, Ny, DesignVariant)

timeAfter = time.time()


calculation_steps = int(input("введите число расчетных месяцев:"))  # расчетный шаг в месяцах

a_matrix_oil = np.zeros((Ny * Nx, Nx * Ny), dtype="float32")  # a_matrix{y,x] где у - номер ячейки, для которой считаем производную, x - по которой
b_matrix_oil = np.zeros((Ny * Nx), dtype="float32")  # один b для каждой ячейки
a_matrix_water = np.zeros((Ny * Nx, Nx * Ny), dtype="float32")
b_matrix_water = np.zeros((Ny * Nx), dtype="float32")

for step in range(calculation_steps):
    do_iter = 0
    while True:
        "# прохожусь по ячейкам, передаю координаты текущей ячейки в матбаланс"
        for y in range(Ny):
            for x in range(Nx):
                _material_balance(x, y, a_matrix_oil, b_matrix_oil, scenario="oil")
                _material_balance(x, y, a_matrix_water, b_matrix_water, scenario="water")

        for for_which in range(Nx*Ny):
            for by_which in range(Nx*Ny):
                water_pressure_in_by_which = CellsBox.cells_numbers[by_which].get_pressure_water(step)
                oil_pressure_in_by_which = CellsBox.cells_numbers[by_which].get_pressure_oil(step)

                b_matrix_water[for_which] += a_matrix_water[for_which, by_which] * water_pressure_in_by_which
                b_matrix_oil[for_which] += a_matrix_oil[for_which, by_which] * oil_pressure_in_by_which

        pressure_water_roots = np.linalg.solve(a_matrix_water, b_matrix_water)
        pressure_oil_roots = np.linalg.solve(a_matrix_oil, b_matrix_oil)

        pressure_accuracy = True
        for cell in range(Nx*Ny):
            water_accuracy = (abs(CellsBox.cells_numbers[cell].get_pressure_water(step) - pressure_water_roots[cell]) > 0.1)
            oil_accuracy = (abs(CellsBox.cells_numbers[cell].get_pressure_oil(step) - pressure_oil_roots[cell]) > 0.1)
            if water_accuracy or oil_accuracy:
                pressure_accuracy = False
                break

        for cell in range(Nx * Ny):
            CellsBox.cells_numbers[cell].new_approach(pressure_water_roots[cell], pressure_oil_roots[cell], step, pressure_accuracy)

        if pressure_accuracy:
            break
        do_iter +=1
        print(do_iter)
"# давления на последний месяц"
print(f"давление по воде")
for i in range(Ny):
    for j in range(Nx):
        print(CellsBox.matrix[i, j].layer_pressure_oil[step], end="|")
    print(f"\n{'-'*Nx*Nx}")

print(f"давление по нефти")
for i in range(Ny):
    for j in range(Nx):
        print(CellsBox.matrix[i, j].layer_pressure_water[step], end="|")
    print(f"\n{'-'*Nx*Nx}")

print(CellsBox.matrix[int(Ny/2), int(Nx/2)].well_presence.accumulated_water_injection)
print(CellsBox.matrix[int(Ny/2), int(Nx/2)].well_presence.accumulated_water_production)
print(CellsBox.matrix[int(Ny/2), int(Nx/2)].well_presence.accumulated_oil_production)
"#поля для перетоков у объекта скважина сделать в виде словарей {направление: [массив значений по месяцам]}"
print(f'тип хранилища ячеек {type(CellsBox)}')
print(f'время на инициализацию сетки: {timeAfter-timeBefore} секунд')



