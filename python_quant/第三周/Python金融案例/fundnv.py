#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 23:42:49 2020

@author: wangxiaochuan
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 17:23:42 2020

@author: wxc
"""

#%% 基金分析
import pandas as pd
import numpy as np
import os
os.chdir(r'/Users/wangxiaochuan/Desktop/易方达全新Python教学模式2')
windengine = 'mssql+pymssql://hcquant:Quant_17885@192.168.10.200:1433/nWind?charset=GBK'
from empyrical import ( alpha ,beta, annual_volatility, cum_returns, annual_return, downside_risk, max_drawdown, sharpe_ratio, sortino_ratio, calmar_ratio, omega_ratio, tail_ratio )

#%% 导入基金净值与基准数据【数据库】
# sql="""
# select * from CHINAMUTUALFUNDNAV where F_INFO_WINDCODE='110011.OF' order by PRICE_DATE
# """
# fundnav=pd.read_sql(sql,windengine)

# sql="""
# select * from AIndexEODPrices where S_INFO_WINDCODE='000300.SH' order by TRADE_DT"""
# benchmarknav=pd.read_sql(sql,windengine)


#%% 读取本地csv
fundnav=pd.read_csv(r'110011_nav.csv',encoding='utf8',converters={'PRICE_DATE':str})
benchmarknav=pd.read_csv('000300_nav.csv',converters={'TRADE_DT':str})
data=fundnav.merge(benchmarknav,left_on='PRICE_DATE',right_on='TRADE_DT').set_index('PRICE_DATE').sort_index()

# 计算基金和基准的收益率
returns = data.F_NAV_ADJUSTED.pct_change()
benchmark_returns = data.S_DQ_PCTCHANGE / 100

#计算累计收益
creturns = cum_returns(returns)
creturns.plot(title='creturns')

#计算年化收益率
annual_return(returns)

#计算最大回撤
max_drawdown(returns)

#年化Volatility (策略波动率)
annual_volatility(returns, period='daily')

#Calmar比率
calmar_ratio(returns)

#Omega比率
#公式意义：Omega越高越好，它是对偏度和峰值的一个调整。
omega_ratio(returns=returns, risk_free=0.0001)

#Sharpe比率
#公式意义：夏普指数代表投资人每多承担一分风险，可以拿到几分收益；若为正值，代表基金收益率高过波动风险；若为负值，代表基金操作风险大过于收益率。每个投资组合都可以计算Sharpe ratio，即投资回报与多冒风险的比例，这个比例越高，投资组合越佳。
sharpe_ratio(returns=returns)

#sortino比率
sortino_ratio(returns=returns)

#下降风险
downside_risk(returns=returns)


#Alpha
alpha(returns=returns, factor_returns=benchmark_returns, risk_free=0.01)

#Beta
beta(returns=returns, factor_returns=benchmark_returns, risk_free=0.01)

#Tail Ratio
tail_ratio(returns=returns)

['OBJECT_ID_x', 'F_INFO_WINDCODE', 'ANN_DATE', 'PRICE_DATE',
       'F_NAV_UNIT', 'F_NAV_ACCUMULATED', 'F_NAV_DIVACCUMULATED',
       'F_NAV_ADJFACTOR', 'CRNCY_CODE_x', 'F_PRT_NETASSET',
       'F_ASSET_MERGEDSHARESORNOT', 'NETASSET_TOTAL', 'F_NAV_ADJUSTED',
       'IS_EXDIVIDENDDATE', 'F_NAV_DISTRIBUTION', 'OPDATE_x', 'OPMODE_x',
       'OBJECT_ID_y', 'S_INFO_WINDCODE', 'TRADE_DT', 'CRNCY_CODE_y',
       'S_DQ_PRECLOSE', 'S_DQ_OPEN', 'S_DQ_HIGH', 'S_DQ_LOW', 'S_DQ_CLOSE',
       'S_DQ_CHANGE', 'S_DQ_PCTCHANGE', 'S_DQ_VOLUME', 'S_DQ_AMOUNT', 'SEC_ID',
       'OPDATE_y', 'OPMODE_y']


