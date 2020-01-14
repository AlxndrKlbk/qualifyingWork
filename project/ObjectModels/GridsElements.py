import numpy


class GridsCell:
    """
    в классовых переменных указаные общие параметры для ячеек:
    -----------
    beginningPressure -  Начальное пластовое давление (атм)
    beginningOil - начальные запасы нефти (тыс.м3.)
    CellSize - размер ребра ячейки (м)
    CellHeight - мощность ННТ в ячейке (м)
    """
    porosity = 0.4
    beginningPressure = 250.0  #начальное пластовое давление (атм)
    beginningOilSaturation = 0.6 #доля нефти в жидкости
    CellSize = 100.0  #размер ребра ячейки (м)
    CellHeight = 3.0   #мощность ННТ в ячейке (м)
    beginningFluid = ((CellSize ** 3) * porosity)/1000  # начальные запасы жидкости тыс м3
    beginningOil = beginningFluid*beginningOilSaturation  # начальные запасы нефти тыс м3
    beginningWater = beginningFluid - beginningOil  # начальные запасы воды тыс м3

    def __init__(self, well_presence = None, neighbours=None, cell_number=None):
        self.layer_pressure_water = {}  # пластовое давление в ячейке (атмосферы) на конец месяца
        self.layer_pressure_oil = {}
        self.water_flow_accumulated = {"west": None, "north": None, "east": None, "south": None}  # словарь перетоков, по ключу хранится накопленный по данному направлению переток
        self.water_flow_fict = {"west": None, "north": None, "east": None, "south": None}  # словарь фиктивных перетоков на i шаге, после схождения эти значения суммируются в flow_accumulated
        self.oil_flow_accumulated = {"west": None, "north": None, "east": None, "south": None}
        self.oil_flow_fict = {"west": None, "north": None, "east": None, "south": None}
        self.well_presence = well_presence  # есть ли в ячейке скважина, если есть нужно хранить ссылку на объект скважины
        self.OilSaturation = float()    # текущая нефтенасыщенность на конец месяца
        self.neighbours = neighbours  # словарь соседей
        self.cell_number = cell_number

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


class GridsWell:

    def __init__(self, coordinate_x=None, coordinate_y=None, well_number=None, destiny=None):
        self.well_number = well_number
        self.destiny = destiny
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.accumulated_water_injection = []  # накопленная скважиной закачка на текущий момент
        self.accumulated_water_production = []  # накопленная скважиной добыча на текущий момент
        self.accumulated_oil_production = []

        if self.destiny == "inject":
            self.well_pressure = GridsCell.beginningPressure + 50
        elif self.destiny == "extract":
            self.well_pressure = GridsCell.beginningPressure - 80