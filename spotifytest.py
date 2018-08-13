import pandas as pd
import numpy as np
import json
from scipy.sparse import csr_matrix
import random

pd.set_option('max_columns',10)


songPlaylistArray = [] 
for i in range(10):
	path = '/mpd.slice.' + str(i*1000) + "-" + str(i*1000+999) + '.json'
	d= json.load(open(path, 'r'))
	thisSlice = pd.DataFrame.from_dict(d['playlists'], orient='columns')
	for index, row in thisSlice.iterrows():
	    for track in row['tracks']:
	        songPlaylistArray.append([track['track_uri'], track['artist_name'], track['track_name'], row['pid']])
	songPlaylist = pd.DataFrame(songPlaylistArray, columns=['trackid', 'artist_name', 'track_name', 'pid'])
	songPlaylist.append(songPlaylist)

A = songPlaylist.drop(['artist_name', 'track_name'], axis=1).pivot_table(index=["pid"], columns="trackid", aggfunc=lambda x: 1, fill_value=0)

songlist = songPlaylist.drop(['pid'], axis=1)
songlist = songlist.drop_duplicates()
songlist.index = pd.RangeIndex(len(songlist.index))

cols = songlist['trackid']
A = A.reindex(columns=cols)


prefering = []

for i in range(100):
	if len(prefering) <5:
		random_number =[]
		for x in range(10):
			random_number.append(random.randint(0,34443))
		print(songlist.iloc[random_number,1:])
		interst = [int(x) for x in input('Enter songs you like, or 0 : ').split()]
		for j in interst:
			if j not in random_number and j != 0:
				print('Wrong number, try again')
			elif j not in random_number and j in prefering:
				print('You have chosen this song before, try again')
			elif j == 0:
				print("Don't have what you like? Please wait")
			else:
				prefering.append(j)


A = csr_matrix(A) 
C = A.T * A


song_freq_vec  = np.sum(A, axis=0)

song_freq_vec = song_freq_vec.reshape(34443, 1)
C1 = C.toarray()

D  = (song_freq_vec + song_freq_vec.T)-C1 


S1 = np.divide(C1, D)
S2 = pd.DataFrame(S1)

recommendation = S2.loc[prefering]
recom = recommendation.loc[:, ((recommendation >0) & (recommendation <1)).any(axis=0)]
recom_list = recom.columns.values.tolist()
slist = recom_list[:30]
spotify_recommendatyion= songlist.iloc[slist]
print('Recommended Songs For You')
print(spotify_recommendatyion.iloc[:,1:])
