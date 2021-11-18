import numpy as np


class Embedding:
    """ Transforms MolSmiles to fingerprints by using the RDKit fingerprints (standard, Morgan and
            MACCS) and then adds them to the fingerprint_list of an object of the FingerprintContainer class.
        input:
               list of MolSmiles -- every smile encodes one molecule, the characters represent chemical
               elements
        output:
               object of the FingerprintContainerClass -- fingerprints are represented as bit vectors (lists
               with 0 and 1 or numbers) and are added to the fingerprint_list
        """

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
