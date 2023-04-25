import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
import os
import re
import copy

def corrX_orig(df, cut = 0.9) :

    # Get correlation matrix and upper triagle
    corr_mtx = df.corr().abs()
    avg_corr = corr_mtx.mean(axis = 1)
    up = corr_mtx.where(np.triu(np.ones(corr_mtx.shape), k=1).astype(np.bool_))

    drop = list()
    for row in range(len(up)-1):
        col_idx = row + 1
        for col in range (col_idx, len(up)):
            if(corr_mtx.iloc[row, col] > cut):
                if(avg_corr.iloc[row] > avg_corr.iloc[col]): 
                    drop.append(row)
                else: 
                    drop.append(col)

    drop_set = list(set(drop))
    # dropcols_idx = drop_set
    dropcols_names = list(df.columns[[item for item in drop_set]])
    
    return(dropcols_names)

def select_feature():
    full_data = pd.DataFrame()
    filename = './mis_data/'
    filelist = os.listdir(filename)
    for f in filelist:
        df = pd.read_csv(os.path.join(filename,f),encoding='utf-16',sep='\t')
        df['时间'] = df['时间'].astype('datetime64[ns]')
        df['时间'] = df[['时间']].apply(lambda x: x[0].timestamp(), axis=1).astype(int)
        # data['时间'] = data['时间'].astype('int64') // 10**9
        df['时间'] = df['时间'] - df['时间'][0]
        full_data = pd.concat([full_data, df], axis=0)
    full_data.reset_index(drop=True, inplace=True)

    data = copy.deepcopy(full_data)
    data.dropna(axis=1,inplace=True)
    # 值全为0的列
    data = data.loc[:, (data != 0).any(axis=0)]
    data.drop(columns=['Unnamed: 0','序号'], inplace=True) # ,'时间'
    # # 整列值相同
    # data = data.loc[:,(data != data.mean()).all(axis=0)]
    data.drop(data.columns[data.std() < 1e-200], axis=1, inplace=True)

    # 不相关列
    drop_col = []
    coli = data.columns.to_list()
    for c in coli:
        if re.match('(?=Sirox)', c) or re.match('(?=市政)', c) or re.match('(?=冷凝水)', c) or re.match('(?=SIROXD)', c):
            drop_col.append(c)
    data.drop(columns=drop_col,inplace=True)

    # 数值集中于某几个值,数值于小数点后几位浮动
    col = ['1号切丝机运行', 'KLD筒转速（l/min）d', '切丝机选中','是否是设备自动控制','筒体电机实际频率d','膨胀轮电机频率d','锅炉分汽缸温度-薄板D']
    for c in col:
        if c in data.columns:
            data.drop(columns=[c],inplace=True)
    # data.drop(columns=['1号切丝机运行', 'KLD筒转速（l/min）d', '切丝机选中','是否是设备自动控制','筒体电机实际频率d','膨胀轮电机频率d'], inplace=True)
    # data.drop(columns=['锅炉分汽缸温度-薄板D'], inplace=True)

    # corr > 0.85
    dropcols_names = corrX_orig(data, cut = 0.85)
    data.drop(columns=dropcols_names, inplace=True)

    data = pd.concat([data,full_data['KLD热风风门开度（%）d']], axis=1)

    data.to_csv('./full_data.csv', encoding='utf-16', sep='\t')

    # x = data.drop(columns = ['KLD1区蒸汽薄膜阀开度（%）d'])
    # y = data.loc[:,['KLD1区蒸汽薄膜阀开度（%）d']]
    # test = SelectKBest(score_func=f_regression,k=10)
    # fit = test.fit(x,y)
    # score =fit.scores_
    # ind = np.where(score > 400)
    # data = x.iloc[:,ind[0]]
    # break
select_feature()
