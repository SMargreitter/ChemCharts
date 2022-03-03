import statistics

import pandas as pd
from sklearn.cluster import KMeans
from copy import deepcopy

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.container.embedding import Embedding


class Clustering:
    """
        Clusters Embeddings with KMeans.

        Method
        ----------
        clustering <chemdata: ChemData, k: int>
            returns a ChemData object containing a clustered Embedding object
    """

    def __init__(self):
        pass

    @staticmethod
    def clustering(chemdata: ChemData, k: int) -> ChemData:
        """
            The clustering function accesses an Embedding of a given ChemData and clusters it with KMeans.

            Parameters
            ----------
            chemdata: ChemData
                object of ChemData
            k: int
                the number of desired KMeans clusters

            Returns
            -------
            ChemData
                returns a ChemData object containing a clustered Embedding object
        """

        chemdata = deepcopy(chemdata)
        assert len(chemdata.get_embedding()) >= k

        kmeans = KMeans(n_clusters=k, random_state=0).fit(chemdata.get_embedding().np_array)
        assert kmeans.cluster_centers_.shape[1] == 2

        def generate_value_df(value_df: pd.DataFrame) -> pd.DataFrame:
            # preparation
            number_clusters = len(kmeans.cluster_centers_)
            number_cluster_rows = len(kmeans.labels_)
            column_names = list(value_df.columns)

            # initialization of df
            clustered_value_df = pd.DataFrame(index=range(number_clusters),
                                              columns=column_names)

            # filling of df
            # TODO replace by pandas "group by"
            for cluster_idx in range(number_clusters):
                current_cluster_indices = []
                for label_idx in range(number_cluster_rows):
                    if kmeans.labels_[label_idx] == cluster_idx:
                        current_cluster_indices.append(label_idx)

                for column in column_names:
                    cluster_values = list(value_df[column].iloc[current_cluster_indices])
                    cluster_values = [float(x) for x in cluster_values]
                    median_value = statistics.median(cluster_values)
                    clustered_value_df.at[cluster_idx, column] = median_value

            return clustered_value_df

        chemdata.set_values(generate_value_df(chemdata.get_values()))
        chemdata.set_embedding(Embedding(kmeans.cluster_centers_))

        return chemdata
