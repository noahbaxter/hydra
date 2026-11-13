import os
import unittest
import json

import hydra.hyutil as hyutil
import hydra.hydata as hydata
import hydra.hysong as hysong
import hydra.hypath as hypath

class TestUpperbound(unittest.TestCase):
    """Test cases for songs where the optimal path is only visible with a >140
        upper bound. By default a squeeze is allowed when it fits the activation
        note's and the squeezed note's half windows (up to ~171 ms), so some
        of these are found without a custom bound.
    """
    def setUp(self):
        self.chartfolder = os.sep.join(["..","test","input","test_upperbound"])
    
    def _test_optimals(self, filename, upperbound, expected_score, expected_ms, fits_hit_windows=False):
        input_file = self.chartfolder + os.sep + filename
        default_record = hyutil.analyze_chart_file(input_file, 'Expert', True, True, 'scores', 0, None, None)
        upperbound_record = hyutil.analyze_chart_file(input_file, 'Expert', True, True, 'scores', 0, None, upperbound)
        
        if fits_hit_windows:
            self.assertEqual(default_record.best_path().totalscore(), upperbound_record.best_path().totalscore())
        else:
            self.assertLess(default_record.best_path().totalscore(), upperbound_record.best_path().totalscore())
        self.assertEqual(upperbound_record.best_path().totalscore(), expected_score)
        self.assertAlmostEqual(upperbound_record.best_path().difficulty(), expected_ms, places=2)        

    def test_dumpweed(self):
        self._test_optimals('dumpweed.mid', 190, 422940, 143.129, fits_hit_windows=True)

    def test_maladapted(self):
        self._test_optimals('maladapted.mid', 190, 444435, 184.048)

    def test_burnout(self):
        self._test_optimals('burnout.mid', 190, 378315, 163.043, fits_hit_windows=True)

    def test_poyw(self):
        self._test_optimals('poyw.mid', 190, 312590, 178.571)

