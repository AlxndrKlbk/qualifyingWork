import numpy
import math

class GridsCell:
    """
    в классовых переменных указаные общие параметры для ячеек:
    -----------
    beginningPressure -  Начальное пластовое давление (атм)
    beginningOil - начальные запасы нефти (тыс.м3.)
    CellSize - размер ребра ячейки (м)
    CellHeight - мощность ННТ в ячейке (м)
    """
    ce = 0.0000149  # сжимаемость системы, аналитическая функция есть в курсаче (1/атм)
    mu_oil = 10  # сП
    mu_water = 1  # сП
    porosity = 0.4
    beginningPressure = 250.0  #начальное пластовое давление (атм)
    beginningOilSaturation = 0.6 #доля нефти в жидкости
    CellSize = 100.0  #размер ребра ячейки (м)
    CellHeight = 3.0   #мощность ННТ в ячейке (м)
    beginningFluid = ((CellSize ** 3) * porosity)/1000  # начальные запасы жидкости тыс м3
    beginningOil = beginningFluid*beginningOilSaturation  # начальные запасы нефти тыс м3
    beginningWater = beginningFluid - beginningOil  # начальные запасы воды тыс м3
    absolute_permeability = 50  # абсолютная проницаемость в мД

    def __init__(self, well_presence = None, neighbours=None, cell_number=None):
        self.layer_pressure_water = {}  # пластовое давление в ячейке (атмосферы) на конец месяца
        self.layer_pressure_oil = {}
        self.water_flow_accumulated = {"west": None, "north": None, "east": None, "south": None}  # словарь перетоков, по ключу хранится накопленный по данному направлению переток
        self.water_flow_fict = {"west": None, "north": None, "east": None, "south": None}  # словарь фиктивных перетоков на i шаге, после схождения эти значения суммируются в flow_accumulated
        self.oil_flow_accumulated = {"west": None, "north": None, "east": None, "south": None}
        self.oil_flow_fict = {"west": None, "north": None, "east": None, "south": None}
        self.well_presence = well_presence  # есть ли в ячейке скважина, если есть нужно хранить ссылку на объект скважины
        self.oil_saturation = float()    # текущая нефтенасыщенность на конец месяца
        self.neighbours = neighbours  # словарь соседей
        self.cell_number = cell_number
        self.absolute_permeability = GridsCell.absolute_permeability
        self.oil_fund = GridsCell.beginningOil
        self.water_fund = GridsCell.beginningWater

    def get_accumulated_water_flow(self, step, direction):
        if step == 0:
            return 0  # давление на -1 шаге на 1 атм больше, чем beginningPressure
        else:
            return self.water_flow_accumulated[direction]

    def get_accumulated_oil_flow(self, step, direction):
        if step == 0:
            return 0  # давление на -1 шаге на 1 атм больше, чем beginningPressure
        else:
            return self.oil_flow_accumulated[direction]

    def delta_pressure_water(self, step):
        if step == 0:
            return -1  # давление на -1 шаге на 1 атм больше, чем beginningPressure
        else:
            return self.layer_pressure_water[step] - self.layer_pressure_water[step - 1]

    def get_pressure_water(self, step):
        if step == 0:
            return GridsCell.beginningPressure
        else:
            return self.layer_pressure_water[step - 1]

    def get_prev_pressure_water(self, step):
        if step == 0:
            return GridsCell.beginningPressure + 1
        else:
            return self.layer_pressure_water[step - 1]

    def delta_pressure_oil(self, step):
        if step == 0:
            return -1  # давление на -1 шаге на 1 атм больше, чем beginningPressure
        else:
            return self.layer_pressure_oil[step] - self.layer_pressure_oil[step - 1]

    def get_pressure_oil(self, step):
        if step == 0:
            return GridsCell.beginningPressure
        else:
            return self.layer_pressure_oil[step - 1]

    def get_prev_pressure_oil(self, step):
        if step == 0:
            return GridsCell.beginningPressure + 1
        else:
            return self.layer_pressure_oil[step - 1]

    def get_water_permeability(self):
        Sw = self.water_fund / self.beginningFluid
        if Sw < 0.272:
            Sw = 0.272
        elif Sw > 0.572:
            Sw = 0.572
        RPP = (14.358*(Sw**3) - 15.464*(Sw**2) + 5.5374*Sw - 0.6512)  # relative phase permeability
        return self.absolute_permeability * RPP

    def get_oil_permeability(self):
        So = self.oil_fund / self.beginningFluid
        if So < 0.428 :
            So = 0.428
        elif So > 0.728:
            So = 0.728
        RPP = (440.02*(So**4) - 859.22*(So**3) + 628.34*(So**2) - 204.27*So + 24.955)  # relative phase permeability
        return self.absolute_permeability * RPP

    def calculate_flow_water(self, direction, another_cell_pressure, this_cell_pressure, grid, step):
        """This function calculate water flow and use upstream permeability

        :param direction: flow direction (west, north, east, south)
        :param another_cell_pressure: pressure in that direction
        :param this_cell_pressure: pressure in this cell
        :param grid: numeric field, given for taking pressure in another cell
        :param step: calculation step (month)
        :return: fixes in entity and return value of flow in thousand meters**3
        """
        permeability = self.get_water_permeability()
        if self.neighbours[direction] and (this_cell_pressure >= another_cell_pressure):
            neighbour_x = self.neighbours[direction][1]
            neighbour_y = self.neighbours[direction][0]
            permeability = grid.matrix[neighbour_y, neighbour_x].get_water_permeability()
        delta_pressure = another_cell_pressure - this_cell_pressure
        acc_flow = self.get_accumulated_water_flow(step, direction)  # накопленный по направлению поток
        self.water_flow_fict[direction] = ((permeability * GridsCell.CellHeight * delta_pressure)
                                           / (GridsCell.mu_water * GridsCell.CellSize)) * 0.03 + acc_flow
        return self.water_flow_fict[direction]

    def calculate_flow_oil(self, direction, another_cell_pressure, this_cell_pressure, grid, step):
        """This function calculate oil flow and use upstream permeability

        :param direction: flow direction (west, north, east, south)
        :param another_cell_pressure: pressure in that direction
        :param this_cell_pressure: pressure in this cell
        :param grid: numeric field, given for taking pressure in another cell
        :param step: calculation step (month)
        :return: fixes in entity and return value of flow in thousand meters**3
        """
        permeability = self.get_oil_permeability()
        if self.neighbours[direction] and (this_cell_pressure >= another_cell_pressure):
            neighbour_x = self.neighbours[direction][1]
            neighbour_y = self.neighbours[direction][0]
            permeability = grid.matrix[neighbour_y, neighbour_x].get_oil_permeability()
        delta_pressure = another_cell_pressure - this_cell_pressure
        acc_flow = self.get_accumulated_oil_flow(step, direction)  # накопленный по направлению поток
        self.oil_flow_fict[direction] = ((permeability * GridsCell.CellHeight * delta_pressure)
                                           / (GridsCell.mu_oil * GridsCell.CellSize)) * 0.03 + acc_flow
        return self.oil_flow_fict[direction]


class GridsWell:

    Rb = 250  # радиус контура питания, м
    Rw = 0.15  # радиус ствола скважины, м
    Skin = -3  # скин фактор

    def __init__(self, coordinate_x=None, coordinate_y=None, well_number=None, destiny=None):
        self.well_number = well_number
        self.destiny = destiny
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.accumulated_water_injection = {}  # накопленная скважиной закачка на текущий момент
        self.accumulated_water_production = {}  # накопленная скважиной добыча на текущий момент
        self.accumulated_oil_production = {}
        self.fict_water_injection = None
        self.fict_water_production = None
        self.fict_oil_production = None

        if self.destiny == "inject":
            self.well_pressure = GridsCell.beginningPressure + 50
        elif self.destiny == "extract":
            self.well_pressure = GridsCell.beginningPressure - 80

    def get_accumulated_injection(self, step):
        if step == 0:
            return 0
        else:
            return self.accumulated_water_injection[step-1]

    def get_accumulated_water_production(self, step):
        if step == 0:
            return 0
        else:
            return self.accumulated_water_production[step-1]

    def get_accumulated_oil_production(self, step):
        if step == 0:
            return 0
        else:
            return self.accumulated_oil_production[step-1]

    def water_injection(self, cell, step):
        """This function return accumulated water injection considering current mouth production

        :param cell: cell entity, which contain this well
        :param step: current month
        :return: fictitious water injection
        """
        layer_pressure = cell.get_pressure_water(step)
        delta_pressure = layer_pressure - self.well_pressure
        self.fict_water_production = ((cell.get_water_permeability() * GridsCell.CellHeight * delta_pressure)/
                                      (18.41 * GridsCell.mu_water * (math.log((self.Rb / self.Rw)) - 0.75 + self.Skin)) * 0.03
                                      + self.get_accumulated_injection(step))
        return self.fict_water_production

    def water_production(self, cell, step):
        """This function return accumulated water production considering current mouth production

        :param cell: cell entity, which contain this well
        :param step: current month
        :return: fictitious water production
        """
        layer_pressure = cell.get_pressure_water(step)
        delta_pressure = layer_pressure - self.well_pressure
        self.fict_water_production = ((cell.get_water_permeability() * GridsCell.CellHeight * delta_pressure)/
                                      (18.41 * GridsCell.mu_water * (math.log((self.Rb/self.Rw)) - 0.75 + self.Skin))*0.03
                                      + self.get_accumulated_water_production(step))
        return self.fict_water_production

    def oil_production(self, cell, step):
        """This function return accumulated oil production considering current mouth production

        :param cell: cell entity, which contain this well
        :param step: current month
        :return: fictitious oil production
        """
        layer_pressure = cell.get_pressure_oil(step)
        delta_pressure = layer_pressure - self.well_pressure
        self.fict_oil_production = ((cell.get_oil_permeability() * GridsCell.CellHeight * delta_pressure)/
                                    (18.41 * GridsCell.mu_oil * (math.log((self.Rb/self.Rw)) - 0.75 + self.Skin))*0.03
                                    + self.get_accumulated_oil_production(step))
        return self.fict_oil_production
