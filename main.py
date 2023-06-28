import os
import pandas as pd
import random


def max_size(dir_classes, data_max_size=0):
    if data_max_size == 0:
        for dir_class in dir_classes:
            file = os.listdir(dir_class)
            if data_max_size == 0:
                data_max_size = len(file)
            else:
                data_max_size = min(data_max_size, len(file))
        return data_max_size
    else:
        return data_max_size


def make_data_class(dir_class, data_max_size=0):
    datas = os.scandir(dir_class)

    file = list()
    for data in datas:
        file.append(data)

    random.shuffle(file)
    if data_max_size == 0:
        return file
    else:
        return file[0:data_max_size]


def cat_class(dir_class_1, dir_class_2):
    df_buf = pd.DataFrame(columns=['file_name_1', 'file_name_2', 'label'])
    label = 1
    data_max_size = min(len(dir_class_1), len(dir_class_2))

    if len(dir_class_1) == len(dir_class_2):
        label = 0
        for i in range(int(data_max_size/2)):
            df_buf = df_buf._append(
                {'file_name_1': dir_class_1[i].path, 'file_name_2': dir_class_2[data_max_size - i - 1].path,
                 'label': label},
                ignore_index=True)
            df_buf = df_buf._append(
                {'file_name_1': dir_class_2[i].path, 'file_name_2': dir_class_1[data_max_size - i - 1].path,
                 'label': label},
                ignore_index=True)
    else:
        for i in range(int(data_max_size/2)):
            df_buf = df_buf._append(
                {'file_name_1': dir_class_1[i].path, 'file_name_2': dir_class_2[data_max_size - i - 1].path,
                 'label': label},
                ignore_index=True)
            df_buf = df_buf._append(
                {'file_name_1': dir_class_2[i].path, 'file_name_2': dir_class_1[data_max_size - i - 1].path,
                 'label': label},
                ignore_index=True)
    return df_buf

def make_siam_dataset(dir_classes, max_size_class):
    df = pd.DataFrame(columns=['file_name_1', 'file_name_2', 'label'])

    for i in range(len(dir_classes)):
        class_1 = make_data_class(dir_classes[i], max_size_class)
        for j in range(len(dir_classes)):
            class_2 = None
            if i == j:
                class_2 = make_data_class(dir_classes[j], int(max_size_class))
            else:
                class_2 = make_data_class(dir_classes[j], int(max_size_class / (len(dir_classes) - 1)))

            df = df._append(cat_class(class_1, class_2))
    return df

# 9 category
dir_class = list()
dir_class.append('../../../source/dataRGB/Основное зерно отобранное')
dir_class.append('../../../source/dataRGB/Пшеница битые отобранное')
dir_class.append('../../../source/dataRGB/Пшеница в оболочке отобранное')
dir_class.append('../../../source/dataRGB/Пшеница головня отобранное')
dir_class.append('../../../source/dataRGB/Пшеница изъеденные отобранное')
dir_class.append('../../../source/dataRGB/Пшеница испорченные отобранное')
dir_class.append('../../../source/dataRGB/Пшеница клоп черепашка отобранное')
dir_class.append('../../../source/dataRGB/Пшеница поврежденная сушкой отобранное')
dir_class.append('../../../source/dataRGB/Пшеница щуплые отобранное')

max_size_class = max_size(dir_class)

print("Max size class: " + str(max_size_class))

df = make_siam_dataset(dir_class, max_size_class)

df["file_name_1"] = df["file_name_1"].str.replace('\\', '/')

df = df.sample(frac=1).reset_index(drop=True)

df_train = df[:int(len(df)*0.8)]
df_val = df[int(len(df)*0.8):int(len(df)*0.9)]
df_test = df[int(len(df)*0.9):]

df_train.to_csv('siam_data_train.csv', header=None, index=False, encoding="ansi")
df_val.to_csv('siam_data_val.csv', header=None, index=False, encoding="ansi")
df_test.to_csv('siam_data_test.csv', header=None, index=False, encoding="ansi")

print(df['label'].value_counts())
print(df_train['label'].value_counts())
print(df_val['label'].value_counts())
print(df_test['label'].value_counts())