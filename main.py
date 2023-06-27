import os
import pandas as pd
import random

# iterators over files in respective folders
data_1 = os.scandir('../../../source/dataRGB/Основное зерно отобранное')
data_2 = os.scandir('../../../source/dataRGB/Пшеница битые отобранное')

count = 1
category_1 = list()
category_2 = list()

for data in data_1:
    category_1.append(data)


for data in data_2:
    category_2.append(data)

random.shuffle(category_1)
random.shuffle(category_2)


max_size = min(len(category_1), len(category_2))

# create a data frame to save locations and labels
df_train = pd.DataFrame(columns=['file_name_1', 'file_name_2', 'label'])
df_val = pd.DataFrame(columns=['file_name_1', 'file_name_2', 'label'])
df_test = pd.DataFrame(columns=['file_name_1', 'file_name_2', 'label'])

j = max_size - 1

for i in range(max_size):
    df_buf = pd.DataFrame(columns=['file_name_1', 'file_name_2', 'label'])

    df_buf = df_buf._append({'file_name_1': category_1[i].path, 'file_name_2': category_2[j].path, 'label': 1}, ignore_index=True)
    df_buf = df_buf._append({'file_name_1': category_1[j].path, 'file_name_2': category_1[i].path, 'label': 0}, ignore_index=True)
    df_buf = df_buf._append({'file_name_1': category_1[j].path, 'file_name_2': category_2[i].path, 'label': 1}, ignore_index=True)
    df_buf = df_buf._append({'file_name_1': category_2[i].path, 'file_name_2': category_2[j].path, 'label': 0}, ignore_index=True)

    if i < (max_size * 0.8)/2:
        df_train = df_train._append(df_buf, ignore_index=True)
    else:
        if i < (max_size * 0.9)/2:
            df_val = df_val._append(df_buf, ignore_index=True)
        else:
            df_test = df_test._append(df_buf, ignore_index=True)

    j -= 1
    if i >= j:
        break

#df = df.sample(frac=1).reset_index(drop=True)
df_train = df_train.sample(frac=1)
df_val = df_val.sample(frac=1)
df_test = df_test.sample(frac=1)

# save as csv file
df_train.to_csv('train.csv', header=None, index=False)
df_val.to_csv('val.csv', header=None, index=False)
df_test.to_csv('test.csv', header=None, index=False)
