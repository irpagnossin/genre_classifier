#!/usr/bin/env python
# -*- coding: utf-8 -*-

from progressbar import printProgress
from read_large_csv import get_row
from trackoccurrences import TrackOccurrences
import csv
import numpy as np
import pickle
import time
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.sparse import csr_matrix


def track_occurrences(csvfile, delimiter=',', rows=-1, min_occur=1):
    """
    Scans the detections data-set (CSV file) and count occurrences of each track in each source.
    This is equivalent to a pivot-table operation.
    :param csvfile: the name of the CSV file containing detections, in format <created_at>,<audio_source_id>,<track_id>
    :param delimiter: delimiter character
    :param rows: amount of rows to scan. If -1, all data-set shall be scanned
    :return: an optimized representation of tracks-spectra
    :rtype: TrackComponents
    """

    tracks = TrackOccurrences(min_occur)

    count = 0
    for row in get_row(csvfile, delimiter, rows):
        try:
            track_id = int(row[2])
            source_id = int(row[1])
            tracks.add(track_id, source_id)

            count += 1
            if count % 100 == 0:
                time.sleep(0)

        except IndexError:  # Ignore malformed rows
            pass

        except ValueError:  # Ignore malformed rows
            pass

    return tracks


def spectra(tracks):
    """
    Construct spectra np.array based on track occurrences
    :param tracks: TrackOccurrences obtained from track_occurrences
    :return: tracks spectra as np.array
    :rtype: (list,np.array)
    """

    n_tracks = tracks.n_tracks()
    n_components = tracks.n_components()

    assert(n_tracks > 0)
    assert(n_components > 0)

    print('{} tracks x {} features'.format(n_tracks, n_components))

    __spectra = np.zeros(shape=(n_tracks, n_components))

    track_ids = []  # TODO: change to array
    i = 0
    for track_id, spectrum in tracks.get_tracks().iteritems():
        for component_idx, value in spectrum.iteritems():
            __spectra[i, component_idx] = value
        i += 1
        track_ids.append(track_id)

        if i % 100 == 0:
            printProgress(i, n_tracks)
            time.sleep(0)

    printProgress(n_tracks, n_tracks)

    return track_ids, __spectra


def build_optimal_track2genre_map(spectra_csr, track_ids_filename, result, track2genre_filename, max_nclusters=10):
    """
    Builds the best (optimized) mapping track->genre, based on k-means and silhouette analysis.
    :param spectra_csr: file .npz containing the spectra as np.array in CSR (compact sparse row) format
    :param track_ids_filename: file .pickle containing the list of track_id which fulfill occurrence threshold
    :param result: CSV with silhouette analysis diagnosis, showing score for each choice of cluster
    :param track2genre_filename: output .pickle file
    :param max_nclusters: maximum amount of clusters to analyse
    :return:
    """

    analysis_output = open(result, 'w')
    writer = csv.writer(analysis_output)

    loader = np.load(spectra_csr)
    X = csr_matrix((loader['data'], loader['indices'], loader['indptr']), shape = loader['shape']).toarray()

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