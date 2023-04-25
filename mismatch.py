import pandas as pd
import os
from itertools import groupby
import copy
deti = -380

file_name = './mis_data/'
filename = "./D线薄板烘丝的历史数据"
file_list = os.listdir(filename)
n = 1
for f in file_list:
    data = pd.read_excel(os.path.join(filename,f))
    data['KLD烘后水分（%）d']  = data['KLD烘后水分（%）d'].shift(periods=int(deti / 10), fill_value=-1)
    data['KLD烘后温度（℃）d']  = data['KLD烘后温度（℃）d'].shift(periods=int(deti / 10), fill_value=-1)
    index = data[(data['烘前叶丝流量（kg/h）d'] != 0) & (data['KLD烘后水分（%）d'] > 0)].index.tolist()
    start = index[0]

    for i in range(len(index) - 1):
        if index[i+1] - index[i] > 1 or i == len(index) - 2:
            end = index[i]
            if end - start < 600:
                start = index[i]
                continue
            new = data.iloc[start-1:end+2,:]

            # KLD排潮风门开度（%）d 开度 50 开始
            a = groupby(new['KLD排潮风门开度（%）d'].tolist())
            l = 0
            for j, v in a:
                l -= len([_ for _ in v])
                if j == 50:
                    df = data['KLD排潮风门开度（%）d'].shift(periods=l, fill_value=-1).loc[start-1:end+2].copy()
                    new['KLD排潮风门开度（%）d']  = df
                    break
            print(f[:-4])
            new.to_csv(file_name+ f[:-4] +'_' + str(n) + '.csv', encoding='utf-16', sep='\t')
            start = index[i+1]
            n += 1
