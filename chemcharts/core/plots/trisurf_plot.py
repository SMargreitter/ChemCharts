import plotly.figure_factory as ff

import numpy as np
from scipy.spatial import Delaunay

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.plots.base_plot import BasePlot


class TrisurfPlot(BasePlot):
    def __init__(self):
        super().__init__()

    @staticmethod
    def plot(chemdata: ChemData, path: str, xlim: tuple = None, ylim: tuple = None, scorelim: tuple = None):
        x = chemdata.get_embedding().np_array[:, 0]
        y = chemdata.get_embedding().np_array[:, 1]
        z = chemdata.get_scores()

        tri = Delaunay(np.array([x, y]).T)
        simplices = tri.simplices

        fig = ff.create_trisurf(x=x, y=y, z=z,
                                colormap="Portland",
                                simplices=simplices,
                                title="Trisurf ChemCharts Plot")

        fig.update_layout(
            scene=dict(
                xaxis=dict(nticks=4, range=xlim, ),
                yaxis=dict(nticks=4, range=ylim, ),
                zaxis=dict(nticks=4, range=scorelim, ), ),
            width=700,
            margin=dict(r=20, l=10, b=10, t=10))

  #      fig.show()          ACTIVATE ME VIA JSON!!!!!!!!!!!!!!!!!
        fig.write_image(path)
