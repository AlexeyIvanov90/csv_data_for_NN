import os
import pandas as pd
import random


def is_png(file_name):
    if file_name.find(".png") == -1:
        return False
    return True


def max_size(work_folder, data_max_size=0):
    if data_max_size == 0:
        for class_dir in work_folder:
            file_names = os.listdir(class_dir)
            buf_len = 0
            if data_max_size == 0:
                for file_name in file_names:
                    if is_png(file_name):
                        buf_len += 1
                data_max_size = buf_len
            else:
                for file_name in file_names:
                    if is_png(file_name):
                        buf_len += 1

                data_max_size = min(data_max_size, buf_len)
        return data_max_size
    else:
        return data_max_size


def make_data_category(work_dir_class):
    datas = os.scandir(work_dir_class)
    category = list()

    for data in datas:
        if is_png(data.name):
            category.append(data)

    random.shuffle(category)

    return category


def cat_class(dir_category_1, dir_category_2):
    data_frame = pd.DataFrame(columns=['file_name_1', 'file_name_2', 'label'])

    label = 0
    if dir_category_1.iloc[0]['label'] != dir_category_2.iloc[0]['label']:
        label = 1

    dir_category_1 = dir_category_1.sample(frac=1).reset_index(drop=True)
    dir_category_2 = dir_category_2.sample(frac=1).reset_index(drop=True)

    data_frame['file_name_1'] = dir_category_1['file_name']
    data_frame['file_name_2'] = dir_category_2['file_name']
    data_frame['label'] = [label] * len(data_frame.index)

    print(data_frame)

    return data_frame


def make_dataset(work_folder, max_size_class):
    data_frame = pd.DataFrame(columns=['file_name', 'label'])
    for i in range(len(work_folder)):
        class_buf = make_data_category(work_folder[i])
        class_buf = class_buf[0:max_size_class]

        for j in range(len(class_buf)):
            data_frame = data_frame._append({'file_name': class_buf[j].path, 'label': i}, ignore_index=True)

    return data_frame


def make_seam_dataset(data_set):
    data_frame = pd.DataFrame(columns=['file_name_1', 'file_name_2', 'label'])

    category_size = len(data_set[data_set.columns[1]].unique())

    for i in range(category_size):
        for j in range(category_size):
            class_1 = data_set.loc[data_set['label'] == i]
            class_2 = data_set.loc[data_set['label'] == j]

            if i != j:
                class_1 = class_1[:int(len(class_1)/(category_size-1))]
                class_2 = class_2[:int(len(class_2)/(category_size-1))]

            data_frame = data_frame._append(cat_class(class_1, class_2))

    data_frame = data_frame.sample(frac=1).reset_index(drop=True)
    return data_frame


# 10 category
dir_class = list()

dir_class.append('../../../source/dataRGB/Основное зерно отобранное')
dir_class.append('../../../source/dataRGB/Пшеница альтернариоз отобранное 2')
dir_class.append('../../../source/dataRGB/Пшеница битые отобранное')
dir_class.append('../../../source/dataRGB/Пшеница в оболочке отобранное')
dir_class.append('../../../source/dataRGB/Пшеница головня отобранное')
dir_class.append('../../../source/dataRGB/Пшеница изъеденные отобранное')
dir_class.append('../../../source/dataRGB/Пшеница испорченные отобранное')
dir_class.append('../../../source/dataRGB/Пшеница клоп черепашка отобранное 1')
dir_class.append('../../../source/dataRGB/Пшеница поврежденная сушкой отобранное')
dir_class.append('../../../source/dataRGB/Пшеница щуплые отобранное')

max_size = max_size(dir_class)

print("Max size class: " + str(max_size))

df = make_dataset(dir_class, max_size)

df["file_name"] = df["file_name"].str.replace('\\', '/')

df_train = pd.DataFrame(columns=['file_name', 'label'])
df_val = pd.DataFrame(columns=['file_name', 'label'])
df_test = pd.DataFrame(columns=['file_name', 'label'])

for i in range(len(dir_class)):
    df_buf = df.loc[df['label'] == i]
    df_train = df_train._append(df_buf[:int(len(df_buf) * 0.8)])
    df_val = df_val._append(df_buf[int(len(df_buf) * 0.8):int(len(df_buf) * 0.9)])
    df_test = df_test._append(df_buf[int(len(df_buf) * 0.9):])

df_train = df_train.sample(frac=1).reset_index(drop=True)
df_val = df_val.sample(frac=1).reset_index(drop=True)
df_test = df_test.sample(frac=1).reset_index(drop=True)

df_train.to_csv('data_train.csv', header=None, index=False, encoding="ansi")
df_val.to_csv('data_val.csv', header=None, index=False, encoding="ansi")
df_test.to_csv('data_test.csv', header=None, index=False, encoding="ansi")

print(df['label'].value_counts())
print(df_train['label'].value_counts())
print(df_val['label'].value_counts())
print(df_test['label'].value_counts())

seam_train_data_set = make_seam_dataset(df_train)
seam_val_data_set = make_seam_dataset(df_val)
seam_test_data_set = make_seam_dataset(df_test)

print(seam_train_data_set['label'].value_counts())
print(seam_val_data_set['label'].value_counts())
print(seam_test_data_set['label'].value_counts())
