import os
import pandas as pd

# iterators over files in respective folders
data_1 = os.scandir('data/data_1')
data_2 = os.scandir('data/data_2')

# create a data frame to save locations and labels
df = pd.DataFrame(columns=['file_name', 'label'])

count = 1

for data in data_1:
    old_name_file = 'data/data_1/' + data.name
    new_name_file = 'data/category_1/' + str(count) + ".png"
    os.rename(old_name_file, new_name_file)
    count += 1

count = 1

for data in data_2:
    old_name_file = 'data/data_2/' + data.name
    new_name_file = 'data/category_2/' + str(count) + ".png"
    os.rename(old_name_file, new_name_file)
    count += 1

categories_1 = os.scandir('data/category_1')
categories_2 = os.scandir('data/category_2')

for category in categories_1:
    loc = 'data/category_1/{}'.format(category.name)
    df = df.append({'file_name': loc, 'label': 0}, ignore_index=True)

count = 1

for category in categories_2:
    loc = 'data/category_2/{}'.format(category.name)
    df = df.append({'file_name': loc, 'label': 1}, ignore_index=True)

# save as csv file
df.to_csv('file_names.csv', header=None, index=False)