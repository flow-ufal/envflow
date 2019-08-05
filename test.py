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
        data = pd.read_csv(path, ';', index_col=0)
        return data

    def test_mean_month(self):
        data = self.read_iha('Group1.csv')
        data2 = self.read().mean_month()

        for i in data.index:
            self.assertEqual('{:=4.0f}'.format(data.Means[i]), '{:=4.0f}'.format(data2.Means[i]))
            self.assertEqual('{:=4.0f}'.format(data['Coeff. of Var.'][i]), '{:=4.0f}'.format(data2['Coeff. of Var.'][i]))

    def test_moving_averages(self):
        data = self.read_iha('Group2.csv')
        data2 = self.read().moving_averages()
        print(data2)
        for i in data.index:
            self.assertEqual('{:=4.0f}'.format(data.Means[i]), '{:=4.0f}'.format(data2.Means[i]))
            self.assertEqual('{:=4.0f}'.format(data['Coeff. of Var.'][i]), '{:=4.0f}'.format(data2['Coeff. of Var.'][i]))

    def test_year_water(self):
        year_water = self.read().mesInicioAnoHidrologico()

        self.assertEqual((9, 'SEP'), year_water, 'Year Water: %s, %s' % (9, 'SEP'))

    def test_days_julian(self):
        dfDayJ, dayJMean, dayJCv = self.read().daysJulian(reducao="Maxima")
        data = self.read_iha('Group3.csv')
        print(data)
        print(dfDayJ, dayJMean, dayJCv)

    def test_pulse(self):
        picos, eventos_por_ano, dM, dCv, pM, pCv, limiar = self.read().pulsosDuracao(tipoEvento='cheia')
        data = self.read_iha('Group4.csv')
        print(limiar)
        print(eventos_por_ano)

    def test_rise_fall(self):
        data = self.read_iha('Group5.csv')
