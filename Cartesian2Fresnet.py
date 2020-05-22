
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import os

class Fresnet:
    global spline_ob
    start_x_ = 0.0
    end_x_ = 0.0
    current_s = 0.0
    
    def plot_initial_data(self,df):
        plt.scatter(df['x'],df['y'])
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()
    
    def plot_interpolation(self,df,frenet):
        xnew = np.linspace(0, 41, num=41, endpoint=True)
        plt.plot(df['x'], df['y'], 'o', xnew, spline_ob(xnew), '--', frenet['d'], frenet['s'],'o')
        plt.legend(['data', 'interpolation','fresnet_point'], loc='best')
        plt.show()
    
    def calculate_euclidean_distance(self,x1, x2, y1, y2):
        return np.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

    def calculate_sign(self,x1, x2, y1, y2):
        check_sum = (x2-x1) + (y2-y1)
        if check_sum < 0:
            return -1.0
        else:
            return 1.0    

    def reference_spline(self,df):
        return interp1d(df['x'], df['y'], kind='cubic',fill_value="extrapolate")

    def calculate_boundaries(self,spline_start_x_value, spline_end_x_value):
        self.start_x_ = spline_start_x_value
        self.end_x_ = spline_end_x_value
        
    def cartesian2frenet(self,coordinate_x, coordinate_y, precision= 0.001):
        current_s = 0
        if (self.end_x_ - self.start_x_) > 0.0:
            current_x = self.start_x_
        else:
            current_x = self.end_x_
        while (current_x < (self.end_x_ - self.start_x_) > 0.0 if self.end_x_ else self.start_x_):
            distance = self.calculate_euclidean_distance(current_x, coordinate_x, spline_ob(current_x), coordinate_y)
            frenet_coordinates = {'d':10000,'s':10000}
            if (distance <= frenet_coordinates['d']):
                frenet_coordinates['d'] = distance
                frenet_coordinates['s'] = current_s - precision

            current_s += self.calculate_euclidean_distance(
                current_x, (current_x - precision), spline_ob(current_x), spline_ob(current_x - precision))
            current_x += precision


        frenet_coordinates['d'] *= self.calculate_sign(current_x, coordinate_x, spline_ob(current_x), coordinate_y)

        return frenet_coordinates




dictpat = r'\{((?:\s*\w+\s*:\s*\D+\w+.\d+\s*)+)\}' 
itempat = r'(\s*(\w+)\s*:\s*(\D+\w+.\d+)\s*)'      

with open('reference_points.pb.txt') as f:
    lod = [{group[1]:group[2] for group in re.findall(itempat, items)}
                                for items in re.findall(dictpat, f.read())]


df = pd.DataFrame(lod)
df = df.apply(pd.to_numeric)

fr = Fresnet()
spline_ob = fr.reference_spline(df)
fr.calculate_boundaries(spline_ob.x[0],spline_ob.x[spline_ob.x.size-1])

x = os.environ['X']
y = os.environ['Y']

frenet = fr.cartesian2frenet(float(x),float(y))
print(frenet)
