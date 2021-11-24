import numpy as np


class Embedding:
    """The Embedding class contains dimensionally reduced fingerprints in np-array format."""

    def __init__(self, np_array: np.ndarray):
        self.np_array = np_array

    def __len__(self):
        return self.np_array.size

    def __repr__(self) -> str:
        return f"Embedding: {self.np_array}"

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, item):
        if isinstance(item, (int, slice)):
            return self.np_array[item]
        return [self.np_array[i] for i in item]
