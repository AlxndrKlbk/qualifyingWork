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

    def __init__(self, coordinateX = None, coordinateY = None, neihgbours = None):
        self.coordinateX = coordinateX
        self.coordinateY = coordinateY
        self.layerPressure = {}  #пластовое давление в ячейке (атмосферы) на конец месяца
        self.neighbours = neihgbours
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


if __name__ == "__main__":
    array_of_cells = []
    for i in range(10):
        array_of_cells.append(GridsCell(
            cellNumber=i
        ))


    print(len(array_of_cells))