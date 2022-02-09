import warnings
from typing import List

with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    import umap
import numpy as np

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.container.embedding import Embedding
from chemcharts.core.container.fingerprint import *


class DimensionalReduction:
    """
        Reduces fingerprints with UMAP function.

        Method
        ----------
        calculate <chemdata_list: List[ChemData])>
            returns a chemdata_list containing ChemData objects containing an Embedding (clustered
             fingerprints) which is based on observations from all ChemData objects in the list
    """

    def __init__(self):
        pass

    @staticmethod
    def _generating_array_list(fingerprints: FingerprintContainer) -> list:
        array_list = []
        for fingerprint in fingerprints:
            array = np.array(list(fingerprint))
            array_list.append(array)
        return array_list

    def _dimensional_reduction(self, fingerprints: FingerprintContainer) -> Embedding:
        array_list = self._generating_array_list(fingerprints)
        reducer = umap.UMAP(random_state=42)

        # fix random seed to enhance reproducibility of embedding
        embedding = Embedding(reducer.fit_transform(array_list))
        return embedding

    def calculate(self, chemdata_list: List[ChemData]) -> List[ChemData]:
        """
            The calculate function accesses ChemData objects in a list and then reduces their fingerprints
            (based on observations from all ChemData objects in the list) with UMAP and then adds the
            clustered fingerprints as Embedding to the ChemData in the list.

            Parameters
            ----------
            chemdata_list: List[ChemData]
                List of ChemData objects

            Returns
            -------
            List[ChemData]
                returns a list of ChemData objects with Embeddings (clustered fingerprints) based on all
                observations from all ChemData objects
        """

        # combine all fingerprints of all ChemData object for the embedding stage,
        # because all observations influence the dimensional reduction
        fps_buffer = FingerprintContainer()
        for chemdata in chemdata_list:
            fps_buffer += chemdata.get_fingerprints()

        # embeddings for all fingerprints
        embedding = self._dimensional_reduction(fps_buffer)

        # add embeddings to respective ChemCharts objects
        last_index = 0
        for chemdata in chemdata_list:
            # generate a sliced Embedding based on the chemdata's fingerprint length
            len_fps = len(chemdata.get_fingerprints())
            end_index = last_index + len_fps
            np_buffer = embedding.np_array[last_index:end_index]
            slice_embedding = Embedding(np_buffer)

            # update chemdata and set index for next iteration
            chemdata.set_embedding(slice_embedding)

            # update last_index
            last_index = end_index

        return chemdata_list
