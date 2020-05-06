import matplotlib.pyplot as plot
from matplotlib import cm
import numpy
from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage import zoom

def draw_graph(Nx, Ny, myData, month):
    zoom_power = 2
    x = numpy.arange(0, Nx, 1)
    y = numpy.arange(0, Ny, 1)
    xgrid, ygrid = numpy.meshgrid(x, y)
    #xgrid = zoom(xgrid, zoom_power )
    #ygrid = zoom(ygrid, zoom_power)
    zgrid = numpy.zeros((Ny, Nx))
    for i in range(Ny):
        for j in range(Nx):
            zgrid[i,j] = myData.matrix[i, j].layer_pressure_fluid[month]
    #zgrid = zoom(zgrid, zoom_power)

    fiqure = plot.figure()
    axes = Axes3D(fiqure)
    axes.plot_surface(xgrid, ygrid, zgrid, cmap="summer", antialiased=True)
    plot.xlim(0, Nx)
    plot.ylim(0, Ny)
    plot.show()
