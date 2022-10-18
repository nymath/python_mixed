# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 17:42:01 2022

@author: ChaoyiZhao

此为《量化投资》教材第4.5节《案例：低beta择股策略》所用代码。
非常欢迎同学们指出代码以及教材中的问题！如有问题或建议，可以联系编者 zhaochaoyi@pku.edu.cn

此版本用于2022年秋季学期北京大学数学科学学院“量化交易”课程。
更新日期：2022年9月20日

Copyright: 孙健 吴岚 赵朝熠
"""



import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib
import os
from scipy import stats 
plt.rcParams['font.sans-serif']=['Microsoft YaHei']
plt.rcParams['axes.unicode_minus']=False

matplotlib.rc('xtick', labelsize=30)
matplotlib.rc('ytick', labelsize=30)


################ 第4章案例：低beta择股
#

"""
下面被注释掉的这段代码用于从Wind数据库中下载上证50历史成分股数据，
只有拥有Wind账号且配置好WindPy接口才能运行。
如果没有Wind，可以忽略这段代码。
"""

"""

from WindPy import w
import datetime

#################
# 从Wind提取数据
w.start()

data_sz50 = pd.read_excel('上证50月数据.xlsx', index_col = 2)
time_index = data_sz50.index[12:]

path_name = '上证50成分股收盘价/'
for i in range(len(time_index)-1):
    temp_time = time_index[i]
    next_time = time_index[i+1]
    print(temp_time)
    
    constituent = w.wset( 'sectorconstituent', options="date="+str(temp_time)+"; windcode=000016.SH", usedf=True)[1]
        
    temp_stock_list = list(constituent['wind_code'].values)
    temp_stock_name = list(constituent['sec_name'].values)
    listandname = pd.DataFrame([temp_stock_list, temp_stock_name]).T
    listandname = listandname.set_index(0)
    
    history_price = w.wsd(temp_stock_list, "close", temp_time - datetime.timedelta(days=100), next_time, "unit=1;currencyType=;Period=D;PriceAdj=F", usedf=True)
    
    if not os.path.exists(path_name):   
        os.mkdir(path_name)
    pd.concat([listandname, history_price]).to_csv(path_name + str(temp_time)[:10]+ '.csv', encoding='gbk')

"""






"""
运行前，请将工作路径设置为本代码所在文件夹。
"""

########### STEP 1: 读数据

# 提取每月最后一个交易日列表
month_index = os.listdir('上证50成分股收盘价')
month_index = [x[:10] for x in month_index]
month_index = pd.to_datetime(month_index)

# 读取上证指数日数据并计算收益率
data_szzs = pd.read_excel('上证指数日数据.xlsx', index_col = 2)
data_szzs = data_szzs['收盘价(元)']
data_szzs = data_szzs['2009-12-31': '2020-12-31']
return_szzs = data_szzs / data_szzs.shift(1) - 1

# 无风险日收益率
riskfreedata = pd.read_excel('十年期国债收益率.xlsx', index_col = 0)
riskfreedata = riskfreedata['收盘'].sort_index()
riskfreedata = riskfreedata / 100 / 252

########### STEP 2: 生成信号：选择10个低beta股票
beta_result_list = []
stock_choose_list = []
stock_choose_name_list = []

for i in range(len(month_index)):
    # 当前月
    temp_time = month_index[i]
    print(temp_time)
    
    # 读取当前月成分股收盘价数据
    temp_data = pd.read_csv('上证50成分股收盘价/'+str(temp_time)[:10]+'.csv', index_col=0, encoding='gbk')
    temp_stock_list = temp_data.columns
    listandname = temp_data.iloc[0]
    temp_price = temp_data.iloc[1:].astype('float')
    temp_price.index = pd.to_datetime(temp_price.index)
    
    # 提取历史51天
    history_price = temp_price.loc[:temp_time]
    history_price = history_price.iloc[-51:]
    
    # 计算历史50天日超额收益率
    history_return = history_price / history_price.shift(1) - 1
    history_return = history_return.dropna()
    history_ex_return = history_return.apply(lambda x: x - riskfreedata[history_return.index])
    history_rm_return = return_szzs[history_return.index]
    history_rm_ex_return = history_rm_return - riskfreedata[history_return.index]
    
    ### 对每只股票时间序列做线性回归估计beta
    # 自变量：(上证指数日超额收益率)+常数项
    temp_x = history_rm_ex_return.values
    temp_x = sm.add_constant(temp_x)
    
    beta_list = []
    for stock in history_ex_return.columns:
        # 因变量：个股日超额收益率
        temp_y = history_ex_return[stock].values
        res = sm.OLS(temp_y, temp_x).fit()
        # beta估计结果
        temp_beta = res.params[1]
        beta_list.append(temp_beta)
    
    # 汇总beta估计
    beta_result = pd.DataFrame( [history_return.columns, beta_list] ).T
    beta_result_list.append(beta_result)
    
    # 排序，取beta最小的10个股票
    stock_choose = list(beta_result.sort_values([1]).iloc[:10, 0].values)
    stock_choose_name = listandname.loc[stock_choose].values
    stock_choose_list.append(stock_choose)
    stock_choose_name_list.append(stock_choose_name)
    


########### STEP 3: 回测：计算该策略的每日收益率
temp_return_list = []

for i in range(len(month_index)):
    # 当前月
    temp_time = month_index[i]
    print(temp_time)
    
    # 读取当前月成分股收盘价数据
    temp_data = pd.read_csv('上证50成分股收盘价/'+str(temp_time)[:10]+'.csv', index_col=0, encoding='gbk')
    temp_stock_list = temp_data.columns
    listandname = temp_data.iloc[0]
    temp_price = temp_data.iloc[1:].astype('float')
    temp_price.index = pd.to_datetime(temp_price.index)
    
    # 提取未来1个月收盘价并计算收益率
    future_price = temp_price.loc[temp_time:]
    future_return = future_price / future_price.shift(1) - 1
    future_return.iloc[0,:] = 0
    
    # 提取选择的10个股票的未来收益率
    stock_choose = stock_choose_list[i]
    future_return = future_return[stock_choose]
    
    # 计算等权重持有一个月的组合收益率
    cum_pnl_each_stock = (1+future_return).cumprod()
    cum_pnl_portfolio = cum_pnl_each_stock.sum(axis=1) / 10
    temp_return = cum_pnl_portfolio / cum_pnl_portfolio.shift(1) - 1
    temp_return = temp_return.iloc[1:]
    
    temp_return_list.append(temp_return)

# 汇总组合在各个时间的收益率
temp_return_list = pd.concat(temp_return_list)


########### STEP 4: 回测：计算评判指标

# 创建结果保存路径
result_path = 'result/'
if not os.path.exists(result_path):   
    os.mkdir(result_path)


# 上证指数日收益率
data_rm = pd.read_excel('上证指数日数据.xlsx', index_col = 2)
data_rm = data_rm['收盘价(元)']
data_rm = data_rm['2010-12-31': '2020-12-31']
data_rm = data_rm / data_rm.shift(1) - 1
data_rm = data_rm.dropna()

# 上证50日收益率
data_sz50 = pd.read_excel('上证50日数据.xlsx', index_col = 2)
data_sz50 = data_sz50['收盘价(元)']
data_sz50 = data_sz50['2010-12-31': '2020-12-31']
r_sz50 = data_sz50 / data_sz50.shift(1) - 1
r_sz50 = r_sz50.dropna()

# 转成对数收益率
log_return = pd.DataFrame([temp_return_list, data_rm, r_sz50], columns=temp_return_list.index, index=['低beta股票等权重组合', '上证综指', '上证50']).T
log_return = np.log(1+log_return)

# 无风险收益率
riskfreedata = riskfreedata.loc[data_rm.index]
annual_riskfree_mean = riskfreedata.resample('y').mean()
all_riskfree_mean = riskfreedata.mean() * 252

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
    excess_return[s] = log_return[s] - riskfreedata

excess_rm = log_return['上证综指'] - riskfreedata
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
money_list = pd.concat([pd.DataFrame([1,1,1], index=money_list.columns).T, money_list], axis=0)
money_list.index = data_sz50['2010-12-31': '2020-12-31'].index
money_list = money_list * start_money

plt.figure(figsize = (20,10))
plt.plot(money_list['低beta股票等权重组合'], linewidth = 5, label = '低beta股票等权重组合')
plt.plot(money_list['上证综指'], linewidth = 4, linestyle = '-.', label = '上证综指')
plt.plot(money_list['上证50'], linewidth = 4, linestyle = ':', label = '上证50')

plt.legend()
plt.grid()

plt.ylabel(r'资金量 $V_t$ (万元)', fontsize = 30)
plt.xlabel(r'时间', fontsize = 30)
plt.legend(fontsize = 30, loc = 'upper left')
plt.savefig(result_path+'case_4_pnl.png', bbox_inches = 'tight' , dpi=150)

# 最大回撤
MDD_list = all_log_return_Sharpe.copy()
for s in money_list.columns:
    temp_list = money_list[s]
    MDD_list[s] = np.max(temp_list.cummax() - temp_list)


#########################
# 结果整合

res = pd.DataFrame(index = ['低beta股票等权重组合', '上证综指', '上证50'],
                   columns = ['平均收益率', '标准差', '夏普比率', 'alpha', 'beta', '特雷诺比率', '信息比率', '最大回撤'])
res['平均收益率'] = all_log_return_mean
res['标准差'] = all_log_return_std
res['夏普比率'] = all_log_return_Sharpe
res['alpha'] = alpha_list
res['beta'] = beta_list
res['特雷诺比率'] = all_log_return_Treynor
res['信息比率'] = all_log_return_IR
res['最大回撤'] = MDD_list

res.to_csv(result_path+'case_4_result_metrics.csv', encoding='gbk')

annual_log_return_mean.T.to_csv(result_path+'case_4_average_return.csv', encoding='gbk')
annual_log_return_std.T.to_csv(result_path+'case_4_std_return.csv', encoding='gbk')



#########################
# 其他杂图
### beta直方图
allbeta_list = []
for betaresult in beta_result_list:
    allbeta_list = allbeta_list + list(betaresult[1].values)
allbeta_list = np.array(allbeta_list)

plt.figure(figsize = (24,16))
plt.grid()
plt.xticks(fontsize = 50)
plt.yticks(fontsize = 50)
plt.xlim(-1, 3)
plt.hist(allbeta_list, bins = 50, density = True)
mean = np.mean(allbeta_list)
std = np.std(allbeta_list)
normalxrange = np.arange(-1, 3, 0.001)
plt.plot( normalxrange,  stats.norm.pdf(normalxrange, loc = mean, scale = std), linewidth = 8)

plt.savefig(result_path+'case_4_beta_hist.png', bbox_inches = 'tight' , dpi=150)



### 持仓列表
allstock_list = pd.DataFrame(stock_choose_name_list, index=month_index)
allstock_list.to_csv(result_path+'case_4_allstock_list.csv', encoding='gbk')#


### 上证50与上证指数走势示意
data_sz50 = pd.read_excel('上证50日数据.xlsx', index_col = 2)
data_sz50 = data_sz50['收盘价(元)']
data_sz50 = data_sz50['2010-12-31': '2020-12-31']
data_szzs = pd.read_excel('上证指数日数据.xlsx', index_col = 2)
data_szzs = data_szzs['收盘价(元)']
data_szzs = data_szzs['2010-12-31': '2020-12-31']


plt.figure(figsize = (20,10))
plt.plot(data_szzs, linewidth = 4, linestyle = '-.', label = '上证综指')
plt.plot(data_sz50, linewidth = 4, linestyle = ':', label = '上证50')
plt.legend()
plt.grid()
plt.ylabel(r'指数', fontsize = 30)
plt.xlabel(r'时间', fontsize = 30)
plt.legend(fontsize = 30, loc = 'upper left')
plt.savefig(result_path+'case_4_indices.png', bbox_inches = 'tight' , dpi=150)


### 换手率计算
stock_reserve = pd.read_csv(result_path+'case_4_allstock_list.csv', encoding='gbk')
numlist = []
for i in range(1,len(stock_reserve.index)):
    last_stock_list = stock_reserve.iloc[i-1,:]
    temp_stock_list = stock_reserve.iloc[i,:]
    set1 = set(last_stock_list)
    set2 = set(temp_stock_list)
    intersec = set1.intersection(set2)
    internum = len(list(intersec))
    numlist.append(10 - internum)

print('换手率: ',np.mean(numlist)/10)



