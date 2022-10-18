# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 17:40:54 2022

@author: ChaoyiZhao

此为《量化投资》教材第5.9节《案例：构建一个沪深300指数增强基金》所用代码之二：
“ch5 - case - Step2 - SingleFactorTest.py”。

【本代码为本案例的第二步，功能包括：】
1. 计算流通市值与账面市值比在样本内（2011-2014）的IC时间序列的统计指标：均值、标准差、ICIR，并绘制IC与IC累积值的时间序列图像；
2. 绘制流通市值与账面市值比在样本内（2011-2014）的分层回测P&L图像。

非常欢迎同学们指出代码以及教材中的问题！如有问题或建议，可以联系编者 zhaochaoyi@pku.edu.cn

此版本用于2022年秋季学期北京大学数学科学学院“量化交易”课程。
更新日期：2022年10月9日

Copyright: 孙健 吴岚 赵朝熠

"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

plt.rcParams['font.sans-serif']=['Microsoft YaHei']
plt.rcParams['axes.unicode_minus']=False

matplotlib.rc('xtick', labelsize=30)
matplotlib.rc('ytick', labelsize=30)


# 读取样本内（2011-2014）的IC时间序列
data = pd.read_csv('FFfactorreturn.csv', index_col = 0, parse_dates = True, encoding = 'gbk')
data = data.loc['2010-12-31': '2014-12-31']
data = data[['IC_cap', 'IC_bp', 'rankIC_cap', 'rankIC_bp']]

# 计算两种因子的IC和rankIC的时间序列的均值、标准差和ICIR
ICsummary = pd.DataFrame( index = ['mean', 'std', 'ICIR'], columns = ['IC_cap', 'IC_bp', 'rankIC_cap', 'rankIC_bp'] )
ICsummary.loc['mean'] = data.mean()
ICsummary.loc['std'] = data.std()
ICsummary.loc['ICIR'] = data.mean() / data.std()

ICsummary.to_csv('ICsummary.csv')


# 绘制样本内两种因子的IC与rankIC时间序列
labels = ['流通市值 IC', '账面市值比 IC', '流通市值 rank IC', '账面市值比 rank IC']
fig = plt.figure(figsize = (25,18))
for i in range(len(data.columns)):
    temp_col = data.columns[i]
    ax1 = fig.add_subplot(4,1,i+1) 
    ax1.grid()
    ax1.plot(data[temp_col], linewidth = 3, label = labels[i])
    ax1.set_ylim(-0.3, 0.3)
    ax1.legend(fontsize = 30, loc = 'upper left')
    
plt.savefig('case_multifactor_ICseries.png', bbox_inches = 'tight' , dpi=150)

# 绘制样本内两种因子的IC与rankIC累积值时间序列
fig = plt.figure(figsize = (20,14))
ax1 = fig.add_subplot(2,1,1) 
ax1.grid()
ax1.plot(data['rankIC_cap'].cumsum(), linewidth = 3, label = '流通市值累积 rank IC')
ax1.legend(fontsize = 30, loc = 'upper right')
ax1 = fig.add_subplot(2,1,2) 
ax1.grid()
ax1.plot(data['rankIC_bp'].cumsum(), linewidth = 3, label = '账面市值比累积 rank IC')
ax1.legend(fontsize = 30, loc = 'upper right')

plt.savefig('case_multifactor_ICcumsum.png', bbox_inches = 'tight' , dpi=150)


# 绘制样本内按流通市值来分层得到的5个组合的P&L时间序列
data = pd.read_csv('groupcapreturn.csv', index_col = 0, parse_dates = True, encoding = 'gbk')
data = data.loc['2010-12-31': '2014-12-31']
data = data.fillna(0)
data = data + 1
data = data.cumprod()

plt.figure(figsize = (20,10))
for i in range(len(data.columns)):
    plt.grid()
    plt.plot(data[data.columns[i]], linewidth = 3, label = data.columns[i], c = 'black', alpha = i/6+0.2)
plt.xlabel(r'时间', fontsize = 30)
plt.ylabel(r'分层累积收益', fontsize = 30)
plt.legend(fontsize = 30, loc = 'upper left')
        
plt.savefig('case_multifactor_cap_layer.png', bbox_inches = 'tight' , dpi=150)


# 绘制样本内按账面市值比来分层得到的5个组合的P&L时间序列
data = pd.read_csv('groupbpreturn.csv', index_col = 0, parse_dates = True, encoding = 'gbk')
data = data.loc['2010-12-31': '2014-12-31']
data = data.fillna(0)
data = data + 1
data = data.cumprod()

plt.figure(figsize = (20,10))
for i in range(len(data.columns)):
    plt.grid()
    plt.plot(data[data.columns[i]], linewidth = 3, label = data.columns[i], c = 'black', alpha = i/6+0.2)
plt.xlabel(r'时间', fontsize = 30)
plt.ylabel(r'分层累积收益', fontsize = 30)
plt.legend(fontsize = 30, loc = 'upper left')
    
plt.savefig('case_multifactor_bp_layer.png', bbox_inches = 'tight' , dpi=150)




