# -*- coding: utf-7 -*-
"""
Created on Mon Dec 18 10:27:15 2017

@author: Administrator
"""

import os

os.chdir('D:\pydata-book-2nd-edition')
cwd = os.getcwd()

from pandas import DataFrame, Series

import pandas as pd; import numpy as np

firmhs8 = pd.read_stata("./identifyFirm/FirmHs8/FirmHs82000.dta")

location = np.unique(firmhs8.location)
locationList = list(location)
locfirmhs8 = firmhs8.set_index(['location', 'firm'])

locfirmhs8 = locfirmhs8['hs8']



##构造函数选取企业的出口产品
##地区层面
for i in range(0, len(locationList) - 1):
    names = locals()
    names['loc_%sfirmProduct' % locationList[i]] = DataFrame(locfirmhs8.ix[[locationList[i]]])
    names['loc_%sfirmhs8' % locationList[i]] = names['loc_%sfirmProduct' % locationList[i]].reset_index()
    names['loc_%sfirm' % locationList[i]] = names['loc_%sfirmhs8' % locationList[i]]['firm']
    names['loc_%sfirm' % locationList[i]] = list(np.unique(names['loc_%sfirm' % locationList[i]]))
    

###循环生成同一地区两企业出口同种产品个数的N*N矩阵
for i in range(0, len(locationList) - 1):
    names = locals()
    firmList = names['loc_%sfirm' % locationList[i]]
    locfirmProd = names['loc_%sfirmhs8' % locationList[i]][['firm', 'hs8']]
    locfirmProd =locfirmProd.set_index(['firm', 'hs8'])
    locfirmProd['value'] = 1

    firmProduct = locfirmProd.unstack()
    firmProduct = firmProduct.fillna(0)
    
    FirmProd = np.array(firmProduct)
    ProdFirm = FirmProd.T
    locArray = np.dot(FirmProd, ProdFirm)
    
    for j in range(0, len(firmList)):
        locArray[j][j] = 0
        locdata = DataFrame(locArray, index = firmList, columns= firmList)
    
        locdata.to_csv('./firmProdAttr/NetworkAttr2000/loc%sdata.csv' % locationList[i])
