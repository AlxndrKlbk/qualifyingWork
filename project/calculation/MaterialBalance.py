from project.ObjectModels import GridsElements
import numpy as np
import time


def initialization(Nx, Ny, well_location=None):
    """This function create numeric field and add in each cell element of Grid

    :param Nx:  amount of cells along the X axis
    :param Ny:  amount of cells along the Y axis
    :param well_location: should my object DesignVariant
    :return: generated numeric field
    """
    CellsBox = np.zeros((Ny, Nx), dtype=type(GridsElements.GridsCell))
    for y in range(Ny):
        for x in range(Nx):
            CellsBox[y, x] = GridsElements.GridsCell(coordinateX=x, coordinateY=y)
            '#прописать присвоение объекта скважина к ячейке'
    return CellsBox

Nx = 1000
Ny = 1000

timeBefore = time.time()

CellsBox = initialization(Nx, Ny)

timeAfter = time.time()

print(f'\n координата х = {CellsBox[999,999].coordinateX} '
      f'\n координата у = {CellsBox[999,999].coordinateY} ')
print(f'тип хранилища ячеек {type(CellsBox)}')
print(f'время на инициализацию сетки: {timeAfter-timeBefore} секунд')

