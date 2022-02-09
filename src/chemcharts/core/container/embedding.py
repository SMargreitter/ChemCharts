import numpy as np
from copy import deepcopy


class Embedding:
    """The Embedding contains dimensionally reduced fingerprints in np-array format."""

    def __init__(self, np_array: np.ndarray = None):
        self.np_array = np.empty((0, 2), float) if np_array is None else np_array

    def __repr__(self) -> str:
        return f"Embedding: {self.np_array}"

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return self.np_array.size

    def __getitem__(self, item):
        if isinstance(item, (int, slice)):
            return self.np_array[item]
        return [self.np_array[i] for i in item]

    def __setitem__(self, obj, idx: int):
        self.np_array[idx] = obj

    def __add__(self, obj):
        copy_self = deepcopy(self)
        obj = deepcopy(obj)
        copy_self.np_array = np.concatenate((copy_self.np_array, obj.np_array))
        return copy_self
