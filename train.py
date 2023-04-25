import os
import pandas as pd


filepath = './mis_data'
file = os.listdir(filepath)
tes_f = int(len(file) * 0.8)
testd = pd.DataFrame()
for f in file[:tes_f]:
    data = pd.read_csv(os.path.join(filepath, f), encoding='utf-16', sep='\t')
    
    data['时间'] = data['时间'].astype('datetime64[ns]')
    data['时间'] = data[['时间']].apply(lambda x: x[0].timestamp(), axis=1).astype(int)
    # data['时间'] = data['时间'].astype('int64') // 10**9
    data['时间'] = data['时间'] - data['时间'][0]

    y = data['KLD热风风门开度（%）d']
    x = data.drop(columns=['KLD热风风门开度（%）d','Unnamed: 0'])

    testd = pd.concat([testd, data])
