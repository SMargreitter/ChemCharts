from typing import Tuple

import pandas as pd

from copy import deepcopy

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.container.embedding import Embedding


class Filtering:
    def __init__(self):
        pass

    def filter_range(self, chemdata: ChemData, range_dim1: Tuple[float, float], range_dim2: Tuple[float, float]) -> ChemData:
        chemdata = deepcopy(chemdata)
        embedding_df = pd.DataFrame(
            {"UMAP_1": chemdata.get_embedding().np_array[:, 0],
             "UMAP_2": chemdata.get_embedding().np_array[:, 1],
             "Scores": chemdata.get_scores()})

        df = embedding_df[embedding_df['UMAP_1'].between(range_dim1[0], range_dim1[1])]
        df = df[df['UMAP_2'].between(range_dim2[0], range_dim2[1])]
        chemdata.set_scores(list(df["Scores"]))

        df.drop("Scores", axis=1, inplace=True)
        chemdata.set_embedding(Embedding(df.to_numpy()))

        return chemdata
