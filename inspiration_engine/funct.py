#!/usr/bin/python3

from sklearn.cluster import KMeans

def normalize(frequences):
    maxi = max([max(songFreq) for songFreq in frequences])
    normalized = []
    for songFreq in frequences:
        normalized.append([ freq/maxi for freq in songFreq ])
    return normalized

#songs need to be normalized
def distance(mySong, otherSongs):
    # from scipy.spatial.distance import cosine
    from scipy.spatial import distance
    distances = [distance.euclidean(mySong, otherSong) for otherSong in otherSongs]
    return distances


#receive raw frequences
def distancesGraph(frequences):
    normalizedSong = normalize(frequences)
    matrix = []
    for song in normalizedSong:
        matrix.append(distance(song, normalizedSong))
    return matrix

def clusterize(data):
    model = KMeans(n_clusters=5, random_state=0).fit(data)
    return model

if __name__ == '__main__':
    #Notes: A B C D E F G
    train = [
        [1, 0, 2, 5, 3, 0, 0, 1, 0, 5],
        [0, 1, 0, 9, 1, 1, 2, 0, 0, 0],
        [5, 9, 6, 3, 2, 1, 5, 1, 7, 2],
        [0, 0, 0, 0, 1, 8, 1, 2, 3, 6],
        [0, 0, 0, 2, 5, 0, 4, 6, 9, 8],
        [1, 0, 2, 5, 3, 0, 0, 1, 0, 5],
        [0, 1, 0, 9, 1, 1, 2, 0, 0, 0],
        [5, 9, 6, 3, 2, 1, 5, 1, 7, 2],
        [0, 0, 0, 0, 1, 8, 1, 2, 3, 6],
        [0, 0, 0, 0, 1, 8, 1, 2, 3, 6]
    ]

    test = [
        [1, 0, 2, 5, 3, 0, 0, 1, 0, 5],
        [0, 1, 0, 9, 1, 1, 2, 0, 0, 0],
        [5, 9, 6, 3, 2, 1, 5, 1, 7, 2],
        [0, 0, 0, 0, 1, 8, 1, 2, 3, 6],
        [5, 9, 6, 3, 2, 1, 5, 1, 7, 2],
    ]
    trainData = distancesGraph(train)
    testData = distancesGraph(test)

    kmeans = clusterize(train)
    print(kmeans.labels_)
    predicted = kmeans.predict(test)
    print(predicted)
