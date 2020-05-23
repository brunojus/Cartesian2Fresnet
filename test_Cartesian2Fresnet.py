import Cartesian2Fresnet
import unittest

import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import os

class TestFresnet(unittest.TestCase):

    def setUp(self):
        dictpat = r'\{((?:\s*\w+\s*:\s*\D+\w+.\d+\s*)+)\}' 
        itempat = r'(\s*(\w+)\s*:\s*(\D+\w+.\d+)\s*)'      

        with open('reference_points.pb.txt') as f:
            lod = [{group[1]:group[2] for group in re.findall(itempat, items)}
                                        for items in re.findall(dictpat, f.read())]
        self.df = pd.DataFrame(lod)
        self.df = self.df.apply(pd.to_numeric)

    def test_reference_spline(self):
        spline = Cartesian2Fresnet.fr.reference_spline(self.df)
        expected_y_value = 0.119615256786
        self.assertEqual(spline.y[0],expected_y_value)


        
    def test_current_s(self):
        """
        Test the current point
        """
        result = Cartesian2Fresnet.fr.current_s
        self.assertEqual(result, 0.0)

if __name__ == '__main__':

    unittest.main()