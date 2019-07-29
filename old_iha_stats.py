"""
Created on Wed Mar 15 22:57:24 2017

@author: clebson
"""
import pandas as pd
import numpy as np
from datetime import date
import calendar as cal
import math


class Caracteristicas(object):
    def __init__(self, dataFlow, nPosto=None, dateStart=None, dateEnd=None):
        self.nPosto = nPosto.upper()
        if dateStart != None and dateEnd != None:
            self.dateStart = pd.to_datetime(dateStart, dayfirst=True)
            self.dateEnd = pd.to_datetime(dateEnd, dayfirst=True)
            self.dataFlow = dataFlow.loc[self.dateStart:self.dateEnd]
        elif dateStart != None:
            self.dateStart = pd.to_datetime(dateStart, dayfirst=True)
            self.dataFlow = dataFlow.loc[self.dateStart:]
        elif dateEnd != None:
            self.dateEnd = pd.to_datetime(dateEnd, dayfirst=True)
            self.dataFlow = dataFlow.loc[:self.dateEnd]
        else:
            self.dataFlow = dataFlow

    # Ano hidrologico
    def mesInicioAnoHidrologico(self):
        mediaMes = [self.dataFlow[self.nPosto].loc[self.dataFlow.index.month == i].mean()
                    for i in range(1, 13)]
        mesHidro = 1 + mediaMes.index(min(mediaMes))
        mesHidroAbr = cal.month_abbr[mesHidro]
        return mesHidro, mesHidroAbr.upper()

    # Periodos sem falhas
    def periodoSemFalhas(self):
        aux = []
        listaInicio = []
        listaFim = []
        ganttBool = self.dataFlow.isnull()[self.nPosto]
        for i in ganttBool.index:
            if ~ganttBool.loc[i]:
                aux.append(i)
            elif len(aux) > 2 and ganttBool.loc[i]:
                listaInicio.append(aux[0])
                listaFim.append(aux[-1])
                aux = []
        if len(aux) > 0:
            listaInicio.append(aux[0])
            listaFim.append(aux[-1])
        dic = {'Inicio': listaInicio, 'Fim': listaFim}
        return pd.DataFrame(dic)

    def parcialEventoPercentil(self, quartilLimiar, tipoEvento):
        limiar = self.dataFlow[self.nPosto].quantile(quartilLimiar)
        if tipoEvento == 'cheia':
            eventoL = self.dataFlow[self.nPosto].isin(
                self.dataFlow.loc[self.dataFlow[self.nPosto] >= limiar, self.nPosto])
            return eventoL, limiar
        elif tipoEvento == 'estiagem':
            eventoL = self.dataFlow[self.nPosto].isin(
                self.dataFlow.loc[self.dataFlow[self.nPosto] <= limiar, self.nPosto])
            return eventoL, limiar
        else:
            return 'Evento erro!'

    def parcialEventoMediaMaxima(self, tipoEvento):
        limiar = self.maxAnual()[self.nPosto].mean()
        if tipoEvento == 'cheia':
            eventoL = self.dataFlow[self.nPosto].isin(
                self.dataFlow.loc[self.dataFlow[self.nPosto] >= limiar, self.nPosto])
            return eventoL, limiar
        elif tipoEvento == 'estiagem':
            eventoL = self.dataFlow[self.nPosto].isin(
                self.dataFlow.loc[self.dataFlow[self.nPosto] <= limiar, self.nPosto])
            return eventoL, limiar
        else:
            return 'Evento erro!'

    def parcialEventoPorAno(self, limiar, tipoEvento):
        if tipoEvento == 'cheia':
            eventoL = self.dataFlow[self.nPosto].isin(
                self.dataFlow.loc[self.dataFlow[self.nPosto] >= limiar, self.nPosto])
            return eventoL
        elif tipoEvento == 'estiagem':
            eventoL = self.dataFlow[self.nPosto].isin(
                self.dataFlow.loc[self.dataFlow[self.nPosto] <= limiar, self.nPosto])
            return eventoL
        else:
            return 'Evento erro!'

    def parcialPorAno(self, nEventos, tipoEvento):
        nAnos = self.dataFlow[self.nPosto].index.year[-1] - \
                self.dataFlow[self.nPosto].index.year[0]
        l = self.dataFlow[self.nPosto].quantile(0.7)
        #vazao = -np.sort(-self.dadosVazao.loc[self.dadosVazao[self.nPosto] <= l, self.nPosto])
        q = 0.8
        while q != 0:
            limiar = self.dataFlow[self.nPosto].quantile(q)
            print(limiar)
            eventosL = self.parcialEventoPorAno(limiar, tipoEvento)
            picos = self.eventos_picos(eventosL, tipoEvento)
            print(len(picos), nEventos * nAnos)
            if len(picos) >= nEventos * nAnos:
                return picos, limiar
            q -= 0.005

    def maxAnual(self):
        gDados = self.dataFlow.groupby(pd.Grouper(
            freq='AS-%s' % self.mesInicioAnoHidrologico()[1]))
        maxVazao = gDados[self.nPosto].max().values
        dataVazao = gDados[self.nPosto].idxmax().values

        dfMax = pd.DataFrame(maxVazao, index=dataVazao, columns=[self.nPosto])
        return dfMax

    def daysJulian(self, reducao):

        if reducao.title() == "Maxima":
            data = pd.DatetimeIndex(self.dataFlow.groupby(pd.Grouper(
                freq='AS-%s' % self.mesInicioAnoHidrologico()[1])).idxmax()[self.nPosto].values)
        elif reducao.title() == "Minima":
            data = pd.DatetimeIndex(self.dataFlow.groupby(pd.Grouper(
                freq='AS-%s' % self.mesInicioAnoHidrologico()[1])).idxmin()[self.nPosto].values)

        dfDayJulian = pd.DataFrame(
            list(map(int, data.strftime("%j"))), index=data)
        dayJulianMedia = dfDayJulian.mean()[0]
        dayJulianCv = dfDayJulian.std()[0]/dayJulianMedia
        return dfDayJulian, dayJulianMedia, dayJulianCv

    def __criterioMediana(self, dados, index, tipoEvento):
        median = self.dataFlow[self.nPosto].median()
        if tipoEvento == 'cheia':
            eventos = self.dataFlow[self.nPosto].isin(
                self.dataFlow.loc[self.dataFlow[self.nPosto] >= median, self.nPosto])
        elif tipoEvento == 'estiagem':
            eventos = self.dataFlow[self.nPosto].isin(
                self.dataFlow.loc[self.dataFlow[self.nPosto] <= median, self.nPosto])

        if len(dados['Vazao']) > 0 and (not eventos.loc[index] or
                                        index == pd.to_datetime("%s0831" % index.year)):
            return True
        else:
            return False

    def __criterioMedia(self, dados, index, tipoEvento):
        mean = self.dataFlow[self.nPosto].mean()
        if tipoEvento == 'cheia':
            eventos = self.dataFlow[self.nPosto].isin(
                self.dataFlow.loc[self.dataFlow[self.nPosto] >= mean, self.nPosto])
        elif tipoEvento == 'estiagem':
            eventos = self.dataFlow[self.nPosto].isin(
                self.dataFlow.loc[self.dataFlow[self.nPosto] <= mean, self.nPosto])

        if len(dados['Vazao']) > 0 and (not eventos.loc[index] or
                                        index == pd.to_datetime("%s0831" % index.year)):
            return True
        else:
            return False

    def __criterio_autocorrelacao(self, dados, max_evento, dias):

        if len(max_evento['Data']) == 0:
            return True
        elif len(dados['Data']) == 0:
            return False
        else:
            data_max = dados['Data'][dados['Vazao'].index(max(dados['Vazao']))]
            distancia_dias = data_max - max_evento['Data'][-1]
            if distancia_dias.days <= dias:
                return False
            return True

    def test_autocorrelacao(self, eventos_picos):

        x = eventos_picos.index
        y = eventos_picos.Vazao
        N = len(y)
        serie = pd.Series(y, index=x)
        r1 = serie.autocorr(lag=1)
        r2 = serie.autocorr(lag=2)
        r11_n = (-1 + 1.645 * math.sqrt(N - 1 - 1)) / (N - 1)
        r12_n = (-1 - 1.645 * math.sqrt(N - 1 - 1)) / (N - 1)
        r21_n = (-1 + 1.645 * math.sqrt(N - 2 - 1)) / (N - 2)
        r22_n = (-1 - 1.645 * math.sqrt(N - 2 - 1)) / (N - 2)

        if r11_n > r1 > r12_n and r21_n > r2 > r22_n:
            return False, r1, r2
        return True, r1, r2

    def eventos_picos(self, eventosL, tipoEvento, dias=1):
        grupoEventos = eventosL.groupby(pd.Grouper(
            freq='AS-%s' % self.mesInicioAnoHidrologico()[1]))
        max_evento = {'Data': [], 'Ano': [], 'Vazao': [],
                     'Inicio': [], 'Fim': [], 'Duracao': []}
        iAntes = eventosL.index[1]
        lowLimiar = False
        dados = {'Data': [], 'Vazao': []}
        for key, serie in grupoEventos:
            for i in serie.index:
                if serie.loc[i]:
                    dados['Vazao'].append(
                        self.dataFlow.loc[iAntes, self.nPosto])
                    dados['Data'].append(iAntes)
                    lowLimiar = True
                elif lowLimiar:
                    dados['Vazao'].append(
                        self.dataFlow.loc[iAntes, self.nPosto])
                    dados['Data'].append(iAntes)
                    dados['Vazao'].append(self.dataFlow.loc[i, self.nPosto])
                    dados['Data'].append(i)
                    lowLimiar = False

                elif self.__criterioMedia(dados, i , tipoEvento):
                    max_evento['Ano'].append(key.year)
                    max_evento['Vazao'].append(max(dados['Vazao']))
                    max_evento['Inicio'].append(dados['Data'][0])
                    max_evento['Fim'].append(dados['Data'][-1])
                    max_evento['Duracao'].append(len(dados['Data']))
                    max_evento['Data'].append(dados['Data'][dados['Vazao'].index(max(dados['Vazao']))])
                    dados = {'Data': [], 'Vazao': []}
                """
                elif dias > 0 and len(dados['Vazao']) > 0 and max_evento['Vazao'][-1] < max(dados['Vazao']):
                    max_evento['Ano'][-1] = key.year
                    max_evento['Vazao'][-1] = max(dados['Vazao'])
                    max_evento['Fim'][-1] = dados['Data'][-1]
                    max_evento['Duracao'][-1] = len(dados['Data'])
                    max_evento['Data'][-1] = dados['Data'][dados['Vazao'].index(max(dados['Vazao']))]
                    dados = {'Data': [], 'Vazao': []}
                """
                iAntes = i
        return pd.DataFrame(max_evento,
                            columns=['Ano', 'Duracao', 'Inicio', 'Fim', 'Vazao'],
                            index=max_evento['Data'])

    def pulsosDuracao(self, tipoEvento='cheia'):
        eventosPicos, limiar = self.parcialPorAno(2.3, tipoEvento)
        #eventosPicos = self.eventos_picos(eventosL, tipoEvento)

        print(self.test_autocorrelacao(eventosPicos)[0])

        grupoEventos = self.dataFlow[self.nPosto].groupby(
            pd.Grouper(freq='AS-%s' % self.mesInicioAnoHidrologico()[1]))
        dic = {'Ano': [], 'Duracao': [], 'nPulsos': []}
        for i, serie in grupoEventos:
            dic['Ano'].append(i.year)
            dic['Duracao'].append(
                eventosPicos.Duracao.loc[eventosPicos.Ano == i.year].mean())
            dic['nPulsos'].append(
                len(eventosPicos.loc[eventosPicos.Ano == i.year]))
        evento_por_ano = pd.DataFrame(dic)
        evento_por_ano.set_value(
            evento_por_ano.loc[evento_por_ano.Duracao.isnull()].index, 'Duracao', 0)
        durMedia = evento_por_ano.Duracao.mean()
        durCv = evento_por_ano.Duracao.std()/durMedia
        nPulsoMedio = evento_por_ano.nPulsos.mean()
        nPulsoCv = evento_por_ano.nPulsos.std()/nPulsoMedio
        return eventosPicos, evento_por_ano, durMedia, durCv, nPulsoMedio, nPulsoCv, limiar

    def autocorrelacao_por_vazao(self, tipoEvento):

        percentil = 0.8
        autocorrelacao = {'Vazao': [], 'Lag1': [], 'Lag2': []}
        while percentil >= 0:
            eventosL, limiar = self.parcialEventoPercentil(percentil, tipoEvento)
            eventosPicos = self.eventos_picos(eventosL, tipoEvento, dias=0)
            test_autocorrelacao = self.test_autocorrelacao(eventosPicos)
            r1 = test_autocorrelacao[1]
            r2 = test_autocorrelacao[2]
            autocorrelacao['Vazao'].append(limiar)
            autocorrelacao['Lag1'].append(abs(r1))
            autocorrelacao['Lag2'].append(abs(r2))
            percentil -= 0.005
        return pd.DataFrame(autocorrelacao,
                            columns=['Lag1', 'Lag2'],
                            index=autocorrelacao['Vazao'])

    def ChecksTypeRate(self, value1, value2, typeRate):
        if typeRate == 'rise':
            return value1 < value2
        elif typeRate == 'fall':
            return value1 > value2

    def rate(self, tipo, quartilLimiar, evento):
        eventos = self.parcialEvento(quartilLimiar, evento)[0]
        grupoEventos = eventos.groupby(pd.Grouper(
            freq='AS-%s' % self.mesInicioAnoHidrologico()[1]))
        rate = {'Data1': [], 'Vazao1': [],
                'Data2': [], 'Vazao2': [], 'Taxa': []}
        rise = {'Ano': [], 'Soma': [], 'Media': []}
        boo = False
        for key, serie in grupoEventos:
            d1 = None
            cont = 0
            values = []
            for i in serie.loc[serie.values == True].index:
                if d1 != None:
                    if self.ChecksTypeRate(self.dataFlow.loc[d1, self.nPosto],
                                           self.dataFlow.loc[i, self.nPosto], tipo):
                        boo = True
                        rate['Data1'].append(d1)
                        rate['Data2'].append(i)
                        rate['Vazao1'].append(
                            self.dataFlow.loc[d1, self.nPosto])
                        rate['Vazao2'].append(
                            self.dataFlow.loc[i, self.nPosto])
                        rate['Taxa'].append(
                            self.dataFlow.loc[i, self.nPosto] - self.dataFlow.loc[d1, self.nPosto])
                        values.append(
                            self.dataFlow.loc[i, self.nPosto] - self.dataFlow.loc[d1, self.nPosto])
                    else:
                        if boo:
                            mean = np.mean(values)
                            cont += 1
                            boo = False

                d1 = i
            if boo:
                mean = np.mean(values)
                cont += 1
                boo = False

            rise['Ano'].append(key.year)
            rise['Soma'].append(cont)
            rise['Media'].append(mean)

        ratesDf = pd.DataFrame(rate)
        riseDf = pd.DataFrame(rise)
        riseMed = riseDf.Media.mean()
        riseCv = riseDf.Media.std()/riseMed
        nMedia = riseDf.Soma.mean()
        nCv = riseDf.Soma.std()/nMedia
        return ratesDf, riseDf, riseMed, riseCv, nMedia, nCv

    def precipitacao_anual(self):
        dados_anual = self.dataFlow.groupby(
            pd.Grouper(freq='A')).sum().to_period()
        return dados_anual
