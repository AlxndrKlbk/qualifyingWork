import numpy


class GridsCell():
    """
    в классовых переменных указаные общие параметры для ячеек:
    -----------
    beginningPressure -  Начальное пластовое давление (атм)
    beginningOil - начальные запасы нефти (тыс.м3.)
    CellSize - размер ребра ячейки (м)
    CellHeight - мощность ННТ в ячейке (м)
    """

    beginningPressure = float
    beginningOil = float    #начальные запасы нефти тыс.м3
    CellSize = float   #размер ребра ячейки
    CellHeight = float #мощность ННТ в ячейке


    def __init__(self, cellNumber):
        self.coordinateX = int
        self.coordinateY = int
        self.cellNumber = cellNumber   #номер ячейки
        self.layerPressure = float  #текущее пластовое давление в ячейке (атмосферы)
        self.neighbours = {}  #словарь с номерами соседних ячеек
        self.Qwest = []   #список перетоков в ячейку слева
        self.Qnorth = list  #список перетоков в ячейку сверху
        self.Qeast = list   #список перетоков в ячейку справа
        self.Qsouth = list  #список перетоков в ячейку снизу
        self.QwestFict = list  # список перетоков в ячейку слева до схождения по погрешности
        self.QnorthFict = list  # список перетоков в ячейку сверху до схождения по погрешности
        self.QeastFict = list  # список перетоков в ячейку справа до схождения по погрешности
        self.QsouthFict = list  # список перетоков в ячейку снизу до схождения по погрешности
        self.WellPresence = str #есть ли в ячейке скважина, если есть нужно хранить ссылку на объект скважины
        self.AccumulatedWaterInjection = list    #накопленная по ячейке закачка на текущий момент
        self.AccumulatedFluidProduction = list #накопленная по ячейке добыча на текущий момент

    def NeighbourIdentification(self):
        """
        Эта функция должна определять соседние ячейки через координаты
        ----------
        записывает соседние ячейки в словарь каждого экземляра
        класса GridCell
        """
        pass


array_of_cells = []
for i in range(10):
    array_of_cells.append(GridsCell(
        cellNumber=i
    ))


print(len(array_of_cells))