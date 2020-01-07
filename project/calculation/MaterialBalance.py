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
            CellsBox[y, x] = GridsElements.GridsCell(coordinateX=x, coordinateY=y,
                                                     neihgbours=neighbour_identification(x, y))
            '#прописать присвоение объекта скважина к ячейке'
    return CellsBox


def neighbour_identification(x, y):

    if x - 1 >= 0:
        west_neighbour = {"coordinateX": x-1, "coordinateY": y}
    else:
        west_neighbour = {"coordinateX": None, "coordinateY": None}
    if x + 1 <= Nx - 1:
        east_neighbour = {"coordinateX": x+1, "coordinateY": y}
    else:
        east_neighbour = {"coordinateX": None, "coordinateY": None}
    if y - 1 >= 0:
        north_neighbour = {"coordinateX": x, "coordinateY": y-1}
    else:
        north_neighbour = {"coordinateX": None, "coordinateY": None}
    if y + 1 <= Ny - 1:
        south_neighbour = {"coordinateX": x, "coordinateY": y+1}
    else:
        south_neighbour = {"coordinateX": None, "coordinateY": None}
    return {"west": west_neighbour, "north": north_neighbour , "east":east_neighbour, "south": south_neighbour}



Nx = 100
Ny = 100

timeBefore = time.time()

CellsBox = initialization(Nx, Ny)

timeAfter = time.time()

print(f'\n координата х = {CellsBox[99,99].coordinateX} '
      f'\n координата у = {CellsBox[99,99].coordinateY} ')
print(f'тип хранилища ячеек {type(CellsBox)}')
print(f'время на инициализацию сетки: {timeAfter-timeBefore} секунд')

neighbours_dict = CellsBox[99,99].neighbours
print(f'координаты северного соседа х={(neighbours_dict.get("north").get("coordinateX"))}, y='
      f'{(neighbours_dict.get("north").get("coordinateY"))}')
print(f'тип значения в словаре {type(neighbours_dict.get("north").get("coordinateX"))}')

