from unittest import TestCase
import pandas as pd
import os
from old_iha_stats import Caracteristicas


class Test_IHA(TestCase):

    @staticmethod
    def read():
        path = os.path.abspath(os.path.join('test_data', 'dadosXingo_nat.csv'))
        data = pd.read_csv(path, ',', index_col=0, names=["Data", "XINGO"], parse_dates=True)
        crt = Caracteristicas(data, nPosto='XINGO')
        return crt

    @staticmethod
    def read_iha(file):
        path = os.path.abspath(os.path.join('test_data', file))
        data = pd.read_csv(path, ';')
        return data

    def test_mean_month(self):
        data = self.read_iha('Group1.csv')
        data2 = self.read().mean_month()

        print(data2)

    def test_moving_averages(self):
        data = self.read_iha('Group2.csv')

    def test_year_water(self):
        year_water = self.read().mesInicioAnoHidrologico()

        self.assertEqual((9, 'SEP'), year_water, 'Year Water: %s, %s' % (9, 'SEP'))

    def test_days_julian(self):
        data = self.read_iha('Group3.csv')

    def test_pulse(self):
        data = self.read_iha('Group4.csv')

    def test_rise_fall(self):
        data = self.read_iha('Group5.csv')
