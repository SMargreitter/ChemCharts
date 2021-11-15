import pandas as pd
import plotly.express as px
from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.plots.base_plot import BasePlot


class ScatterInteractivePlot(BasePlot):
    def __init__(self):
        super().__init__()

    @staticmethod
    def plot(chemdata: ChemData, path: str):
        scatter_df = pd.DataFrame({"UMAP_1": chemdata.get_embedding().np_array[:, 0],
                                   "UMAP_2": chemdata.get_embedding().np_array[:, 1],
                                   "Scores": chemdata.get_scores()
                                   })
        fig = px.scatter_3d(scatter_df,
                            x="UMAP_1", y="UMAP_2", z="Scores",
                            color='Scores',
                            color_discrete_sequence=px.colors.qualitative.Plotly
                            )
        fig.update_traces(marker_size=1)
        fig.show()
        fig.write_image(path)






