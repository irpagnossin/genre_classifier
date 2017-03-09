#!/usr/bin/env python
# -*- coding: utf-8 -*-

from configuration import *
from os.path import exists
from outputfilename import get_output_filename
from trackspectra import build_optimal_track2genre_map
import sys
import time


def main():
    """
    Builds the optimal map track->genre based on k-means and silhouette analysis.
    As result, it writes the following files:
    - output/silhouette_x.csv: diagnostic of silhouette analysis, in format <# of clusters>,<silhouette score>.
      x is the occurrence threshold, ie, the minimum amount of times a track must show up to be considered.
    - output/track2genre_x.pickle: Python dictionary in format {track_id: genre_id}, where genre_id was obtained
      from classification.
    """

    try:
        n = int(sys.argv[1])  # Occurrence threshold
    except IndexError:
        n = 1
    except ValueError:
        n = 1

    assert (type(n) == int)

    n_str = str(n)
    tracks = get_output_filename(n, TRACKS)
    track_ids = get_output_filename(n, TRACK_IDS)
    silhouette = get_output_filename(n, SILHOUETTE_ANALYSIS_RESULT)
    track2genre = get_output_filename(n, TRACK2GENRES)

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


if __name__ == '__main__':
    main()
