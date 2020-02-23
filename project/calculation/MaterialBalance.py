import sys
from project.ObjectModels import Grid
from project.calculation import Leverett
import numpy as np
import time
import copy
import math


def MB_calculation(Nx, Ny, DesignVariant, calculation_steps):
    def _material_balance(x, y, a_matrix, b_matrix, scenario=None):
        def _calculate_material_balance_fluid(step, direction = None, coordinates = None):
            """This function calculate material balance
            :param step: moment of time
            :param direction: if this parameter given, should take one pressure from last step
            :param coordinates: index for neighbour cells
            :return: material balance value
            """
            pressures_copy = copy.deepcopy(neighbours_pressure)

            if direction:
                x = coordinates[1]
                y = coordinates[0]
                pressures_copy[direction] = CellsBox.matrix[y, x].get_prev_pressure_fluid(step)

            "# если в ячейке есть скважина, проверяю ее назначение и пересчитываю накопленные параметры"
            injection = 0
            production = 0
            if cell.well_presence:
                well = cell.well_presence
                pressure_well = cell.well_presence.well_pressure
                if pressure_well < pressures_copy["itself"]:
                    injection = well.get_accumulated_injection(step)
                    production = well.fluid_production(cell, step)
                elif pressure_well >= pressures_copy["itself"]:
                    injection = well.water_injection(cell, step)
                    production = well.get_accumulated_fluid_production(step)

            "# записываю давление в текущей ячейке в переменную, чтобы дальше удобно считать поток по соседям"
            cell_pressure = pressures_copy.pop("itself")  # cell_pressure давление в ячейке, для которой считается Матбаланс
            summary_flow = 0
            for flow_to, pressure in pressures_copy.items():
                summary_flow += cell.calculate_flow_fluid(flow_to, pressure, cell_pressure, CellsBox, step)
            ini_fluid = Grid.GridsElements.GridsCell.beginningFluid
            ce = Grid.GridsElements.GridsCell.ce

            MatBal = Grid.GridsElements.GridsCell.beginningPressure - cell_pressure - ((production + injection + summary_flow)/
                                                                                       (ini_fluid * ce))
            return MatBal

        cell = CellsBox.matrix[y, x]
        neighbours_pressure = {"itself":  None, "west": None, "north": None, "east": None, "south": None}
        "# давления из ячеек соседнего окружения, если соседняя ячейка за контуром, то беру начальное пластовое"
        for direction, coordinates in cell.neighbours.items():
            if coordinates and scenario == "fluid":
                neighbours_pressure[direction] = CellsBox.matrix[coordinates[0], coordinates[1]].get_pressure_fluid(step)
            else:  # если входим в это условие, то значит соседняя ячейка это аквифер
                neighbours_pressure[direction] = Grid.GridsElements.GridsCell.beginningPressure

        "# заполнение матриц а, матрица в вписывается значение мб с текущими давлениями, чтобы после снова не считать "
        for direction, coordinates in cell.neighbours.items():
            for_which = cell.cell_number  # ячейка, для которой считаем мб
            if coordinates and scenario == "fluid":
                by_which = CellsBox.matrix[coordinates[0], coordinates[1]].cell_number  # ячейка, из которой берем приближение давления
                mb_current_pressure = _calculate_material_balance_fluid(step)  # пересчет мб с текущими давлениями
                b_matrix_fluid[for_which] = -mb_current_pressure
                mb_dif_pressure = _calculate_material_balance_fluid(step, direction, coordinates) # пересчет мб с давлением прошлого шага
                delta_pressure = CellsBox.matrix[coordinates[0], coordinates[1]].delta_pressure_fluid(step)
                a_matrix[for_which, by_which] = (mb_current_pressure - mb_dif_pressure)/delta_pressure# считаю коэффициент a

    "# Выше матбаланс, готовь акваланг"

    timeBefore = time.time()
    CellsBox = Grid.Grid(Nx, Ny, DesignVariant)
    timeAfter = time.time()

    a_matrix_fluid = np.zeros((Ny * Nx, Nx * Ny), dtype="float32")  # a_matrix{y,x] где у - номер ячейки, для которой считаем производную, x - по которой
    b_matrix_fluid = np.zeros((Ny * Nx), dtype="float32")   # один b для каждой ячейки

    for step in range(calculation_steps):
        do_iter = 0
        while True:
            "# прохожусь по ячейкам, передаю координаты текущей ячейки в матбаланс"
            for y in range(Ny):
                for x in range(Nx):
                    _material_balance(x, y, a_matrix_fluid, b_matrix_fluid, scenario="fluid")

            for for_which in range(Nx*Ny):
                for by_which in range(Nx*Ny):
                    fluid_pressure_in_by_which = CellsBox.cells_numbers[by_which].get_pressure_fluid(step)
                    b_matrix_fluid[for_which] += a_matrix_fluid[for_which, by_which] * fluid_pressure_in_by_which

            pressure_fluid_roots = np.linalg.solve(a_matrix_fluid, b_matrix_fluid)

            pressure_accuracy = True
            for cell in range(Nx*Ny):
                fluid_accuracy = (abs(CellsBox.cells_numbers[cell].get_pressure_fluid(step) - pressure_fluid_roots[cell]) > 0.1)
                if fluid_accuracy:
                    pressure_accuracy = False
                    break
            """
            выше получено давление по жидкости:
            1)Если погрешность по жидкости сошлась, то через J-функцию нужно определить капилярное давление, 
            потом по нефти как их разность.
            - посчитать перетоки в соответствии с полученными давлениями для ячеек. (Выразить из матбаланса текущие 
            запасы фазы в ячейке)
            - записать приближения, перейти на новый шаг по времени
            2)Если погрешность по жидкости не сошлась, взять новые приближения по жидкости  
            """
            #  выполнится если сошлось давление по жидкости
            if pressure_accuracy:
                pressure_oil_roots = []
                for cell in range(Nx*Ny):
                    water_saturation = CellsBox.cells_numbers[cell].water_fund/CellsBox.cells_numbers[cell].beginningFluid
                    pressure_oil_roots.append(pressure_fluid_roots[cell] - Leverett.JFunction(water_saturation))
                    CellsBox.cells_numbers[cell].save_pressures_oil(pressure_oil_roots[cell], step)


                for cell in range(Nx * Ny):
                    element = CellsBox.cells_numbers[cell]
                    if CellsBox.cells_numbers[cell].well_presence :
                        well = CellsBox.cells_numbers[cell].well_presence
                        if well.destiny == "extract":
                            layer_pressure = element.get_pressure_oil(step+1)
                            delta_pressure = layer_pressure - well.well_pressure
                            production = ((element.get_oil_permeability() * delta_pressure * element.CellHeight)/
                                          (18.41 *element.mu_oil*(math.log((well.Rb/well.Rw)) - 0.75 + well.Skin)))*0.03
                            well.save_production(step, production)
                            element.oil_fund += production
                        else:
                            delta_pressure = element.beginningPressure - element.get_pressure_oil(step+1)
                            beginning_fund = element.beginningFluid * element.ce*element.Boil
                            mass_change = delta_pressure*beginning_fund
                            element.oil_fund += mass_change

                    # посчитать перетоки используя давления по нефти и воде

            for cell in range(Nx * Ny):
                CellsBox.cells_numbers[cell].new_approach(pressure_fluid_roots[cell], step, pressure_accuracy)

            if pressure_accuracy:
                break
            do_iter +=1
            print(do_iter)

    "# давления на последний месяц"
    print(f"давление по нефти")
    for i in range(Ny):
        for j in range(Nx):
            for_print = str(CellsBox.matrix[i, j].layer_pressure_oil[step])
            print(for_print[0:6], end="|")
        print(f"\n{'-'*Nx*Nx}")

    print(f"давление по воде")
    for i in range(Ny):
        for j in range(Nx):
            for_print = str(CellsBox.matrix[i, j].layer_pressure_fluid[step])
            print(for_print[0:6], end="|")
        print(f"\n{'-'*Nx*Nx}")

    print(CellsBox.matrix[int(Ny/2), int(Nx/2)].well_presence.accumulated_water_injection)
    print(CellsBox.matrix[int(Ny/2), int(Nx/2)].well_presence.accumulated_water_production)
    print(CellsBox.matrix[int(Ny/2), int(Nx/2)].well_presence.accumulated_oil_production)

    print(f'тип хранилища ячеек {type(CellsBox)}')
    print(f'время на инициализацию сетки: {timeAfter-timeBefore} секунд')
    return CellsBox


if __name__ == "__main__":
    Nx = 10
    Ny = 10
    DesignVariant = [(int(Ny/2), int(Nx/2), "extract")]
    months = 5
    MB_calculation(Nx, Ny, DesignVariant, months)