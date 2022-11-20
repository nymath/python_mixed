# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 12:59:34 2022

@author: ChaoyiZhao

此为《量化投资》教材第2.8节《案例：两资产等权重投资组合》所用代码。
非常欢迎同学们指出代码以及教材中的问题！如有问题或建议，可以联系编者 zhaochaoyi@pku.edu.cn

此版本用于2022年秋季学期北京大学数学科学学院“量化交易”课程。
更新日期：2022年9月20日

Copyright: 孙健 吴岚 赵朝熠
"""

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib

plt.rcParams['font.sans-serif']=['Microsoft YaHei']
plt.rcParams['axes.unicode_minus']=False

matplotlib.rc('xtick', labelsize=30)
matplotlib.rc('ytick', labelsize=30)


################ 第2章案例：等权重投资组合



"""
运行前，请将工作路径设置为本代码所在文件夹。
"""

# 创建结果保存路径
result_path = 'result/'
if not os.path.exists(result_path):   
    os.mkdir(result_path)
    

#### 股票数据
timeframe_s = '2010-12-31'
timeframe_e = '2021-01-01'

data1 = pd.read_excel('平安银行.xlsx', index_col = 2)['收盘价(元)']
data1 = data1.loc[timeframe_s:timeframe_e]
data2 = pd.read_excel('万科A.xlsx', index_col = 2)['收盘价(元)']
data2 = data2.loc[timeframe_s:timeframe_e]
data_stock = pd.merge(data1, data2, left_index=True, right_index=True)
data_stock.columns = ['平安银行', '万科A']

# 无风险收益率数据
riskfreedata = pd.read_excel('十年期国债收益率.xlsx', index_col = 0)
riskfreedata = riskfreedata['收盘'].sort_index()
riskfreedata = riskfreedata.loc[data_stock.index]
riskfreedata = riskfreedata / 100
annual_riskfree_mean = riskfreedata.resample('y').mean()
all_riskfree_mean = riskfreedata.mean()

# 市场指数数据
data_m = pd.read_excel('上证综指.xlsx', index_col = 2)['收盘价(元)']
data_m = data_m.loc[data_stock.index]
# 每日连续复利收益率
data_rm = np.log(data_m) - np.log(data_m.shift(1))
data_rm.name = '上证综指'

###########
# 策略：等权重
data_stock = data_stock / data1.iloc[0] * 10
data_stock['portfolio'] = 0.5 * data_stock['平安银行'] + 0.5 * data_stock['万科A']
# 每日连续复利收益率
log_return = np.log(data_stock) - np.log(data_stock.shift(1))
log_return = pd.merge(log_return, data_rm, left_index = True, right_index = True)
###########

# 各年收益率
annual_log_return_mean = log_return.resample('y').mean() * 252
annual_log_return_std = log_return.resample('y').std() * np.sqrt(252)

# 总收益率
all_log_return_mean = log_return.mean() * 252
all_log_return_std = log_return.std() * np.sqrt(252)

# 各年夏普比
annual_log_return_Sharpe = annual_log_return_mean.copy()
for s in annual_log_return_Sharpe.columns:
    annual_log_return_Sharpe[s] = ( annual_log_return_mean[s] - annual_riskfree_mean ) / annual_log_return_std[s]

# 总夏普比
all_log_return_Sharpe = ( all_log_return_mean - all_riskfree_mean ) / all_log_return_std

###########
# CAPM
import statsmodels.api as sm

excess_return = log_return.copy()
for s in log_return.columns:
    excess_return[s] = log_return[s] - riskfreedata / 252

excess_rm = data_rm - riskfreedata / 252

beta_list = all_log_return_Sharpe.copy()
alpha_list = all_log_return_Sharpe.copy()
beta_p_list = all_log_return_Sharpe.copy()
alpha_p_list = all_log_return_Sharpe.copy()
epsilon_list = log_return.copy()
for s in beta_list.index:
    X = sm.add_constant(excess_rm.values[1:])
    Y = excess_return[s].values[1:]
    model = sm.OLS(Y,X)
    results = model.fit()
    beta_list[s] = results.params[1]
    alpha_list[s] = results.params[0]
    beta_p_list[s] = results.pvalues[1]
    alpha_p_list[s] = results.pvalues[0]
    epsilon_list[s] = excess_return[s] - beta_list[s] * excess_rm - alpha_list[s]
    print(results.summary())
alpha_list = alpha_list * 252 
sigma_epsilon_list = epsilon_list.std() * np.sqrt(252)

# Treynor ratio
all_log_return_Treynor = ( all_log_return_mean - all_riskfree_mean ) / beta_list
# Information ratio
all_log_return_IR = alpha_list / sigma_epsilon_list

###########
# PNL曲线
start_money = 10
money_list = np.exp(log_return).cumprod()
money_list.iloc[0] = 1
money_list = money_list * start_money

plt.figure(figsize = (20,10))
plt.grid()
plt.plot(money_list['portfolio'], linewidth = 5, label = '等权重组合')
plt.plot(money_list['平安银行'], linewidth = 4, linestyle = '-.', label = '平安银行')
plt.plot(money_list['万科A'], linewidth = 4, linestyle = ':', label = '万科A')
plt.plot(data_m/data_m.iloc[0]*start_money, linewidth = 3, linestyle = '--', label = '上证综指')
plt.ylabel(r'资金量 $V_t$ (万元)', fontsize = 30)
plt.xlabel(r'时间', fontsize = 30)
plt.legend(fontsize = 30, loc = 'upper left')
plt.savefig(result_path+'case_2_pnl.png', bbox_inches = 'tight' , dpi=150)



# 两股票权重
plt.figure(figsize = (20,10))
plt.grid()
weight_payh = money_list['平安银行'] / (money_list['平安银行']+money_list['万科A'])
plt.plot(weight_payh, linewidth = 5, label = '持有平安银行的权重')
plt.plot(1-weight_payh, linewidth = 5, label = '持有万科A的权重')
plt.ylabel(r'权重', fontsize = 30)
plt.xlabel(r'时间', fontsize = 30)
plt.legend(fontsize = 30, loc = 'upper left')
plt.savefig(result_path+'case_2_weight_trend.png', bbox_inches = 'tight' , dpi=150)




# 最大回撤
MDD_list = all_log_return_Sharpe.copy()

for s in money_list.columns:
    temp_list = money_list[s]
    MDD_list[s] = np.max(temp_list.cummax() - temp_list)

#########################
# 结果整合

res = pd.DataFrame(index = ['平安银行', '万科A', 'portfolio','上证综指'],
                   columns = ['平均收益率', '标准差', '夏普比率', 'alpha', 'beta', '特雷诺比率', '信息比率', '最大回撤'])
res['平均收益率'] = all_log_return_mean
res['标准差'] = all_log_return_std
res['夏普比率'] = all_log_return_Sharpe
res['alpha'] = alpha_list
res['beta'] = beta_list
res['特雷诺比率'] = all_log_return_Treynor
res['信息比率'] = all_log_return_IR
res['最大回撤'] = MDD_list

res.to_csv(result_path+'case_2_result_metrics.csv', encoding='gbk')

annual_log_return_mean.T.to_csv(result_path+'case_2_average_return.csv', encoding='gbk')
annual_log_return_std.T.to_csv(result_path+'case_2_std_return.csv', encoding='gbk')



