import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.plots.base_plot import BasePlot


class ScatterInteractivePlot(BasePlot):
    def __init__(self):
        super().__init__()

    @staticmethod
    #def plot(chemdata: ChemData, path: str, xlim: tuple = None,
    #         ylim: tuple = None, scorelim: tuple = None, total_number_observations: int = None):
    def plot(chemdata: ChemData, parameters: dict, settings: dict):

        scatter_df = pd.DataFrame({"UMAP_1": chemdata.get_embedding().np_array[:, 0],
                                   "UMAP_2": chemdata.get_embedding().np_array[:, 1],
                                   "Scores": chemdata.get_scores()
                                   })
        fig = px.scatter_3d(scatter_df,
                            x="UMAP_1", y="UMAP_2", z="Scores",
                            color='Scores',
                            color_discrete_sequence=px.colors.qualitative.Plotly,
                            range_color=parameters["scorelim"]
                            )
        fig.update_traces(marker_size=1)

        fig.update_layout(
            scene=dict(
                xaxis={} if parameters["xlim"] is None else dict(nticks=6, range=xlim),
                yaxis={} if parameters["ylim"] is None else dict(nticks=6, range=ylim),
                zaxis={} if parameters["scorelim"] is None else dict(nticks=6, range=scorelim)),
            width=700,
            margin=dict(r=20, l=10, b=10, t=10))
        if settings["view"] is True:
            fig.show()
        fig.write_image(settings["path"])
        plt.close("all")






