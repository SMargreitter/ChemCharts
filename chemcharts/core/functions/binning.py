from copy import deepcopy
from rdkit import DataStructs
import numpy as np

from chemcharts.core.container.chemdata import ChemData


class Binning:
    def __init__(self):
        pass

    @staticmethod
    def binning(chemdata: ChemData) -> ChemData:
        chemdata = deepcopy(chemdata)
        np.linspace(start=-2.1, stop=8.0, num=3)
        np.digitize([1.333, 2.33, -1, -2, -1.3, 7.9], bins=[-2.1, 2.95, 8.]) - 1

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