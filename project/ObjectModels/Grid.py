import numpy as np
import project.ObjectModels.GridsElements as GridsElements


class Grid:

    def __init__(self, Nx, Ny, DesignVariant = None):
        """This function create Numpy array and add in each cell element of Grid

        :param Nx:  amount of cells along the X axis
        :param Ny:  amount of cells along the Y axis
        :param well_location: should my object DesignVariant
        :return: generated numeric field
        """

        def _neighbour_identification(x, y):
            """This function define cell's neighbours

            :param x: cell's x coordinate
            :param y: cell's y coordinate
            :return: dict containing neighbours
            """
            neighbours = {"itself":  (y, x), "west": None, "north": None, "east": None, "south": None}
            if x != 0:
                neighbours["west"] = (y, x - 1)
            if x != Nx - 1:
                neighbours["east"] = (y, x + 1)
            if y != 0:
                neighbours["north"] = (y - 1, x)
            if y != Ny - 1:
                neighbours["south"] = (y + 1, x)

            return neighbours

        def _create_matrix():
            matrix = np.zeros((Ny, Nx), dtype=type(GridsElements.GridsCell))
            number = 0
            for y in range(Ny):
                for x in range(Nx):
                    neighbours = _neighbour_identification(x, y)
                    matrix[y, x] = GridsElements.GridsCell(neighbours=neighbours, cell_number= number)
                    number += 1

            for i in range(len(DesignVariant)):  # список кортежей-вариантов (y,x, назнеачение)
                variant = DesignVariant[i]
                x = variant[1]
                y = variant[0]
                well_type = variant[2]
                matrix[y, x].well_presence = GridsElements.GridsWell(destiny=well_type,
                                                                     coordinate_x=x,
                                                                     coordinate_y=y,
                                                                     well_number=i+1)
            return matrix

        self.Nx = Nx
        self.Ny = Ny
        self.matrix = _create_matrix()
