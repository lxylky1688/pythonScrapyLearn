# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 14:29:54 2017

@author: Administrator
"""
###2006
import os

os.chdir('D:\pydata-book-2nd-edition')
cwd = os.getcwd()

from pandas import DataFrame, Series

import pandas as pd; import numpy as np

firmhs8 = pd.read_stata("./identifyFirm/FirmHs8/FirmHs82006.dta")

location = np.unique(firmhs8.location)
locationList = list(location)
locfirmhs8 = firmhs8.set_index(['location','firm'])

locfirmhs8 = locfirmhs8['hs8']

locationList = locationList[289:]


##构造函数选取企业的出口产品
##地区层面
for i in range(0, len(locationList) - 1):
    names = locals()
    names['loc_%sfirmProduct' % locationList[i]] = DataFrame(locfirmhs8.ix[[locationList[i]]])
    names['loc_%sfirmhs8' % locationList[i]] = names['loc_%sfirmProduct' % locationList[i]].reset_index()
    names['loc_%sfirm' % locationList[i]] = names['loc_%sfirmhs8' % locationList[i]]['firm']
    names['loc_%sfirm' % locationList[i]] = list(np.unique(names['loc_%sfirm' % locationList[i]]))
    
###循环生成N*N矩阵
for i in range(0, len(locationList) - 1):
    names = locals()
    firmList = names['loc_%sfirm' % locationList[i]]
    locfirmProd = names['loc_%sfirmhs8' % locationList[i]][['firm', 'hs8']]
    locfirmProd =locfirmProd.set_index(['firm'])
    
    for j in range(0, len(firmList) - 1):
        names = locals()
        names['loc_firm%s' % (firmList[j])] = locfirmProd.ix[[firmList[j]]]
        names['locfirm%s' % firmList[j]] = names['loc_firm%s' % firmList[j]].reset_index()
        names['lstfirm%s' % firmList[j]] = set(names['locfirm%s' % firmList[j]]['hs8'])
        locArr = np.zeros((len(firmList), len(firmList)))
        
    for j in range(0, len(firmList) - 1):
        for k in range(0, len(firmList) - 1):
            ##j代表行，K代表列
            names = locals()
            if set(names['lstfirm%s' % firmList[j]]).issubset(set(names['lstfirm%s' % firmList[k]])):
                locArr[j][k] = 1
            else:
                locArr[j][k] = 0
    for j in range(0, len(firmList) - 1):
        locArr[j][j] = 0
        locdata = DataFrame(locArr, index = firmList, columns= firmList)
    
        locdata.to_csv('./identifyFirm/Identify2006/loc%sdata.csv' % locationList[i])

                

    
