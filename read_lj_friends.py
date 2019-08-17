# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 14:54:37 2017

@author: Administrator
"""

import os

os.chdir('D:\pydata-book-2nd-edition\identifyFirm')
cwd = os.getcwd()

from pandas import DataFrame, Series

import pandas as pd; import numpy as np

import csv #使用内置的CSV库

name = 'valerois'
with open('./Identify2001/friendship.txt', 'rt', encoding="utf-8") as csvfile:
    
    for line in csvfile.readlines():

        if line.startswith('#'): continue
        parts = line.split()                           
        if len(parts) == 0: continue
        if parts[0] == '<':
            g.add_edge(parts[1], name)
        else:
            g.add_edge(name, parts[1])
    