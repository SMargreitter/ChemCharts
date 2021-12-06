import numpy as np
import plotly.figure_factory as ff
from scipy.spatial import Delaunay

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.plots.base_plot import BasePlot

from chemcharts.core.utils.enums import PlottingEnum
_PE = PlottingEnum


class TrisurfInteractivePlot(BasePlot):
    def __init__(self):
        super().__init__()

    def plot(self, chemdata: ChemData, parameters: dict, settings: dict):
        xlim = parameters.get(_PE.PARAMETERS_XLIM, None)
        ylim = parameters.get(_PE.PARAMETERS_YLIM, None)
        path = settings.get(_PE.SETTINGS_PATH, None)
        scorelim = parameters.get(_PE.PARAMETERS_SCORELIM, None)

        self._prepare_folder(path=path)

        x = chemdata.get_embedding().np_array[:, 0]
        y = chemdata.get_embedding().np_array[:, 1]
        z = chemdata.get_scores()

        tri = Delaunay(np.array([x, y]).T)
        simplices = tri.simplices

        fig = ff.create_trisurf(x=x, y=y, z=z,
                                colormap="Portland",
                                simplices=simplices,
                                title="Trisurf ChemCharts Plot"
                                )

        fig.update_layout(
            scene=dict(
                xaxis={} if xlim is None else dict(nticks=6, range=xlim),
                yaxis={} if ylim is None else dict(nticks=6, range=ylim),
                zaxis={} if scorelim is None else dict(nticks=6, range=scorelim)),
            width=700,
            margin=dict(r=20, l=10, b=10, t=10))

        if settings["view"] is True:
            fig.show()

        fig.write_image(path)
