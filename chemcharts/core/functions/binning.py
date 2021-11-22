from copy import deepcopy
from rdkit import DataStructs
import numpy as np
import statistics

from chemcharts.core.container.chemdata import ChemData


class Binning:
    def __init__(self):
        pass

    @staticmethod
    def _preparation(scores, num_bins):
        bins = list(np.linspace(start=min(scores) - 0.1, stop=max(scores) + 0.1, num=num_bins))
        bin_idx = list(np.digitize(scores, bins=bins) - 1)
        sorted_bin_idx = list(set(bin_idx))
        sorted_bin_idx.sort()
        return sorted_bin_idx, bin_idx

    @staticmethod
    def _group_scores_bins(scores, sorted_bin_idx, bin_idx):
        buffer = []
        for item in sorted_bin_idx:
            me = []
            for idx in range(len(bin_idx)):
                if item == bin_idx[idx]:
                    me.append(scores[idx])
            buffer.append(me)
        return buffer

    @staticmethod
    def _calculate_medians(buffer):
        median_list = []
        for item in buffer:
            if not item:
                median_list.append(None)
                continue
            median_scores = statistics.median(item)
            median_list.append(median_scores)
        return median_list

    @staticmethod
    def _overwrite_scores_medians(bin_idx, median_list):
        new_scores = []
        for i_bin in range(len(bin_idx)):
            # get current bin index for observation i_bin
            cur_bin_idx = bin_idx[i_bin]

            # append median for current bin index
            new_scores.append(median_list[cur_bin_idx])
        return new_scores

    def binning(self, chemdata: ChemData, num_bins: int) -> ChemData:
        chemdata = deepcopy(chemdata)
        scores = list(chemdata.get_scores())
        sorted_bin_idx, bin_idx = self._preparation(scores, num_bins)
        buffer = self._group_scores_bins(scores, sorted_bin_idx, bin_idx)
        median_list = self._calculate_medians(buffer)
        new_scores = self._overwrite_scores_medians(bin_idx, median_list)

        chemdata.set_scores(new_scores)

        return chemdata
