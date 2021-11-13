import statistics

from sklearn.cluster import KMeans
from copy import deepcopy

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.container.embedding import Embedding


class Clustering:
    def __init__(self):
        pass

    @staticmethod
    def clustering(chemdata: ChemData, k: int) -> ChemData:
        chemdata = deepcopy(chemdata)
        assert len(chemdata.get_embedding()) >= k

        kmeans = KMeans(n_clusters=k, random_state=0).fit(chemdata.get_embedding().np_array)
        assert kmeans.cluster_centers_.shape[1] == 2
        chemdata.set_embedding(Embedding(kmeans.cluster_centers_))

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

        return chemdata
