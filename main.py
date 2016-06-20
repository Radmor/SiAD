# -*- coding: utf-8 -*-

from __future__ import division

from scipy.stats import ttest_ind
from scipy.stats import norm
from scipy.stats import wilcoxon
from scipy.stats import chi2
from scipy.stats import f
from scipy.stats import uniform
from scipy.stats import pearsonr
import matplotlib.pyplot as pyplot
import matplotlib.cm as cmx
import matplotlib.colors as colors
import itertools

from itertools import cycle


import numpy

def tStatistics(mean1, mean2, var1, var2, sampleSize1, sampleSize2):
    return (mean1 - mean2) / numpy.sqrt(
        ((sampleSize1 - 1) * var1 + (sampleSize2 - 1) * var2) / (sampleSize1 + sampleSize2 - 2) * (
        1 / sampleSize1 + 1 / sampleSize1))


cycol = cycle('bgrcmyk').next

meansAmount = 20

stddev=10
howFarStddevsFromMean=0.1
stddevStep=howFarStddevsFromMean/meansAmount


minMean = 0
maxMean = stddev*howFarStddevsFromMean
step = (maxMean - minMean) / meansAmount


stddevsSteps=numpy.arange(0,howFarStddevsFromMean,stddevStep)
distributionMeans = numpy.arange(minMean, maxMean, step)

df1=5
df2=2


# distributionMeans=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6]
sampleSizes = [5, 10, 15,20,25,30,35]
#sampleSizes=[40,50,60,70,80,90,100]
#sampleSizes=[50,75,100,150,200,250,500]


alpha = 0.05
iterationAmount = 500


def shiftdistribution(distribution,mean):
    for i,item in enumerate(distribution):
        distribution[i]=distribution[i]+mean
    return distribution


def perform_tests():
    plotlegend=list(itertools.chain.from_iterable([[u'n={0}, T-Student'.format(sampleSize),u'n={0}, Wilcoxon'.format(sampleSize)] for sampleSize in sampleSizes]))

    pyplot.rc('font', family='DejaVu Sans')
    for znacznikkoloru,sampleSize in enumerate(sampleSizes):
        wilcoxonRejectedPercentagesVector = []
        tTestRejectedPercentagesVector = []

        for mean in distributionMeans:
            rejectedCounterTTest = 0
            rejectedCounterWilcoxon = 0

            for i in xrange(iterationAmount):

                # losowanie wektora liczb z rozkladu normalnego

                baseDistribution = norm.rvs(loc=0, scale=stddev, size=sampleSize)
                shiftedDistribution = norm.rvs(loc=mean, scale=stddev, size=sampleSize)



                # wyliczanie niesparowanego testu t

                tStatistic, pValueTTest = ttest_ind(baseDistribution, shiftedDistribution)

                if (pValueTTest < alpha):
                    rejectedCounterTTest = rejectedCounterTTest + 1

                # przeprowadzanie wilcoxon signed-rank test

                wilcoxStatistic, pValueWilcox = wilcoxon(baseDistribution, shiftedDistribution, zero_method="wilcox")

                if (pValueWilcox < alpha):
                    rejectedCounterWilcoxon = rejectedCounterWilcoxon + 1

            # wyliczanie ulamka odrzuconych H0

            tTestRejectedPercentagesVector.append(rejectedCounterTTest / iterationAmount)
            wilcoxonRejectedPercentagesVector.append(rejectedCounterWilcoxon / iterationAmount)

        print "WIELKOSC PROBKI: {0}".format(sampleSize)
        print "WARTOSCI OCZEKIWANE ROZKLADOW \n {0}".format(distributionMeans)
        print "ULAMEK ODRZUCONYCH HIPOTEZ H0 PRZY KOLEJNYCH WARTOSCIACH OCZEKIWANYCH W TESCIE NIESPAROWANYM T \n {0}".format(
            tTestRejectedPercentagesVector)
        print "ULAMEK ODRZUCONYCH HIPOTEZ H0 PRZY KOLEJNYCH WARTOSCIACH OCZEKIWANYCH W TESCIE WILCOXONA \n {0}".format(
            wilcoxonRejectedPercentagesVector)


        # pyplot.plot(tTestRejectedPercentagesVector)
        # pyplot.axis(distributionMeans)
        # pyplot.show()

        currentcolor=cycol()
        pyplot.plot(stddevsSteps, tTestRejectedPercentagesVector,color=currentcolor)
        pyplot.plot(stddevsSteps,wilcoxonRejectedPercentagesVector,color=currentcolor,linestyle='dashed')
        # pyplot.legend(sampleSize)
        # pyplot.axis([min(distributionMeans),max(distributionMeans),min(wilcoxonRejectedPercentagesVector),max(wilcoxonRejectedPercentagesVector)])
    pyplot.legend(plotlegend, bbox_to_anchor=(0.99, 0.5))
    pyplot.title(u'Wyniki eksperymentu dla różnych rozmiarów próby o rozkładzie normalnym')
    pyplot.xlabel(u'Liczba odchyleń standardowych, o którą przesunięty jest względem standardowego rozkładu normalnego badany rozkład')
    pyplot.ylabel(u'Stosunek liczby testów, w których odrzucona \n została hipoteza H0 do liczby wszystkich testów')
    pyplot.show()


def perform_rest():
    plotlegend=list(itertools.chain.from_iterable([[u'n={0}, T-Student'.format(sampleSize),u'n={0}, Wilcoxon'.format(sampleSize)] for sampleSize in sampleSizes]))

    pyplot.rc('font', family='DejaVu Sans')
    for znacznikkoloru,sampleSize in enumerate(sampleSizes):
        wilcoxonRejectedPercentagesVector = []
        tTestRejectedPercentagesVector = []

        for mean in distributionMeans:
            rejectedCounterTTest = 0
            rejectedCounterWilcoxon = 0

            for i in xrange(iterationAmount):

                # losowanie wektora liczb z rozkladu normalnego

                baseDistribution = uniform.rvs(size=sampleSize)
                shiftedDistribution = uniform.rvs(size=sampleSize)
                shiftedDistribution=shiftdistribution(shiftedDistribution,mean)





                # wyliczanie niesparowanego testu t

                tStatistic, pValueTTest = ttest_ind(baseDistribution, shiftedDistribution)

                if (pValueTTest < alpha):
                    rejectedCounterTTest = rejectedCounterTTest + 1

                # przeprowadzanie wilcoxon signed-rank test

                wilcoxStatistic, pValueWilcox = wilcoxon(baseDistribution, shiftedDistribution, zero_method="wilcox")

                if (pValueWilcox < alpha):
                    rejectedCounterWilcoxon = rejectedCounterWilcoxon + 1

            # wyliczanie ulamka odrzuconych H0

            tTestRejectedPercentagesVector.append(rejectedCounterTTest / iterationAmount)
            wilcoxonRejectedPercentagesVector.append(rejectedCounterWilcoxon / iterationAmount)

        print "WIELKOSC PROBKI: {0}".format(sampleSize)
        print "WARTOSCI OCZEKIWANE ROZKLADOW \n {0}".format(distributionMeans)
        print "ULAMEK ODRZUCONYCH HIPOTEZ H0 PRZY KOLEJNYCH WARTOSCIACH OCZEKIWANYCH W TESCIE NIESPAROWANYM T \n {0}".format(
            tTestRejectedPercentagesVector)
        print "ULAMEK ODRZUCONYCH HIPOTEZ H0 PRZY KOLEJNYCH WARTOSCIACH OCZEKIWANYCH W TESCIE WILCOXONA \n {0}".format(
            wilcoxonRejectedPercentagesVector)


        # pyplot.plot(tTestRejectedPercentagesVector)
        # pyplot.axis(distributionMeans)
        # pyplot.show()

        currentcolor=cycol()
        pyplot.plot(distributionMeans, tTestRejectedPercentagesVector,color=currentcolor)
        pyplot.plot(distributionMeans,wilcoxonRejectedPercentagesVector,color=currentcolor,linestyle='dashed')
        # pyplot.legend(sampleSize)
        # pyplot.axis([min(distributionMeans),max(distributionMeans),min(wilcoxonRejectedPercentagesVector),max(wilcoxonRejectedPercentagesVector)])
    pyplot.legend(plotlegend, bbox_to_anchor=(0.99, 0.5))
    pyplot.title(u'Wyniki eksperymentu dla różnych rozmiarów próby  dla rozkładu jednorodnego')
    pyplot.xlabel(u'Wielkość stałej, o którą przesunięte są między sobą badane rozkłady')
    pyplot.ylabel(u'Stosunek liczby testów, w których odrzucona \n została hipoteza H0 do liczby wszystkich testów')
    pyplot.show()



#perform_tests()
perform_rest()
