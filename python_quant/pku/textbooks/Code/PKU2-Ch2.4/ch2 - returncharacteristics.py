# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 22:48:04 2022

@author: ChaoyiZhao

此为《量化投资》教材第2.4节《股票收益率特征性事实》所用代码。
非常欢迎同学们指出代码以及教材中的问题！如有问题或建议，可以联系编者 zhaochaoyi@pku.edu.cn

此版本用于2022年秋季学期北京大学数学科学学院“量化交易”课程。
更新日期：2022年9月20日

Copyright: 孙健 吴岚 赵朝熠
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats 
import os


plt.rcParams['font.sans-serif']=['Microsoft YaHei']
plt.rcParams['axes.unicode_minus']=False


"""
运行前，请将工作路径设置为本代码所在文件夹。
"""

# 创建结果保存路径
result_path = 'result/'
if not os.path.exists(result_path):   
    os.mkdir(result_path)
    
#############################
### 日频数据
data = pd.read_excel("000001.xlsx", index_col = 2)
data = data.loc[:'2021-01-01']
close_price = data['收盘价(元)']

# 平安银行收盘价走势
plt.figure(figsize = (24,10))
plt.grid()
plt.xticks(fontsize = 40)
plt.yticks(fontsize = 40)
plt.plot(close_price, linewidth = 3)
plt.savefig(result_path+'000001.png', bbox_inches = 'tight' , dpi=100, pad_inches = 0.0)


# 平安银行日收益率时序
daily_return = close_price / close_price.shift(1) - 1
daily_return = daily_return.dropna()
plt.figure(figsize = (24,8))
plt.grid()
plt.xticks(fontsize = 40)
plt.yticks(fontsize = 40)
plt.ylim(-0.45, 0.45)
plt.plot(daily_return)

plt.savefig(result_path+'000001returntimeseries.png', bbox_inches = 'tight' , dpi=100, pad_inches = 0.0)


# 平安银行日收益率直方图
plt.figure(figsize = (24,16))
plt.grid()
plt.xticks(fontsize = 50)
plt.yticks(fontsize = 50)
plt.xlim(-0.15, 0.15)
daily_return.hist(bins = 101, density = True, alpha=0.5)
mean = np.mean(daily_return)
std = np.std(daily_return)
normalxrange = np.arange(-0.15, 0.15, 0.001)
plt.plot( normalxrange,  stats.norm.pdf(normalxrange, loc = mean, scale = std), linewidth = 8)
plt.ylabel(r'密度', fontsize = 50)
print(daily_return.describe())
print('skew:', daily_return.skew())
print('kurt:', daily_return.kurt())
print('autocoef:', np.corrcoef(daily_return[1:], daily_return[:-1])[0,1])
print('autocoef2:', np.corrcoef(daily_return[1:]**2, daily_return[:-1]**2)[0,1])

print('annualized_mean: ', daily_return.describe()['mean']*252)
print('annualized_std: ', daily_return.describe()['std']*np.sqrt(252))

plt.savefig(result_path+'000001returnhistdaily.png', bbox_inches = 'tight' , dpi=100, pad_inches = 0.0)


# 平安银行周收益率直方图
week_price = close_price.resample('w').first()
week_return = week_price / week_price.shift(1) - 1
week_return = week_return.dropna()
plt.figure(figsize = (24,16))
plt.grid()
plt.xticks(fontsize = 50)
plt.yticks(fontsize = 50)
plt.xlim(-0.3, 0.3)
week_return.hist(bins = 50, density = True, alpha=0.5)
mean = np.mean(week_return)
std = np.std(week_return)
normalxrange = np.arange(-0.3, 0.3, 0.001)
plt.plot( normalxrange,  stats.norm.pdf(normalxrange, loc = mean, scale = std), linewidth = 8)
plt.ylabel(r'密度', fontsize = 50)

print(week_return.describe())
print('skew:', week_return.skew())
print('kurt:', week_return.kurt())
print('autocoef:', np.corrcoef(week_return[1:], week_return[:-1])[0,1])
print('autocoef2:', np.corrcoef(week_return[1:]**2, week_return[:-1]**2)[0,1])

print('annualized_mean: ', week_return.describe()['mean']*52)
print('annualized_std: ', week_return.describe()['std']*np.sqrt(52))

plt.savefig(result_path+'000001returnhistweek.png', bbox_inches = 'tight' , dpi=100, pad_inches = 0.0)



# 平安银行月收益率直方图
month_price = close_price.resample('m').first()
month_return = month_price / month_price.shift(1) - 1
month_return = month_return.dropna()
plt.figure(figsize = (24,16))
plt.grid()
plt.xticks(fontsize = 50)
plt.yticks(fontsize = 50)
plt.xlim(-0.5, 0.5)
month_return.hist(bins = 50, density = True, alpha=0.5)
mean = np.mean(month_return)
std = np.std(month_return)
normalxrange = np.arange(-0.5, 0.5, 0.001)
plt.plot( normalxrange,  stats.norm.pdf(normalxrange, loc = mean, scale = std), linewidth = 8)
plt.ylabel(r'密度', fontsize = 50)

print(month_return.describe())
print('skew:', month_return.skew())
print('kurt:', month_return.kurt())
print('autocoef:', np.corrcoef(month_return[1:], month_return[:-1])[0,1])
print('autocoef2:', np.corrcoef(month_return[1:]**2, month_return[:-1]**2)[0,1])

print('annualized_mean: ', month_return.describe()['mean']*12)
print('annualized_std: ', month_return.describe()['std']*np.sqrt(12))

plt.savefig(result_path+'000001returnhistmonth.png', bbox_inches = 'tight' , dpi=100, pad_inches = 0.0)





#############################
### 日内3秒快照中间价数据
data = pd.read_csv("000001_20200102_3秒.csv", index_col = 0)
data = data['mid_price']


# 平安银行日内走势
plt.figure(figsize = (24,10))
data.plot(linewidth = 3)
plt.grid()
locs, labels = plt.xticks()
plt.xticks(ticks = locs[1:-1], labels = [str(i)[-10:-5] for i in labels[1:-1]], fontsize = 40)
plt.yticks(fontsize = 40)
plt.xlabel("")
plt.savefig(result_path+'000001_20200102.png', bbox_inches = 'tight' , dpi=100, pad_inches = 0.0)


# 平安银行日内价格差分时序
intra_return = data - data.shift(1)
intra_return = intra_return.dropna()
plt.figure(figsize = (24,8))
intra_return.plot(linewidth = 3)
plt.grid()
locs, labels = plt.xticks()
plt.xticks(ticks = locs[1:-1], labels = [str(i)[-10:-5] for i in labels[1:-1]], fontsize = 40)
plt.yticks(fontsize = 40)
plt.ylim(-0.05, 0.05)
plt.xlabel("")
plt.savefig(result_path+'000001_20200102delta.png', bbox_inches = 'tight' , dpi=100, pad_inches = 0.0)

print(intra_return.describe())
print('skew:', intra_return.skew())
print('kurt:', intra_return.kurt())
print('autocoef:', np.corrcoef(intra_return[1:], intra_return[:-1])[0,1])
print('autocoef2:', np.corrcoef(intra_return[1:]**2, intra_return[:-1]**2)[0,1])

intra_return.count()