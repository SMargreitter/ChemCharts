from copy import deepcopy
import numpy as np
import pandas as pd
import statistics

from chemcharts.core.container.chemdata import ChemData


class Binning:
    """
        The Binning contains a ChemData with binned median scores.

        Method
        ----------
        binning <chemdata: ChemData, num_bins: int>
            returns a ChemData object with binned median scores
    """

    def __init__(self):
        pass
    """"
    @staticmethod
    def _preparation(scores: list, num_bins: int) -> tuple:
        # return number spaces evenly w.r.t interval
        bins = list(np.linspace(start=min(scores) - 0.1, stop=max(scores) + 0.1, num=num_bins))

        # get the indices of the bins to which each value belongs
        bin_idx = list(np.digitize(scores, bins=bins) - 1)

        sorted_bin_idx = list(set(bin_idx))
        sorted_bin_idx.sort()

        return sorted_bin_idx, bin_idx

    @staticmethod
    def _group_scores_bins(scores: list, sorted_bin_idx: list, bin_idx: list) -> list:
        grouped_scores_bins = []
        for item in sorted_bin_idx:
            scores_bin = []
            for idx in range(len(bin_idx)):
                if item == bin_idx[idx]:
                    scores_bin.append(scores[idx])
            grouped_scores_bins.append(scores_bin)
        return grouped_scores_bins

    @staticmethod
    def _calculate_medians(grouped_scores_bins: list) -> list:
        median_scores = []
        for item in grouped_scores_bins:
            if not item:
                median_scores.append(None)
                continue
            median_score = statistics.median(item)
            median_scores.append(median_score)
        return median_scores

    @staticmethod
    def _overwrite_scores_medians(bin_idx: list, median_scores: list) -> list:
        new_scores = []
        for i_bin in range(len(bin_idx)):

            # get current bin index for observation i_bin
            cur_bin_idx = bin_idx[i_bin]

            # append median for current bin index
            if cur_bin_idx < len(median_scores):
                new_scores.append(median_scores[cur_bin_idx])
            else:
                continue

        return new_scores

    def binning(self, chemdata: ChemData, num_bins: int) -> ChemData:
        '''
            The binning function accesses scores of a given Chemdata, calculates the binned scores and then
             returns their median.

            Parameters
            ----------
            chemdata: ChemData
                object of ChemData
            num_bins: int
                the number of desired bins

            Returns
            -------
            ChemData
                an object of ChemData with binned median scores
        '''

        chemdata = deepcopy(chemdata)
        scores = list(chemdata.get_scores())
        sorted_bin_idx, bin_idx = self._preparation(scores, num_bins)
        grouped_scores_bins = self._group_scores_bins(scores, sorted_bin_idx, bin_idx)
        median_scores = self._calculate_medians(grouped_scores_bins)
        new_scores = self._overwrite_scores_medians(bin_idx, median_scores)

        chemdata.set_scores(new_scores)
        """

    @staticmethod
    def _preparation(values: list, num_bins: int) -> tuple:
        # return number spaces evenly w.r.t interval
        bins = list(np.linspace(start=min(values) - 0.1, stop=max(values) + 0.1, num=num_bins))

        # get the indices of the bins to which each value belongs
        bin_idx = list(np.digitize(values, bins=bins) - 1)

        sorted_bin_idx = list(set(bin_idx))
        sorted_bin_idx.sort()

        return sorted_bin_idx, bin_idx

    @staticmethod
    def _group_values_bins(values: list, sorted_bin_idx: list, bin_idx: list) -> list:
        grouped_values_bins = []
        for item in sorted_bin_idx:
            values_bin = []
            for idx in range(len(bin_idx)):
                if item == bin_idx[idx]:
                    values_bin.append(values[idx])
            grouped_values_bins.append(values_bin)
        return grouped_values_bins

    @staticmethod
    def _calculate_medians(grouped_value_bins: list) -> list:
        median_values = []
        for item in grouped_value_bins:
            if not item:
                median_values.append(None)
                continue
            median_value = statistics.median(item)
            median_values.append(median_value)
        return median_values

    @staticmethod
    def _overwrite_value_medians(bin_idx: list, median_values: list, sorted_bin_idx: list) -> list:
        new_values = []
        for i_bin in range(len(bin_idx)):

            # get current bin index for observation i_bin
            cur_bin_idx = bin_idx[i_bin]

            # get current position in sorted_bin_idx
            median_idx = sorted_bin_idx.index(cur_bin_idx)

            # append median for current bin index
            if median_idx < len(median_values):
                new_values.append(median_values[median_idx])
            else:
                raise ValueError("Median index out of range, list length would not be equal to input.")

        return new_values

    def binning(self, chemdata: ChemData, num_bins: int) -> ChemData:
        """
            The binning function accesses values of a given Chemdata, calculates the binned values and then
             returns their median.

            Parameters
            ----------
            chemdata: ChemData
                object of ChemData
            num_bins: int
                the number of desired bins

            Returns
            -------
            ChemData
                an object of ChemData with binned median values
        """

        chemdata = deepcopy(chemdata)

        # preparation
        value_df = chemdata.get_values()
        column_names = list(value_df.columns)

        # initialization of df
        binned_value_df = pd.DataFrame(index=range(len(value_df)),
                                       columns=column_names)

        for column in column_names:
            list_of_values = value_df[column].to_list()   #597  # bins: 10
            sorted_bin_idx, bin_idx = self._preparation(list_of_values, num_bins) # 5 # 597
            grouped_value_bins = self._group_values_bins(list_of_values, sorted_bin_idx, bin_idx) #5
            median_values = self._calculate_medians(grouped_value_bins) #5
            new_values = self._overwrite_value_medians(bin_idx, median_values, sorted_bin_idx) #565
            binned_value_df.loc[:, column] = new_values  #565

        chemdata.set_values(binned_value_df)

        return chemdata
