
from project.ObjectModels import Grid
import numpy as np
import time


Nx = 1000
Ny = 1000
DesignVariant = [(0, 0, "inject"), (Ny-1, Nx-1, "extract")]


timeBefore = time.time()

CellsBox = Grid.Grid(Nx, Ny, DesignVariant)

timeAfter = time.time()


"#поля для перетоков у объекта скважина сделать в виде словарей {направление: [массив значений по месяцам]}"

print(f'тип хранилища ячеек {type(CellsBox)}')
print(f'время на инициализацию сетки: {timeAfter-timeBefore} секунд')



