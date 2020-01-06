
from project.ObjectModels import grid
import numpy as np

def initialization(Nx, Ny, well_location = None):

    amount_of_cells = Nx * Ny +1
    for i in range(1, amount_of_cells):
        CellsBox.append(grid.GridsCell(cellNumber=i))
        CellsBox[-1].NeighbourIdentification

Nx = 10
Ny = 10

CellsBox =[] # Массив объектов-ячеек
initialization(Nx, Ny)



print(len(CellsBox))