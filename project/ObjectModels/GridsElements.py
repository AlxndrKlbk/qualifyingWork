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
    mu_fluid = 5.5  # посмотреть как пересчитывать в зависимости от содержания компонент
    porosity = 0.4
    Boil = 1.126
    Bw = 1
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
        self.layer_pressure_fluid = {}
        self.layer_pressure_oil = {}
        self.layer_pressure_water_prev = GridsCell.beginningPressure + 1  # пластовое давление в ячейке (атмосферы) на конец месяца
        self.layer_pressure_oil_prev = GridsCell.beginningPressure + 1
        self.layer_pressure_fluid_prev = GridsCell.beginningPressure + 1
        self.water_flow_accumulated = {"west": 0, "north": 0, "east": 0, "south": 0}  # словарь перетоков, по ключу хранится накопленный по данному направлению переток
        self.water_flow_fict = {"west": 0, "north": 0, "east": 0, "south": 0}  # словарь фиктивных перетоков на i шаге, после схождения эти значения суммируются в flow_accumulated
        self.oil_flow_accumulated = {"west": 0, "north": 0, "east": 0, "south": 0}
        self.oil_flow_fict = {"west": 0, "north": 0, "east": 0, "south": 0}
        self.fluid_flow_accumulated = {"west": 0, "north": 0, "east": 0, "south": 0}
        self.fluid_flow_fict = {"west": 0, "north": 0, "east": 0, "south": 0}
        self.well_presence = well_presence  # есть ли в ячейке скважина, если есть нужно хранить ссылку на объект скважины
        self.oil_saturation = float()    # текущая нефтенасыщенность на конец месяца
        self.neighbours = neighbours  # словарь соседей
        self.cell_number = cell_number
        self.absolute_permeability = GridsCell.absolute_permeability
        self.oil_fund = GridsCell.beginningOil
        self.water_fund = GridsCell.beginningWater
        self.fluid_fund = GridsCell.beginningFluid
        self.layer_pressure_water[0] = GridsCell.beginningPressure
        self.layer_pressure_oil[0] = GridsCell.beginningPressure
        self.layer_pressure_fluid[0] = GridsCell.beginningPressure

    def get_accumulated_fluid_flow(self, step, direction):
        if step == 0:
            return 0
        else:
            return self.fluid_flow_accumulated[direction]

    def get_accumulated_water_flow(self, step, direction):
        if step == 0:
            return 0
        else:
            return self.water_flow_accumulated[direction]

    def get_accumulated_oil_flow(self, step, direction):
        if step == 0:
            return 0
        else:
            return self.oil_flow_accumulated[direction]

    def delta_pressure_fluid(self, step):
        return self.layer_pressure_fluid[step] - self.layer_pressure_fluid_prev

    def get_pressure_fluid(self, step):
        return self.layer_pressure_fluid[step]

    def get_prev_pressure_fluid(self, step):
        return self.layer_pressure_fluid_prev

    def delta_pressure_oil(self, step):
        return self.layer_pressure_oil[step] - self.layer_pressure_oil_prev

    def get_pressure_oil(self, step):
        return self.layer_pressure_oil[step]

    def get_prev_pressure_oil(self, step):
        return self.layer_pressure_oil_prev

    def get_fluid_permeability(self):
        return self.absolute_permeability

    def get_water_permeability(self):
        Sw = self.water_fund / self.beginningFluid
        if Sw < 0:
            Sw = 0
        elif Sw > 1:
            Sw = 1
        RPP = 0.3*Sw
        #RPP = (14.358*(Sw**3) - 15.464*(Sw**2) + 5.5374*Sw - 0.6512)  # relative phase permeability
        return self.absolute_permeability * RPP

    def get_oil_permeability(self):
        Sw = self.water_fund / self.beginningFluid
        if Sw < 0 :
            Sw = 0
        elif Sw > 1:
            Sw = 1

        RPP = 0.5357*(Sw**4) - 2.1071 * (Sw**3) + 3.4232*(Sw**2) - 2.8518*Sw + 1
        #RPP = (440.02*(Sw**4) - 859.22*(Sw**3) + 628.34*(Sw**2) - 204.27*So + 24.955)  # relative phase permeability
        return self.absolute_permeability * RPP

    def save_pressures_oil(self, new_oil_press, step):
        self.layer_pressure_oil_prev = self.layer_pressure_oil[step]
        self.layer_pressure_oil[step + 1] = new_oil_press

    def calculate_flow_fluid(self, direction, another_cell_pressure, this_cell_pressure, grid, step):
        """This function calculate fluid flow

        :param direction: flow direction (west, north, east, south)
        :param another_cell_pressure: pressure in that direction
        :param this_cell_pressure: pressure in this cell
        :param grid: numeric field, given for taking pressure in another cell
        :param step: calculation step (month)
        :return: fixes in entity and return value of flow in thousand meters**3
        """
        permeability = self.get_fluid_permeability()
        if self.neighbours[direction] and (this_cell_pressure >= another_cell_pressure):
            neighbour_x = self.neighbours[direction][1]
            neighbour_y = self.neighbours[direction][0]
            permeability = grid.matrix[neighbour_y, neighbour_x].get_fluid_permeability()
        contact_space = GridsCell.CellHeight * 1.5  # GridsCell.CellSize
        delta_pressure = this_cell_pressure - another_cell_pressure
        acc_flow = self.get_accumulated_fluid_flow(step, direction)  # накопленный по направлению поток
        self.fluid_flow_fict[direction] = ((permeability * contact_space * delta_pressure)
                                           / (GridsCell.mu_fluid * GridsCell.CellSize)) * 0.03 + acc_flow
        return self.fluid_flow_fict[direction]
    
    def calculate_flow_water(self, direction, another_cell_pressure, this_cell_pressure, grid, step):
        """This function calculate water flow using upstream permeability

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
        contact_space = GridsCell.CellHeight * 1.5  # GridsCell.CellSize
        delta_pressure = this_cell_pressure - another_cell_pressure
        self.water_flow_fict[direction] = ((permeability * contact_space * delta_pressure)
                                           / (GridsCell.mu_water * GridsCell.CellSize)) * 0.03
        return self.water_flow_fict[direction]

    def calculate_flow_oil(self, direction, another_cell_pressure, this_cell_pressure, grid, step):
        """This function calculate oil flow using upstream permeability

        :param direction: flow direction (west, north, east, south)
        :param another_cell_pressure: pressure in that direction
        :param this_cell_pressure: pressure in this cell
        :param grid: numeric field, given for taking pressure in another cell
        :param step: calculation step (month)
        :return: fixes in entity and return value of flow in thousand meters**3
        """
        permeability = self.get_oil_permeability()
        if self.neighbours[direction]:
            if self.neighbours[direction] and (this_cell_pressure >= another_cell_pressure):
                neighbour_x = self.neighbours[direction][1]
                neighbour_y = self.neighbours[direction][0]
                permeability = grid.matrix[neighbour_y, neighbour_x].get_oil_permeability()
            contact_space = GridsCell.CellHeight * 1.5  # GridsCell.CellSize
            delta_pressure = this_cell_pressure - another_cell_pressure
            self.oil_flow_fict[direction] = ((permeability * contact_space * delta_pressure)
                                                / (GridsCell.mu_oil * GridsCell.CellSize)) * 0.03 # 0.3 => * 30 дней / 1000
            return self.oil_flow_fict[direction]
        else:
            return 0

    def new_approach(self, new_fluid_pres, step, accuracy):  # если accuracy True, то следующий шаг по времени, в противном случае только замена давлений
        if not accuracy:
            self.layer_pressure_fluid_prev = self.layer_pressure_fluid[step]
            self.layer_pressure_fluid[step] = new_fluid_pres

        else:
            self.layer_pressure_fluid_prev = new_fluid_pres + 1
            self.layer_pressure_fluid[step + 1] = new_fluid_pres

            directions = self.fluid_flow_accumulated.keys()
            fluid_summ = 0

            for direction in directions:
                self.fluid_flow_accumulated[direction] = self.fluid_flow_fict[direction]
                fluid_summ += self.fluid_flow_fict[direction]
            if self.well_presence:
                well = self.well_presence
                well.new_approach(step)   # этим действием вызывается запись накопленных показателей по скважине
                fluid_summ += well.fict_fluid_production + well.fict_water_injection

            self.fluid_fund -= fluid_summ


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
        self.accumulated_fluid_production = {}
        self.accumulated_oil_production = {}
        self.fict_water_injection = 0
        self.fict_water_production = 0
        self.fict_fluid_production = 0
        self.fict_oil_production = 0

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

    def get_accumulated_fluid_production(self, step):
        if step == 0:
            return 0
        else:
            return self.accumulated_fluid_production[step-1]

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
    
    def fluid_production(self, cell, step):
        """This function return accumulated fluid production considering current mouth production

        :param cell: cell entity, which contain this well
        :param step: current month
        :return: fictitious fluid production
        """
        layer_pressure = cell.get_pressure_fluid(step)
        delta_pressure = layer_pressure - self.well_pressure
        self.fict_fluid_production = ((cell.get_fluid_permeability() * GridsCell.CellHeight * delta_pressure)/
                                      (18.41 * GridsCell.mu_fluid * (math.log((self.Rb/self.Rw)) - 0.75 + self.Skin))*0.03
                                      + self.get_accumulated_fluid_production(step))
        return self.fict_fluid_production

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

    def new_approach(self, step):
        """ this function fix well job for month

        :param step: calculation month
        :return: nothing
        """
        self.accumulated_fluid_production[step] = self.fict_fluid_production
        self.accumulated_water_injection[step] = self.fict_water_injection

    def save_production(self, step, production):
        self.accumulated_oil_production[step] = production

