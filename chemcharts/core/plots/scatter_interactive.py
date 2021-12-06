import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.plots.base_plot import BasePlot

from chemcharts.core.utils.enums import PlottingEnum
from chemcharts.core.utils.enums import PlotLabellingEnum
_PE = PlottingEnum
_PLE = PlotLabellingEnum


class ScatterInteractivePlot(BasePlot):
    def __init__(self):
        super().__init__()

    def plot(self, chemdata: ChemData, parameters: dict, settings: dict):
        xlim = parameters.get(_PE.PARAMETERS_XLIM, None)
        ylim = parameters.get(_PE.PARAMETERS_YLIM, None)
        path = settings.get(_PE.SETTINGS_PATH, None)
        scorelim = parameters.get(_PE.PARAMETERS_SCORELIM, None)


        self._prepare_folder(path=path)

        scatter_df = pd.DataFrame({_PLE.UMAP_1: chemdata.get_embedding().np_array[:, 0],
                                   _PLE.UMAP_2: chemdata.get_embedding().np_array[:, 1],
                                   _PLE.SCORES: chemdata.get_scores()
                                   })
        fig = px.scatter_3d(scatter_df,
                            x=_PLE.UMAP_1, y=_PLE.UMAP_2, z=_PLE.SCORES,
                            color='Scores',
                            color_discrete_sequence=px.colors.qualitative.Plotly,
                            range_color=scorelim
                            )
        fig.update_traces(marker_size=1)

        fig.update_layout(
            scene=dict(
                xaxis={} if xlim is None else dict(nticks=6, range=xlim),
                yaxis={} if ylim is None else dict(nticks=6, range=ylim),
                zaxis={} if scorelim is None else dict(nticks=6, range=scorelim)),
            width=700,
            margin=dict(r=20, l=10, b=10, t=10))

        if _PE.SETTINGS_VIEW is True:
            fig.show()

        fig.write_image(path)
        plt.close("all")






