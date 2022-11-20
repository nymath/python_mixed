# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 16:01:21 2022

@author: ChaoyiZhao

此为《量化投资》教材第5.9节《案例：构建一个沪深300指数增强基金》所用代码之四：
“ch5 - case - Step4 - BackTest.py”。

【本代码为本案例的第四步，功能包括：】
1. 策略样本外（2015-2020）回测，输出各类策略统计指标。

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

# 读取策略权重数据（测试集：2015-2020）
data_weight = pd.read_csv('plus_weight_list_IC_constraint.csv', index_col = 0, parse_dates = True)
data_weight = data_weight.loc['2014-12-31': '2020-12-31']
# 读取股票未来周收益率数据
data_future_return = pd.read_csv('future_return_list_IC_constraint.csv', index_col = 0, parse_dates = True)
data_future_return = data_future_return.loc['2014-12-31': '2020-12-31']

# 持仓总价值
value_list = pd.Series(index = data_weight.index)
value_list.iloc[0] = 1

# 调仓前持仓各个股票价值与调仓后持仓各个股票价值（用于计算换手率）
value_each_list_before = pd.DataFrame(columns = data_weight.columns, index = data_weight.index )
value_each_list_after = pd.DataFrame(columns = data_weight.columns, index = data_weight.index )

# 各期持股数
hold_num_list = pd.Series(index = data_weight.index)

# 滚动回测
for date in range(len(data_weight.index)-1):
    temp_date = data_weight.index[date]
    next_date = data_weight.index[date+1]
    
    # 记录每期调仓后持仓各个股票价值
    value_each_list_after.loc[temp_date] = data_weight.loc[temp_date] * value_list.loc[temp_date]
    # 记录每期调仓前持仓各个股票价值
    value_each_list_before.loc[next_date] = value_each_list_after.loc[temp_date] * (1+data_future_return.loc[next_date])
    # 记录持仓总价值
    value_list.loc[next_date] = np.sum(value_each_list_before.loc[next_date])
    # 记录持股数
    hold_num_list.loc[temp_date] = np.sum(data_weight.loc[temp_date] > 1e-5)

value_each_list_before = value_each_list_before.fillna(0)
value_each_list_after = value_each_list_after.fillna(0)

# 计算并绘制换手率
turnover = np.sum( np.abs( value_each_list_after - value_each_list_before ), axis=1) / 2 / value_list
turnover = turnover.iloc[1:-1]
plt.figure(figsize = (20,10))
plt.grid()
plt.plot(turnover, linewidth = 4)
plt.xlabel(r'时间', fontsize = 30)
plt.ylabel(r'换手率', fontsize = 30)
plt.savefig('case_multifactor_turnover.png', bbox_inches = 'tight' , dpi=150)
print('平均换手率', turnover.mean())

# 绘制各期持股数
plt.figure(figsize = (20,10))
plt.grid()
plt.plot(hold_num_list, linewidth = 4)
plt.xlabel(r'时间', fontsize = 30)
plt.ylabel(r'持股数', fontsize = 30)
plt.savefig('case_multifactor_holdstock.png', bbox_inches = 'tight' , dpi=150)
print('平均持股数', hold_num_list.mean())

# 绘制P&L
data_benchmark = pd.read_excel('沪深300指数.xlsx', index_col = 2)
data_benchmark = data_benchmark.loc['2014-12-31': '2020-12-31']
data_benchmark = data_benchmark['收盘价(元)']
data_benchmark = data_benchmark / data_benchmark.iloc[0]


fig, ax1 = plt.subplots(figsize = (20,10))
plt.grid(axis='x')
plt.xlabel('时间', fontsize = 30)
ax2 = ax1.twinx()
ax2.grid()
ax1.plot(data_benchmark, linewidth = 4, label = '沪深300')
ax1.plot(value_list, linewidth = 4, linestyle = '--', label = '指数增强策略')
ax2.plot(value_list - data_benchmark, linewidth = 4, linestyle = ':', label = '超额净值', color = 'tab:green')
ax1.legend(fontsize = 30, loc = 'upper left')
ax2.legend(fontsize = 30, loc = 'upper right')
ax1.set_ylabel("净值 (初始为1)", fontsize = 30)
ax2.set_ylabel("超额净值", fontsize = 30)
ax1.set_ylim(0,4.5)
ax2.set_ylim(-0.5,4.0)

plt.savefig('case_multifactor_pnl.png', bbox_inches = 'tight' , dpi=150)

# 计算最大回撤
MDDport = np.max(value_list.cummax() - value_list)
MDDhs300 = np.max(data_benchmark.cummax() - data_benchmark)
MDDexcess = np.max((value_list - data_benchmark).cummax() - (value_list - data_benchmark))
print('最大回撤')
print('投资组合: ', MDDport)
print('benchmark: ', MDDhs300)
print('超额: ', MDDexcess)


###### 评判指标

# 无风险收益率数据
riskfreedata = pd.read_excel('十年期国债收益率.xlsx', index_col = 0, parse_dates = True)
riskfreedata = riskfreedata['收盘'].sort_index()
riskfreedata = riskfreedata.loc['2014-12-31': '2020-12-31']
riskfreedata = riskfreedata / 100
riskfreedata = riskfreedata.loc[value_list.index]
annual_riskfree_mean = riskfreedata.resample('y').mean()
all_riskfree_mean = riskfreedata.mean()

data_stock = pd.concat( [value_list, data_benchmark], axis=1 )
data_stock.columns = ['投资组合', '沪深300']

# 每周连续复利收益率
log_return = np.log(data_stock) - np.log(data_stock.shift(1))
###########

# 各年收益率
annual_log_return_mean = log_return.resample('y').mean() * 52
annual_log_return_std = log_return.resample('y').std() * np.sqrt(52)

# 总收益率
all_log_return_mean = log_return.mean() * 52
all_log_return_std = log_return.std() * np.sqrt(52)

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
    excess_return[s] = log_return[s] - riskfreedata / 52

excess_rm = log_return['沪深300'] - riskfreedata / 52

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
alpha_list = alpha_list * 52 
sigma_epsilon_list = epsilon_list.std() * np.sqrt(52)

# Treynor ratio
all_log_return_Treynor = ( all_log_return_mean - all_riskfree_mean ) / beta_list
# Information ratio
all_log_return_IR = alpha_list / sigma_epsilon_list



#########################
# 结果整合

res = pd.DataFrame(index = ['投资组合', '沪深300'],
                   columns = ['平均收益率', '标准差', '夏普比率', 'alpha', 'beta', '特雷诺比率', '信息比率', '最大回撤'])
res['平均收益率'] = all_log_return_mean
res['标准差'] = all_log_return_std
res['夏普比率'] = all_log_return_Sharpe
res['alpha'] = alpha_list
res['beta'] = beta_list
res['特雷诺比率'] = all_log_return_Treynor
res['信息比率'] = all_log_return_IR
res['最大回撤'] = [MDDport, MDDhs300]

res.to_csv('case_result_metrics_ch5.csv', encoding='gbk')

annual_log_return_mean.T.to_csv('case_average_return_ch5.csv', encoding='gbk')
annual_log_return_std.T.to_csv('case_std_return_ch5.csv', encoding='gbk')


######### 绘制沪深300的图像

data_benchmark = pd.read_excel('沪深300指数.xlsx', index_col = 2)
data_benchmark = data_benchmark.loc['2010-12-31': '2020-12-31']
data_benchmark = data_benchmark['收盘价(元)']
plt.figure(figsize = (20,10))
plt.grid()
plt.plot(data_benchmark, linewidth = 4)
plt.xlabel(r'时间', fontsize = 30)
plt.ylabel(r'沪深300指数', fontsize = 30)
plt.savefig('case_multifactor_hs300.png', bbox_inches = 'tight' , dpi=150)


