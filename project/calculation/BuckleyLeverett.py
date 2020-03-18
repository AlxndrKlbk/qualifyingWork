from project.ObjectModels import GridsElements


def BuckleyLeverett(water_permeability, oil_permeability):
    mu_oil = GridsElements.GridsCell.mu_oil
    mu_water = GridsElements.GridsCell.mu_water
    return water_permeability/(water_permeability + (mu_water/mu_oil)*oil_permeability)
