from project.ObjectModels import grid
import numpy as np
import time

def initialization(Nx, Ny, well_location=None):

    CellsBox = [[grid.GridsCell(coordinateX=x, coordinateY=y) for x in range(Nx)] for y in range(Ny)]
    #прописать объект скважина
    #попытаться сделать класс Grid, который представляет из себя текущий CellsBox
    return CellsBox

Nx = 4
Ny = 4

timeBefore = time.time()

CellBox = initialization(Nx, Ny)

timeAfter = time.time()

print(f'\n координата х = {CellBox[2][1].coordinateX} '
      f'\n координата у = {CellBox[2][1].coordinateY} ')

print(timeAfter-timeBefore)

