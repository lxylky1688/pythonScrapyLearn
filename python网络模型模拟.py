# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 16:54:25 2017

@author: Administrator
"""

###Python中的一个简单动态模型
import sys
import os
import networkx as net
import matplotlib.pyplot as plot
import matplotlib.colors as colors
import random as r

#首先构造一个类-人的定义
class Person(object):
    def __init__(self, id):        
        #从一个单一偏好开始
        self.id = id
        self.i = r.random()
        self.a = self.i
        ##将初始意见和随后的信息对等
        self.alpha = 0.6 #轻信因子
    def __str__(self):
        return(str(self.id))


density = 0.1
g = nx.Graph()

##构造一个以人为对象的网络
for i in range(10):
    p = Person(i)
    g.add_node(p)
    
#构造一个简单的随机网络，没对节点之间的链接概率相同
for x in g.nodes():
    for y in g.nodes():
        if r.random() <= density:
            g.add_edge(x, y)
                
##画出这个生成网络并按照节点的数字给节点赋予颜色
col = [n.a for n in g.nodes()]
pos = nx.spring_layout(g)
nx.draw_networkx(g, pos = pos, node_color = col)

plt.axis('off')
plt.show()
plt.clf()
plt.close()

##扩展模型
#首先构造一个类-人的定义
class Person(object):
    def __init__(self, id):        
        #从一个单一偏好开始
        self.id = id
        self.i = r.random()
        self.a = self.i
        ##将初始意见和随后的信息对等
        self.alpha = 0.6 #轻信因子
    def __str__(self):
        return(str(self.id))
        
    def step(self):
        ###loop through the neighbors and aggregate their preferences
        neighbors = g[self]
        w = 1/float((len(neighbors) + 1))
        s = w * self.a
        for node in neighbors:
            s += w * self.a
            
        #更新我的意见为初始意见加上所有其他影响
        self.a = (1 - self.alpha) * self.i + self.alpha * s
        
        
for i in range(30):
    ## 循环遍历所有的网络节点并让它们走一步
    for node in g.nodes():
        node.step()
    ## 汇总演化的态度数值，然后输出到终端并画出结果
    col = [n.a for n in g.nodes()]
    print(col)
    plot.plot(col)
    
    
## 中间影响者
    
class Influencer(Person):
    def __init__(self, id):
        self.id = id
        self.i = r.random()
        self.a = 1 ## 他们的意见很强并且不可动摇
        
    def step(self):
        pass
    

    
