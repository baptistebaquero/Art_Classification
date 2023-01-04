
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import shutil

database = 'd:\dataset'
path_csv_database = pd.read_csv(database + '\classes.csv') #return datapath

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #return the path of the project
data_path = os.path.join(project_path, 'data') #return the path of the data folder
new_csv_path = os.path.join(data_path, 'new_classes.csv')

# recover the name of all the artists
artists = path_csv_database['artist'].unique() # return a list of all the artists
# create a dictionary with the name of the artist and the number of paintings
dict_artists = {}
for i in range(len(artists)):
    dict_artists[artists[i]] = len(path_csv_database[path_csv_database['artist'] == artists[i]])
# print(dict_artists)
# find the 10 artists with the most paintings
max_artists = sorted(dict_artists.items(), key=lambda x: x[1], reverse=True)[:10] #list of tuples (artist, number of paintings)

#create a new csv with only the 10 artists with the most paintings
if os.path.exists(os.path.join(data_path, 'new_classes.csv')):
    print('New csv file already created')
    #read the new csv
    new_csv = pd.read_csv(new_csv_path)
else:

    new_csv = pd.DataFrame(columns=['artist', 'path'])
    print('Creation of the new csv file ...')
    for i in range(len(max_artists)):
        new_csv = new_csv.append(path_csv_database[path_csv_database['artist'] == max_artists[i][0]])
    # keep only 500 random paintings for each artist
    for i in range(len(max_artists)):
        new_csv = new_csv[new_csv['artist'] != max_artists[i][0]].append(new_csv[new_csv['artist'] == max_artists[i][0]].sample(n=500, random_state=1))
    new_csv.to_csv(new_csv_path, index=False)
    print('New csv file created')


# add a colum label at the end of new_csv and put a numer between 0 and 9 for the different artists
# new_csv['label'] = 0
# for i in range(len(max_artists)):
#     new_csv.loc[new_csv['artist'] == max_artists[i][0], 'label'] = i
# new_csv.to_csv(new_csv_path, index=False)



# plot an histogram of the CSV for the height and width of the paintings
plt.figure(1)
plt.subplot(211)
plt.hist(new_csv['height'], bins=100)
plt.subplot(212)
plt.hist(new_csv['width'], bins=100)
# plt.show()

# print index of the max of the histogram
# print(new_csv['height'].value_counts().index[0])
# print(new_csv['width'].value_counts().index[0])

# print number of painting above 2500px width 
# print(len(new_csv[new_csv['width'] > 2500]))
# print(len(new_csv[new_csv['height'] > 2500]))

# remove from the excel the paintings above 2500px width and the paintings above 2500px height
# new_csv = new_csv[new_csv['width'] <= 2500]
# new_csv = new_csv[new_csv['height'] <= 2500]
# new_csv.to_csv(new_csv_path, index=False)

#print number painting per artist
# for i in range(len(max_artists)):
#     print(max_artists[i][0], len(new_csv[new_csv['artist'] == max_artists[i][0]]))

# print number of painting in the new csv
# print('Nunber of painting :', len(new_csv))

# recover the first filename in the new csv
# print(new_csv['filename'][0])

# print(os.path.join(database, new_csv['filename'][0]))
# plt.imshow(plt.imread(os.path.join(database, new_csv['filename'][0])))
# plt.show()

# create a folder data artist with subfolders with all the files of the artist in new csv from database
all_artists_path = os.path.join(data_path, 'artists')
if not os.path.exists(all_artists_path):
    os.makedirs(all_artists_path)
    print("creation of the folder artists")
else:
    print("folder artists already exists")

for i in range(len(max_artists)):
    artists_path = os.path.join(all_artists_path, max_artists[i][0])
    if not os.path.exists(artists_path):
        print("creation of the folder", max_artists[i][0])
        os.makedirs(artists_path)
    else:
        print("folder", max_artists[i][0], "already exists")
    # copy all the files of the artist from d inside the new artist folders in data
    # recover the good filename from the artist

    for j in range(len(new_csv[new_csv['artist'] == max_artists[i][0]])):
        #recover filename
        filename = new_csv[new_csv['artist'] == max_artists[i][0]]['filename'].iloc[j]
        shutil.copy(os.path.join(database,filename), artists_path)

