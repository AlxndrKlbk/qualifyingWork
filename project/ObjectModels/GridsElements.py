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

    beginningPressure = float(250)  #начальное пластовое давление (атм)
    beginningFluid = float(200*(10 ** 3))    #начальные запасы жидкости м3
    beginningOilSaturation = float(0.6) #доля нефти в жидкости
    CellSize = float(100)  #размер ребра ячейки (м)
    CellHeight = float(3)    #мощность ННТ в ячейке (м)

    def __init__(self, Nx, Ny, coordinateX = None, coordinateY = None):
        self.coordinateX = coordinateX
        self.coordinateY = coordinateY
        self.layerPressure = {}  #пластовое давление в ячейке (атмосферы) на конец месяца
        self.Qwest = []   #накопленный переток в ячейку слева
        self.Qnorth = []  #накопленный переток в ячейку сверху
        self.Qeast = []   #накопленный переток в ячейку справа
        self.Qsouth = []  #накопленный переток в ячейку снизу
        self.QwestFict = float()  # переток в ячейку слева до схождения по погрешности
        self.QnorthFict = float()  # переток в ячейку сверху до схождения по погрешности
        self.QeastFict = float()  # переток в ячейку справа до схождения по погрешности
        self.QsouthFict = float()  # переток в ячейку снизу до схождения по погрешности
        self.WellPresence = [] #есть ли в ячейке скважина, если есть нужно хранить ссылку на объект скважины
        self.AccumulatedWaterInjection = []    #накопленная по ячейке закачка на текущий момент
        self.AccumulatedFluidProduction = [] #накопленная по ячейке добыча на текущий момент
        self.OilSaturation = float()    #текущая нефтенасыщенность на конец месяца
        self.neighbours = self.neighbour_identification(coordinateX, coordinateY, Nx, Ny)

    def neighbour_identification(self, x, y, Nx, Ny):
        if x - 1 >= 0:
            west_neighbour = {"coordinateX": x - 1, "coordinateY": y}
        else:
            west_neighbour = {"coordinateX": None, "coordinateY": None}
        if x + 1 <= Nx - 1:
            east_neighbour = {"coordinateX": x + 1, "coordinateY": y}
        else:
            east_neighbour = {"coordinateX": None, "coordinateY": None}
        if y - 1 >= 0:
            north_neighbour = {"coordinateX": x, "coordinateY": y - 1}
        else:
            north_neighbour = {"coordinateX": None, "coordinateY": None}
        if y + 1 <= Ny - 1:
            south_neighbour = {"coordinateX": x, "coordinateY": y + 1}
        else:
            south_neighbour = {"coordinateX": None, "coordinateY": None}
        return {"west": west_neighbour, "north": north_neighbour, "east": east_neighbour, "south": south_neighbour}