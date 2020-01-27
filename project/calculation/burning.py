import copy
import random
import math
from project.calculation import MaterialBalance

"""
имитация отжига
"""


def temperature_k(Tini, k):
    return Tini/(math.log(1+k))

def income_calculation(wells_list, last_mouth, price):
    amount = len(wells_list)
    accumulated_production = 0
    for well in wells_list:
        accumulated_production += well.accumulated_oil_production[int(last_mouth-1)]

    calc_npv = (accumulated_production * 1000 * 0.85 * price)/(amount * nns_cost)
    return calc_npv

oil_price = 23000 # руб/т
nns_cost = 19153500  # цена бурения ННС рублей
Tini = 10
Tmin = 1
"# обязательные параметры "
fate = ["extract", "inject"]
Nx = 10
Ny = 10
months = int(input("введите число месяцев для прогноза:"))  # расчетный шаг в месяцах
DesignVariant = [(int(Ny/2), int(Nx/2), "extract")]

"# задаю предполагаемый охват у скважины"
coverage = [250, 300, 400]
wells_amount = []
for item in coverage:
    wells_amount.append((Nx*Ny*(100**2)//(item**2)))
smallest_amount = min(wells_amount)
wells_amount.append(smallest_amount + 1)
wells_amount.append(smallest_amount - 1)

k = 1

Temperature = Tini

for wells in wells_amount:
    while Temperature > Tmin:
        taken_coords = []
        compited_iterations = 0
        while compited_iterations < wells:
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

        result = MaterialBalance.MB_calculation(Nx, Ny, DesignVariant, months)  # CellBox запихать в цикл и смотреть динамику скважин
        NPV = income_calculation(result.wells_list, months, oil_price)

        Temperature = temperature_k(Tini,k)
        k += 1







print(f"итераций {k}")