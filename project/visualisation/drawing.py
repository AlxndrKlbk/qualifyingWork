import matplotlib.pyplot as plot
from matplotlib import cm
import numpy
from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage import zoom


def draw_pressure_graph(Nx, Ny, myData, month):
    zoom_power = 2
    x = numpy.arange(0, Nx, 1)
    y = numpy.arange(0, Ny, 1)
    xgrid, ygrid = numpy.meshgrid(x, y)
    xgrid = zoom(xgrid, zoom_power )
    ygrid = zoom(ygrid, zoom_power)
    zgrid = numpy.zeros((Ny, Nx))
    for i in range(Ny):
        for j in range(Nx):
            zgrid[i,j] = myData.matrix[i, j].layer_pressure_fluid[month]
    zgrid = zoom(zgrid, zoom_power)
    fiqure = plot.figure()
    axes = Axes3D(fiqure)
    axes.plot_surface(xgrid, ygrid, zgrid, cmap="summer", antialiased=True)
    axes.set_xlabel("ось X", color="red")
    axes.set_ylabel("ось Y", color="red")
    axes.set_zlabel("Давление, атм.", color="red")
    plot.xlim(0, Nx)
    plot.ylim(0, Ny)

    plot.show()

def draw_NPV_grapg(NPV_list):
    fiqure = plot.figure()
    wells_amount = []
    NPV_per_variant = []
    axes2 = fiqure.add_subplot()
    for wells, npv in NPV_list:
        wells_amount.append(wells)
        NPV_per_variant.append(npv)
    wells_amount = numpy.array(wells_amount)
    NPV_per_variant = numpy.array(NPV_per_variant)
    axes2.scatter(wells_amount, NPV_per_variant)
    axes2.set_xlabel("Добывающих скважин", color="red")
    axes2.set_ylabel("NPV", color="red")
    axes2.grid()

    plot.show()
