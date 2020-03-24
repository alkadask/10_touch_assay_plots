#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 16:45:37 2019

@author: alkadas
"""

import matplotlib.pyplot as plt
import xlrd
import numpy as np
import seaborn as sns
import pandas as pd


filename = 'Sample_Data'
book = xlrd.open_workbook('C:/Users/alaka/Google Drive/Touch_tests/'+filename+'.xlsx')
sheets = book.sheet_names()
strain = []
date = []
for sheet in sheets:
    name = sheet.split('_')
    if name[0] not in date: date = np.append(date, name[0])
    if name[1] not in strain: strain = np.append(strain, name[1])
    
    
#raster plot of touch response data
plt.figure(figsize=(len(strain)*2,len(date)*5))
i=1
for sheet in sheets:
    s = book.sheet_by_name(sheet)
    b=[0]*25
    for y in range(0,25): 
        row = s.row_values(y)[0:10]
        a=[]
        for x in range(0,10):
            if row[x]==1: a = np.append(a, x+1)
            else: a = np.append(a, -1)
        b[y] = a
    ax=plt.subplot(len(date),len(strain),i)
    ax.set_title(sheet)
    ax.set_yticklabels([])
    ax.set_yticks([])
    ax.set_xticks(np.arange(1,11))
    ax.set_xticklabels(['A','P','A','P','A','P','A','P','A','P'])
    ax.axis([0.5, 10.5, -1, 25])
    ax.eventplot(b, orientation='horizontal', lineoffsets=1, linelengths=0.5, linewidths=5, colors='black', linestyles='solid')
    i=i+1  
plt.savefig('C:/Users/alaka/Google Drive/Touch_tests/'+filename+'_Rasterplot.png')


#create pandas dataframe of aggregate individual responses and plot bar graphs
df = pd.DataFrame()
for sheet in sheets:
    s = book.sheet_by_name(sheet)
    col = s.col_values(10)[0:25]
    df1 = pd.DataFrame({'Date':[sheet.split('_')[0]]*25, 'Strain':[sheet.split('_')[1]]*25, 'Touch_response':col}, columns=['Date','Strain','Touch_response'])
    df = df.append(df1)
plt.figure(figsize=(len(strain)*3,5))
ax1 = plt.subplot(121)
ax1.set_title('Overall mean touch response')
sns.barplot(x='Strain', y='Touch_response', data=df, estimator=np.mean, ci='sd', palette=sns.hls_palette(len(strain), l=.5, s=.7))

ax2 = plt.subplot(122)
ax2.set_title('Daily mean touch response')
sns.barplot(x='Strain', y='Touch_response', hue='Date', data=df, estimator=np.mean, ci='sd',palette='gray')
plt.savefig('C:/Users/alaka/Google Drive/Touch_tests/'+filename+'_Barplot.png')
