import unittest

import numpy as np

from chemcharts.core.container.embedding import Embedding


class TestEmbedding(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.array = np.array([[1, 2],
                              [2, 2],
                              [4, 2],
                              [2, 3],
                              [2.6, 5],
                              [11.2, 2],
                              [5, 1.2],
                              [4, 5]])

    def setUp(self) -> None:
        pass

    def test_embedding(self):
        test_embedding = Embedding(self.array)
        test_array = np.array(test_embedding)
        self.assertListEqual([1, 2], [int(x) for x in list(test_embedding[0])])
        self.assertIsInstance(test_embedding, Embedding)
        self.assertEqual(test_array.size, 16)

    def test_get_len(self):
        test_embedding = Embedding(self.array)
        length = len(test_embedding)
        self.assertEqual(length, 16)

    def test_set_item(self):
        test_array = Embedding(self.array)
        test_array[8, 1] = 1   # test_array.__setitem__([8, 1], 1)
        self.assertListEqual(list([8, 1]), list(test_array[1]))

    def test_add_item(self):
        test_embedding = Embedding(self.array)
        array_to_add = np.array([[2, 2],
                                 [3, 3],
                                 [2, 2],
                                 [4, 4],
                                 [5, 5],
                                 [11, 11],
                                 [7, 7],
                                 [1, 1]])
        test = test_embedding + Embedding(array_to_add)
        self.assertIn([1, 1], test.np_array)
