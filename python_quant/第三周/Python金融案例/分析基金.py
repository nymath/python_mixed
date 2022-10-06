# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 17:23:42 2020

@author: wxc
"""
'''
那个数据处理的案例可以以统计基金公司规模为例子

各家基金公司的各类资产规模
分类统计基金公司规模的例子，原始数据发到两张excel表格里
做规模统计时，循环各家公司做成历年规模走势图

'''

#%% 基金分析
import pandas as pd
import os
# 解决画图时中文字体的问题
import matplotlib
#matplotlib.use('qt4agg')
#指定默认字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.family']='sans-serif'
os.chdir(r'/Users/wangxiaochuan/Desktop/易方达全新Python教学模式2')# windengine = 'mssql+pymssql://hcquant:Quant_17885@192.168.10.200:1433/nWind?charset=GBK'

#%% 导入基金净值与基准数据【数据库】
#sql="""
#SELECT a.F_INFO_WINDCODE, a.F_INFO_NAME, a.F_INFO_ISSUEDATE, b.S_INFO_SECTORNAME, a.F_INFO_CORP_FUNDMANAGEMENTCOMP  FROM [dbo].[CHINAMUTUALFUNDDESCRIPTION] as a
#INNER JOIN CMFSECClass as b
#on a.F_INFO_WINDCODE = b.F_INFO_WINDCODE
#"""
#jjs = pd.read_sql(sql,windengine).dropna()
#jjs.to_excel('基金列表.xlsx')
#
#sql = '''
#SELECT S_INFO_WINDCODE, REPORT_PERIOD, ANN_DT, PRT_TOTALASSET FROM [dbo].[CMFFINANCIALINDICATOR] ORDER BY S_INFO_WINDCODE ASC, REPORT_PERIOD ASC
#'''
#jj_gm = pd.read_sql(sql,windengine)
#jj_gm.to_excel('基金规模.xlsx')

# 获取规模

#%% 读取本地Excel数据

jjs = pd.read_excel('基金列表.xlsx', index_col='Unnamed: 0' )
jj_gm = pd.read_excel('基金规模.xlsx', index_col='Unnamed: 0' )

jjs.groupby(by='F_INFO_CORP_FUNDMANAGEMENTCOMP').count()['F_INFO_WINDCODE'].plot(kind='bar')
b=jjs[jjs.F_INFO_CORP_FUNDMANAGEMENTCOMP=='华夏基金']
a=jjs.groupby(by=['F_INFO_CORP_FUNDMANAGEMENTCOMP','S_INFO_SECTORNAME']).count()['F_INFO_WINDCODE']
c=jjs[(jjs.F_INFO_CORP_FUNDMANAGEMENTCOMP=='华夏基金') & (jjs.F_INFO_ISSUEDATE>=20200101)]



# 合并两张表格

merge_df = jjs.merge( jj_gm, left_on='F_INFO_WINDCODE', right_on='S_INFO_WINDCODE' )
merge_df.PRT_TOTALASSET = merge_df.PRT_TOTALASSET / 1e8


# 计算各家基金公募每个季报的总规模
jj_firm_gm = merge_df.groupby(['F_INFO_CORP_FUNDMANAGEMENTCOMP', 'REPORT_PERIOD']).PRT_TOTALASSET.sum().reset_index()

# 计算各家基金公募每个季报每个分类的总规模
jj_firm_type_gm = merge_df.groupby(['F_INFO_CORP_FUNDMANAGEMENTCOMP', 'REPORT_PERIOD', 'S_INFO_SECTORNAME']).PRT_TOTALASSET.sum().reset_index()


# 画单个基金公司规模变化图
name = '易方达'
df_plot = jj_firm_gm[ jj_firm_gm.F_INFO_CORP_FUNDMANAGEMENTCOMP.str.contains(name) ].set_index('REPORT_PERIOD').sort_index()
df_plot.PRT_TOTALASSET.plot(title=f'{name}总规模(亿元)')

['F_INFO_CORP_FUNDMANAGEMENTCOMP', 'F_INFO_NAME', 'REPORT_PERIOD',
       'PRT_TOTALASSET']








