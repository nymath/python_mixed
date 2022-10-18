# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 17:30:44 2022

@author: ChaoyiZhao

此为《量化投资》教材第5.9节《案例：构建一个沪深300指数增强基金》所用代码之三：
“ch5 - case - Step3 - Strategy - NoWind.py”。

【本代码为本案例的第三步（无Wind版本），功能包括：】
1. 根据案例描述，计算最优多空策略权重与最优整体策略权重（多空+基准）；
2. 计算个股未来周收益率。

非常欢迎同学们指出代码以及教材中的问题！如有问题或建议，可以联系编者 zhaochaoyi@pku.edu.cn

此版本用于2022年秋季学期北京大学数学科学学院“量化交易”课程。
更新日期：2022年10月9日

Copyright: 孙健 吴岚 赵朝熠

"""


import numpy as np
import pandas as pd
import statsmodels.api as sm
from cvxopt import matrix, solvers


# 读取沪深300指数周数据
data_hs300 = pd.read_excel('沪深300指数.xlsx', index_col = 2)
data_hs300 = data_hs300['收盘价(元)']
data_hs300 = data_hs300['2009-12-31': '2020-12-31']
time_index = data_hs300.index

# 读取FF3因子收益率数据
data_FF = pd.read_csv('FFfactorreturn.csv', encoding='gbk', index_col = 0, parse_dates = True)

# 读取沪深300成分股列表、流通市值、账面市值比数据
constituent_list = pd.read_csv('沪深300指数成分股列表周频数据.csv', encoding='gbk', index_col=0, parse_dates=True)
constituent_weight_list = pd.read_csv('沪深300指数成分股权重周频数据.csv', encoding='gbk', index_col=0, parse_dates=True)
cap_values_list = pd.read_csv('沪深300指数成分股流通市值周频数据.csv', encoding='gbk', index_col=0, parse_dates=True)
bp_values_list = pd.read_csv('沪深300指数成分股账面市值比周频数据.csv', encoding='gbk', index_col=0, parse_dates=True)
close_price_list = pd.read_csv('沪深300指数成分股收盘价周频数据.csv', encoding='gbk', index_col=0, parse_dates=True)
trade_status_list = pd.read_csv('沪深300指数成分股交易状态周频数据.csv', encoding='gbk', index_col=0, parse_dates=True)


# 2015年开始回测
start_date = '2014-12-31'
start_arg = np.where(time_index == start_date)[0][0]

# 初始化
plus_weight_list = pd.DataFrame(index = time_index[start_arg:]) # 组合多空部分的权重
weight_list = pd.DataFrame(index = time_index[start_arg:]) # 组合多空+指数基准权重
future_return_list = pd.DataFrame(index = time_index[start_arg:]) # 个股下一期收益率

# 滚动回测
for time in range( start_arg, len(time_index)-1):
    history_time = time_index[time-50]  # 历史50周
    temp_time = time_index[time]        # 当前周
    next_time = time_index[time+1]      # 下一周
    
    print(temp_time)
    
    # 提取当期沪深300成分股列表
    temp_stock_list = list(constituent_list.loc[temp_time,:].dropna().values)
    # 成分股在区间[t-50,t+1]的收盘价
    temp_price = close_price_list.loc[history_time:next_time,temp_stock_list]
    
    # 提取指数成分股在区间[t-50,t+1]的交易状态（不交易<10周）
    temp_status = trade_status_list.loc[history_time:next_time,temp_stock_list]
    temp_status = ( np.sum( temp_status != '交易') <= 10 )
    # 剔除历史数据不足50周的股票 以及 不交易<10周的股票
    temp_price = temp_price.loc[:, temp_status.values]
    temp_price = temp_price.dropna(axis=1)
    # 剩余股票列表
    temp_stock_list = temp_price.columns
    
    # 剔除指数权重为空的股票
    constituent_weight = constituent_weight_list.loc[temp_time,temp_stock_list]
    constituent_weight = constituent_weight[~np.isnan(constituent_weight)]
    # 剩余股票列表
    temp_stock_list = constituent_weight.index
    
    # 剩余股票收盘价
    temp_price = temp_price.loc[:, temp_stock_list]
    # 剩余股票收益率
    temp_return = temp_price / temp_price.shift(1) - 1
    temp_return = temp_return.dropna()
    
    # 将[t-50,t+1]分成历史区间[t-50,t]和未来区间[t,t+1]
    history_return = temp_return.iloc[:-1, :]
    future_return = temp_return.iloc[-1, :]
    
    # 提取历史FF3因子数据
    history_FF = data_FF.loc[history_time:temp_time, ['rm', 'SMB', 'HML']]
    history_FF = history_FF.iloc[1:]
    
    # B与Omega的确定：线性回归估计多因子模型的B（beta与alpha）
    Bmatrix = np.zeros(( len(history_return.columns), 3 ))
    sigma_e_2 = np.zeros( len(history_return.columns) ) 
    for i in range(len(history_return.columns)):
        y = history_return[ history_return.columns[i] ].values
        X = history_FF.values
        model = sm.OLS(y, X).fit()
        Bmatrix[i, :] = model.params
        sigma_e_2[i] = np.mean( ( y - np.sum(X * model.params,axis=1) )**2 )
    
    beta_Bmatrix = Bmatrix[:, [0,1]]
    alpha_Bmatrix = Bmatrix[:, 2]
    
    # mu 的确定：根据账面市值比rankIC的历史均值的方向
    history_rankIC_bp = data_FF.loc[history_time:temp_time, 'rankIC_bp']
    if history_rankIC_bp.mean() > 0:
        mu = alpha_Bmatrix
    else:
        mu = - alpha_Bmatrix
    
    ### 求解约束优化问题，求最优权重
    B = sm.add_constant(beta_Bmatrix)
    Omega = np.diag(sigma_e_2)
    lam = 10000
    # 基准权重
    benchweight = constituent_weight / np.sum(constituent_weight)
    benchweight = benchweight.values
    # 二次规划参数
    A = B.T  # (3,n)
    b = np.zeros( np.shape(A)[0] )
    P = lam * Omega
    q = - mu
    G = - np.identity( len( temp_stock_list ) )
    h = benchweight
    # 求解
    res1 = solvers.qp(matrix(P), matrix(q), matrix(G), matrix(h), matrix(A), matrix(b))
    weight = np.array(res1['x']).T[0]
    
    # 记录结果
    for s in range(len(temp_stock_list)):
        weight_list.loc[temp_time, temp_stock_list[s]] = weight[s]
        plus_weight_list.loc[temp_time, temp_stock_list[s]] = weight[s] + benchweight[s]
        future_return_list.loc[next_time, temp_stock_list[s]] = future_return[s]

# 输出结果：多空权重、整体权重、个股未来收益率
weight_list.to_csv('weight_list_IC_constraint.csv')
plus_weight_list.to_csv('plus_weight_list_IC_constraint.csv')
future_return_list.to_csv('future_return_list_IC_constraint.csv')
