import csv
import numpy as np
import pickle
import time
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.sparse import csr_matrix


def construct_track2genre_map(spectra, track_ids_filename, result, track2genre_filename, max_nclusters=10):

    analysis_output = open(result, 'w')
    writer = csv.writer(analysis_output)

    loader = np.load(spectra)
    X = csr_matrix((loader['data'], loader['indices'], loader['indptr']), shape = loader['shape']).toarray()
#    X = X[:500, :]  # <-- I do not have enough memory to run over all data-set

    n_samples, n_features = np.shape(X)
    print("{} samples x {} dimensions".format(n_samples, n_features))

    n_clusters_candidates = range(2, max_nclusters+1)  # Analysis is defined for > 2 clusters
    chosen_ng = -1  # "ng" means "amount (n) of genres"
    chosen_ng_score = -1  # The minimum score in silhouette analysis is -1
    chosen_ng_labels = np.zeros(shape=n_samples)

    writer.writerow(['n_clusters', 'score'])
    for n in n_clusters_candidates:

        # Run k-means on track spectra
        model = KMeans(n_clusters=n, random_state=10).fit(X)

        # Find mean score (among all sample's scores)
        score = silhouette_score(X, model.labels_)
        print("{0} clusters => score {1:.5f}".format(n, score))
        writer.writerow([n, score])

        # Choose the amount of clusters (genres) which maximize mean score
        if score > chosen_ng_score:
            chosen_ng = n
            chosen_ng_score = score
            chosen_ng_labels = model.labels_

    analysis_output.close()

    if chosen_ng == -1:
        print("Unable to identify clusters.")
    else:
        print("{} genres were found".format(chosen_ng))

    print('Creating track to genre map...')
    track_ids = pickle.load(file(track_ids_filename, 'rb'))
    mapper = dict(zip(track_ids, chosen_ng_labels))

    print('Saving track to genre map...')
    pickle.dump(mapper, file(track2genre_filename, 'wb'), pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':

    n_str = str(400)
    tracks = 'output/tracks_' + n_str + '.npz'
    track_ids = 'output/track_ids_' + n_str + '.pickle'
    silhouette = 'output/silhouette_' + n_str + '.csv'
    track2genre = 'output/track2genre_' + n_str + '.pickle'

    start = time.time()
    construct_track2genre_map(tracks, track_ids, silhouette, track2genre, 30)
    end = time.time()
    print('It took {} seconds'.format(end-start))
