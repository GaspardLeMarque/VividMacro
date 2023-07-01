"""
Parsing Greenbook data ASCII files
"""
import os
import re
from datetime import datetime
import pandas as pd

# Column labels: -12 to +7 periods from current data
col_names = ["B12", "B11", "B10", "B9", "B8",
             "B7", "B6", "B5", "B4", "B3", "B2", "B1",
             "C", "F1", "F2", "F3", "F4", "F5", "F6", "F7"]

folder_path = r'greenbook_data/'
filepaths = [os.path.join(folder_path, name) for name in os.listdir(folder_path)]

all_files = []


def parse_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        file.seek(0)
        fcast_date = re.findall(r'\d{4}_\d{2}_\d{2}', file.readlines()[-3])[0]
        file.seek(0)
        tmp1, tmp2 = [], []
        for i in file.readlines()[10:-3]:
            if "ND" or "NA" in i:
                i = i.replace("ND", "0.0")
                i = i.replace("NA", "0.0")
            tmp1.append(re.findall(r'^.*\[\w*]', i.strip()))
            tmp2.append(re.findall(r'\d+\.\d+', i.strip()))
        tmp1, tmp2 = list(filter(None, tmp1)), list(filter(None, tmp2))
        top, bot = [], []
        for i in [str(*i) for i in tmp1]:
            top.append([i + "_" + j for j in col_names])
        for i in tmp2:
            if len(i) == 8:
                bot.append(["NaN"]*10 + [str(j) for j in i] + ["NaN"]*2)
            if len(i) == 10:
                bot.append(["NaN"]*10 + [str(j) for j in i])
            if len(i) == 16:
                bot.append(["NaN"]*4 + [str(j) for j in i])
            if len(i) == 20:
                bot.append([float(j) for j in i])
        tpls_lst = [list(zip(top[i], bot[i])) for i in range(len(top))]
        unpkd = []
        for i in tpls_lst:
            for j in i:
                unpkd.append(j)
        dataframe = pd.DataFrame(unpkd, columns=["Date", fcast_date])
        dataframe = dataframe.set_index('Date')
        all_files.append(dataframe)


for p in filepaths:
    parse_file(p)

df = pd.concat(all_files, axis=1, sort=False, join='outer')
df = df.reindex(sorted(df.columns), axis=1).T

# Convert dates into datetime objects and rename index col
df.index = pd.to_datetime(df.index, format="%Y_%m_%d")
df.index = [datetime.strptime(i, '%Y-%m') for i in [i.strftime('%Y-%m') for i in df.index]]
df.index.names = ['Date']
