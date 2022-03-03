from typing import Tuple

import pandas as pd

from copy import deepcopy

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.container.embedding import Embedding

from chemcharts.core.utils.enums import PlotLabellingEnum
_PLE = PlotLabellingEnum


class Filtering:
    """
        Filters the Embedding and scores according to a user defined range.

        Method
        ----------
        filter_range<chemdata: ChemData, range_dim1: Tuple[float, float], range_dim2: Tuple[float, float]>
            returns a ChemData object containing a filtered Embedding object and filtered scores
    """

    def __init__(self):
        pass

    def filter_range(self, chemdata: ChemData, range_dim1: Tuple[float, float], range_dim2: Tuple[float, float]) \
            -> ChemData:
        """
            The filter_range function filters the Embedding of a given ChemData according to a user
            defined range.

            Parameters
            ----------
            chemdata: ChemData
                object of ChemData
            range_dim1: Tuple[float, float]
                setting the filter range for values on x axis
            range_dim2: Tuple[float, float]
                setting the filter range for values on y axis

            Returns
            -------
            ChemData
                returns a ChemData object containing a filtered Embedding object and
                filtered scores
        """

        chemdata = deepcopy(chemdata)

        embedding_df = pd.DataFrame(
            {_PLE.UMAP_1: chemdata.get_embedding().np_array[:, 0],
             _PLE.UMAP_2: chemdata.get_embedding().np_array[:, 1]})

        value_names = list(chemdata.get_values().columns)
        embedding_df = pd.concat([embedding_df, chemdata.get_values()])

        df = embedding_df[embedding_df[_PLE.UMAP_1].between(range_dim1[0], range_dim1[1])]
        df = df[df[_PLE.UMAP_2].between(range_dim2[0], range_dim2[1])]

        # set scores in chemdata
        chemdata.set_values(pd.DataFrame(df[value_names]))

        # delete scores from dataframe
        df.drop(value_names, axis=1, inplace=True)

        chemdata.set_embedding(Embedding(df.to_numpy()))

        return chemdata
