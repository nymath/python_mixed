# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 15:28:01 2022

@author: ChaoyiZhao

此为《量化投资》教材第5.9节《案例：构建一个沪深300指数增强基金》所用代码之一：
“ch5 - case - Step1 - FactorCalculation - Wind.py”。

【本代码为本案例的第一步（使用Wind版本），功能包括：】
1. 计算Fama-French 3因子模型中的SMB与HML时间序列数据，以及流通市值和账面市值比二者的IC和rankIC时间序列；
2. 计算流通市值与账面市值比因子分层回测表现，即分层收益率时间序列。

非常欢迎同学们指出代码以及教材中的问题！如有问题或建议，可以联系编者 zhaochaoyi@pku.edu.cn

此版本用于2022年秋季学期北京大学数学科学学院“量化交易”课程。
更新日期：2022年10月9日

Copyright: 孙健 吴岚 赵朝熠

"""

"""
本代码只有拥有Wind账号且配置好WindPy接口才能运行。
不使用该接口的代码可见“ch5 - case - Step1 - FactorCalculation - NoWind.py”
"""


from WindPy import w
import numpy as np
import pandas as pd


w.start()

# 读取沪深300指数的【周】收益率数据
data_hs300 = pd.read_excel('沪深300指数.xlsx', index_col = 2)
data_hs300 = data_hs300['收盘价(元)']
data_hs300 = data_hs300['2009-12-31': '2020-12-31']
return_hs300 = data_hs300 / data_hs300.shift(1) - 1
time_index = data_hs300.index

# 新建dataframe用于存储因子收益率与IC时间序列
factor_return_list = pd.DataFrame(index = time_index, columns = ['rm', 'SMB', 'HML', 'IC_cap', 'IC_bp', 'rankIC_cap', 'rankIC_bp'])
factor_return_list['rm'] = return_hs300

# 新建dataframe用于存储市值和账面市值比的分组收益率时间序列，用于分层回测
group_cap_return_list = pd.DataFrame(index = time_index, columns = ['G1', 'G2', 'G3', 'G4', 'G5'])
group_bp_return_list = pd.DataFrame(index = time_index, columns = ['G1', 'G2', 'G3', 'G4', 'G5'])

# 循环
for i in range(len(time_index)-1):
    temp_time = time_index[i]
    next_time = time_index[i+1]
    print(temp_time)
    
    # 提取当期沪深300成分股列表
    constituent = w.wset( 'indexconstituent', options="date="+str(temp_time)+", windcode=000300.SH, field=date,wind_code,sec_name,i_weight,industry", usedf=True)[1]
    temp_stock_list = list(constituent['wind_code'].values)
    
    # 提取当期各股票的流动市值
    mkt_cap_float = w.wsd(temp_stock_list, "mkt_cap_float", temp_time, temp_time, "unit=1;currencyType=;Period=W;PriceAdj=F")
    cap_values = np.array(mkt_cap_float.Data[0])
    
    # 提取当期各股票的账面市值比
    pb_lf = w.wsd(temp_stock_list, "pb_lf", temp_time, temp_time, "unit=1;currencyType=;Period=W;PriceAdj=F")
    bp_values = 1 / np.array(pb_lf.Data[0])
    
    # 计算下一期各股票收益率
    temp_price = w.wsd(temp_stock_list, "close", temp_time, temp_time, "unit=1;currencyType=;Period=W;PriceAdj=F")
    next_price = w.wsd(temp_stock_list, "close", next_time, next_time, "unit=1;currencyType=;Period=W;PriceAdj=F")
    next_return = np.array(next_price.Data[0]) / np.array(temp_price.Data[0]) - 1
    
    # 计算流动市值与账面市值比的IC与rankIC时间序列
    temp_IC_cap = np.corrcoef( (cap_values), (next_return) )[0,1]
    temp_IC_bp = np.corrcoef( (bp_values), (next_return) )[0,1]
    temp_rankIC_cap = np.corrcoef( np.argsort(cap_values), np.argsort(next_return) )[0,1]
    temp_rankIC_bp = np.corrcoef( np.argsort(bp_values), np.argsort(next_return) )[0,1]
    
    # 仿照Fama and French (1993)用流通市值和账面市值比构造6个投资组合，用于后续计算SMB和HML
    temp_50_cap = np.percentile( cap_values, 50 )
    temp_30_bp = np.percentile( bp_values, 30 )
    temp_70_bp = np.percentile( bp_values, 70 )
    
    temp_stock_list = np.array(temp_stock_list)
    S_L =  (cap_values <= temp_50_cap) & (bp_values <= temp_30_bp) 
    S_M =  (cap_values <= temp_50_cap) & (bp_values > temp_30_bp) & (bp_values <= temp_70_bp)
    S_H =  (cap_values <= temp_50_cap) & (bp_values > temp_70_bp) 
    B_L =  (cap_values > temp_50_cap) & (bp_values <= temp_30_bp) 
    B_M =  (cap_values > temp_50_cap) & (bp_values > temp_30_bp) & (bp_values <= temp_70_bp) 
    B_H =  (cap_values > temp_50_cap) & (bp_values > temp_70_bp) 
    
    # 6个投资组合内部均按流通市值加权投资，计算6个组合的收益率时间序列
    FFnamelist = ['S_L', 'S_M', 'S_H', 'B_L', 'B_M', 'B_H'] 
    for name in FFnamelist:
        exec( name + '_weight = cap_values[' + name +'] / np.sum(cap_values[' + name + '])' )
    for name in FFnamelist:
        exec( name + '_return = next_return[' + name +']' )
    for name in FFnamelist:
        exec( name + '_capreturn = np.sum(' + name +'_weight * ' + name + '_return)' )
    
    # 计算SMB和HML时间序列
    temp_SMB = (S_L_capreturn + S_M_capreturn + S_H_capreturn - B_L_capreturn - B_M_capreturn - B_H_capreturn)/3
    temp_HML = (S_H_capreturn + B_H_capreturn - S_L_capreturn - B_L_capreturn) / 2
    
    # 汇总各个因子收益率的时间序列
    factor_return_list.loc[next_time, ['SMB', 'HML', 'IC_cap', 'IC_bp', 'rankIC_cap', 'rankIC_bp']] = [temp_SMB, temp_HML, temp_IC_cap, temp_IC_bp, temp_rankIC_cap, temp_rankIC_bp]
    
    # 因子分层回测：按流通市值分5层，每组内部按流通市值加权
    temp_0_cap = 0
    temp_100_cap = np.max(cap_values)
    for perc in [20, 40, 60, 80]:
        exec('temp_' + str(perc) +'_cap = np.percentile( cap_values,' + str(perc) + ')')
    for group in [1, 2, 3, 4, 5]:
        exec('G' + str(group) +' = (cap_values <= temp_' + str(group*20) + '_cap) & (cap_values > temp_' + str((group-1)*20) + '_cap)' )
    for group in ['G1', 'G2', 'G3', 'G4', 'G5']:
        exec(  group + '_weight = cap_values[' + group +'] / np.sum(cap_values[' + group + '])' )
    for group in ['G1', 'G2', 'G3', 'G4', 'G5']:
        exec( group + '_return = next_return[' + group +']' )
    for group in ['G1', 'G2', 'G3', 'G4', 'G5']:
        exec( group + '_capreturn = np.sum(' + group +'_weight * ' + group + '_return)' )
    
    group_cap_return_list.loc[next_time, ['G1', 'G2', 'G3', 'G4', 'G5']] = [G1_capreturn, G2_capreturn, G3_capreturn, G4_capreturn, G5_capreturn]

    # 因子分层回测：按账面市值比分5层，每组内部按流通市值加权
    temp_0_bp = 0
    temp_100_bp = np.max(bp_values)
    for perc in [20, 40, 60, 80]:
        exec('temp_' + str(perc) +'_bp = np.percentile( bp_values,' + str(perc) + ')')
    for group in [1, 2, 3, 4, 5]:
        exec('G' + str(group) +' = (bp_values <= temp_' + str(group*20) + '_bp) & (bp_values > temp_' + str((group-1)*20) + '_bp)' )
    for group in ['G1', 'G2', 'G3', 'G4', 'G5']:
        exec(  group + '_weight = cap_values[' + group +'] / np.sum(cap_values[' + group + '])' )
    for group in ['G1', 'G2', 'G3', 'G4', 'G5']:
        exec( group + '_return = next_return[' + group +']' )
    for group in ['G1', 'G2', 'G3', 'G4', 'G5']:
        exec( group + '_bpreturn = np.sum(' + group +'_weight * ' + group + '_return)' )
    
    group_bp_return_list.loc[next_time, ['G1', 'G2', 'G3', 'G4', 'G5']] = [G1_bpreturn, G2_bpreturn, G3_bpreturn, G4_bpreturn, G5_bpreturn]
    
# 输出结果
factor_return_list.to_csv('FFfactorreturn.csv', encoding = 'gbk')
group_cap_return_list.to_csv('groupcapreturn.csv', encoding = 'gbk')
group_bp_return_list.to_csv('groupbpreturn.csv', encoding = 'gbk')