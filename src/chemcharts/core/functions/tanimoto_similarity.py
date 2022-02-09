from copy import deepcopy
from rdkit import DataStructs
import numpy as np

from chemcharts.core.container.chemdata import ChemData


class TanimotoSimilarity:
    ########################################################
    # TODO:
                   # not (yet) integrated!!!!

    ########################################################

    """
        Simplifies the scores with RDKit's BulkTanimotoSimilarity() function.

        Method
        ----------
        simplify <chemdata: ChemData>
            returns a ChemData object containing simplified scores
    """

    def __init__(self):
        pass

    @staticmethod
    def simplify(chemdata: ChemData) -> ChemData:
        """
            The simplify function simplifies the scores a given ChemData with RDKit's
            BulkTanimotoSimilarity() function.

            Parameters
            ----------
            chemdata: ChemData
                object of ChemData

            Returns
            -------
            ChemData
                returns a ChemData object containing simplified scores
        """

        chemdata = deepcopy(chemdata)
        fps_list = chemdata.get_fingerprints()
        tan_sim_list = []
        length_fps_list = len(fps_list)
        for index in range(length_fps_list-1):
                tan_sim = DataStructs.BulkTanimotoSimilarity(fps_list[index], fps_list[index + 1:])
                tan_sim_list.append(tan_sim)

        def fill_list_with_NaNs(tan_sim_list, length_fps_list):
            reversed_list = []
            for fp in tan_sim_list:
                fp.reverse()
                reversed_list.append(fp)
            for idx in range(length_fps_list):
                for fp in reversed_list:
                    if len(fp) < length_fps_list:
                        # add nans to match length of fps in fps_list
                        fp.append(np.NaN)
            final_list = []
            for fp in reversed_list:
                fp.reverse()
                final_list.append(fp)
            # add a list of nans to match length of fps_list
            final_list.append([np.NaN] * length_fps_list)
            score_array = np.array(final_list)
            return score_array

        chemdata.set_tanimoto_similarity(fill_list_with_NaNs(tan_sim_list, length_fps_list))

        return chemdata
