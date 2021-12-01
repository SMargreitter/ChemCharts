import unittest

from chemcharts.core.plots.base_plot import BasePlot


class TestBasePlot(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass

    def test_path_update_snapshot(self):
        test_base_plot = BasePlot()
        test_updated_path = test_base_plot._path_update_snapshot(
            ori_path="../junk/base_plot_test/path_update.png", epoch_id=2)
        self.assertEqual(
            "/home/nutzer/Documents/Projects/ChemCharts/tests/junk/base_plot_test/0002_path_update.png",
            test_updated_path)

        test_updated_path = test_base_plot._path_update_snapshot(
            ori_path="../junk/base_plot_test/path_update", epoch_id=6)
        self.assertEqual(
            "/home/nutzer/Documents/Projects/ChemCharts/tests/junk/base_plot_test/0006_path_update.png",
            test_updated_path)

        test_updated_path = test_base_plot._path_update_snapshot(
            ori_path="../junk/base_plot_test/path_update.jpeg", epoch_id=12)
        self.assertEqual(
            "/home/nutzer/Documents/Projects/ChemCharts/tests/junk/base_plot_test/0012_path_update.png",
            test_updated_path)
