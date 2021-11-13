import umap
import numpy as np
from chemcharts.core.container.embedding import Embedding


def generating_array_list(fingerprint_obj):
    # generating array list of fingerprint_lists
    array_list = []
    for fingerprint in fingerprint_obj:
        array = np.array(fingerprint)
        array_list.append(array)
    return array_list


def dimensional_reduction(fingerprint_obj):
    np.random.seed(42)

    array_list = generating_array_list(fingerprint_obj)

    reducer = umap.UMAP()
    embedding = Embedding(reducer.fit_transform(array_list))

    return embedding


def calculate_embedding(data_set_obj):
    for fingerprint_obj in data_set_obj.fingerprint_lists:
        array_list = generating_array_list(fingerprint_obj)
        embedding = dimensional_reduction(array_list)
        data_set_obj.add_embedding_list(embedding)
