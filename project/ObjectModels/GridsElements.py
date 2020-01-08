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

    beginningPressure = 250.0  #начальное пластовое давление (атм)
    beginningFluid = 200*(10 ** 3)    #начальные запасы жидкости м3
    beginningOilSaturation = 0.6 #доля нефти в жидкости
    CellSize = 100.0  #размер ребра ячейки (м)
    CellHeight = 3.0   #мощность ННТ в ячейке (м)

    def __init__(self, well_presence = None, neighbours=None):
        self.layerPressure = {}  #пластовое давление в ячейке (атмосферы) на конец месяца
        self.Qwest = []   #накопленный переток в ячейку слева
        self.Qnorth = []  #накопленный переток в ячейку сверху
        self.Qeast = []   #накопленный переток в ячейку справа
        self.Qsouth = []  #накопленный переток в ячейку снизу
        self.QwestFict = float()  # переток в ячейку слева до схождения по погрешности
        self.QnorthFict = float()  # переток в ячейку сверху до схождения по погрешности
        self.QeastFict = float()  # переток в ячейку справа до схождения по погрешности
        self.QsouthFict = float()  # переток в ячейку снизу до схождения по погрешности
        self.well_presence = well_presence #есть ли в ячейке скважина, если есть нужно хранить ссылку на объект скважины
        self.accumulated_water_injection = []  # накопленная по ячейке закачка на текущий момент
        self.accumulated_fluid_production = []  # накопленная по ячейке добыча на текущий момент
        self.OilSaturation = float()    #текущая нефтенасыщенность на конец месяца
        self.neighbours = neighbours


class GridsWell:

    def __init__(self, coordinate_x=None, coordinate_y=None, well_number=None, destiny=None):
        self.well_number = well_number
        self.destiny = destiny
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.accumulated_water_injection = []  # накопленная по ячейке закачка на текущий момент
        self.accumulated_fluid_production = []  # накопленная по ячейке добыча на текущий момент
        self.well_pressure = float()