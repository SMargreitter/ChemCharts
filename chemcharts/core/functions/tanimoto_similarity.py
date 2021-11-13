from copy import deepcopy
from rdkit import DataStructs
import numpy as np

from chemcharts.core.container.chemdata import ChemData


class TanimotoSimilarity:
    def __init__(self):
        pass

    @staticmethod
    def simplify(chemdata: ChemData) -> ChemData:
        chemdata = deepcopy(chemdata)
        fps_list = chemdata.get_fingerprints()

        tan_sim_list = []
        length_fps_list = len(fps_list)
        for index in range(length_fps_list-1):
                tan_sim = DataStructs.BulkTanimotoSimilarity(fps_list[index], fps_list[index + 1:])
                tan_sim_list.append(tan_sim)

        def fill_list_with_Nones(tan_sim_list, length_fps_list):
            reversed_list = []
            for fp in tan_sim_list:
                fp.reverse()
                reversed_list.append(fp)
            for idx in range(length_fps_list):
                for fp in reversed_list:
                    if len(fp) < length_fps_list:
                        fp.append(np.NaN)
            final_list = []
            for fp in reversed_list:
                fp.reverse()
                final_list.append(fp)
            final_list.append([np.NaN] * length_fps_list)
            score_array = np.array(final_list)
            return score_array

        chemdata.set_tanimoto_similarity(fill_list_with_Nones(tan_sim_list, length_fps_list))

        return chemdata
