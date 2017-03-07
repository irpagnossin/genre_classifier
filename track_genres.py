import numpy as np
import pickle
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.sparse import csr_matrix
from configuration import *


def construct_track2genre_map(spectra):

    loader = np.load(spectra)
    X = csr_matrix((loader['data'], loader['indices'], loader['indptr']), shape = loader['shape']).toarray()
    X = X[:1000, :]  # <-- I do not have enough memory to run over all data-set

    n_samples, n_features = np.shape(X)
    print("{} samples x {} dimensions".format(n_samples, n_features))

    n_clusters_candidates = range(2, 10)  # Analysis fail for 1 cluster
    chosen_ng = -1  # "ng" means "amount (n) of genres"
    chosen_ng_score = -1  # The minimum score in silhouette analysis is -1
    chosen_ng_labels = np.zeros(shape=n_samples)

    for n in n_clusters_candidates:

        # Run k-means on track spectra
        model = KMeans(n_clusters=n, random_state=10).fit(X)

        # Find mean score (among all sample's scores)
        score = silhouette_score(X, model.labels_)
        print("{0} clusters => score {1:.5f}".format(n, score))

        # Choose the amount of clusters (genres) which maximize mean score
        if score > chosen_ng_score:
            chosen_ng = n
            chosen_ng_score = score
            chosen_ng_labels = model.labels_

    if chosen_ng == -1:
        print("Unable to identify clusters.")
    else:
        print("{} genres were found".format(chosen_ng))

    print('Creating track to genre map...')
    track_ids = pickle.load(file(TRACK_IDS, 'rb'))
    mapper = dict(zip(track_ids, chosen_ng_labels))

    print('Saving track to genre map...')
    pickle.dump(mapper, file(TRACK_GENRES_BINARY, 'wb'), pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    construct_track2genre_map(TRACKS)
