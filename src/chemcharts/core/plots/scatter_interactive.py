from typing import List

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.plots.base_plot import BasePlot, _check_value_input
from chemcharts.core.utils.value_functions import generate_value

from chemcharts.core.utils.enums import PlottingEnum
from chemcharts.core.utils.enums import PlotLabellingEnum
_PE = PlottingEnum
_PLE = PlotLabellingEnum


class ScatterInteractivePlot(BasePlot):
    def __init__(self):
        super().__init__()

    def plot(self, chemdata_list: List[ChemData], parameters: dict, settings: dict):
        # base class call
        super(ScatterInteractivePlot, self).plot(chemdata_list, parameters, settings)

        # checks whether there is a score input
        value_input_result = _check_value_input(chemdata_list, "Scatter_interactive")

        # checks whether there are multiple input objects
        if value_input_result:      # checks whether _check_value_input function returns 'True'
            if isinstance(chemdata_list, list):
                print("Scatter interactive function does not support multiple input objects. "
                      "Proceeding with first object.")
                chemdata_list = chemdata_list[0]

            xlim = parameters.get(_PE.PARAMETERS_XLIM, None)
            ylim = parameters.get(_PE.PARAMETERS_YLIM, None)
            path = settings.get(_PE.SETTINGS_PATH, None)
            valuelim = parameters.get(_PE.PARAMETERS_VALUELIM, None)

            value_column, value_name = generate_value(chemdata_list=chemdata_list,
                                                      parameters=parameters,
                                                      idx=None)

            self._prepare_folder(path=path)

            scatter_df = pd.DataFrame({_PLE.UMAP_1: chemdata_list.get_embedding().np_array[:, 0],
                                       _PLE.UMAP_2: chemdata_list.get_embedding().np_array[:, 1],
                                       value_name: value_column
                                       })

            fig = px.scatter_3d(scatter_df,
                                x=_PLE.UMAP_1, y=_PLE.UMAP_2, z=value_name,
                                color=value_column,
                                color_discrete_sequence=px.colors.qualitative.Plotly,
                                range_color=valuelim,
                                title=parameters.get(_PE.PARAMETERS_PLOT_TITLE, "Scatter Interactive ChemCharts Plot")
                                )
            fig.update_traces(marker_size=parameters.get(_PE.PARAMETERS_PLOT_MARKER_SIZE, 1))

            fig.update_layout(
                scene=dict(
                    xaxis={} if xlim is None else dict(nticks=6, range=xlim),
                    yaxis={} if ylim is None else dict(nticks=6, range=ylim),
                    zaxis={} if valuelim is None else dict(nticks=6, range=valuelim)),
                width=settings.get(_PE.SETTINGS_FIG_SIZE[0], 900),
                height=settings.get(_PE.SETTINGS_FIG_SIZE[1], 900),
                margin=dict(r=20, l=10, b=30, t=70),
                )

            # set colorbar title
            fig.layout.coloraxis.colorbar.title = value_name

            if settings.get(_PE.SETTINGS_VIEW) is True:
                fig.show()

            fig.write_image(path,
                            format=settings.get(_PE.SETTINGS_FIG_FORMAT, 'png'))

            plt.close("all")






