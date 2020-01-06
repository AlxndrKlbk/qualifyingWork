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

    beginningPressure = float()
    beginningOil = float()    #начальные запасы нефти тыс.м3
    CellSize = float()  #размер ребра ячейки
    CellHeight = float()    #мощность ННТ в ячейке


    def __init__(self, coordinateX = None, coordinateY = None):
        self.coordinateX = coordinateX
        self.coordinateY = coordinateY
        self.layerPressure = {}  #пластовое давление в ячейке (атмосферы) на начало месяца
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



    def NeighbourIdentification(self):
        """
        Эта функция должна определять соседние ячейки через координаты
        ----------
        записывает соседние ячейки в словарь каждого экземляра
        класса GridCell
        формат словаря {north : number , west :number ...}
        """

        self.coordinateX = self.cellNumber
        pass


if __name__ == "__main__":
    array_of_cells = []
    for i in range(10):
        array_of_cells.append(GridsCell(
            cellNumber=i
        ))


    print(len(array_of_cells))