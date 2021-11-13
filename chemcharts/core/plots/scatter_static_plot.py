import matplotlib.pyplot as plt

from chemcharts.core.container.chemdata import ChemData


class ScatterStaticPlot:
    def __init__(self):
        pass

    @staticmethod
    def plot(chemdata: ChemData, path: str):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        plt.gcf().set_size_inches((15, 15))

        ax.scatter(chemdata.get_embedding().np_array[:, 0],
                   chemdata.get_embedding().np_array[:, 1],
                   zs=chemdata.get_scores(),
                   s=1)

        ax.set_title("Scatter Static ChemCharts Plot")
        ax.set_xlabel('UMAP 1')
        ax.set_ylabel('UMAP 2')
        ax.set_zlabel('Scores')

        plt.savefig(path)
