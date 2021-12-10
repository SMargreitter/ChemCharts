import statistics

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

        def generate_score_list(scores):
            score_list = []
            for cluster_idx in range(len(kmeans.cluster_centers_)):
                tmp = []
                for label_idx in range(len(kmeans.labels_)):
                    if kmeans.labels_[label_idx] == cluster_idx:
                        tmp.append(scores[label_idx])
                score_list.append(statistics.median(tmp))
            return score_list

        chemdata.set_scores(generate_score_list(chemdata.get_scores()))
        chemdata.set_embedding(Embedding(kmeans.cluster_centers_))
        return chemdata
