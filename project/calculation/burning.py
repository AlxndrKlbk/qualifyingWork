import copy
import random
import math
from project.calculation import MaterialBalance

"""
имитация отжига
"""


def temperature_k(Tini, k):
    return Tini/(math.log(1+k))

Tini = 10
Tmin = 1
"# обязательные параметры "
fate = ["extract", "inject"]
Nx = 10
Ny = 10
DesignVariant = [(int(Ny/2), int(Nx/2), "extract")]
# DesignVariant = []  # [(int(Ny/2), int(Nx/2), "extract")]

k = 1

Temperature = Tini

while Temperature > Tmin:
    taken_coords = []
    wells_amount = random.randint(1, Nx * Ny / 4)
    compited_iterations = 0
    while compited_iterations < wells_amount:
        x = random.randint(0, Nx-1)
        y = random.randint(0, Ny-1)
        if (y, x) not in taken_coords:
            if compited_iterations > 0:
                destiny = random.choice(fate)
            else:
                destiny = "extract"
            DesignVariant.append((y, x, destiny))
            # сделать назначение роли, добавление в DesignVariant
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    taken_coords.append((y + dy, x + dx))
            taken_coords = list(set(taken_coords))
            compited_iterations += 1
    print(DesignVariant)

    result = MaterialBalance.MB_calculation(Nx, Ny, DesignVariant)  # CellBox запихать в цикл и смотреть динамику скважин

    Temperature = temperature_k(Tini,k)
    k += 1






print(f"итераций {k}")