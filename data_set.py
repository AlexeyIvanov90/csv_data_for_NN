import pandas as pd
import os
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


# возвращает перемешанные названия файлов в папке
def make_data_category(work_dir_class):
    datas = os.scandir(work_dir_class)
    category = list()

    for data in datas:
        if is_png(data.name):
            category.append(data)

    random.shuffle(category)

    return category


# возвращает dataset с одним классом label, который создается путём соединения классов из папок work_folder
def make_dataset(work_folder, label, max_size_class=0):
    data_frame = pd.DataFrame(columns=['file_name', 'label'])
    for i in range(len(work_folder)):
        class_buf = make_data_category(work_folder[i])

        if max_size_class != 0:
            class_buf = class_buf[0:max_size_class]
        else:
            class_buf = class_buf[0:max_size(work_folder)]

        for j in range(len(class_buf)):
            data_frame = data_frame._append({'file_name': class_buf[j].path, 'label': label}, ignore_index=True)

        print("Subclass " +
              work_folder[i][work_folder[i].rfind("/") + 1:] +
              "(" + str(max_size_class) + ") add class " + str(label))

    return data_frame


# возвращает dataset один (class_1) против 11 (class_2)
def make_two_class(class_1, class_2):
    data_frame = pd.DataFrame(columns=['file_name', 'label'])

    data_frame = data_frame._append(class_1)
    data_frame = data_frame._append(class_2)

    print("Make dataset success: " + str(len(data_frame)))

    return data_frame


# перемешивание и сохранение датасета в test val train для обучения
def save_dataset(in_data):
    in_data["file_name"] = in_data["file_name"].str.replace('\\', '/')
    in_data = in_data.sample(frac=1).reset_index(drop=True)

    out_data_train = pd.DataFrame(columns=['file_name', 'label'])
    out_data_val = pd.DataFrame(columns=['file_name', 'label'])
    out_data_test = pd.DataFrame(columns=['file_name', 'label'])

    for i in range(len(in_data.label.unique())):
        df_buf = in_data.loc[in_data['label'] == i]
        out_data_train = out_data_train._append(df_buf[:int(len(df_buf) * 0.8)])
        out_data_val = out_data_val._append(df_buf[int(len(df_buf) * 0.8):int(len(df_buf) * 0.9)])
        out_data_test = out_data_test._append(df_buf[int(len(df_buf) * 0.9):])

    out_data_train = out_data_train.sample(frac=1).reset_index(drop=True)
    out_data_val = out_data_val.sample(frac=1).reset_index(drop=True)
    out_data_test = out_data_test.sample(frac=1).reset_index(drop=True)

    in_data.to_csv('data.csv', header=None, index=False, encoding="ansi")

    out_data_train.to_csv('data_train.csv', header=None, index=False, encoding="ansi")
    out_data_val.to_csv('data_val.csv', header=None, index=False, encoding="ansi")
    out_data_test.to_csv('data_test.csv', header=None, index=False, encoding="ansi")

    print("All data:\n" + str(in_data['label'].value_counts()))
    print("Data train:\n" + str(out_data_train['label'].value_counts()))
    print("Data val:\n" + str(out_data_val['label'].value_counts()))
    print("Data test:\n" + str(out_data_test['label'].value_counts()))


# подсчтавет размеры подклассов для каждого класа
def calculation_size_data(dir_class_1, dir_class_2):
    size_class_1 = max_size(dir_class_1)
    size_class_2 = max_size(dir_class_2)

    count_category_1 = len(dir_class_1)
    count_category_2 = len(dir_class_2)

    print("Max размер подкласса: " + str(size_class_1) + " | " + str(size_class_2))
    print("Кол-во подклассов для обьединения: " + str(count_category_1) + " | " + str(count_category_2))

    if size_class_1 * count_category_1 < size_class_2 * count_category_2:
        size_class_2 = int((size_class_1 * count_category_1) / count_category_2)
    else:
        size_class_1 = int((size_class_2 * count_category_2) / count_category_1)

    print("Размер подкласса в классе: " + str(size_class_1) + " | " + str(size_class_2))

    return pd.array([size_class_1, size_class_2])


# папки с файлами для обьединения в класс 1 класс 2
dir_class_1 = list()
dir_class_2 = list()

# Основное зерно
dir_class_1.append('D:/source x4/dataRGB/Основное зерно отобранное')

# Зерновая примесь
dir_class_2.append('D:/source x4/dataRGB/Пшеница битые отобранное')
dir_class_1.append('D:/source x4/dataRGB/Пшеница испорченные отобранное')
dir_class_1.append('D:/Проросшая пшеница перебранное/sprouted_wheat_vis')
dir_class_1.append('D:/source x4/dataRGB/Пшеница щуплые отобранное')
dir_class_1.append('D:/source x4/dataRGB/Рожь основное отобранное')

# Сорная примесь
dir_class_2.append('D:/source x4/dataRGB/Амброзия отобранное')
dir_class_2.append('D:/source x4/dataRGB/Овсюг отобранное')
dir_class_2.append('D:/source x4/dataRGB/Органика отобранное')
dir_class_2.append('D:/source x4/dataRGB/Пшеница головня отобранное')
dir_class_2.append('D:/source x4/dataRGB/Сорные семена отобранное')
dir_class_2.append('D:/source x4/dataRGB/Ячмень отобранное')


def save_path(file_name, list_path):
    if len(list_path) == 0:
        return
    file_path = open(file_name, 'w')
    for path in list_path:
        file_path.write(path + '\n')
    file_path.close()


def load_path(file_name):
    out = list()
    if os.path.exists(file_name):
        file_path = open(file_name, 'r')
        out = [path.strip() for path in file_path]
        file_path.close()
    return out
