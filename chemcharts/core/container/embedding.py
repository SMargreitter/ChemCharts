import numpy as np


class Embedding:
    def __init__(self, np_array: np.ndarray):
        self.np_array = np_array

    def __len__(self):
        return self.np_array.size

    def __repr__(self) -> str:
        return f"Embeddings: {self.np_array}"

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, item):
        if isinstance(item, (int, slice)):
            return self.np_array[item]
        return [self.np_array[i] for i in item]

    #def __setitem__(self, item, np_array):
    #    if isinstance(item, int):
    #        self.np_array[item] = np_array
    #    elif isinstance(item, slice):
    #        raise ValueError('Cannot interpret slice with multiindexing')
    #    else:
    #        for i in item:
    #            if isinstance(i, slice):
    #                raise ValueError('Cannot interpret slice with multiindexing')
    #            self.np_array[i] = np_array

    #def __delitem__(self, item):
    #    if isinstance(item, int):
    #        del self.np_array[item]
    #    elif isinstance(item, slice):
    #        del self.np_array[item]
    #    else:
    #        if any(isinstance(elem, slice) for elem in item):
    #            raise ValueError('Cannot interpret slice with multiindexing')
    #        item = sorted(item, reverse=True)
    #        for elem in item:
    #            del self.np_array[elem]
