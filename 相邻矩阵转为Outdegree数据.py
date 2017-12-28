# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 19:02:14 2017

@author: Administrator
"""

##代码优化
##将过程拆为两个部分一个部分为画图分析，一部分为数据导出
import os

os.chdir('D:\pydata-book-2nd-edition\identifyFirm')
cwd = os.getcwd()

from pandas import DataFrame, Series

import pandas as pd; import numpy as np

import csv #使用内置的CSV库
import matplotlib.pyplot as plt
import networkx as nx

from networkx import algorithms
from networkx.algorithms import traversal

##将firm和Outdegree数据（list格式）整合为DataFrame
def get_dataframe(firm, outdegree):
    f = np.array(firm)
    o = np.array(outdegree)
    data = DataFrame(f, index = o, columns = ['firm'])
    data.index.name = 'outdegree'
    data = data.reset_index()
    return data

##
NetOutdegree = []
prodNum = pd.read_stata("./FirmProduction/firmprodNum%s.dta" % '2000')

location = pd.read_excel("locationlst%s.xls" % '2000', header = None)
location.columns = ['city', 'location']
locationlst = list(location['location'])
del location

for loc in locationlst:
    try:
        with open('./Identify%s/loc%sdata.csv' % ('2000', loc), 'rt', encoding = "utf-8") as csvfile:
            df = list(csv.reader(csvfile))
            header, values = df[0], df[1:]
            index = [i[0] for i in values]
            values =[i[1:] for i in values]
            dataf = DataFrame(values, columns = header[1:], index = index)
        df = dataf.unstack().reset_index()
        df['cityid'] = str(loc)
        df.columns = ['firm', 'subfirm', 'children', 'location']
        df['children'] = df['children'].astype(float)
        ## 仅保留存在链接的数据
        links = df['children'] == 1
        df = df[links]
        ## 将产品个数进行匹配
        df = pd.merge(df, prodNum, on = ['firm', 'location'], how = 'inner')
        df.rename(columns = {'firm':'superfirm','subfirm':'firm','prodNum':'SuperNum'}, inplace = True)

        df = pd.merge(df, prodNum, on = ['firm', 'location'],how = 'inner')

        df.rename(columns = {'firm':'subfirm','prodNum':'SubNum'}, inplace = True)
        
        ## 构建有向网络
        subfirmlst = df['subfirm']
        superfirmlst = df['superfirm']

        linkslst = list(zip(subfirmlst, superfirmlst))

        g = nx.DiGraph(name = "Product Set Network for Each Firm") #有向网络图
        g.add_edges_from(linkslst)
        
        ## 生成OUTDEGREE和INDEGREE
        firmComponents = list(nx.weakly_connected_component_subgraphs(g))
        firmoutdegree = [dict(j.out_degree()) for j in firmComponents]

        firms = [list(j.keys()) for j in firmoutdegree]
        outdegrees = [list(j.values()) for j in firmoutdegree]

        components = [list(j) for j in enumerate(firmoutdegree)]
        componentsId = [j[0] for j in components]


        lst = list(map(get_dataframe, firms, outdegrees))
        ##使用pd.concat()对数据整合
        try:
            SuperFirm = pd.concat(lst, keys = componentsId)
            SuperFirm = SuperFirm.reset_index()
            SuperFirm.columns = ['componentsId', 'level', 'outdegree', 'superfirm']
            SuperFirm = SuperFirm[['componentsId', 'outdegree', 'superfirm']]
            ## 将链接数据和OUTDEGREE数据合并
            FirmNetdf = pd.merge(df, SuperFirm, on = 'superfirm', how = 'inner')
        
            FirmNetdf['outdegree'] = FirmNetdf['outdegree'].astype(float)
            criterial = FirmNetdf.outdegree == 0
            FirmNetworkdf = FirmNetdf[criterial]
    
            NetOutdegree.append(FirmNetworkdf)
        except ValueError as r:
            pass
    except (FileNotFoundError, OSError) as e:
        print("No such file or directory")
        pass
    
##将各地区的数据整合
FirmNetSpillover = pd.concat(NetOutdegree)
del NetOutdegree
FirmNetSpillover.to_stata('./FirmSpillover/FirmSpillover%s.dta' % '2000', write_index = False)    
      

  
##2001
NetOutdegree = []
prodNum = pd.read_stata("./FirmProduction/firmprodNum%s.dta" % '2001')

location = pd.read_excel("locationlst%s.xls" % '2001', header = None)
location.columns = ['city', 'location']
locationlst = list(location['location'])
del location

for loc in locationlst:
    try:
        with open('./Identify%s/loc%sdata.csv' % ('2001', loc), 'rt', encoding = "utf-8") as csvfile:
            df = list(csv.reader(csvfile))
            header, values = df[0], df[1:]
            index = [i[0] for i in values]
            values =[i[1:] for i in values]
            dataf = DataFrame(values, columns = header[1:], index = index)
        df = dataf.unstack().reset_index()
        df['cityid'] = str(loc)
        df.columns = ['firm', 'subfirm', 'children', 'location']
        df['children'] = df['children'].astype(float)
        ## 仅保留存在链接的数据
        links = df['children'] == 1
        df = df[links]
        ## 将产品个数进行匹配
        df = pd.merge(df, prodNum, on = ['firm', 'location'], how = 'inner')
        df.rename(columns = {'firm':'superfirm','subfirm':'firm','prodNum':'SuperNum'}, inplace = True)

        df = pd.merge(df, prodNum, on = ['firm', 'location'],how = 'inner')

        df.rename(columns = {'firm':'subfirm','prodNum':'SubNum'}, inplace = True)
        
        ## 构建有向网络
        subfirmlst = df['subfirm']
        superfirmlst = df['superfirm']

        linkslst = list(zip(subfirmlst, superfirmlst))

        g = nx.DiGraph(name = "Product Set Network for Each Firm") #有向网络图
        g.add_edges_from(linkslst)
        
        ## 生成OUTDEGREE和INDEGREE
        firmComponents = list(nx.weakly_connected_component_subgraphs(g))
        firmoutdegree = [dict(j.out_degree()) for j in firmComponents]

        firms = [list(j.keys()) for j in firmoutdegree]
        outdegrees = [list(j.values()) for j in firmoutdegree]

        components = [list(j) for j in enumerate(firmoutdegree)]
        componentsId = [j[0] for j in components]


        lst = list(map(get_dataframe, firms, outdegrees))
        ##使用pd.concat()对数据整合
        try:
            SuperFirm = pd.concat(lst, keys = componentsId)
            SuperFirm = SuperFirm.reset_index()
            SuperFirm.columns = ['componentsId', 'level', 'outdegree', 'superfirm']
            SuperFirm = SuperFirm[['componentsId', 'outdegree', 'superfirm']]
            ## 将链接数据和OUTDEGREE数据合并
            FirmNetdf = pd.merge(df, SuperFirm, on = 'superfirm', how = 'inner')
        
            FirmNetdf['outdegree'] = FirmNetdf['outdegree'].astype(float)
            criterial = FirmNetdf.outdegree == 0
            FirmNetworkdf = FirmNetdf[criterial]
    
            NetOutdegree.append(FirmNetworkdf)
        except ValueError as r:
            pass
    except (FileNotFoundError, OSError) as e:
        print("No such file or directory")
        pass
    
##将各地区的数据整合
FirmNetSpillover = pd.concat(NetOutdegree)
del NetOutdegree
FirmNetSpillover.to_stata('./FirmSpillover/FirmSpillover%s.dta' % '2001', write_index = False)
        
##2002
NetOutdegree = []
prodNum = pd.read_stata("./FirmProduction/firmprodNum%s.dta" % '2002')

location = pd.read_excel("locationlst%s.xls" % '2002', header = None)
location.columns = ['city', 'location']
locationlst = list(location['location'])
del location

for loc in locationlst:
    try:
        with open('./Identify%s/loc%sdata.csv' % ('2002', loc), 'rt', encoding = "utf-8") as csvfile:
            df = list(csv.reader(csvfile))
            header, values = df[0], df[1:]
            index = [i[0] for i in values]
            values =[i[1:] for i in values]
            dataf = DataFrame(values, columns = header[1:], index = index)
        df = dataf.unstack().reset_index()
        df['cityid'] = str(loc)
        df.columns = ['firm', 'subfirm', 'children', 'location']
        df['children'] = df['children'].astype(float)
        ## 仅保留存在链接的数据
        links = df['children'] == 1
        df = df[links]
        ## 将产品个数进行匹配
        df = pd.merge(df, prodNum, on = ['firm', 'location'], how = 'inner')
        df.rename(columns = {'firm':'superfirm','subfirm':'firm','prodNum':'SuperNum'}, inplace = True)

        df = pd.merge(df, prodNum, on = ['firm', 'location'],how = 'inner')

        df.rename(columns = {'firm':'subfirm','prodNum':'SubNum'}, inplace = True)
        
        ## 构建有向网络
        subfirmlst = df['subfirm']
        superfirmlst = df['superfirm']

        linkslst = list(zip(subfirmlst, superfirmlst))

        g = nx.DiGraph(name = "Product Set Network for Each Firm") #有向网络图
        g.add_edges_from(linkslst)
        
        ## 生成OUTDEGREE和INDEGREE
        firmComponents = list(nx.weakly_connected_component_subgraphs(g))
        firmoutdegree = [dict(j.out_degree()) for j in firmComponents]

        firms = [list(j.keys()) for j in firmoutdegree]
        outdegrees = [list(j.values()) for j in firmoutdegree]

        components = [list(j) for j in enumerate(firmoutdegree)]
        componentsId = [j[0] for j in components]


        lst = list(map(get_dataframe, firms, outdegrees))
        ##使用pd.concat()对数据整合
        try:
            SuperFirm = pd.concat(lst, keys = componentsId)
            SuperFirm = SuperFirm.reset_index()
            SuperFirm.columns = ['componentsId', 'level', 'outdegree', 'superfirm']
            SuperFirm = SuperFirm[['componentsId', 'outdegree', 'superfirm']]
            ## 将链接数据和OUTDEGREE数据合并
            FirmNetdf = pd.merge(df, SuperFirm, on = 'superfirm', how = 'inner')
        
            FirmNetdf['outdegree'] = FirmNetdf['outdegree'].astype(float)
            criterial = FirmNetdf.outdegree == 0
            FirmNetworkdf = FirmNetdf[criterial]
    
            NetOutdegree.append(FirmNetworkdf)
        except ValueError as r:
            pass
    except (FileNotFoundError, OSError) as e:
        print("No such file or directory")
        pass
    
##将各地区的数据整合
FirmNetSpillover = pd.concat(NetOutdegree)
del NetOutdegree
FirmNetSpillover.to_stata('./FirmSpillover/FirmSpillover%s.dta' % '2002', write_index = False)

##2003
NetOutdegree = []
prodNum = pd.read_stata("./FirmProduction/firmprodNum%s.dta" % '2003')

location = pd.read_excel("locationlst%s.xls" % '2003', header = None)
location.columns = ['city', 'location']
locationlst = list(location['location'])
del location

for loc in locationlst:
    try:
        with open('./Identify%s/loc%sdata.csv' % ('2003', loc), 'rt', encoding = "utf-8") as csvfile:
            df = list(csv.reader(csvfile))
            header, values = df[0], df[1:]
            index = [i[0] for i in values]
            values =[i[1:] for i in values]
            dataf = DataFrame(values, columns = header[1:], index = index)
        df = dataf.unstack().reset_index()
        df['cityid'] = str(loc)
        df.columns = ['firm', 'subfirm', 'children', 'location']
        df['children'] = df['children'].astype(float)
        ## 仅保留存在链接的数据
        links = df['children'] == 1
        df = df[links]
        ## 将产品个数进行匹配
        df = pd.merge(df, prodNum, on = ['firm', 'location'], how = 'inner')
        df.rename(columns = {'firm':'superfirm','subfirm':'firm','prodNum':'SuperNum'}, inplace = True)

        df = pd.merge(df, prodNum, on = ['firm', 'location'],how = 'inner')

        df.rename(columns = {'firm':'subfirm','prodNum':'SubNum'}, inplace = True)
        
        ## 构建有向网络
        subfirmlst = df['subfirm']
        superfirmlst = df['superfirm']

        linkslst = list(zip(subfirmlst, superfirmlst))

        g = nx.DiGraph(name = "Product Set Network for Each Firm") #有向网络图
        g.add_edges_from(linkslst)
        
        ## 生成OUTDEGREE和INDEGREE
        firmComponents = list(nx.weakly_connected_component_subgraphs(g))
        firmoutdegree = [dict(j.out_degree()) for j in firmComponents]

        firms = [list(j.keys()) for j in firmoutdegree]
        outdegrees = [list(j.values()) for j in firmoutdegree]

        components = [list(j) for j in enumerate(firmoutdegree)]
        componentsId = [j[0] for j in components]


        lst = list(map(get_dataframe, firms, outdegrees))
        ##使用pd.concat()对数据整合
        try:
            SuperFirm = pd.concat(lst, keys = componentsId)
            SuperFirm = SuperFirm.reset_index()
            SuperFirm.columns = ['componentsId', 'level', 'outdegree', 'superfirm']
            SuperFirm = SuperFirm[['componentsId', 'outdegree', 'superfirm']]
            ## 将链接数据和OUTDEGREE数据合并
            FirmNetdf = pd.merge(df, SuperFirm, on = 'superfirm', how = 'inner')
        
            FirmNetdf['outdegree'] = FirmNetdf['outdegree'].astype(float)
            criterial = FirmNetdf.outdegree == 0
            FirmNetworkdf = FirmNetdf[criterial]
    
            NetOutdegree.append(FirmNetworkdf)
        except ValueError as r:
            pass
    except (FileNotFoundError, OSError) as e:
        print("No such file or directory")
        pass
    
##将各地区的数据整合
FirmNetSpillover = pd.concat(NetOutdegree)
del NetOutdegree
FirmNetSpillover.to_stata('./FirmSpillover/FirmSpillover%s.dta' % '2003', write_index = False)

##2004
NetOutdegree = []
prodNum = pd.read_stata("./FirmProduction/firmprodNum%s.dta" % '2004')

location = pd.read_excel("locationlst%s.xls" % '2004', header = None)
location.columns = ['city', 'location']
locationlst = list(location['location'])
del location

for loc in locationlst:
    try:
        with open('./Identify%s/loc%sdata.csv' % ('2004', loc), 'rt', encoding = "utf-8") as csvfile:
            df = list(csv.reader(csvfile))
            header, values = df[0], df[1:]
            index = [i[0] for i in values]
            values =[i[1:] for i in values]
            dataf = DataFrame(values, columns = header[1:], index = index)
        df = dataf.unstack().reset_index()
        df['cityid'] = str(loc)
        df.columns = ['firm', 'subfirm', 'children', 'location']
        df['children'] = df['children'].astype(float)
        ## 仅保留存在链接的数据
        links = df['children'] == 1
        df = df[links]
        ## 将产品个数进行匹配
        df = pd.merge(df, prodNum, on = ['firm', 'location'], how = 'inner')
        df.rename(columns = {'firm':'superfirm','subfirm':'firm','prodNum':'SuperNum'}, inplace = True)

        df = pd.merge(df, prodNum, on = ['firm', 'location'],how = 'inner')

        df.rename(columns = {'firm':'subfirm','prodNum':'SubNum'}, inplace = True)
        
        ## 构建有向网络
        subfirmlst = df['subfirm']
        superfirmlst = df['superfirm']

        linkslst = list(zip(subfirmlst, superfirmlst))

        g = nx.DiGraph(name = "Product Set Network for Each Firm") #有向网络图
        g.add_edges_from(linkslst)
        
        ## 生成OUTDEGREE和INDEGREE
        firmComponents = list(nx.weakly_connected_component_subgraphs(g))
        firmoutdegree = [dict(j.out_degree()) for j in firmComponents]

        firms = [list(j.keys()) for j in firmoutdegree]
        outdegrees = [list(j.values()) for j in firmoutdegree]

        components = [list(j) for j in enumerate(firmoutdegree)]
        componentsId = [j[0] for j in components]


        lst = list(map(get_dataframe, firms, outdegrees))
        ##使用pd.concat()对数据整合
        try:
            SuperFirm = pd.concat(lst, keys = componentsId)
            SuperFirm = SuperFirm.reset_index()
            SuperFirm.columns = ['componentsId', 'level', 'outdegree', 'superfirm']
            SuperFirm = SuperFirm[['componentsId', 'outdegree', 'superfirm']]
            ## 将链接数据和OUTDEGREE数据合并
            FirmNetdf = pd.merge(df, SuperFirm, on = 'superfirm', how = 'inner')
        
            FirmNetdf['outdegree'] = FirmNetdf['outdegree'].astype(float)
            criterial = FirmNetdf.outdegree == 0
            FirmNetworkdf = FirmNetdf[criterial]
    
            NetOutdegree.append(FirmNetworkdf)
        except ValueError as r:
            pass
    except (FileNotFoundError, OSError) as e:
        print("No such file or directory")
        pass
    
##将各地区的数据整合
FirmNetSpillover = pd.concat(NetOutdegree)
del NetOutdegree
FirmNetSpillover.to_stata('./FirmSpillover/FirmSpillover%s.dta' % '2004', write_index = False)


##2005
NetOutdegree = []
prodNum = pd.read_stata("./FirmProduction/firmprodNum%s.dta" % '2005')

location = pd.read_excel("locationlst%s.xls" % '2005', header = None)
location.columns = ['city', 'location']
locationlst = list(location['location'])
del location

for loc in locationlst:
    try:
        with open('./Identify%s/loc%sdata.csv' % ('2005', loc), 'rt', encoding = "utf-8") as csvfile:
            df = list(csv.reader(csvfile))
            header, values = df[0], df[1:]
            index = [i[0] for i in values]
            values =[i[1:] for i in values]
            dataf = DataFrame(values, columns = header[1:], index = index)
        df = dataf.unstack().reset_index()
        df['cityid'] = str(loc)
        df.columns = ['firm', 'subfirm', 'children', 'location']
        df['children'] = df['children'].astype(float)
        ## 仅保留存在链接的数据
        links = df['children'] == 1
        df = df[links]
        ## 将产品个数进行匹配
        df = pd.merge(df, prodNum, on = ['firm', 'location'], how = 'inner')
        df.rename(columns = {'firm':'superfirm','subfirm':'firm','prodNum':'SuperNum'}, inplace = True)

        df = pd.merge(df, prodNum, on = ['firm', 'location'],how = 'inner')

        df.rename(columns = {'firm':'subfirm','prodNum':'SubNum'}, inplace = True)
        
        ## 构建有向网络
        subfirmlst = df['subfirm']
        superfirmlst = df['superfirm']

        linkslst = list(zip(subfirmlst, superfirmlst))

        g = nx.DiGraph(name = "Product Set Network for Each Firm") #有向网络图
        g.add_edges_from(linkslst)
        
        ## 生成OUTDEGREE和INDEGREE
        firmComponents = list(nx.weakly_connected_component_subgraphs(g))
        firmoutdegree = [dict(j.out_degree()) for j in firmComponents]

        firms = [list(j.keys()) for j in firmoutdegree]
        outdegrees = [list(j.values()) for j in firmoutdegree]

        components = [list(j) for j in enumerate(firmoutdegree)]
        componentsId = [j[0] for j in components]


        lst = list(map(get_dataframe, firms, outdegrees))
        ##使用pd.concat()对数据整合
        try:
            SuperFirm = pd.concat(lst, keys = componentsId)
            SuperFirm = SuperFirm.reset_index()
            SuperFirm.columns = ['componentsId', 'level', 'outdegree', 'superfirm']
            SuperFirm = SuperFirm[['componentsId', 'outdegree', 'superfirm']]
            ## 将链接数据和OUTDEGREE数据合并
            FirmNetdf = pd.merge(df, SuperFirm, on = 'superfirm', how = 'inner')
        
            FirmNetdf['outdegree'] = FirmNetdf['outdegree'].astype(float)
            criterial = FirmNetdf.outdegree == 0
            FirmNetworkdf = FirmNetdf[criterial]
    
            NetOutdegree.append(FirmNetworkdf)
        except ValueError as r:
            pass
    except (FileNotFoundError, OSError) as e:
        print("No such file or directory")
        pass
    
##将各地区的数据整合
FirmNetSpillover = pd.concat(NetOutdegree)
del NetOutdegree
FirmNetSpillover.to_stata('./FirmSpillover/FirmSpillover%s.dta' % '2005', write_index = False)


##2006
NetOutdegree = []
prodNum = pd.read_stata("./FirmProduction/firmprodNum%s.dta" % '2006')

location = pd.read_excel("locationlst%s.xls" % '2006', header = None)
location.columns = ['city', 'location']
locationlst = list(location['location'])
del location

for loc in locationlst:
    try:
        with open('./Identify%s/loc%sdata.csv' % ('2006', loc), 'rt', encoding = "utf-8") as csvfile:
            df = list(csv.reader(csvfile))
            header, values = df[0], df[1:]
            index = [i[0] for i in values]
            values =[i[1:] for i in values]
            dataf = DataFrame(values, columns = header[1:], index = index)
        df = dataf.unstack().reset_index()
        df['cityid'] = str(loc)
        df.columns = ['firm', 'subfirm', 'children', 'location']
        df['children'] = df['children'].astype(float)
        ## 仅保留存在链接的数据
        links = df['children'] == 1
        df = df[links]
        ## 将产品个数进行匹配
        df = pd.merge(df, prodNum, on = ['firm', 'location'], how = 'inner')
        df.rename(columns = {'firm':'superfirm','subfirm':'firm','prodNum':'SuperNum'}, inplace = True)

        df = pd.merge(df, prodNum, on = ['firm', 'location'],how = 'inner')

        df.rename(columns = {'firm':'subfirm','prodNum':'SubNum'}, inplace = True)
        
        ## 构建有向网络
        subfirmlst = df['subfirm']
        superfirmlst = df['superfirm']

        linkslst = list(zip(subfirmlst, superfirmlst))

        g = nx.DiGraph(name = "Product Set Network for Each Firm") #有向网络图
        g.add_edges_from(linkslst)
        
        ## 生成OUTDEGREE和INDEGREE
        firmComponents = list(nx.weakly_connected_component_subgraphs(g))
        firmoutdegree = [dict(j.out_degree()) for j in firmComponents]

        firms = [list(j.keys()) for j in firmoutdegree]
        outdegrees = [list(j.values()) for j in firmoutdegree]

        components = [list(j) for j in enumerate(firmoutdegree)]
        componentsId = [j[0] for j in components]


        lst = list(map(get_dataframe, firms, outdegrees))
        ##使用pd.concat()对数据整合
        try:
            SuperFirm = pd.concat(lst, keys = componentsId)
            SuperFirm = SuperFirm.reset_index()
            SuperFirm.columns = ['componentsId', 'level', 'outdegree', 'superfirm']
            SuperFirm = SuperFirm[['componentsId', 'outdegree', 'superfirm']]
            ## 将链接数据和OUTDEGREE数据合并
            FirmNetdf = pd.merge(df, SuperFirm, on = 'superfirm', how = 'inner')
        
            FirmNetdf['outdegree'] = FirmNetdf['outdegree'].astype(float)
            criterial = FirmNetdf.outdegree == 0
            FirmNetworkdf = FirmNetdf[criterial]
    
            NetOutdegree.append(FirmNetworkdf)
        except ValueError as r:
            pass
    except (FileNotFoundError, OSError) as e:
        print("No such file or directory")
        pass
    
##将各地区的数据整合
FirmNetSpillover = pd.concat(NetOutdegree)
del NetOutdegree
FirmNetSpillover.to_stata('./FirmSpillover/FirmSpillover%s.dta' % '2006', write_index = False)

##2007
NetOutdegree = []
prodNum = pd.read_stata("./FirmProduction/firmprodNum%s.dta" % '2007')

location = pd.read_excel("locationlst%s.xls" % '2007', header = None)
location.columns = ['city', 'location']
locationlst = list(location['location'])
del location

for loc in locationlst:
    try:
        with open('./Identify%s/loc%sdata.csv' % ('2007', loc), 'rt', encoding = "utf-8") as csvfile:
            df = list(csv.reader(csvfile))
            header, values = df[0], df[1:]
            index = [i[0] for i in values]
            values =[i[1:] for i in values]
            dataf = DataFrame(values, columns = header[1:], index = index)
        df = dataf.unstack().reset_index()
        df['cityid'] = str(loc)
        df.columns = ['firm', 'subfirm', 'children', 'location']
        df['children'] = df['children'].astype(float)
        ## 仅保留存在链接的数据
        links = df['children'] == 1
        df = df[links]
        ## 将产品个数进行匹配
        df = pd.merge(df, prodNum, on = ['firm', 'location'], how = 'inner')
        df.rename(columns = {'firm':'superfirm','subfirm':'firm','prodNum':'SuperNum'}, inplace = True)

        df = pd.merge(df, prodNum, on = ['firm', 'location'],how = 'inner')

        df.rename(columns = {'firm':'subfirm','prodNum':'SubNum'}, inplace = True)
        
        ## 构建有向网络
        subfirmlst = df['subfirm']
        superfirmlst = df['superfirm']

        linkslst = list(zip(subfirmlst, superfirmlst))

        g = nx.DiGraph(name = "Product Set Network for Each Firm") #有向网络图
        g.add_edges_from(linkslst)
        
        ## 生成OUTDEGREE和INDEGREE
        firmComponents = list(nx.weakly_connected_component_subgraphs(g))
        firmoutdegree = [dict(j.out_degree()) for j in firmComponents]

        firms = [list(j.keys()) for j in firmoutdegree]
        outdegrees = [list(j.values()) for j in firmoutdegree]

        components = [list(j) for j in enumerate(firmoutdegree)]
        componentsId = [j[0] for j in components]


        lst = list(map(get_dataframe, firms, outdegrees))
        ##使用pd.concat()对数据整合
        try:
            SuperFirm = pd.concat(lst, keys = componentsId)
            SuperFirm = SuperFirm.reset_index()
            SuperFirm.columns = ['componentsId', 'level', 'outdegree', 'superfirm']
            SuperFirm = SuperFirm[['componentsId', 'outdegree', 'superfirm']]
            ## 将链接数据和OUTDEGREE数据合并
            FirmNetdf = pd.merge(df, SuperFirm, on = 'superfirm', how = 'inner')
        
            FirmNetdf['outdegree'] = FirmNetdf['outdegree'].astype(float)
            criterial = FirmNetdf.outdegree == 0
            FirmNetworkdf = FirmNetdf[criterial]
    
            NetOutdegree.append(FirmNetworkdf)
        except ValueError as r:
            pass
    except (FileNotFoundError, OSError) as e:
        print("No such file or directory")
        pass
    
##将各地区的数据整合
FirmNetSpillover = pd.concat(NetOutdegree)
del NetOutdegree
FirmNetSpillover.to_stata('./FirmSpillover/FirmSpillover%s.dta' % '2007', write_index = False)
