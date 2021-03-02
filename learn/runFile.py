# -*- coding: utf-8 -*-
import numpy
numpy.set_printoptions(suppress=True)
hight=[1.88,1.66,1.78];
hair=[1.4,15.3,22.6];
smoke=[1,0,0];
gence=[1,0,0]
covValue=[hight,hair,smoke,gence];
a =numpy.cov(covValue);
print(a)
print(numpy.cov([10,11,8,3,2,1]))
print(numpy.cov([6,4,5,3,2.8,1]))
print(numpy.cov([12,9,10,2.5,1.3,2]))

