from unittest import TestCase
import pandas as pd
import os


class Test_IHA(TestCase):

    @staticmethod
    def read(file):
        path = os.path.abspath(os.path.join('test_data', file))
        data = pd.read_csv(path, ';')
        return data

    def test_mean_month(self):
        data = self.read('Group1.csv')
        print(data)

    def test_moving_averages(self):
        data = self.read('Group2.csv')
        print(data)

    def test_year_water(self):
        pass

    def test_days_julian(self):
        data = self.read('Group3.csv')
        print(data)

    def test_pulse(self):
        data = self.read('Group4.csv')
        print(data)

    def test_rise_fall(self):
        data = self.read('Group5.csv')
        print(data)
