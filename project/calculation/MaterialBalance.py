
from project.ObjectModels import grid


CellsArray =[]

for i in range(1, 3):
    CellsArray.append(grid.GridsCell(cellNumber=i))

for cells in CellsArray:
    cells.coordinateX = cells.cellNumber


print(CellsArray)