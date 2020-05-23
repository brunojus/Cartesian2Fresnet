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

    def test_cartesian2frenet(self):

        points = Cartesian2Fresnet.fr.cartesian2frenet(20.0,2)
        
        self.assertGreaterEqual(points['d'],-23.0)
        self.assertGreaterEqual(points['s'],41.0)

    def test_calculate_boundaries(self):

        boudaries = Cartesian2Fresnet.fr.calculate_boundaries(0.0,41.9993400574)
        self.assertEqual(boudaries[0],0.0)
        self.assertEqual(boudaries[1],41.9993400574)
    
    def test_calculate_euclidean_distance(self):
        distance = Cartesian2Fresnet.fr.calculate_euclidean_distance(0.0,1.0,2.0,0.0)
        self.assertGreaterEqual(distance,2)

    def test_calculate_sign(self):
        sign = Cartesian2Fresnet.fr.calculate_sign(41.999999999992816, 20.0, -0.10119433914335003, 2.0)
        self.assertEqual(sign,-1.0)




if __name__ == '__main__':

    unittest.main()