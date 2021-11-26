import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.plots.base_plot import BasePlot


class ScatterDensityPlot(BasePlot):
    def __init__(self):
        super().__init__()

    @staticmethod
    #def plot(chemdata: ChemData, path: str, selection: str = "scores"):
    def plot(chemdata: ChemData, path: str, xlim: tuple = None, ylim: tuple = None, scorelim: tuple = None,
             selection: str = "scores"):
        if selection == "tanimoto_similarity":
            scores_input = chemdata.get_tanimoto_similarity()
            score_name = "Tanimoto Similarity"
        elif selection == "scores":
            scores_input = chemdata.get_scores()
            score_name = "Scores"
        else:
            raise ValueError(f"Selection input: {selection} is not as expected.")

        scatter_df = pd.DataFrame({"UMAP_1": chemdata.get_embedding().np_array[:, 0],
                                  "UMAP_2": chemdata.get_embedding().np_array[:, 1],
                                   score_name: scores_input})

        sns.set_context("talk", font_scale=0.5)
        plt.figure(figsize=(17, 17))
        sns.displot(scatter_df, x=score_name, kind="kde")

       # plt.xlim(xlim)
       # plt.ylim(ylim)

        plt.subplots_adjust(top=0.9)
        plt.suptitle('Scatter Density ChemCharts Plot', fontsize=14)

        plt.savefig(path, format='png', dpi=150)
        plt.close("all")



