from __future__ import division

from numpy.random import normal
from scipy.stats import ttest_ind
from scipy.stats import norm
from scipy.stats import wilcoxon
import matplotlib.pyplot as pyplot

import numpy


def tStatistics(mean1,mean2,var1,var2,sampleSize1,sampleSize2):
    return (mean1-mean2)/numpy.sqrt(((sampleSize1-1)*var1+(sampleSize2-1)*var2)/(sampleSize1+sampleSize2-2)*(1/sampleSize1+1/sampleSize1))


distributionMeans=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6]
sampleSizes=[5,10,100]


stddev=2
alpha=0.05
iterationAmount=500

#sampleSize=100



for sampleSize in sampleSizes:
    wilcoxonRejectedPercentagesVector=[]
    tTestRejectedPercentagesVector=[]

    for mean in distributionMeans:
        rejectedCounterTTest=0
        rejectedCounterWilcoxon=0




        for i in xrange(iterationAmount):

            #losowanie wektora liczb z rozkladu normalnego

            standardNormalDistributionNumbers=norm.rvs(loc=0,scale=stddev,size=sampleSize)
            otherNormalDistributionNumbers=norm.rvs(loc=mean,scale=stddev,size=sampleSize)

            #wyliczanie niesparowanego testu t

            tStatistic,pValueTTest=ttest_ind(standardNormalDistributionNumbers,otherNormalDistributionNumbers)

            if(pValueTTest<alpha):
                rejectedCounterTTest=rejectedCounterTTest+1


            #przeprowadzanie wilcoxon signed-rank test

            wilcoxStatistic,pValueWilcox=wilcoxon(standardNormalDistributionNumbers,otherNormalDistributionNumbers,zero_method="wilcox")

            if(pValueWilcox<alpha):
                rejectedCounterWilcoxon=rejectedCounterWilcoxon+1


        #wyliczanie ulamka odrzuconych H0

        tTestRejectedPercentagesVector.append(rejectedCounterTTest/iterationAmount)
        wilcoxonRejectedPercentagesVector.append(rejectedCounterWilcoxon/iterationAmount)




    print "WIELKOSC PROBKI: {0}".format(sampleSize)
    print "WARTOSCI OCZEKIWANE ROZKLADOW \n {0}".format(distributionMeans)
    print "ULAMEK ODRZUCONYCH HIPOTEZ H0 PRZY KOLEJNYCH WARTOSCIACH OCZEKIWANYCH W TESCIE NIESPAROWANYM T \n {0}".format(tTestRejectedPercentagesVector)
    print "ULAMEK ODRZUCONYCH HIPOTEZ H0 PRZY KOLEJNYCH WARTOSCIACH OCZEKIWANYCH W TESCIE WILCOXONA \n {0}".format(wilcoxonRejectedPercentagesVector)

    #pyplot.plot(tTestRejectedPercentagesVector)
    #pyplot.axis(distributionMeans)
    #pyplot.show()

    pyplot.plot(distributionMeans,tTestRejectedPercentagesVector,'ro',distributionMeans,wilcoxonRejectedPercentagesVector,'bs')
    #pyplot.axis([min(distributionMeans),max(distributionMeans),min(wilcoxonRejectedPercentagesVector),max(wilcoxonRejectedPercentagesVector)])
    pyplot.show()








