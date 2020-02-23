from project.calculation import MaterialBalance
from project.ObjectModels import GridsElements
import math

sigma = 0.03  # Н/м
cosTeta = 0.5  # краевой угол 45 градусов


def JFunction(Sw):
    """This function calculate capillary pressure, using laboratory data interpolation

    :param Sw: cells water saturation
    :return: capillary pressure
    """
    if Sw < 0.3:
        Sw = 0.3
    elif Sw > 1:
        Sw = 1
    porosity = GridsElements.GridsCell.porosity
    permeability = GridsElements.GridsCell.absolute_permeability * (10**(-15))  # проницаемость переводится из мД в м2
    J = 0.005 * Sw ** (-6.483)  # interpolation put here
    if __name__ == '__main__':
        print(f"J*sigma*cosTeta =  {(J*sigma*cosTeta)}")
        print(f"проницаемость на пористость {(permeability/porosity)**0.5}")
    return (J*sigma*cosTeta)/((permeability/porosity)**0.5)*(10**(-5))


water_saturation_table = [
    0.3,
    0.326,
    0.376,
    0.416,
    0.456,
    0.496,
    0.536,
    0.576,
    0.602,
    0.619,
    0.651,
    0.66,
    0.672,
    0.685,
    0.7,
    0.719,
    0.99,
    1]
if __name__ == '__main__':
    for saturation in water_saturation_table:
        print(f"капилярное давление равно {JFunction(saturation)} Па")