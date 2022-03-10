from typing import List

import numpy as np
import plotly.figure_factory as ff
from scipy.spatial import Delaunay

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.plots.base_plot import BasePlot, _check_value_input
from chemcharts.core.utils.value_functions import generate_value

from chemcharts.core.utils.enums import PlottingEnum
from chemcharts.core.utils.enums import PlotLabellingEnum
_PE = PlottingEnum
_PLE = PlotLabellingEnum


class TrisurfInteractivePlot(BasePlot):
    def __init__(self):
        super().__init__()

    def plot(self, chemdata_list: List[ChemData], parameters: dict, settings: dict):
        # base class call
        super(TrisurfInteractivePlot, self).plot(chemdata_list, parameters, settings)

        # checks whether there is a value input
        value_input_result = _check_value_input(chemdata_list, "Trisurf_interactive")

        # checks whether there are multiple input objects
        if value_input_result:      # checks whether _check_value_input function returns 'True'
            if isinstance(chemdata_list, list):
                print("Trisurf interactive function does not support multiple input objects. "
                      "Proceeding with first object.")
                chemdata_list = chemdata_list[0]

            xlim = parameters.get(_PE.PARAMETERS_XLIM, None)
            ylim = parameters.get(_PE.PARAMETERS_YLIM, None)
            path = settings.get(_PE.SETTINGS_PATH, None)
            scorelim = parameters.get(_PE.PARAMETERS_VALUELIM, None)

            value_column, value_name = generate_value(chemdata_list=chemdata_list,
                                                      parameters=parameters,
                                                      idx=None)

            self._prepare_folder(path=path)

            x = chemdata_list.get_embedding().np_array[:, 0]
            y = chemdata_list.get_embedding().np_array[:, 1]
            z = value_column

            tri = Delaunay(np.array([x, y]).T)
            simplices = tri.simplices

            fig = ff.create_trisurf(x=x, y=y, z=z,
                                    colormap=parameters.get(_PE.PARAMETERS_PLOT_COLOR, "Portland"),
                                    simplices=simplices,
                                    title=parameters.get(_PE.PARAMETERS_PLOT_TITLE, "Trisurf Interactive ChemCharts Plot")
                                    )

            fig.update_layout(
                scene=dict(
                    xaxis={} if xlim is None else dict(nticks=6, range=xlim),
                    yaxis={} if ylim is None else dict(nticks=6, range=ylim),
                    zaxis={} if scorelim is None else dict(nticks=6, range=scorelim)),
                width=settings.get(_PE.SETTINGS_FIG_SIZE[0], 900),
                height=settings.get(_PE.SETTINGS_FIG_SIZE[1], 900),
                margin=dict(r=50, l=50, b=50, t=100)
            )

            # update axis title
            fig.layout.scene.xaxis.title = _PLE.UMAP_1
            fig.layout.scene.yaxis.title = _PLE.UMAP_2
            fig.layout.scene.zaxis.title = value_name

            if settings.get(_PE.SETTINGS_VIEW) is True:
                fig.show()

            fig.write_image(path,
                            format=settings.get(_PE.SETTINGS_FIG_FORMAT, 'png'))
