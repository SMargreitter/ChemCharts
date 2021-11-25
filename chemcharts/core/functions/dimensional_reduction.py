from copy import deepcopy

import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    import umap
import numpy as np

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.container.embedding import Embedding


class DimensionalReduction:
    """
    Reduces fingerprints with UMAP function.
    """

    def __init__(self):
        pass

    @staticmethod
    def _generating_array_list(chemdata: ChemData) -> list:
        """
        Generates an array list.

        Parameters
        ----------
        chemdata : ChemData
            object of ChemData class
        second :
            the 2nd param
        third : {'value', 'other'}, optional
            the 3rd param, by default 'value'

        Returns
        -------
        list
            an array list
        """

        array_list = []
        for fingerprint in chemdata.fingerprints:
            array = np.array(list(fingerprint))
            array_list.append(array)
        return array_list

    def _dimensional_reduction(self, chemdata: ChemData) -> Embedding:
        array_list = self._generating_array_list(chemdata)
        reducer = umap.UMAP(random_state=42)

        # fix random seed to enhance reproducibility of embedding
        embedding = Embedding(reducer.fit_transform(array_list))
        return embedding

    def calculate(self, chemdata: ChemData) -> ChemData:
        chemdata = deepcopy(chemdata)
        embedding = self._dimensional_reduction(chemdata)
        chemdata.set_embedding(embedding)
        return chemdata
