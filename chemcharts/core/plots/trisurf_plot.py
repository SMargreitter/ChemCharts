import plotly.figure_factory as ff

import numpy as np
from scipy.spatial import Delaunay

from chemcharts.core.container.chemdata import ChemData


class TrisurfPlot:
    def __init__(self):
        pass

    @staticmethod
    def plot(chemdata: ChemData, path: str):
        x = chemdata.get_embedding().np_array[:, 0]
        y = chemdata.get_embedding().np_array[:, 1]
        z = chemdata.get_scores()

        tri = Delaunay(np.array([x, y]).T)
        simplices = tri.simplices

        fig = ff.create_trisurf(x=x, y=y, z=z,
                                colormap="Portland",
                                simplices=simplices,
                                title="Trisurf ChemCharts Plot")

        fig.show()
        fig.write_image(path)


