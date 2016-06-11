from __future__ import division

from numpy.random import normal
from scipy.stats import ttest_ind
from scipy.stats import norm

import numpy


def tStatistics(mean1,mean2,var1,var2,sampleSize1,sampleSize2):
    return (mean1-mean2)/numpy.sqrt(((sampleSize1-1)*var1+(sampleSize2-1)*var2)/(sampleSize1+sampleSize2-2)*(1/sampleSize1+1/sampleSize1))


distributionMeans=[0,0.95]
sampleSizes=[5,7,10,12,14,16,18,20,25,30,35,10000]


stddev=2
alpha=0.05
iterationAmount=100

sampleSize=100

wilcoxonRejectedPercentagesVector=[]

for mean in distributionMeans:
    rejectedCounterWilcoxon=0


    for i in xrange(iterationAmount):


        standardNormalDistributionNumbers=norm.rvs(loc=0,scale=stddev,size=sampleSize)
        otherNormalDistributionNumbers=norm.rvs(loc=mean,scale=stddev,size=sampleSize)

        #standardNormalDistributionNumbers=normal(loc=0,scale=stddev,size=sampleSize)
        #otherNormalDistributionNumbers=normal(loc=mean,scale=stddev,size=sampleSize)

        tStatistic,pValue=ttest_ind(standardNormalDistributionNumbers,otherNormalDistributionNumbers)

        if(pValue<alpha):
            rejectedCounterWilcoxon=rejectedCounterWilcoxon+1


    print rejectedCounterWilcoxon/iterationAmount
    wilcoxonRejectedPercentagesVector.append(rejectedCounterWilcoxon/iterationAmount)


print wilcoxonRejectedPercentagesVector




