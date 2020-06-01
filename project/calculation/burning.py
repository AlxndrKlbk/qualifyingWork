import copy
import random
import math
from project.calculation import MaterialBalance
from project.visualisation import drawing

"""
имитация отжига
"""


def temperature_k(Tini, k):
    return Tini/(math.log(1+k))

def income_calculation(wells_list, last_mouth, price):
    amount = len(wells_list)
    accumulated_production = 0
    for well in wells_list:
        if well.destiny == 'extract':
            accumulated_production += well.accumulated_oil_production[last_mouth-1]
    calc_npv = (accumulated_production * 1000 * 0.85 * price)/(amount * nns_cost)
    return calc_npv

Best_npv = 0
Best_variant = None

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
coverage = [400]
wells_amount = []
for item in coverage:
    wells_amount.append((Nx*Ny*(100**2)//(item**2)))
smallest_amount = min(wells_amount)
wells_amount.append(smallest_amount + 1)
wells_amount.append(smallest_amount - 1)



Temperature = Tini
economic_list = []
result = None

for wells in wells_amount:
    k = 1
    while k < 10:
        extract_amount = 0
        DesignVariant = []
        taken_coords = []
        compited_iterations = 0
        while compited_iterations < wells:
            x = random.randint(0, Nx-1)
            y = random.randint(0, Ny-1)
            if (y, x) not in taken_coords:
                if compited_iterations > 0:
                    destiny = random.choice(fate)
                    if destiny == "extract":
                        extract_amount +=1
                else:
                    destiny = "extract"
                    extract_amount += 1
                DesignVariant.append((int(y), int(x), destiny))
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        taken_coords.append((y + dy, x + dx))
                taken_coords = list(set(taken_coords))
                compited_iterations += 1

        print(f"добывающих {extract_amount} из {wells}")
        print(DesignVariant)


        result = MaterialBalance.MB_calculation(Nx, Ny, DesignVariant, months)
        NPV = income_calculation(result.wells_list, months, oil_price)
        prodaction_to_injection = 0
        for well in result.wells_list:
            if well.destiny is "extract":
                prodaction_to_injection += 1
        prodaction_to_injection = prodaction_to_injection
        economic_list.append((prodaction_to_injection, NPV))
        if NPV > Best_npv:
            Best_variant = result
        print(NPV)

        Temperature = temperature_k(Tini, k)
        k += 1

    drawing.draw_pressure_graph(Nx, Ny, result, months)
    drawing.draw_NPV_grapg(economic_list)
    drawing.draw_oil_saturation(Nx, Ny, result, months)
print(f"итераций {k}")