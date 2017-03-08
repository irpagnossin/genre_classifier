#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import exists
from trackspectra import build_optimal_track2genre_map
import sys
import time


if __name__ == '__main__':
    """
    Builds the optimal map track->genre based on k-means and silhouette analysis.
    As result, it writes the following files:
    - output/silhouette_x.csv: diagnostic of silhouette analysis, in format <# of clusters>,<silhouette score>.
      x is the occurrence threshold, ie, the minimum amount of times a track must show up to be considered.
    - output/track2genre_x.pickle: Python dictionary in format {track_id: genre_id}, where genre_id was obtained
      from classification.
    """

    try:
        n = sys.argv[1]  # Occurrence threshold
    except IndexError:
        n = 1

    n_str = str(n)
    tracks = 'output/tracks_' + n_str + '.npz'
    track_ids = 'output/track_ids_' + n_str + '.pickle'
    silhouette = 'output/silhouette_' + n_str + '.csv'
    track2genre = 'output/track2genre_' + n_str + '.pickle'

    if not exists(tracks):
        print('File {} does not exist. Execute "python stage1.py {}" to generate it.'.format(tracks, n_str))
        sys.exit(-1)

    if not exists(track_ids):
        print('File {} does not exist. Execute "python stage1.py {}" to generate it.'.format(track_ids, n_str))
        sys.exit(-1)

    print('Generating optimal track->genre map for tracks with occurrence threshold >= {}...'.format(n_str))
    start = time.time()
    build_optimal_track2genre_map(tracks, track_ids, silhouette, track2genre, 30)  # <-- The important thing here!
    end = time.time()
    print('It took {} seconds'.format(end-start))
